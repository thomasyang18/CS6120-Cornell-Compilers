from cProfile import label
from operator import truediv
import sys
import os

from domlib import find_dominators
from domlib import build_frontier
from domlib import build_tree
from domlib import make_graph
from worklist import worklist_algo

import json



def id(arg):
    ''

def merge(in_set, apply_set):
    for arg in apply_set:
        in_set[arg] = ''

def transfer(instrs, in_set):
    for instr in instrs:
        if 'dest' in instr:
            in_set[instr['dest']] = ''

    return in_set

def to_ssa(func):
    dominators = find_dominators(func, False, False)
    tree = build_tree(dominators, False)
    frontier = build_frontier(func, tree, dominators, False)
    name, args, blocks, succ, pred = make_graph(func)   
    
    in_set, out_set = worklist_algo(func, id, merge, transfer)

    vars = set()

    defs = {} # map of variables to list of blocks

    argnames = {}
    if 'args' in func:
        argnames = {arg['name'] for arg in func['args']}
    vars.update(argnames)

    for var in vars:
        defs[var] = []

    #blocks MUST start with labels
    bbloccnt = 0

  #  print(name)

    for i in range(0, len(blocks)):
        if 'label' not in blocks[i][0]:
            instr = {'label': 'bbloc' + str(bbloccnt)}
            bbloccnt+=1
            blocks[i] = [instr] + blocks[i]
        for instr in blocks[i]:
            if 'dest' in instr:
                v= instr['dest']
                vars.add(v)
                defs[v] = []

    #for i in range(0, len(blocks)):
    #    for k in out_set[i]:
    #        if i not in defs[k]:
    #            defs[k].append(i)

    for i in range(0, len(blocks)):
        block = blocks[i]
        for instr in block:
            if 'dest' in instr:
                v = instr['dest']
                if i not in defs[v]:
                    defs[v].append(i)   

    for v in vars:
        i = 0
        has_phi = set()
        while i < len(defs[v]):
            for block in frontier[defs[v][i]]:
                has_phi.add(block)

                if block not in defs[v]:
                    defs[v].append(block)
            i+=1
        for block in has_phi:
            #inefficient to add 1 by 1 but whatever                
            phi = {}
            phi['op'] = 'phi'
            phi['dest'] = v
            phi['args'] = []
            phi['labels'] = []
            #print("Yo ", v, block, pred[block])
            for p in pred[block]:
                phi['args'].append(v)
                phi['labels'].append(blocks[p][0]['label'])
            
            blocks[block] = [blocks[block][0], phi] + blocks[block][1:]

    stack = {}
    for v in vars:
        stack[v] = [0]

    # insert phi nodes before each block for each variable, assuming 
    # that the block has more th

    def get_new_name(v):
        if v in argnames:
            if stack[v][-1] == 0:
                return v
        return v + "." + str(stack[v][-1]) 

    def rename(i):
        block = blocks[i]
        go_back = {}
        for v in stack:
            go_back[v] = stack[v][-1]


        for j in range(0,len(block)):
            instr = block[j]
            if 'op' in instr and instr['op'] == 'phi':
                pass
            elif 'args' in instr:
                instr['args'] = [get_new_name(v) for v in instr['args'] ] 
            if 'dest' in instr:
                v = instr['dest']
                stack[v].append(stack[v][-1]+1)
                instr['dest'] = get_new_name(v)
            
        # this make the phi nodes read from w/e, will be a bit inefficient
        # in this
        # need to somehow track and modify phi nodes this is annoying!!!!

        my_label = block[0]['label']

        for s in succ[i]:
            for j in range(0, len(blocks[s])):
                instr = blocks[s][j]
                if 'op' in instr and instr['op'] == 'phi':
                    for j in range(0, len(instr['labels'])):
                        if instr['labels'][j] == my_label:
                            v = instr['args'][j]
                            instr['args'][j] = get_new_name(v)
                    

        for b in tree[i]:
            rename(b)

        for v in go_back:
            while stack[v][-1] != go_back[v]:
                stack[v].pop()    
            

    rename(0)
    func['instrs'] = []
    for block in blocks:
        for instr in block:
            func['instrs'].append(instr)
    
    return func
    

if __name__ == "__main__":
    prog = json.load(sys.stdin)

    temp = []

    for func in prog['functions']:
        func = to_ssa(func)
        #func = out_of_ssa(func)
        temp.append(func)
    
    prog['functions'] = temp

    json.dump(prog, sys.stdout, indent=2)