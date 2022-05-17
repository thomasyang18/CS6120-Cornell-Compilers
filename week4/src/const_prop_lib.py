def evaluate_expr(op, args):
        if op == 'mul':
            return args[0] * args[1]
        if op == 'div':
            return args[0] // args[1]
        if op == 'add':
            return args[0] + args[1]
        if op == 'sub':
            return args[0] - args[1]
        if op == 'eq':
            return 'true' if args[0] == args[1] else 'false'
        if op == 'lt':
            return 'true' if args[0] < args[1] else 'false'
        if op == 'gt':
            return 'true' if args[0] > args[1] else 'false'
        if op == 'le':
            return 'true' if args[0] <= args[1] else 'false'
        if op == 'ge':
            return 'true' if args[0] >= args[1] else 'false'
        if op == 'not':
            return 'true' if args[0] == 'false' else 'true'
        if op == 'and':
            return 'true' if args[0] == 'true' and args[1] == 'true' else 'false'
        if op == 'or':
            return 'true' if args[0] == 'true' or args[1] == 'true' else 'false'
        if op == 'id':
            return args[0]



def id():
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

        allConst = True
        args = []
        if 'args' in instr:
            for arg in instr['args']:
                if arg not in in_set or in_set[arg] == '?':
                    allConst = False
                elif arg in in_set:
                    args.append(in_set[arg]) 
        
        if instr['op'] == 'const':
            in_set[instr['dest']] = instr['value']
        elif allConst and instr['op'] not in ('jmp', 'br', 'ret', 'call', 'print'):
            in_set[instr['dest']] = evaluate_expr(instr['op'], args)
        else:
            in_set[instr['dest']] = '?'

    return in_set
