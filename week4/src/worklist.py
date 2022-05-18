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
            merge(in_set[b], out_set[p].copy())
        # out[b] = transfser(b, in[b])
        prev_outset = out_set[b].copy()
        
        out_set[b] = transfer(blocks[b], in_set[b].copy())

        # if outset changed, add all successors of b
        if prev_outset != out_set[b]:
            for node in succ[b]:
                worklist.append(node)

    print ("=================== FUNCTION [" + name + "] (" + str(dir) + ")===================")

    if dir != 'forward':
        in_set, out_set = out_set, in_set

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

        