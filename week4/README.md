# Constant Propogation
This was what was discussed in the lecture - Find out which values exist for sure at which times in the basic blocks. I used my week 2 CFG implementation (indexing each block by their actual index in the array made it much easier to think about; because I do a lot of competitive programming, this was just the most natural way to think about the problem for me) and the worklist algorihtm came pretty smoothly.

I tested this by testing that the constant propogation always worked even when there's a jump (in the lvn test section), and then made a simple for loop that added up from 1 to 100. I was kind of surprised my code didn't break here, since everything was constants, but I guess that's why the workflow algorithm works. I also ran it on a couple of my own tests and the lvn benchmarks to see if the constants folded, and they did. I ran it on the benchmarks, and the variable names that were obviously named constants stayed constant, while the more natural variable names had '?' around them, so I'm inclined to believe that my worklist implementation is correct.

Some troubles I had were not realizing that the arguments, if not previously defined, should not be redefined. That messes the invariant, I believe, although I'm still not sure why exactly since as long as you're adding and not subtracting you're always going up, right? Idk, it makes sense if you think it through but not something you'll catch immidiately.

## Lattice Theory

I'm not entirely sure how the lattice theory thing works. My first impressions were thinking of the Bellman Ford algorithm, because of the similar notion of just iterating to convergence randomly, and Dijkstra's, because it also requires a monotonic cost function (and therefore no negative weights). And also because they were graph algorithms.

I'm going to try and write a proof of the constant propogation here, and then try to generalize it later.

```
\sqrt{n}

```

# Worklist Generalization

The idea is to allow the user to pass generic function pointers into the worklist algorithm and make it still function properly. Of course, I still want to make it compatible with my version of a CFG, so I tried best as I can to abstract away the functions so that anyone, given the specifications of the algorithm only, could make it work without knowing how the CFG and worklist algorithm actually was implemented.

# DOCUMENTATION

- func: The function body; get this by calling 'for func in prog['functions']' and each func is the function body
- args_func: the input arguments for the function have to be initialized to something; this will determine it
- ex: constant propogation has default '?'; interval checking may have [-inf, +inf], etc
- merge(in_set, apply): This determines how you should merge two things. The left arg is the base element; you apply the right function.
- transfer(block, in_set[b]): Given an instruction block and an inset, return the corresponding outset after applying instructions from block
- direction: Whether forward or backwards processing in CFG

