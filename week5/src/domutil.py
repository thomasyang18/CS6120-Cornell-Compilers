import json 
import sys
import argparse
import domlib

def parse_args():
    parser = argparse.ArgumentParser(description = 'Domination Util Flags')

    parser.add_argument('-t', '--type', 
                        help = 'dom = Dominators for each node, tree = Dominators Tree, frontier = Dominance Frontier for each node', 
                        default = 'all',
                        type = str,
                        choices = ['all', 'dom', 'tree', 'frontier'])

    parser.add_argument('--printcfg',
                        help = 'option to print CFG',
                        default = 'no',
                        type = str,
                        choices = ['yes','no'])

    parser.add_argument('-p', '--print',
                        help = 'Option to print all the breakpoints and stuff',
                        default = 'yes',
                        type = str,
                        choices = ['yes','no']
                        )

    parser.add_argument('--myway',
                        help = "Seeing if my domination algorithm is the same as theirs",
                        default = "no",
                        type = str,
                        choices = ["yes","no"])

    return vars(parser.parse_args())

if __name__ == "__main__":
    args = parse_args()

    prog = json.load(sys.stdin)

    for func in prog['functions']:
        if args['print'] == 'yes':
            print("==============Operating on function", func['name'], "=========================")
        
        #compute dominance tree
        dominators = None

        if args['myway'] != 'yes':
            dominators = domlib.find_dominators(func,args['printcfg'] == 'yes', args['print'] == 'yes') 
        else:
            dominators = domlib.find_dominators_my_way(func, args['printcfg'] == 'yes',  args['print'] == 'yes')


        if args['type'] == 'dom':
            continue

        tree = domlib.build_tree(dominators,  args['print'] == 'yes')

        if args['type'] == 'tree':
            continue

        frontier = domlib.build_frontier(func, tree, dominators,  args['print'] == 'yes')

        if args['type'] == 'frontier':
            continue

