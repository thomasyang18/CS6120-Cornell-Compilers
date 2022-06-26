from domlib import make_graph
from domlib import TERMINATORS

import sys
import json
import string

DEBUG = False

def from_ssa(func):
    name, args, blocks, succ, pred = make_graph(func)
    # this implementation does the thing where you add before 
    to_add = []
    label2ind = {}
    
    for i in range(0, len(blocks)):
        to_add.append([])
        if 'op' not in blocks[i][0] and 'label' in blocks[i][0]:
            label2ind[blocks[i][0]['label']] = i

    for i in range(0, len(blocks)):
        for instr in blocks[i]:
            if 'op' in instr and instr['op'] == 'phi':
                for j in range(0, len(instr['labels'])):
                    label = instr['labels'][j]
                    if instr['args'][j] != instr['dest'] and instr['args'][j] != "__undefined" and label2ind[label] in pred[i]:
                        p = label2ind[label]
                        
                        to_add_instr = {
                            "op":"id",
                            "dest":instr['dest'],
                            "type":instr['type'],
                            "args":[instr['args'][j]]
                        }
                        to_add[p].append(to_add_instr)


    temp_body =[]
    for i in range (0,len(blocks)):
        at_end = None
        #handling jump statements before adding
        if 'op' in blocks[i][-1] and blocks[i][-1]['op'] in TERMINATORS:
            at_end = blocks[i][-1]
            blocks[i] = blocks[i][:-1]
        
        for instr in blocks[i]:
            if 'op' in instr and instr['op'] == 'phi':
                continue
            temp_body.append(instr)
        
        temp_body+=to_add[i]

        if at_end is not None:
            temp_body.append(at_end)
    
    func['instrs'] = temp_body
    return func

if __name__ == "__main__":
    prog = json.load(sys.stdin)
    temp = []
    for func in prog['functions']:
        func = from_ssa(func)
        temp.append(func)

    prog['functions'] = temp
    if not DEBUG:
        json.dump(prog, sys.stdout, indent=2)