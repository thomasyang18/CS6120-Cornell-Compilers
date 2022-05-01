import json
import sys
import os

TERMINATORS = 'jmp', 'br', 'ret'

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True'

def form_blocks(body):
	cur_block = []
	for instr in body:
		if 'op' in instr:#actual instruction
			cur_block.append(instr)
			
			if instr['op'] in TERMINATORS:
				yield cur_block
				cur_block = []
		else: #label
			if cur_block:
				yield cur_block
	
			cur_block = [instr]

	
	if cur_block:
		yield cur_block


#Takes a basic block  and does DCE Locally on it
def DCE_Local(body):	
	used_vars = {}
	res = []
	
	for instr in body:
		if 'dest' in instr:
			used_vars[instr['dest']] = True
	
	for instr in reversed(body):
		skip = False
		if 'dest' in instr:
			if instr['dest'] not in used_vars:
				skip = True
			else:
				used_vars.pop(instr['dest'])
		
		if 'args' in instr:
			for arg in instr['args']:
				used_vars[arg] = True

		if not skip:
			res.append(instr)
		
	res.reverse()
	return res

SIDE_EFFECTS = 'call', 'print'
JMPS = 'jmp', 'br'

# Takes a function and does DCE globally on it
def DCE_Global(body):
	used = {}
	for instr in body:
		if 'args' not in instr:
			continue
		for arg in instr['args']:
			used[arg]=True
	
	res = []
	for instr in body:
		res.append(instr)
		if 'dest' not in instr:
			#probably an important instruction like label or jmp or something, continue
			continue
		if instr['dest'] in used:
			#used so continue
			continue
		
		if 'op' in instr and (instr['op'] in SIDE_EFFECTS or instr['op'] in JMPS):
			#if it's a call or print function, never remove it, if it's a jmp or br, never remove it
			continue
		res.pop()
	
	return res

def DCE(body):
	# Iterate to convergence; by that probably just count # of instructions or someth

	for i in range(0, len(body)+5):
		temp_body = []
		
		for block in form_blocks(body):
			for instr in DCE_Local(block):
				temp_body.append(instr)	
		
		body = DCE_Global(temp_body)

	return body

# Takes a function and does LVN on it 
def LVN(body):
	return body

# Takes a program from standard input and optimizes it with DCE and LVN
def optimize_blocks():
	prog = json.load(sys.stdin)
	
	functions = []	

	for func in prog['functions']:

		if DEBUG:
			print("Before: ")
			print(func['instrs'])
	
		func['instrs'] = LVN(func['instrs'])
		func['instrs'] = DCE(func['instrs'])
	
		if DEBUG:
			print("After :")
			print(func['instrs'])

		functions.append(func)

	prog['functions'] = functions
	
	if not DEBUG:
		json.dump(prog, sys.stdout, indent=2)

if __name__ == "__main__":
	optimize_blocks()
