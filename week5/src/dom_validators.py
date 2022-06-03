from tokenize import Triple


def is_correct_tree(tree, dominators, v, cur_set):
    cur_set.add(v)

    #print("Ayo? ", dominators[v], cur_set)

    assert dominators[v] == cur_set
    for x in tree[v]:
        is_correct_tree(tree, dominators, x, cur_set)

    cur_set.remove(v)


found = False

def does_dominate(avoid, target, cur, vis, adj):
    #If you find a blocking node, return 
    if cur == avoid:
        return
    # Don't want to find target node, but did anyways
    if cur == target:
        global found
        found = True
        return 
    if cur in vis:
        return 
    vis.add(cur)
    
    for node in adj[cur]:
        does_dominate(avoid, target, node, vis, adj)

def does_dominance_hold(dominators, adj):
    for node in range(0, len(dominators)):
        assert node in dominators[node] #handle reflexive seperately

    for dominator in range(0, len(dominators)):
        for dominatee in range(0, len(dominators)):
            if dominatee == dominator:
                continue
            # IFF between b in dominators[a] and b dominates a
            exists = dominator in dominators[dominatee]
            global found
            found = False
            does_dominate(dominator,dominatee,0, set(), adj)
            #print("Dominator",dominator,"Dominatee",dominatee)
            #print("Found? ", found)
            #print("Exists in set? ", exists)
            assert exists is not found
            