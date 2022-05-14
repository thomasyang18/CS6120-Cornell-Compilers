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


SIDE_EFFECTS = 'print', 'call'

def LVN_Block(block):
	global table
	global var2num
	table = []
	var2num = {}
	remap_times = {}

	temp_body = []
	
	for start in range(len(block)):
		instr = block[start]
		if 'op' not in instr:
			#label continue
			temp_body.append(instr)
			continue
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
		
			#do bookkeeping on duplciate varrs
			dest = instr['dest']
			
			
			for j in range(start+1, len(block)):
				if 'dest' in block[j] and block[j]['dest'] == dest:
					if dest not in remap_times:
						remap_times[dest] = 2
					else:
						remap_times[dest] +=1
					
					dest = dest + "_" + str(remap_times[dest])
					# For all arguments between now and the next remapping, need to rename all references to this thing accordingly		
			
					for k in range(start+1, len(block)):
						if 'args' in block[k]:
							temp_args = []
							for arg in block[k]['args']:
								if arg == instr['dest']:
									arg = dest
								temp_args.append(arg)
							block[k]['args'] = temp_args

						if 'dest' in block[k] and block[k]['dest'] == instr['dest']:
							break

					instr['dest'] = dest
					break

			# end of duplicate vars			

			#if has side effects, don't allow optimization, treat it as a blank var 

			if instr['op'] in SIDE_EFFECTS:
				table.append(((), dest))
			else:
				table.append((value, dest))

			if 'args' in instr:
				instr['args'] = [table[var2num[arg]][1] for arg in instr['args']]

		var2num[instr['dest']] = num
		
		temp_body.append(instr)

	return temp_body
