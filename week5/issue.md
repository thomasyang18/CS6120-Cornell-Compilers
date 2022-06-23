I'm having trouble understanding what happens for this program:
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
  print one;
  jmp .b1;
.b3:
}
```
Following the pseudocode in the video by assuming defs[v] was just anything in which v was assigned, my program didn't add a phi node to b1, because b1 is in the domination frontier of b2, but b2 has no definitions of i.

So I thought it through a bit more, and hypothesized that I should check all blocks that had an i variable that wasn't undefined, but that led to me having the variable n having a useless phi node, because my program would think that *any* variable going into b1 needed a phi node which isn't true. 

I ran the official ssa program on my bril code, and it returned this:

```
@main {
.b0:
  i.0: int = const 0;
  n.0: int = const 10;
  one.0: int = const 1;
  jmp .b1;
.b1:
  i.1: int = phi i.0 i.2 .b0 .b2;
  cond.0: bool = phi __undefined cond.1 .b0 .b2;
  i.2: int = add i.1 one.0;
  cond.1: bool = ge i.2 n.0;
  br cond.1 .b3 .b2;
.b2:
  print one.0;
  jmp .b1;
.b3:
  ret;
}
```

The extra cond phi node was weird but at least the program worked fine and actually added a correct phi node for i.1. One thing I'm noticing is how it only created phi nodes for the .b1 block variables, which sure one is useless, but at least it correctly SSA's the program. So I'm hypothesizing that a correct solution would to add phi nodes to any block that is a dominance frontier of something, but that's needlessly wasteful.

I don't want to look at the ssa source code, so could you give me a hint as to resolve this issue? I feel like the solution is to use a dataflow analysis where you check for a fresh variable at the exit of a block, but I have no idea how to rigorously define that. 