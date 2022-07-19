from lark import Transformer
from graphutils import make_graph   

def reaching_defs(func):
    def id(arg):
        return {-1}
    def merge(in_set, apply_set, i):
        for v in apply_set:
            if v not in in_set:
                in_set[v] = set()
            in_set[v] = in_set[v].union(apply_set[v])
    def transfer(instrs, in_set, i):
        for instr in instrs:
            if 'dest' in instr:
                in_set[instr['dest']] = {i}
        return in_set

    return worklist_algo(func, id, merge, transfer)

def live_var(func):
    def id(arg):
        ''

    def merge(in_set, apply_set, i):
        for arg in apply_set:
            in_set[arg] = ''

    def transfer(instrs, in_set, i):
        for instr in reversed(instrs):

            if 'dest' in instr:
                if instr['dest'] in in_set:
                    in_set.pop(instr['dest'])
            
            if 'args' in instr:
                for arg in instr['args']:
                    in_set[arg] = ''
                    
        return in_set            

    return worklist_algo(func, id, merge, transfer, 'backward')


def worklist_algo(func, id, merge, transfer, dir = 'forward'):
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
        