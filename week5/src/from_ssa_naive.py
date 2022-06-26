from domlib import make_graph

import sys
import json
import string

DEBUG = False

def from_ssa(func):
    name, args, blocks, succ, pred = make_graph(func)
    arg_names = {'__undefined'} #just to avoid that edge case lol 
    for arg in args:
        arg_names.add(arg['name'])
    for block in blocks:
        for i in range(0, len(block)):
            instr = block[i]
            if 'dest' in instr and instr['dest'] not in arg_names:
                instr['dest'] = instr['dest'].rstrip(string.digits)
                instr['dest'] = instr['dest'][:-1]
            if 'args' in instr:
                temp_args = []
                for arg in instr['args']:
                    if arg not in arg_names:
                        arg = arg.rstrip(string.digits)
                        arg = arg[:-1]
                    temp_args.append(arg)
                instr['args'] = temp_args

    
    
    temp_body =[]
    for block in blocks:
        for instr in block:
            if 'op' in instr and instr['op'] == 'phi':
                continue
            temp_body.append(instr)
    
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