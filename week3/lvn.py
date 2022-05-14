table = []
var2num = {}


def build_value(instr):
	global table
	global var2num
	value = (instr['op'],)
	if 'args' in instr:
		for arg in instr['args']:
			if arg not in var2num:
				var2num[arg] = len(table)
				table.append(((), arg))

			value += (var2num[arg],)
	
	if 'value' in instr:
		value += (instr['value'],)

	return value


SIDE_EFF = 'print', 'call'

def LVN_Block(block):
	global table
	global var2num
	table = []
	var2num = {}

	temp_body = []
	
	for instr in block:
		value = build_value(instr)
		
		#TODO: If it's a side effect or no dest, skip stuff
		
		num = len(table)

		if 'dest' not in instr:
			#skip
			if 'args' in instr:
				instr['args'] = [table[var2num[arg]][1] for arg in instr['args']]

			temp_body.append(instr)
			continue

		for i in range(len(table)):
			row = table[i]
			if row[0] == value:
				#Don't add this to the value table, make this a copy operation
				num = i
				instr = {
					'dest': instr['dest'],
					'op': 'id', 'args':
					[row[1]]
				}
				break
		else:
			num = len(table)
			dest = instr['dest']
		
			#do bookkeeping on duplciate varrs


			# end of duplicate vars			

			#if has side effects, don't allow optimization, treat it as a blank var 

			table.append((value, dest))

			instr['args'] = [table[var2num[arg]][1] for arg in instr['args']]

		var2num[instr['dest']] = num
		
		temp_body.append(instr)

	return temp_body
