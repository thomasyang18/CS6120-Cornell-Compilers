import json
import sys

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

def mycfg():
	prog = json.load(sys.stdin)
	
	blocks = []	

	for func in prog['functions']:
		for block in form_blocks(func['instrs']):
			blocks.append(block)
			print(block)

	#if end is jmp or br, add some edges
	#otherwise if end is not terminator, add an edge from one to the next
	
	label_to_ind = {}

	for i in range(len(blocks)):
		if 'op' not in blocks[i][0]: #label
			label_to_ind[blocks[i][0]['label']] = i
	
	edge_list = []

	BREAKAWAYS = 'jmp', 'br'

	for i in range(len(blocks)):
		instr = blocks[i][-1]
		if 'op' in instr and instr['op'] in BREAKAWAYS:
			if instr['op'] == 'jmp':
				edge_list.append((i, label_to_ind[instr['labels'][0]]))
			elif instr['op'] == 'br':
				edge_list.append((i, label_to_ind[instr['labels'][0]]))
				edge_list.append((i, label_to_ind[instr['labels'][1]]))			
		elif instr['op'] not in TERMINATORS and i != len(blocks)-1:
			edge_list.append((i, i+1))
			
	for edge in edge_list:
		print(str(edge[0]) + " is connected to " + str(edge[1]))	
if __name__ == "__main__":
	mycfg()


