from cProfile import label
import sys
import os

from domlib import find_dominators
from domlib import build_frontier
from domlib import build_tree
from domlib import make_graph

import json

def to_ssa(func):
    dominators = find_dominators(func, True, False)
    tree = build_tree(dominators, False)
    frontier = build_frontier(func, tree, dominators, False)
    name, args, blocks, succ, pred = make_graph(func)    

    var2blocks = {}
    var2phiblocks = {}

    label2ind = {}
    for i in range(0, len(blocks)):
        if 'label' in blocks[i][0]:
            label2ind[blocks[i][0]['label']] = i
    
    phi_node_inc = []
    for i in range(0, len(blocks)):
        phi_node_inc.append(set())

    for i in range(0, len(blocks)):
        #print(blocks[i])
        for instr in blocks[i]:
            if 'dest' in instr:
                if instr['dest'] not in var2blocks:
                    var2blocks[instr['dest']] = set()
                    var2phiblocks[instr['dest']] = set()
                var2blocks[instr['dest']].add(i)
                if instr['op'] == 'phi':
                    var2phiblocks[instr['dest']].add(i)
                    for label in instr['labels']:
                        phi_node_inc[i].add(label2ind[label])

    for v in var2blocks: # v = string, defs = set of ints (blocks)
        while True:
            to_upd = set()
            for d in var2blocks[v]: # d = int of blocks
                for block in frontier[d]: # block = int of block
                    #add node to phi block
                    phi_node_inc[block].add(d)
                    var2phiblocks[v].add(block)
                    if block not in var2blocks[v]:
                        to_upd.add(block)
            if len(to_upd) == 0:
                break
            for block in to_upd:
                var2blocks[v].add(block)


    phiblocks2var = {}
    for i in range(0, len(block)):
        phiblocks2var[i] = {}

    stack_cnt = {}
    stack = {}
    for v in var2phiblocks:
        stack[v] = [v + "0"]
        stack_cnt[v] = 1
        for block in var2blocks[v]:
            phiblocks2var[block].add(v)
    
    def rename(i):
        block = blocks[i]
        for instr in block:
            if 'args' in instr:
                for arg in instr['arg']:
                    instr['arg'][arg] = stack[arg][-1]

            if 'dest' in instr:
                cur = instr['dest']
                stack_cnt[cur]+=1
                stack[cur].append(cur + stack_cnt[cur])
                instr['dest'] = stack[cur][-1]

            for s in succ[i]:
                for p in phiblocks2var[s]:
                    
    rename(0)

    func['instrs'].clear()
    for block in blocks:
        for instr in block:
            func['instrs'].append(instr)

    return func

def phi(func):
    return func

if __name__ == "__main__":
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        func = to_ssa(func)
        func = phi(func)

    json.dump(prog, sys.stdout, indent=2)