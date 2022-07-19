import sys, json, argparse
from graphutils import make_graph, locate_next_scc
from worklist import live_var, reaching_defs
from domlib import build_tree, find_dominators, build_matrix

DEBUG = False

def parse_args():
    parser = argparse.ArgumentParser(description='Options')

    parser.add_argument('-d', '--debug', 
                    help='If true, don\'t dump json',    
                    default='false', 
                    type=str, 
                    choices = ['true', 'false'])

    return vars(parser.parse_args())

def limc(func):
    name, args, blocks, succ, pred = make_graph(func)

    #Idea is to isolate natural loops and do LICM on them in a natural way
    # if the SCC is of size one, make a special case for if it pointers back to itself
    n = len(blocks)

    for i in range(0, n):
        if len(blocks[i]) > 0 and 'label' not in blocks[i][0]:
            blocks[i] = [{'label': 'bblock_' + str(i)}] + blocks[i]
    
    # Reaching definitions can be precomputed, since one group's outside reaching definitions
    # are well, outside of the other group and stay "within" the same location, since LICM only
    # lifts up definitions to the top of the loop

    rd_in_set, rd_out_set = reaching_defs(func)
    lv_in_set, lv_out_set = live_var(func)
    """
    for i in range(0, n):
        print("in",i,rd_in_set[i])
    for i in range(0, n):
        print("out",i,rd_out_set[i])

    for i in range(0,n):
        print("in",i,lv_in_set[i])
    for i in range(0,n):
        print("out",i,lv_out_set[i])
    """
    var2reach_defs = {} # inset and outset unioned, so just check if reaching defs are out of loop
    for i in range(0,n):
        for key in rd_in_set[i]:
            if key not in var2reach_defs:
                var2reach_defs[key] = set()
            
            for block in rd_in_set[i][key]:
                var2reach_defs[key].add(block)

        for key in rd_out_set[i]:
            if key not in var2reach_defs:
                var2reach_defs[key] = set()
            
            for block in rd_out_set[i][key]:
                var2reach_defs[key].add(block)

    dom_matrix = build_matrix(build_tree(find_dominators(func)))

    header2preheader = {} # maps headers to preheaders, so we can do one pass later on and replace everything
    blocks_to_add = {}

    for scc, head in locate_next_scc(succ,pred):
#        print("scc:",scc, "head:",head)

        def_cnt = {} # map from dest name to list of uses WITHIN LOOP

        for bi in scc:
            for instr in blocks[bi]:
                if 'dest' in instr:
                    if instr['dest'] not in def_cnt:
                        def_cnt[instr['dest']] = 0
                    def_cnt[instr['dest']]+=1
        
        loop_exits = set()
        for bi in scc:
            for s in succ[bi]:
                if s not in scc:
                    loop_exits.add(bi)

#        print("loop exits", loop_exits)

        marked = {}

        added = True
        while added:
            added = False
            for bi in scc:
                for instr in blocks[bi]:
                    if 'dest' in instr:
                        to_add = instr['op'] != 'call'
                        if instr['dest'] in marked:
                            continue
                        if 'args' in instr:
                            for arg in instr['args']:
                                if arg in def_cnt and def_cnt[arg] == 1 and arg in marked:
                                    pass
                                elif arg in var2reach_defs and len(var2reach_defs[arg].intersection(scc)) == 0:
                                    pass
                                else:
                                    to_add = False  

                        if to_add:
                            added = True
                            marked[instr['dest']] = (instr, bi)

        #print(marked)    

        var_2_use_block = {}
        for bi in scc:
            for instr in blocks[bi]:
                if 'args' in instr:
                    for arg in instr['args']:
                        if arg not in var_2_use_block:
                            var_2_use_block[arg] = set()
                        var_2_use_block[arg].add(bi)

        keep_set = {}
        for key, ins_tup in marked.items():
            instr, bi = ins_tup
            # no other definitions is easy, just def_cnt[arg] <= 1
            only_def = def_cnt[key] <= 1
            
            # no side effects, so no div or call
            side_effects = False

            if 'op' in instr:
                if instr['op'] == 'div':
                    side_effects = True

            # a definition is dead iff it never shows up in the in_set of a non-loop successor of a loop exit
            is_dead = True

            for lei in loop_exits:
                for s in succ[lei]:
                    if s not in scc and instr['dest'] in lv_in_set[s]:
                        is_dead = False

            # dominates all loop exits is easy to check
            dom_all_exits = all([dom_matrix[bi][lei] for lei in loop_exits])


            # "dominates all its uses -> " have edge case for the same node. A use that comes before def in start node does NOT count as dominating. rest can be same tho tbh
            # if no uses, then just assume dominate all loop exits

            dom_all_uses = dom_all_exits

            if instr['dest'] in var_2_use_block:
                dom_all_uses = all([dom_matrix[bi][usei] for usei in var_2_use_block[instr['dest']]])
                for tinstrs in blocks[bi]:
                    if 'args' in tinstrs:
                        if any([arg == instr['dest'] for arg in tinstrs['args']]):
                            dom_all_uses = False
                            break
                    if 'dest' in tinstrs:
                        if tinstrs['dest'] == instr['dest']:
                            break                        

            if dom_all_uses and only_def and (dom_all_exits or (is_dead and not side_effects)):
                keep_set[key] = ins_tup

       # print(keep_set)
        # finally, lift everything up to a pre_header
        gen_preheader = 'gen_preheader_'+str(head)
        tblock = [{'label':gen_preheader}]
        for bi in scc:
            blocks[bi] = [instr for instr in blocks[bi] if not ('dest' in instr and instr['dest'] in keep_set)]
        
        for val in keep_set.values():
            tblock.append(val[0])

        tblock.append({'op':'jmp', 'labels':[blocks[head][0]['label']]})

        blocks_to_add[head] = tblock
        header2preheader[blocks[head][0]['label']] = gen_preheader
        
    func['instrs'].clear()

    for i in range(0, n):
        if i in blocks_to_add:
            for instr in blocks_to_add[i]:
               # print("Preheaeder",i,instr)
                func['instrs'].append(instr)

        for instr in blocks[i]:
            if 'labels' in instr:
                instr['labels'] = [header2preheader[label] if label in header2preheader else label for label in instr['labels']]
            #print("Current",i,instr)
            func['instrs'].append(instr)

    return func

if __name__ == "__main__":
    args = parse_args()

    DEBUG = args['debug'] == 'true'

    prog = json.load(sys.stdin)

    prog['functions'] = [limc(func) for func in prog['functions']]

    if not DEBUG:
        json.dump(prog, sys.stdout, indent=2)