import re
import json
import sys
import os
import random
import string
from lvn import LVN_Block

TERMINATORS = 'jmp', 'br', 'ret'

DEBUG = 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True'


COMM_OPS = 'add', 'mul', 'eq', 'and', 'or'

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

	def noLVN_Block(body):
		#convert to ssa
		ssa_map = {}
		temp_body = []

		rand_suf = "_temp_" + ''.join(random.choices(string.ascii_letters, k=5)) + '_'
		rand_suf = "_"

		#stuff here to 
		#value is denoted as a tuple (instr.op, instr['args'][0], [1]...)
		

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
		table = []
		var2num = {}
                #value is denoted as a tuple (instr.op, instr['args'][0], [1]...)

		for instr in body:
			if 'dest' not in instr:	
				#not an assignment
				temp_body.append(instr)
				continue

			value = (instr['op'])
			if 'args' in instr:

				temp_args = [var2num[arg] for arg in instr['args']]

				if instr['op'] in COMM_OPS:
					temp_args.sort()

				for arg in temp_args:
					value += (arg)

				instr['args'] = temp_args

			
			#no constant folding for now
			#no copy prop for now
			#if value in var2num:
						
			#else:
						
			print(instr)
			print(value)

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


	def no2LVN_Block(body):
		table = [] #table is tuple of ((value tuple), "var name")
		var2num = {}
		temp_body = []
		cnt_up = {}
		
		for j in range(len(body)):
			instr = body[j]
			value = (instr['op'],)
			if 'args' in instr:
				for arg in instr['args']:
					#if it doesn't exist, add it on
					for row in table:
						if row[1] == arg:
							break
					else:
						temp_instr = {}
						temp_instr['op'] = 'none'
						dest = ''

						OverWrite = False
						for k in range(j+1, len(body)):
							instr2 = body[k]
							if 'dest' in instr2 and instr2['dest'] == dest:
								OverWrite = True
								break

						if OverWrite:
							if dest not in cnt_up:
								cnt_up[dest] = 2
							else:
								cnt_up[dest]=cnt_up[dest]+1

							dest += '_' + str(cnt_up[dest])
							arg = dest

						var2num[arg] = len(table)
						table.append((temp_instr, arg))
						
					value += (var2num[arg],)

			num = len(table)
			dest = ''
		
			if 'dest' in instr and instr['op'] not in SIDE_EFFECTS: #okay to optimize 

				dest = instr['dest']

				for i in range(len(table)):
					row = table[i]
					if row[0] == value: #instr = dest = id i
						temp_instr = {}
						temp_instr['dest'] = dest
						temp_instr['op'] = 'id'
						temp_instr['args'] = [i]
						num = i
						instr = temp_instr
						break
				else:
					
					OverWrite = False
					for k in range(j+1, len(body)):
						instr2 = body[k]
						if 'dest' in instr2 and instr2['dest'] == dest:
							OverWrite = True
							break

					if OverWrite:
						if dest not in cnt_up:
							cnt_up[dest] = 2
						else:
							cnt_up[dest]=cnt_up[dest]+1

						dest += '_' + str(cnt_up[dest])
						instr['dest'] = dest
					else:
						dest = instr['dest']
					
					table.append((value, dest))
		
			if 'args' in instr:
				print(instr['args'])
	
			#convert from val form to variable form with table[num][1]
			if 'args' in instr:
				instr['args'] = [table[i][1] for i in instr['args']]

			if 'dest' in instr and instr['op'] not in SIDE_EFFECTS:
				var2num[dest] = num

			temp_body.append(instr)

		return temp_body


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
