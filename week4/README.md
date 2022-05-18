# Constant Propogation
This was what was discussed in the lecture - Find out which values exist for sure at which times in the basic blocks. I used my week 2 CFG implementation (indexing each block by their actual index in the array made it much easier to think about; because I do a lot of competitive programming, this was just the most natural way to think about the problem for me) and the worklist algorihtm came pretty smoothly.

I tested this by testing that the constant propogation always worked even when there's a jump (in the lvn test section), and then made a simple for loop that added up from 1 to 100. I was kind of surprised my code didn't break here, since everything was constants, but I guess that's why the workflow algorithm works. I also ran it on a couple of my own tests and the lvn benchmarks to see if the constants folded, and they did. I ran it on the benchmarks, and the variable names that were obviously named constants stayed constant, while the more natural variable names had '?' around them, so I'm inclined to believe that my worklist implementation is correct.

Some troubles I had were not realizing that the arguments, if not previously defined, should not be redefined. That messes the invariant, I believe, although I'm still not sure why exactly since as long as you're adding and not subtracting you're always going up, right? Idk, it makes sense if you think it through but not something you'll catch immidiately.

## Lattice Theory

I'm not entirely sure how the lattice theory thing works. My first impressions were thinking of the Bellman Ford algorithm, because of the similar notion of just iterating to convergence somehow working, and Dijkstra's, because it also requires a monotonic cost function (and therefore no negative weights). And also because they were graph algorithms.

The lattice that my data formed was like, a partial ordering of subset ordering, but then also, if there were conflict in definitions it would just default to '?', so the highest in the ordering would be the set of all definitions all defined to '?' if it were possible.

I read up on some of the papers but didn't really understand them tbh. The general argument kind of makes sense - if you can only go up in the lattice every time you merge or transfer, then of course you're going to hit some convergence if that lattice is finite, but it's not entirely clear to me why it terminates in O(n^2) or that that it even produces a correct answer.

# Live Variables

This one you had to go backwards and sort of do the variable matching thing you would do for DCE. I didn't really understand what "Live Variables" meant, but it makes sense now - any variable that, going out of the block, will influence other blocks, are live variables. So you "kill" them off by going backwards and seeing if they are re-declared earlier; if they are declared before they are used in that block, then you know in that instance it doesn't matter what value that variable has going into that block. Although I feel like it's kind of hard to make sense of this optimization; sure, you know which variables are dead, but maybe within that block it was used for important calculations.

It was interesting for this one to implement the printing out; in the end, I decided that I would put up a flag indicating which direction the graph went, and then if the graph was reversed, flipping the inset and outset again, so they reflected the "normal" graph, so that you just had to process it bottom up even though the in was really the out. Makes more sense to em that way.

# Interval Analysis

This one forced me to generalize my approach since it was no longer sufficient to just keep the variable names; i needed their types as well. But I didn't want to make my implementation too convoluted, so here was my approach: Each variable is still mapped to only their variable name, but for the ID function, I also passed in the full instruction, so the user has full control over the data. Thus, when the ID gets initialized to whatever data structure you want (tuple of ([interval], type) in my case), then you can operate that in the transfer function, and thus you can also operate on that in the merge function, so I only have to consider one function instead of three.

Also, I realized my constant propogation wasn't entirely correct - for example, anything times zero is zero, anything OR with true is true, so my constant propogation didn't actually catch those edge cases (this is important because, '?' * 0 = 0, for example). Time to fix that.

Also, I just didn't implement interval analysis for booleans - normal intervals are already a nightmare to consider since they wrap around with modulos, so I don't want to consider the edge cases for all of the boolean condtions. So booleans are just treated as constant props '?' in my implementation of Interval Analysis.

To simplify things a bit, if any number overflowed, I would just say it's '?'. I don't want to think about supporting multiple ranges and stuff. I'm pretty sure real compilers can handle overflow, but whatever. 

Adding and subtracting ranges were straightforward - be very generous and assume that you add small to small and big to big (or in the case of subtraction, subtract out the left of the first with the right of the second for the largest left possible difference, and same with the right)

Multiplication I'm also fairly sure works - try all 4 combinations of multiplication between the endpoints of the ranges, and then take the min and max across all of them. This is to handle the sign flipping case - in the case the signs do flip, this guarantees that you get the most bang for your buck, since that implies zero is included in the range, so you're always going to extrema anyways. If the signs dont flip in that interval, then you're straight up taking the max of the numbers which is also fine.

Division is the one I'm not sure about. First, you need to make sure that the denominator doesn't include zero.

# Worklist Generalization

The idea is to allow the user to pass generic function pointers into the worklist algorithm and make it still function properly. Of course, I still want to make it compatible with my version of a CFG, so I tried best as I can to abstract away the functions so that anyone, given the specifications of the algorithm only, could make it work without knowing how the CFG and worklist algorithm actually was implemented.

# DOCUMENTATION

- func: The function body; get this by calling 'for func in prog['functions']' and each func is the function body
- id: the input arguments for the function have to be initialized to something; this will determine it
- ex: constant propogation has default '?'; interval checking may have [-inf, +inf], etc
- merge(in_set, apply): This determines how you should merge two things. The left arg is the base element; you apply the right function.
- transfer(block, in_set[b]): Given an instruction block and an inset, return the corresponding outset after applying instructions from block
- direction: Whether forward or backwards processing in CFG

