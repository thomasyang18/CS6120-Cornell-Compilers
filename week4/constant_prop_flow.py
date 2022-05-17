import json
import sys

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

        elif instr['op'] not in TERMINATORS and i != len(blocks)-1:
            add_edge(i,i+1)

    return name, args, blocks, succ, pred

def worklist_const_prop(func):
    #Given a function, worklist it
    name, in_args, blocks, succ, pred = make_graph(func)

    #print (succ)
    #print(pred)

    in_set = []
    out_set = []
    for i in blocks:
        in_set.append({})
        out_set.append({})

    for arg in in_args:
        in_set[0][arg['name']] = '?'

    def evaluate_expr(op, args):
        if op == 'mul':
            return args[0] * args[1]
        if op == 'div':
            return args[0] // args[1]
        if op == 'add':
            return args[0] + args[1]
        if op == 'sub':
            return args[0] - args[1]
        if op == 'eq':
            return 'true' if args[0] == args[1] else 'false'
        if op == 'lt':
            return 'true' if args[0] < args[1] else 'false'
        if op == 'gt':
            return 'true' if args[0] > args[1] else 'false'
        if op == 'le':
            return 'true' if args[0] <= args[1] else 'false'
        if op == 'ge':
            return 'true' if args[0] >= args[1] else 'false'
        if op == 'not':
            return 'true' if args[0] == 'false' else 'true'
        if op == 'and':
            return 'true' if args[0] == 'true' and args[1] == 'true' else 'false'
        if op == 'or':
            return 'true' if args[0] == 'true' or args[1] == 'true' else 'false'
        if op == 'id':
            return args[0]

    worklist = list(range(0, len(blocks)))
    while worklist:
        # b = pick any block from worklist
        b = worklist[-1]
        worklist.pop()
        # in[b] = merge(out[p] for every predecessor p of b)
        for p in pred[b]:
            for arg in out_set[p]:
                if arg not in in_set[b]:
                    in_set[b][arg] = out_set[p][arg]
                elif in_set[b][arg] != out_set[p][arg]:
                    in_set[b][arg] = '?'
        # out[b] = transfser(b, in[b])
        prev_outset = out_set[b].copy()
        out_set[b] = in_set[b].copy()
        
        for instr in blocks[b]:
            # If the instruction is a basic instruction and the args are constant, evaluate
            if 'dest' not in instr:
                continue

            allConst = True
            args = []
            if 'args' in instr:
                for arg in instr['args']:
                    if arg not in out_set[b] or out_set[b][arg] == '?':
                        allConst = False
                    elif arg in out_set[b]:
                        args.append(out_set[b][arg]) 
            
            if instr['op'] == 'const':
                out_set[b][instr['dest']] = instr['value']
            elif allConst and instr['op'] not in ('jmp', 'br', 'ret', 'call', 'print'):
                out_set[b][instr['dest']] = evaluate_expr(instr['op'], args)
            else:
                out_set[b][instr['dest']] = '?'

        # if outset changed, add all successors of b
        if prev_outset != out_set[b]:
            for node in succ[b]:
                worklist.append(node)

    print ("===================OPERATION ON FUNCTION [" + name + "]===================")

    for i in range(0, len(blocks)):
        print ("Current block:")
        for instr in blocks[i]:
            print(instr)
        print("------------------")
        print ("In nodes:")
        for var in in_set[i]:
            print(var + " " + str(in_set[i][var]))
        print("------------------")
        print ("Out nodes:")
        for var in out_set[i]:
            print(var + " " + str(out_set[i][var]))
        print("+++++++++++++++++")
    

if __name__ == "__main__":
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        worklist_const_prop(func)