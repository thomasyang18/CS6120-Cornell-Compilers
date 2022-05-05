# What I did

I ran the standard bril2json into brili pipe for a bunch of tests, and then tested passing them through optimize.py first. 

Ideally, they should produce the same outputs; cherry on top is less instructions than normal.

# DCE Algorithm

Go backwards. 

First, if this function has any "side effects", don't remove it (If you call a function from it or print)

Next, if this function had no side effects, we can consider removing it if:

The destination is marked as unusued.

If the instruction wasn't removed, mark the destination as used and continue.

# DCE Tests

## noprintnorcall

Output should be empty if there are no print or call statements (so don't optimize anything away that MIGHT do something).

## printandcall

Output should have instructions that contribute to printing and calling, even if they are useless.

## chaining

A chain of useless instructions that keep reassigning the same variable, followed by 1 print message. Only the last two statements should remain.

## chainingmult

A chain of only useful instructions (well, useful disregarding const prop)

## jumping

Jump and break statements mixed in to make sure those are getting optimized properly. For example, only remove one instruction if you compute a boolean twice and then jump somewhere.

#DCE Results

ALl passed, with them optimizing away dead code where needed.

# LVN Algorithm

O(n^2): 

First, make a bunch of passes through the algorithm, such that the first "layer" of a variable becomes "var0", the second layer becomes "var1", etc. Basically, rename to SSA form. A layer is defined as how many previous assignments to that variable came before it.

Data Structure is an array of tuples. Whenever you encounter something of the form (dest) := (op) (args), you first try to match args to a previous variable (if not possible, because for example the variable exists outside of this basic block, then somehow have a dummy variable for "x=x" or something idk)

Then, once args are matched, check if any existing value matches the dest. If so, then replace. If not, then put it in the table.

Finally, to convert it back to normal, replace all instances of "var0" with just var and "varN" with just var, where N is the highest value you went to replacing for that variable.

# LVN Tests

I did constant folding, commutative, copy prop, and common subexpression elimination tests.

I also did a jump during common subexpression elimination to see how my algorithm deals with undeclared variables (since operating on basic blocks, we're bound to have those).

#LVN Results
