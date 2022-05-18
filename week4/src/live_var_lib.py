def id(arg):
    ''

def merge(in_set, apply_set):
    for arg in apply_set:
        in_set[arg] = ''

def transfer(instrs, in_set):
    #print ("Looking at block ")
    #print(instrs)
    #print(in_set)
    #print("-------------------------------")

    for instr in reversed(instrs):

        if 'dest' in instr:
            if instr['dest'] in in_set:
                in_set.pop(instr['dest'])
        
        if 'args' in instr:
            for arg in instr['args']:
                in_set[arg] = ''
        

    return in_set