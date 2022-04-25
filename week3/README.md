# What I did

I ran the standard bril2json into brili pipe for a bunch of tests, and then tested passing them through optimize.py first. 

Ideally, they should produce the same outputs; cherry on top is less instructions than normal.

# DCE Algorithm

Go backwards. 

First, if this function has any "side effects", don't remove it (If you call a function from it or print, for example)

Next, if this function had no side effects, we can consider removing it if:

The destination is marked as unusued.

If the instruction wasn't removed, mark the destination as used and continue.



# LVN Algorithm




# DCE Tests

## noprintnorcall

Output should be empty if there are no print or call statements (so don't optimize anything away that MIGHT do something).

## printandcall

Output should have instructions that contribute to printing and calling, even if they are useless.

## chaining

A chain of useless instructions that keep reassigning the same variable, followed by 1 print message. Only the last two statements should remain.

## chainingmult

A chain of only useful instructions (well, useful disregarding const prop)
