from worklist import worklist_algo
import argparse
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Different Worklist Data Flow Variants')

    #Default is constant propogation
    #Can choose between live variables, initialized variables, and range variables

    parser.add_argument('-t', '--type', 
                    help='Set the Data Flow Analysis Type',    
                    default='const', 
                    type=str, 
                    choices = ['const', 'live', 'init', 'range'])

    return vars(parser.parse_args())




if __name__ == "__main__":
    args = parse_args()
    
    w_id = None
    w_merge = None
    w_transfer = None
    dir = 'forward'

    if args['type'] == 'const':
        from const_prop_lib import id, merge, transfer
        w_id = id
        w_merge = merge
        w_transfer = transfer
    if args['type'] == 'live':
        from live_var_lib import id, merge, transfer
        w_id = id
        w_merge = merge
        w_transfer = transfer
    if args['type'] == 'init':
        from init_var_lib import id, merge, transfer
        w_id = id
        w_merge = merge
        w_transfer = transfer
    if args['type'] == 'range':
        from range_var_lib import id, merge, transfer
        w_id = id
        w_merge = merge
        w_transfer = transfer
    
    
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        worklist_algo(func, w_id, w_merge, w_transfer, dir)