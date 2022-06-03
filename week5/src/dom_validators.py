def is_correct_tree(tree, dominators, v, cur_set):
    cur_set.add(v)

    #print("Ayo? ", dominators[v], cur_set)

    assert dominators[v] == cur_set
    for x in tree[v]:
        is_correct_tree(tree, dominators, x, cur_set)

    cur_set.remove(v)


