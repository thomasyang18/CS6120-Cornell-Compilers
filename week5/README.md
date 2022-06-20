# Domination Section

## Side note

The algorithms actually don't work for *really* weird programs. In the benchmarks, for example, recfact.bril has a statement that looks like this:

.then.0:
  v4: int = const 1;
  ret v4;
  jmp .endif.0;

To my knowledge, jmp .endif.0; is just straight up unreachable. But this breaks my code, because when I do a postorder traversal, 2 needs to be from node 0. But it isn't, so well...

I rewrote my CFG to handle this, which was admittedly a bit annoying, but it worked out. I basically just did a DFS traversal on the first iteration of the CFG, removed any dead nodes, and then did a second building CFG iteration.

## Getting dominators of a node

I basically just copied the algorithm from class and it worked. The algorithm I came up with was something like,

"Let dom = node -> identity set, and then for all vertices do dom[v] = Intersection of all predecessors (if they exist, otherwise empty set) union {v}". It turns out this algorithm actually doesn't work; for the loopcond.bril CFG, the zero just never gets passed down, because it needs to think that 4 is dominated by 0, but the only way 4 dominates zero is if 3, 2, and 1 dominate zero, but 1 depends on 4, etc.

I'm VERY surprised that the iterate to converge algorithm discussed in class works under these assumptions as well. My best guess is that instead of trying to build things up (which my algorithm runs into dependency issues for), by killing off predecessor candidates for domination, it's better somehow? I don't rly know tbh.

I also implemented reverse-post order traversal for the CFG.

Similar to the last one where this is qualitative analysis instead of seeing that an optimization kept the program the same + was faster, I ran this graph on the tests provided in dom and some in benchmark and verified that it was correct.

## Dominator Tree

One case I immidiately thought of was a program that looked like:

@main(){
.loop1:
.loop2:
.loop3:
jmp .loop1;
}

When I ran my dominator algorithm on it, everything was marked as a dominator of another, which was not desirable at all. I ended up just always assuming that the entry block was special and had no dominators except itself (so its set was always {0}) This is correct for the first entry block because the entry block should dominate everything, but the entry block doesn't need to visit anyone besides itself. If it's correct for the first entry block, it's correct for the rest (assuming that the algorithm would work without this weird setting to {0} thing) since we basically just "skipped ahead" in the algorithm to a still correct state for 0 but a fully ambiguous state for the others, which is fine for convergence.

This one was much more straightforward to validate was correct - I wrote a validator function on top of my algorithm to construct the dominator tree, which validated that the path from the root to each node was the same as the dominator set at each node.

The algorithm was to process each node in increasing dominator size, and set the depth of them to be the size of the list and the parent to be the node in the set such that it had depth D[v]-1. This exploits the property that since the resulting dominator set is a tree, we can do this greedy algorithm to basically construct the paths ourselves. I ran into some issues on the benchmarks but that was because there was weird code in the benchmarks, as mentioned above - as long as my CFG returned a sensible CFG where every node is reachable from the start node, and my domination algorithm returned a sensible output, my output was a tree just fine. This one I'm much more confident works than either my domlib and CFG.

## Domination Frontier

This one I sort of just analyzed and went with it. I mean, I did no fancy algorithm - just a brute force O(n^3) algorithm to check. If something's wrong with this, it's just a small typo or one of the previous things was wrong (which would most likely be the dominators function, which I tested thoroughly). I guess this will be reflected in the SSA

## To-SSA Algorithm

```

var2phi = map of variable -> set of blocks
# don't worry about edge case where there's phi nodes already

for v in vars:
  i = 0
  while i < len(defs[v]):
    for block in DF[defs[v][i]]: #dominance frontier
      var2phi[var].add(block)
      if block not in defs[v]:
        defs[v].append(block)

```

## Reflection

I didn't realize that "defined" didn't just mean the variable was defined, but more like live variable analysis kinda deal, where variables carried over through paths still applied.

So for this graph:

0->1 
1->2
2->1
1->3

, I got a domination frontier of {}, {}, {1}, {} respectively for 0-3. But a variable that was declared in 0 wouldn't carry over into the dominaition frontier for the phi node.

This is the program that broke my code:

```
@main(){
.b0:
  i: int = const 0;
  n: int = const 10;
  one: int = const 1;
.b1:
  i: int = add i one;
  cond: bool = ge i n;
  br cond .b3 .b2;
.b2:
  print i;
  jmp .b1;
.b3:
}


```