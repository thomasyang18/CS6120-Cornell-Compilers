import json
import sys

#Code from last week
TERMINATORS = 'jmp', 'br', 'ret'
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


def print_blocks(blocks):
	for block in blocks:
		print("-----------------------")
		for instr in block:
			print(instr)
		print("-----------------------")

# Takes a basic block and does DCE on it
def DCE(body):
	while True:
		kept = []
		is_used = {}
		for instr in reversed(body):
			keep = True

			if 'dest' in instr:
				if instr['dest'] not in is_used:
					keep = False	
			
			if 'args' in instr:
				for arg in instr['args']:
					is_used[arg] = True
			
			if keep:
				kept.append(instr)
			
		kept.reverse()		

		if len(kept) == len(body):
			body = kept
			break

		body = kept

	
	return body

# Takes a basic block and does LVN on it 
def LVN(body):
	return None

# Takes a list of blocks, and performs optimization opt_f() on each block
def optimize(blocks, opt_f):
	ret_blocks = []
	for block in blocks:
		ret_blocks.append(opt_f(block))

	return ret_blocks

# Takes a program from standard input and optimizes it with DCE and LVN
def optimize_blocks():
	prog = json.load(sys.stdin)
	
	blocks = []	

	for func in prog['functions']:
		for block in form_blocks(func['instrs']):
			blocks.append(block)
	
	print_blocks(blocks)	
	
	#blocks = optimize(blocks, LVN)
	blocks = optimize(blocks, DCE)

	print("After Optimization")

	print_blocks(blocks)

if __name__ == "__main__":
	optimize_blocks()
