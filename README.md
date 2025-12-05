# MazeMadness (Data Structures Final Project)
Maze solving program that implements Stakcs and Queues for a DFS and BFS solver. We will see how stacks and queues change exploration behavior and efficiency.

	Stack: Last-In-First-Out (LIFO) structure for Depth-First-Search (DFS)
	Queue: First-In-First-Out (FIFO) structure for Bredth-first-Search (BFS)

## What Each Maze Solving Method Does

### WHY WE USE STACK FOR DFS:

	In DFS, we explore as far down one path as possible before backtracking.
	It picks a path and follows it until it hits a dead end, 
	then backtracks to the last intersection to try a new path.

Stacks allow us to easily backtrack to the most recent position. Each time we visit a new location, we push it onto the stack. We can then pop from the top to get the most recently discovered position. A stack makes sure we go DEEP before exploring different routes.

### WHY WE USE QUEUE IN BFS:

	In BFS, we explore the maze level-by-level, checking all neighbors.
	First, explores all positions one step away from start,
	then all the positions two steps away, and so on, until it finds the exit

This will guarantee the first time we reach the exit is the shortest path.

When we discover a new location, we add it to the end of the queue. This way, positions that were added earlier (the ones closest to the start) are explored first. this makes us explore positions in the order that we found them, ensuring we find the shortest path.

## How To Use

Program is very straight-forward to run. When you start the program, it will show the available mazes that can be run by the server. In our case, it will show that we have mazes 1, 2, and 3. The program will then ask what maze you would like to run. Just keep in mind that there is very little error handling, so if you make an invalid decision, please restart the program.

Your console output should look something like this:

	[Server] MAZE_SERVER READY
	Available mazes:
	MAZES 1 2 3
	
	Choose a maze to initialize: 2
	
	Initializing maze 1...
	OK INIT maze_id=2 rows=9 cols=15
	
	Initial LOOK:
	###############
	#P     #     E#
	# ### ### ### #
	#   #   #   # #
	### # ### # # #
	#   #     #   #
	# ### ##### ###
	#     #       #
	###############
	Running DFS solver ...
	
	[DFS Solver] Starting DFS escape...
	[DFS Solver] Exit found after exploring 28 nodes.
	Path length: 25
	
	Resetting maze...
	Maze reset.
	
	Running BFS solver ...
	
	[BFS Solver] Starting BFS escape...
	[BFS Solver] Exit found after exploring 46 nodes.
	Path length: 21
	
	Comparison of DFS and BFS paths:
	DFS path length: 25
	BFS path length: 21
	
	Quitting maze server...
	[Server] BYE

## Core Functionality

This program communicates with the server using single-line responses to send commands back and forth. The "LOOK" command however, will return a multi-line response. 

The "LOOK" command is the part of the code in the example console output that displays the maze. The program will look for "MAZE BEGIN" and then read the lines in-between until it sees "MAZE END." These lines recieved will be used to construct the maz in the console output.

The function parse_maze then takes the information from the "LOOK" command to construct the maze as a 2D grid. This function will look for 'P' and assign the row and column index to player_pos. The function also does the same with 'E' and exit_pos.

The get_neighbors function is also really important to this program. This function checks each of the four directions. A neighbor is valid if it's within bounds and it's not a wall.

Once DFS and BFS solve our mazes, we will use the reconstruct_path function. This function reconstructs the path by starting at the exit and following a node's parents all the way back to the start.

## DFS And BFS Algorithms

DFS:

	1. Start at inital position, push it onto stack
	2. While the stack isn't empty:
	- Pop the most recent position
	- If EXIT -> Success and reconstruct path
	- Get all neighbors
	- For each unvisited neighbor:
	-- Mark as visited
	-- Track parent
	-- Push onto stack

BFS:

	1. Start at inital position, enqueue
	2. While the queue isn't empty:
	- Dequeue the oldest position
	- If EXIT -> Success and reconstruct path
	- Get all neighbors
	- For each unvisited neighbor
	-- Mark as visited
	-- Track parent
	-- enqueue

## Challenges

With any program that already has it's building blocks exposed, it takes a little bit to figure out exactly how things are expected to work and how everything plays together. Messing with the move function was also a bit of a pain, so I decided not to use it and went with a slightly different approach.

It was also a bit hard to figure out exactly what the difference between DFS and BFS, but a Geeks for Geeks article helped out a bit.

## What I Learned

	1. Data Structures Matter: Changing from a Stack to a Queue completely changes how the algorithm explores.
	2. DFS is simpler but doesn't guarantee the shortest path.
	3. BFS always finds the shortest path, but is more memory demanding.

