# MazeMadness (Data Structures Final Project)
Maze solving program that implements Stakcs and Queues for a DFS and BFS solver

	Stack: Last-In-First-Out (LIFO) structure for Depth-First-Search (DFS)
	Queue: First-In-First-Out (FIFO) structure for Bredth-first-Search (BFS)

## What Each Maze Solving Method Does

WHY WE USE STACK FOR DFS:

	In DFS, we explore as far down a path as possible before backtracking.
	It picks a path and follows it until it hits a dead end, 
	then backtracks to the last intersection to try a new path.

Stacks allow us to easily backtrack to the most recent position. Each time we visit a new location, we push it onto the stack

WHY WE USE QUEUE IN BFS:

	In BFS, we explore the maze level-by-level, checking all neighbors.
	First, explores all positions one step away from start,
	then all the positions two steps away, and so on, until it finds the exit

This will guarantee the first time we reach the exit is the shortest path.

When we discover a new location, we add it to the end of the queue. This way, positions that were added earlier (the ones closest to the start) are explored first. this makes us explore positions in the order that we found them, ensuring we find the shortest path.
