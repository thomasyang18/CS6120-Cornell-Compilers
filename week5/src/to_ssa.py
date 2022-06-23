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
import argparse


DEBUG = False

def parse_args():
    parser = argparse.ArgumentParser(description='Different Worklist Data Flow Variants')

    parser.add_argument('-d', '--debug', 
                    help='If true, don\'t dump json',    
                    default='false', 
                    type=str, 
                    choices = ['true', 'false'])

    return vars(parser.parse_args())


def to_ssa(func):
    dominators = find_dominators(func, False, False)
    tree = build_tree(dominators, False)
    frontier = build_frontier(func, tree, dominators, False)
    name, args, blocks, succ, pred = make_graph(func)  
             
    
    vars = set()

    argnames = {}
    if 'args' in func:
        argnames = {arg['name'] for arg in func['args']}
    vars.update(argnames)

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
    
    func['instrs'] = [{"label":"ssa_dummy_block"}]
    for block in blocks:
        for instr in block:
            func['instrs'].append(instr)    

    in_set, out_set = worklist_algo(func)

    dominators = find_dominators(func, False, False)
    tree = build_tree(dominators, False)
    frontier = build_frontier(func, tree, dominators, False)
    name, args, blocks, succ, pred = make_graph(func) 

    if name == 'gcd' and DEBUG:
        print("preds")
        for i in range(0, len(blocks)):
            print(i,pred[i],in_set[i])
        print("succ")
        for i in range(0, len(blocks)):
            print(i,succ[i],out_set[i])

    defs = {}

    for v in vars:
        defs[v] = []
        for i in range(0, len(blocks)):
            if v in in_set[i] and v in out_set[i] and len(in_set[i][v]) >= 2 and len(out_set[i][v]) == 1:
                defs[v].append(i)

    for v in vars:
        for block in defs[v]:
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

        #return # this means we do not pop off stack variables at the end
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
    args = parse_args()

    DEBUG = args['debug'] == 'true'

    prog = json.load(sys.stdin)

    temp = []

    for func in prog['functions']:
        func = to_ssa(func)
        #func = out_of_ssa(func)
        temp.append(func)
    
    prog['functions'] = temp
    if not DEBUG:
        json.dump(prog, sys.stdout, indent=2)