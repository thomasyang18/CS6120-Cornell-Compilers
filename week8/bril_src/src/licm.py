import sys, json, argparse
from graphutils import make_graph

DEBUG = False

def parse_args():
    parser = argparse.ArgumentParser(description='Options')

    parser.add_argument('-d', '--debug', 
                    help='If true, don\'t dump json',    
                    default='false', 
                    type=str, 
                    choices = ['true', 'false'])

    return vars(parser.parse_args())

"""
This will precompute very little. Premature optimization SUCKS.
The only thing it will precompute is adding headers, and putting
instructions inside of 

This assumes that elements are in SSA form, which makes analysis somewhat
easier on data flow section, but phi nodes should screw things up pretty badly.

Moreover, move the instructions in an orderly way, so that the things marked first 
(dicts preserve insertion order)
"""

def limc(func):
    name, args, blocks, succ, pred = make_graph(func)
    



if __name__ == "__main__":
    args = parse_args()

    DEBUG = args['debug'] == 'true'

    prog = json.load(sys.stdin)

    prog['functions'] = [limc(func) for func in prog['functions']]

    if not DEBUG:
        json.dump(prog, sys.stdout, indent=2)