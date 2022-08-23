# Issues that came up

The main issue that came up (aside from my realization that I should really stop making like 300 line functions) is that I thought natural loops were equivalent to SCC's, but nested loops show otherwise. So I had to modify my natural loops to, instead of just running the standard SCC algorithm, to do something like this:

- Try every node as 

This algorithm's runtime is fine because data flow and dominance are bounded by O(n^2) anyways.