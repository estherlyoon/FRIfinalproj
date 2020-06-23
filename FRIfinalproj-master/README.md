# FRIfinalproj

An extension of an existing research project called Scavenger Hunt, which studied the efficiency of different search algorithms in an abstract simulator. The scavenger hunt problem aims to have an embodied agent to collect specified objects as fast as possible, with only the knowledge of the probabilities with which the objects might appear at certain locations. 

We aimed to improve the previous groups' Exhaustive Bayesian Search algorithm, which performs a serach down all possible paths from the agent's current location, choosing the best path calculated with a weighted cost formula. Our algorithm, the Timed Bayesian Search, aims to limit the runtime of the Exhaustive by completing a breadth-first, stepwise search through the location space. The search is capped by a preset time limit that halts the search when reached.
