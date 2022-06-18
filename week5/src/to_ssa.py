from cProfile import label
import sys
import os

from domlib import find_dominators
from domlib import build_frontier
from domlib import build_tree
from domlib import make_graph

import json

def to_ssa(func):
    dominators = find_dominators(func, False, False)
    tree = build_tree(dominators, False)
    frontier = build_frontier(func, tree, dominators, False)
    name, args, blocks, succ, pred = make_graph(func)    
    
    vars = set()

    defs = {} # map of variables to list of blocks

    for i in range(0, len(blocks)):
        for instr in blocks[i]:
            if 'dest' in instr:
                v= instr['dest']
                vars.add(v)
                
                if v not in defs:
                    defs[v] = []
                if i not in defs[v]:
                    defs[v].append(i) 
        
    for v in vars:
        i = 0
        has_phi = set()
        while i < len(defs[v]):
            for block in frontier[defs[v][i]]:
                #inefficient to add 1 by 1 but whatever                
                has_phi.add(block)

                if block not in defs[v]:
                    defs[v].append(block)
            i+=1

        for block in has_phi:
            blocks[block] = 

    stack = {}
    for v in var2phi:
        stack[v] = [0]

    # insert phi nodes before each block for each variable, assuming 
    # that the block has more th
    

    def rename(i):
        block = blocks[i]
        go_back = {}
        for v in stack:
            go_back[v] = stack[v][-1]

        for j in range(0,len(block)):
            instr = block[j]

            if 'args' in instr:
                instr['args'] = [stack[v][-1] if v in stack else v for v in instr['args'] ] 
            if 'dest' in instr:
                v = instr['dest']
                stack[v].append(stack[v][-1]+1)
                instr['dest'] = stack[v][-1]
            
        # this make the phi nodes read from w/e, will be a bit inefficient
        # in this
        # need to somehow track and modify phi nodes this is annoying!!!!

        for s in succ[i]:
                

        for b in tree[i]:
            rename(b)

        for v in go_back:
            while stack[v][-1] != go_back[v]:
                stack[v].pop()    
            

    rename(0)

if __name__ == "__main__":
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        func = to_ssa(func)
        #func = out_of_ssa(func)

    json.dump(prog, sys.stdout, indent=2)