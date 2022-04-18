import json
import sys

#Given a bril prorgam, 

def add_print8080_after_prints():
	prog = json.load(sys.stdin)
	
	for func in prog['functions']:
		func['instrs'].insert(0,
			{
          		"dest": "unused_8080_val",
          		"op": "const",
          		"type": "int",
          	"value": 8080
        		}			
		)
		for instr in func['instrs']:
			if 'op' in instr and instr['op'] == 'print':
				instr['args'].append('unused_8080_val')						

	#print(prog)

	json.dump(prog, sys.stdout)
	


if __name__ == "__main__":
	add_print8080_after_prints()
