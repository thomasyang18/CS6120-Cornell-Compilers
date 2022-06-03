import dom_validators


def post_order(vis, graph, v, list):
    if v in vis:
        return
    vis[v] = True
    
    for x in graph[v]:
        post_order(vis, graph, x, list)

    if v != 0:
        list.append(v)


TERMINATORS = 'jmp', 'br', 'ret'
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

def find_dominators_my_way(func, print_cfg, printop):
    # Print dominators at end
    name, args, blocks, succ, pred = make_graph(func)

    if print_cfg:
        """for i in range(0, len(blocks)):
            print("b" + str(i), ":")
            for instr in blocks[i]:
                print(instr)
        print("-----------------------------------------")"""

        for i in range(0, len(blocks)):
            print("b" + str(i), ":")
            print("pred: ", pred[i])
            print("succ, ", succ[i])


    dom = {}
    for i in range(0,len(blocks)):
        dom[i] = {i}

    changed = True
    while changed:
        changed = False
        for v in range(0,len(blocks)):
            temp = set()
            if len(pred[v]) > 0:
                temp = dom[pred[v][0]]

            #print("cur",v)
            for p in pred[v]:
              #  print("before temp", temp, "before dom", dom[p])
                temp = temp.intersection(dom[p])
              #  print("after temp", temp)
            
            #print("yoasdfkasdjfkladsjfkladjfk ", v, temp)
            temp = temp.union(dom[v])

            if dom[v] != temp:
                changed = True
                dom[v] = temp
    
    if printop:
        print ("-------------------Finding Dominators -------------------------")
        for i in range(0, len(blocks)):
            print("b"+str(i),":", str(dom[i]))
        
    return dom



def find_dominators(func, print_cfg, printop):
    # Print dominators at end

    name, args, blocks, succ, pred = make_graph(func)

    if print_cfg:
        """for i in range(0, len(blocks)):
            print("b" + str(i), ":")
            for instr in blocks[i]:
                print(instr)
        print("-----------------------------------------")"""

        for i in range(0, len(blocks)):
            print("b" + str(i), ":")
            print("pred: ", pred[i])
            print("succ: ", succ[i])


    dom = {}
    for i in range(1,len(blocks)):
        dom[i] = set(range(0,len(blocks)))

    dom[0] = {0}

    list = []
    post_order({}, succ, 0, list)
    list.reverse()

    changed = True
    while changed:
        changed = False
        for v in list:
            temp = set()
            if len(pred[v]) > 0:
                temp = dom[pred[v][0]]

            for p in pred[v]:
                temp = temp.intersection(dom[p])
            
            temp.add(v)

            if dom[v] != temp:
                changed = True
                dom[v] = temp

    if printop:    
        print ("-------------------Finding Dominators -------------------------")
        for i in range(0, len(blocks)):
            print("b"+str(i),":", str(dom[i]))
        
    return dom

def build_tree(dominators, printop):
    # Print tree at end

    # Just basic O(n^2) Ig
    tree = []
    for i in range(0, len(dominators)):
        tree.append([])

    #Process things in sorted order based on length of the set
    #Given the dominators of the set, append to the one with the biggest depth.
    depth = {}
    depth[0] = 0
    to_check = list(range(1,len(dominators)))

    to_check = sorted(to_check, key = lambda e: len(dominators[e]))

    for v in to_check:
        i = 0
        for j in dominators[v]:
            if v == j:
                continue
            elif depth[j] >= depth[i]:
                i = j
        
        depth[v] = depth[i]+1
        tree[i].append(v)

    if printop:
        print ("-------------------Finding Tree -------------------------")
        for i in range(0, len(dominators)):
            print(i,":",tree[i])

    dom_validators.is_correct_tree(tree, dominators, 0, set())


    return tree

#Kind of bad O(n) algorithm to check but whatever
def dominates(tree, a, b):
    if a == b:
        return True
    for x in tree[a]:
        if dominates(tree, x, b):
            return True
    return False

def build_frontier(func, tree, dominators, printop):
    name, args, blocks, succ, pred = make_graph(func)

    #Do something like this
    frontier = []

    for a in range(0, len(dominators)):
        ans = set()
        for b in range(0, len(dominators)):
            if not dominates(tree,a,b):
                if any(dominates(tree, a, p) for p in pred[b]):
                    ans.add(b) 

        frontier.append(ans)

    #dom_validators.is_correct_frontier(pred, dominators, frontier)


    if printop:
        print("---------------Finding Domination Frontier----------------")
        for i in range(0, len(dominators)):
            print(i,":",frontier[i])
    return frontier