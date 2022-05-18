import sys

def evaluate_expr(op, args):
    # Can be assured that all operations are valid, or if invalid, only invalid because '?' value or div by zero error or someth
        max_int = sys.maxsize
        min_int = -sys.maxsize-1

        #catch edge cases pre-emptively
        if '?' in  args:
            if op == 'mul':
                if 0 in args:
                    return 0
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

            return '?'

        if op == 'mul':
            return args[0] * args[1]
        if op == 'div':
            if args[1] == 0:
                return '?'
            return args[0] // args[1]
        if op == 'add':
            return args[0] + args[1]
        if op == 'sub':
            return args[0] - args[1]
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
    return '?'

def merge(in_set, apply_set):
    for arg in apply_set:
        if arg not in in_set:
            in_set[arg] = apply_set[arg]
        elif in_set[arg] != apply_set[arg]:
            in_set[arg] = id()

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
            in_set[instr['dest']] = instr['value']
        elif instr['op'] not in ('jmp', 'br', 'ret', 'call', 'print'):
            in_set[instr['dest']] = evaluate_expr(instr['op'], args)
        else:
            in_set[instr['dest']] = '?'

    return in_set
