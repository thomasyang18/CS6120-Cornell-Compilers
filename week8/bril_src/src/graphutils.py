TERMINATORS = 'jmp', 'br', 'ret'

def post_order(vis, graph, v, list):
    if v in vis:
        return
    vis[v] = True
    
    for x in graph[v]:
        post_order(vis, graph, x, list)

    if v != 0:
        list.append(v)

def make_graph(func, again=True):
    body = func['instrs']
    args = []
    if 'args' in func:
        args = func['args']
    name = func['name']
    # Transforms to basic block notation
    blocks = []
    cur_block = []
    for instr in body:
        if 'op' in instr:
            cur_block.append(instr)

            if instr['op'] in TERMINATORS:
                blocks.append(cur_block)
                cur_block = []
        else:
            if cur_block:
                blocks.append(cur_block)
            cur_block = [instr]
    if cur_block:
        blocks.append(cur_block)

    label_to_ind = {}

    for i in range(len(blocks)):
        if 'op' not in blocks[i][0]: #label
            label_to_ind[blocks[i][0]['label']] = i

    succ = [] 
    pred = [] 

    for i in blocks:
        succ.append([])
        pred.append([])

    BREAKAWAYS = 'jmp', 'br'

    def add_edge(i, j):
       # print("ayo ", len(blocks), i, j)
        succ[i].append(j)
        pred[j].append(i)

    for i in range(len(blocks)):
        instr = blocks[i][-1]
        if 'op' in instr and instr['op'] in BREAKAWAYS:
            if instr['op'] == 'jmp':
                add_edge(i, label_to_ind[instr['labels'][0]])
            elif instr['op'] == 'br':
                add_edge(i, label_to_ind[instr['labels'][0]])
                add_edge(i, label_to_ind[instr['labels'][1]])

        elif ('op' not in instr or instr['op'] not in TERMINATORS) and i+1 < len(blocks):
            add_edge(i,i+1)

    new_body = []
    vis_set = {}
    post_order(vis_set, succ, 0, [])
    for i in range(len(blocks)):
        if i in vis_set:
            for instr in blocks[i]:
                new_body.append(instr)
    
    if again:
        func['instrs'] = new_body
        #print("Yo yo yo")
        #for arg in new_body:
        #    print(arg)
        return make_graph(func, again=False)

    return name, args, blocks, succ, pred

def locate_next_scc(succ,pred):
    #keeps yielding next scc
    n = len(succ)
    scc = [0] * n
    stack = []

    def dfs1(i):
        if scc[i]!=0:
            return
        scc[i]+=1
        for x in succ[i]:
            dfs1(x)
        stack.append(i)

    def dfs2(i, v):
        if scc[i] != -1:
            return
        scc[i] = v
        for x in pred[i]:
            dfs2(x,v)

    for i in range(0, n):
        dfs1(i)
    scc = [-1] * n
    v = 0
    while len(stack)>0:
        h = stack.pop()
        if scc[h]==-1:
            dfs2(h,v)
            v+=1

    comp = {}
    for i in range(0,n):
        if scc[i] not in comp:
            comp[scc[i]] = set()
        comp[scc[i]].add(i)

    for cc in comp.values():
        if len(cc) == 0:
            continue

        if len(cc) > 1:
            #if there's only one node at most with stuff outside of SCC, then do that.
            #otherwise if no nodes, then it has to be the entry node, aka 0
            in_set = set()
            for v in cc:
                for p in pred[v]:
                    if p not in cc:
                        in_set.add(v)
            
            if len(in_set) > 1:
                continue
            
            ret_v = 0
            if len(in_set) == 1:
                ret_v = in_set.pop()
            
            yield cc, ret_v
            continue
        
        # if it loops back to itself its a loop too, otherwise nah
        v = cc.pop()
        if v in succ[v]:
            yield {v}, v
