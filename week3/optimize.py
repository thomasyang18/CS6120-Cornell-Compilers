import re
import json
import sys
import os
import random
import string
from sortedcontainers import SortedDict

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

	def LVN_Block(body):
		#convert to ssa
		ssa_map = {}
		temp_body = []

		rand_suf = "_temp_" + ''.join(random.choices(string.ascii_letters, k=5)) + '_'

		for instr in body:
			if 'args' in instr:
				temp_args = []
				for var in instr['args']:
					if var not in ssa_map:
						#If it wasn't declared yet, it comes from the outside so just do it like that
						temp_args.append(var)
					else:
						temp_args.append(var + rand_suf + str(ssa_map[var]))
				instr['args'] = temp_args

			if 'dest' in instr:
				var = instr['dest']
				if var not in ssa_map:
					ssa_map[var] = 0
				else:
					ssa_map[var] += 1
				instr['dest'] = var + rand_suf + str(ssa_map[var])

			temp_body.append(instr)		

		body = temp_body
		if DEBUG:
			print("SSA MAP")
			print(ssa_map)	
	
		#do actual LVN algorithm

		temp_body = []
		var_mapping = SortedDict() #mapping var -> (instruction, [...args])

		for instr in body:
			if 'dest' not in instr:	
				#not an assignment
				temp_body.append(instr)
				continue
			
			print ("Current Mapping " + str(var_mapping))
	
			stuff = []
			if 'args' in instr:
				for arg in instr['args']:
					if arg not in var_mapping:
						#external var, so id map it
						var_mapping[arg] = ('id', [arg])
					
					stuff.append(var_mapping[arg])			
	
			elif 'value' in instr:
				#constant so just append
				stuff.append(('const', instr['value']))

			
			if instr['op'] in ('add', 'mul', 'eq', 'and', 'or'):
				stuff.sort()

			value = (instr['op'], stuff)
			
			allConst = True

			#print(value)

			for val in stuff:
				print(val)
				allConst = allConst and (val[0] == 'const')

			allConst = allConst and (instr['op'] in ('add', 'mul', 'sub', 'div', 'eq', 'lt', 'gt', 'le', 'ge', 'not', 'and', 'or'))

			print("Yo " + str(allConst))

			if allConst:
				val = 0
				#print(str(stuff[0][1]) + " " + str(stuff[1][1]))

				if instr['op'] == 'add':
					val = stuff[0][1] + stuff[1][1]
				
				if instr['op'] == 'mul':
					val = stuff[0][1] * stuff[1][1]
					
				if instr['op'] ==  'sub':
					val = stuff[0][1] - stuff[1][1]
					
				if instr['op'] ==  'div':
					val = stuff[0][1] / stuff[1][1]

				if instr['op'] ==  'eq':
					val = stuff[0][1] == stuff[1][1]

				if instr['op'] ==  'lt':
					val = stuff[0][1] < stuff[1][1]

				if instr['op'] ==  'gt':
					val = stuff[0][1] > stuff[1][1]

				if instr['op'] ==  'le':
					val = stuff[0][1] <= stuff[1][1]

				if instr['op'] ==  'ge':
					val = stuff[0][1] >= stuff[1][1]

				if instr['op'] ==  'not':
					val = True if stuff[0][1] == 'false' else False

				if instr['op'] ==  'and':
					val = stuff[0][1] == stuff[1][1] and stuff[0][1] == 'true'

				if instr['op'] ==  'or':
					val = stuff[0][1] = 'true' or stuff[1][1] == 'true'
						
				if instr['type'] == 'int':
					TODO = 3
					#TODO: force twos complement

				elif instr['type'] == 'bool':
					val = 'true' if val else 'false'

				print("# YOOO " + str(val))

				instr = {
					'op': 'const',
					'type': instr['type'],
					'value': val,
					'dest': instr['dest']	
				}
			#check for readdings - allow function calls to be duplicated

			if instr['op'] != 'call' and not allConst:
				for key in var_mapping:
					if value == var_mapping[key]:
						# assign this, break
						var_mapping[instr['dest']] = value

						instr = {
							'op' : 'id',
							'args': [key],
							'dest': instr['dest'],
							'type': instr['type']
						}
						break

			elif allConst:
				var_mapping[instr['dest']] = value
				
			temp_body.append(instr)

		body = temp_body

		#convert back to normal, so that inputs/output variables are reflected normally
		#all variables should end in _temp#, so can easily check numbers

		temp_body = []

		for instr in body:
			if 'args' in instr:
				temp_args = []
				for var in instr['args']:
		
					search = re.search('(.*)' + rand_suf + '([0-9]+)$', var)
					if not search: #so this is an external variable
						temp_args.append(var)
						continue

					actual = search.group(1)
					last = int(search.group(2))

					if last == ssa_map[actual]:
						#Extract something of the form [var]_temp[num]
						temp_args.append(actual)
					else:
						temp_args.append(var)

				instr['args'] = temp_args
			if 'dest' in instr:
				var = instr['dest']
				search = re.search('(.*)' + rand_suf + '([0-9]+)$', var)
				
				if search:
					actual = search.group(1)
					last = int(search.group(2))
					if last == ssa_map[actual]:
						#Extract something of the form [var]_temp[num]
						instr['dest'] = actual

			temp_body.append(instr)

		body = temp_body

		if DEBUG:
			print("LVN BODY")
			print(body)

		return body

	temp_body = []
	for block in form_blocks(body):
		for instr in LVN_Block(block):
			temp_body.append(instr)

	return temp_body

# Takes a program from standard input and optimizes it with DCE and LVN
def optimize_blocks():
	prog = json.load(sys.stdin)
	
	functions = []	

	for func in prog['functions']:

		if DEBUG:
			print("Before: ")
			print(func['instrs'])
	
		func['instrs'] = LVN(func['instrs'])
		#func['instrs'] = DCE(func['instrs'])
	
		if DEBUG:
			print("After :")
			print(func['instrs'])

		functions.append(func)

	prog['functions'] = functions
	
	if not DEBUG:
		json.dump(prog, sys.stdout, indent=2)

if __name__ == "__main__":
	optimize_blocks()
