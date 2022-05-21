import sys
max_int = sys.maxsize
min_int = -sys.maxsize-1
inf = (min_int, max_int)

def evaluate_expr(op, args):
    # Can be assured that all operations are valid, or if invalid, only invalid because '?' value or div by zero error or someth

    #catch edge cases pre-emptively
    if '?' in  args:
        if op == 'mul':
            if 0 in args:
                return (0,0)
        #there's like a bunch of edge cases with this but ill just handle most obvious ones
        if op == 'lt':
            if args[0] == max_int or args[1] == min_int:
                return True
        
        if op == 'gt':
            if args[0] == min_int or args[1] == max_int:
                return True

        if op == 'le':
            if args[0] == min_int or args[1] == max_int:
                return True

        if op == 'ge':
            if args[0] == max_int or args[1] == min_int:
                return True

        if op == 'and':
            if False in args:
                return False

        if op == 'or':
            if True in args:
                return True

        return inf
        
#TODO: rest of this

    #If any number overflows, just assume it's '?'
    def in_range(x):
        return x >= min_int and x <= max_int


    if op == 'mul':
        tlist = []
        for i in range(0,2):
            for j in range(0,2):
                tlist.append(args[0][i]*args[1][j])

        if any(not in_range(x) for x in tlist):
            return inf

        return (min(tlist), max(tlist))

    if op == 'div':
        if args[1][0] <= 0 <= args[1][1]:
            return inf

        tlist = []
        for i in range(0,2):
            for j in range(0,2):
                tlist.append(args[0][i] // args[1][j])

        if any(not in_range(x) for x in tlist):
            return inf

        return (min(tlist), max(tlist))

        
    if op == 'add':
        if not in_range(args[0][0] + args[1][0]) or not in_range(args[0][1] + args[1][1]):
            return inf
        return (args[0][0] + args[1][0], args[0][1] + args[1][1])
    if op == 'sub':
        if not in_range(args[0][0] - args[1][1]) or not in_range(args[1][0] - args[0][1]):
            return inf
        return (args[0][0] - args[1][1], args[1][0] - args[0][1])


    #all normal boolean/id expressions
    if op == 'eq':
        return args[0] == args[1]
    if op == 'lt':
        return  args[0] < args[1] 
    if op == 'gt':
        return  args[0] > args[1] 
    if op == 'le':
        return  args[0] <= args[1] 
    if op == 'ge':
        return  args[0] >= args[1] 
    if op == 'not':
        return  args[0] == 'false' 
    if op == 'and':
        return  args[0] == 'true' and args[1] == 'true' 
    if op == 'or':
        return  args[0] == 'true' or args[1] == 'true' 
    if op == 'id':
        return args[0]



def id(arg):
    if arg['type'] == 'bool':
        return '?'
    if arg['type'] == 'int':
        return '?'
    return None

def merge(in_set, apply_set):
    for arg in apply_set:
        if arg not in in_set:
            in_set[arg] = apply_set[arg]
        
        #print("yo ", arg, in_set[arg])

        if in_set[arg] == '?' or in_set[arg] is True or in_set[arg] is False:
            continue

        in_set[arg] = (min(in_set[arg][0], apply_set[arg][0]), max(in_set[arg][1], apply_set[arg][1]))


        if in_set[arg][0] > in_set[arg][1]:
            in_set[arg] = '?'

def transfer(instrs, in_set):
    for instr in instrs:
        # If the instruction is a basic instruction and the args are constant, evaluate
        if 'dest' not in instr:
            continue

        args = []
        if 'args' in instr:
            for arg in instr['args']:
                if arg not in in_set or in_set[arg] == '?':
                    args.append('?')
                elif arg in in_set:
                    args.append(in_set[arg]) 

        if instr['op'] == 'const':
            if instr['type'] == 'bool':
                in_set[instr['dest']] = instr['value']
            else:
                if instr['dest'] not in in_set or in_set[instr['dest']] == '?':
                    in_set[instr['dest']] = (instr['value'], instr['value'])
                else:
                    #merge em
                    in_set[instr['dest']] = (min(instr['value'], in_set[instr['dest']][0]), max(instr['value'], in_set[instr['dest']][1]))
        elif instr['op'] not in ('jmp', 'br', 'ret', 'call', 'print'):
            in_set[instr['dest']] = evaluate_expr(instr['op'], args)
        else:
            in_set[instr['dest']] = '?'

    return in_set