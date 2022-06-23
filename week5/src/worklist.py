TERMINATORS = 'jmp', 'br', 'ret'

#Given a function, transform it into cfg notation, ones indexed. Returns the name, args, blocks, successors array, predecessors array
def make_graph(func):
    body = func['instrs']
    args = []
    if 'args' in func:
        args = func['args']
    name = func['name']
    # Transforms to basic block notation
    blocks = []
    cur_block = []
    for instr in body:
        if 'op' in instr:
            cur_block.append(instr)

            if instr['op'] in TERMINATORS:
                blocks.append(cur_block)
                cur_block = []
        else:
            if cur_block:
                blocks.append(cur_block)
            cur_block = [instr]
    if cur_block:
        blocks.append(cur_block)

    label_to_ind = {}

    for i in range(len(blocks)):
        if 'op' not in blocks[i][0]: #label
            label_to_ind[blocks[i][0]['label']] = i


    succ = [] 
    pred = [] 

    for i in blocks:
        succ.append([])
        pred.append([])

    BREAKAWAYS = 'jmp', 'br'

    def add_edge(i, j):
        succ[i].append(j)
        pred[j].append(i)

    for i in range(len(blocks)):
        instr = blocks[i][-1]
        if 'op' in instr and instr['op'] in BREAKAWAYS:
            if instr['op'] == 'jmp':
                add_edge(i, label_to_ind[instr['labels'][0]])
            elif instr['op'] == 'br':
                add_edge(i, label_to_ind[instr['labels'][0]])
                add_edge(i, label_to_ind[instr['labels'][1]])

        elif 'op' in instr and instr['op'] not in TERMINATORS and i != len(blocks)-1:
            add_edge(i,i+1)
        elif 'op' not in instr and i != len(blocks)-1:
            add_edge(i,i+1)

    return name, args, blocks, succ, pred


"""
DOCUMENTATION

func: The function body; get this by calling 'for func in prog['functions']' and each func is the function body
id: the input arguments for the function have to be initialized to something; this will determine it. Will be identity function
ex: constant propogation has default '?'; interval checking may have [-inf, +inf], etc
merge(in_set, apply): This determines how you should merge two things. The left arg is the base element; you apply the right function.
transfer(block, in_set[b]): Given an instruction block and an inset, return the corresponding outset after applying instructions from block
direction: Whether forward or backwards processing in CFG
"""

def id(arg):
    return {'ssa_dummy_block': -1}

def merge(in_set, apply_set, i):
    # get all variables
    # it's like a union of dicts keys but applyset overrides any defintiions,
    # but in_set keeps its current definitions, so its weird union

    for var in apply_set:
        #print("Yo", i, var, in_set[var] if var in in_set else "None", 
        #    apply_set[var] if var in in_set else "None")

        if var not in in_set:
            in_set[var] = {}
        for label in apply_set[var]:
            in_set[var][label] = apply_set[var][label]

        #print("After", i, var, in_set[var], apply_set[var])



def transfer(instrs, in_set, i):
    for instr in instrs:
        if 'dest' in instr:
            in_set[instr['dest']] = {instrs[0]['label']: i}
            
    for arg in in_set:
        true_len = len(set(in_set[arg].values()))
        if true_len > 1:
            in_set[arg] = {instrs[0]['label']: i}
        elif true_len == 1:
            # keep the var, but rename the label; that will be useful
            # in future things
            var= list(in_set[arg].values())[0]

            in_set[arg] = {instrs[0]['label']:var}
            #print("Yo wtf", arg, in_set[arg])
    return in_set



def worklist_algo(func, dir = 'forward'):
    #Given a function, worklist it
    name, in_args, blocks, succ, pred = make_graph(func)

    in_set = []
    out_set = []
    for i in blocks:
        in_set.append({})
        out_set.append({})

    for arg in in_args:
        in_set[0][arg['name']] = id(arg.copy())

    if dir != 'forward':
        #flip predecessors and successors, flip in and out sets
        in_set, out_set = out_set, in_set
        pred, succ = succ, pred

    worklist = list(range(0, len(blocks)))
    while worklist:
        # b = pick any block from worklist
        b = worklist[-1]
        worklist.pop()
        #print(b)
        # in[b] = merge(out[p] for every predecessor p of b)
        for p in pred[b]:
            merge(in_set[b], out_set[p].copy(), b)
        # out[b] = transfser(b, in[b])
        prev_outset = out_set[b].copy()
        
        out_set[b] = transfer(blocks[b], in_set[b].copy(), b)

        # if outset changed, add all successors of b
        if prev_outset != out_set[b]:
            for node in succ[b]:
                worklist.append(node)

    
    if dir != 'forward':
        in_set, out_set = out_set, in_set

    """
    print ("=================== FUNCTION [" + name + "] (" + str(dir) + ")===================")

    for i in range(0, len(blocks)):
        print ("b" + str(i) + ":")
        #for instr in blocks[i]:
        #    print(instr)
        if len(in_set[i]) == 0:
            print("  in: Ø")
        else:
            print ("  in:")
            for var in in_set[i]:
                print("    " + var + " " + str(in_set[i][var]))
        
        if len(out_set[i]) == 0:
            print("  out: Ø")
        else:
            print ("  out:")
            for var in out_set[i]:
                print("    " + var + " " + str(out_set[i][var]))
    """
    return in_set, out_set
        