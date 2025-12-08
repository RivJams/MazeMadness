"""
MazeMadness DFS & BFS Solver
Data Structures Final Project Code
River Wallerstedt 12/8/2025

This code provides a framework for solving mazes using
Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms.
This code also includes a client to communicate with a Maze Server
"""

import subprocess
from typing import List, Tuple, Optional, Dict

Position = Tuple[int, int]  # (row, col)

# ============================================================================
# Data Structures: Stack and Queue (YOU COMPLETE CODE) (Class Definitions)
# ============================================================================
# These data structures will be useful for implementing DFS and BFS.
# Stack: Last-In-First-Out (LIFO) structure for DFS.
# Queue: First-In-First-Out (FIFO) structure for BFS.
# These will control how we explore the maze.

class Stack:

    # Why we use stack for DFS:
    # In DFS, we explore as far down a path as possible before backtracking.
    # A stack allows us to easily backtrack to the most recent position.
    # Each time we visit a new position, we push it onto the stack.

    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Pop an item off the stack and return it."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()
    
    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self.items)
    
class Queue:

    # Why we use queue for BFS:
    # In BFS, we explore all neighbors at the present depth prior to moving on to nodes at the next depth level.

    def __init__(self):
        """Initialize an empty queue."""
        self.items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
                raise IndexError("dequeue from empty queue")
        return self.items.pop(0)
    
    def front(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self.items[0]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self.items)

# ============================================================================
# Maze Server Client (Don't edit this code)
# ============================================================================

class MazeServerClient:
    """
    Handles communication with the Maze Server.
    You should copy the maze_server.ext file to the same
    project folder as your main python script for this to work.

    All commands are transmitted as text, and responses are read as text.
    """
    #REMOVE COMMENT TO TEST ON YOUR MACHINE
    #SERVER_CMD = ["./maze_server.exe"]
    
    #THIS IS NOT OPTIMAL, BUT WAS THE ONLY WAY I COULD GET IT TO WORK
    import os
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    SERVER_CMD = [os.path.join(_script_dir, "maze_server.exe")]

    def __init__(self):
        #Start the server as a subprocess
        self.proc = subprocess.Popen(
            self.SERVER_CMD,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        #Read initial "MAZE_SERVER READY" line
        ready_line = self._read_line()
        print(f"[Server] {ready_line}")

    def _write_line(self, line: str) -> None:
        """Send a single command line to the server."""
        assert self.proc.stdin is not None
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def _read_line(self) -> str:
        """Read a single line from the server."""
        assert self.proc.stdout is not None
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("Server closed the connection unexpectedly.")
        return line.rstrip("\n")

    # ------------- Simple commands: single-line responses -------------------
    """
    I have kept my functions just to give you a template - don't have to use this
    """

    def send_simple(self, cmd: str) -> str:
        """Send a command expected to return a single-line response."""
        self._write_line(cmd)
        response = self._read_line()
        return response

    def list_mazes(self) -> str:
        #Will use send_simple
        return self.send_simple("LIST")

    def init_maze(self, maze_id: str) -> str:
        #Will use send_simple to initialize maze 1,2 or 3
        return self.send_simple(f"INIT {maze_id}")
    
    def reset(self) -> str:
        #Uses send_simple with RESET cmd
        return self.send_simple("RESET")

    def quit(self) -> None:
        #QUIT cmd - use try except finally to terminate appropriately
        try:
            self._write_line("QUIT")
            response = self._read_line()
            print(f"[Server] {response}")
        except:
            pass
        finally:
            self.proc.terminate()
            self.proc.wait()

    # ------------- LOOK command: multi-line response ------------------------

    def look(self) -> List[str]:
        """
        Sends LOOK and returns the maze as a list of strings (rows),
        with 'P' indicating the current player position.
        """
        self._write_line("LOOK")
        
        #Read until we see "MAZE BEGIN"
        line = self._read_line()
        while "MAZE BEGIN" not in line:
            line = self._read_line()

        #Now read maze lines until "MAZE END"
        maze_lines = []
        while True:
            line = self._read_line()
            if "MAZE END" in line:
                break
            maze_lines.append(line)

        return maze_lines


# ============================================================================
# Maze Parsing & Helpers (YOU CAN USE / EXTEND)
# ============================================================================

def parse_maze(maze_lines: List[str]) -> Tuple[List[List[str]], Position, Optional[Position]]:
    """
    Convert the list of strings into:
        grid: 2D list of chars
        player_pos: (row, col) where 'P' is
        exit_pos: (row, col) where 'E' is (if visible), else None
    """
    grid = []
    player_pos = None
    exit_pos = None

    # Go through each row
    for row_idx, line in enumerate(maze_lines):
        # Converts the string line into a list of characters
        row = list(line)
        grid.append(row)

        # Search the row for 'P' and 'E'
        for col_idx, cell in enumerate(row):
            if cell == 'P':
                player_pos = (row_idx, col_idx) # Finds player
            elif cell == 'E':
                exit_pos = (row_idx, col_idx) # Finds exit

    return grid, player_pos, exit_pos

def print_maze(maze_lines: List[str]) -> None:
    """Pretty-print the maze to the console."""
    for line in maze_lines:
        print(line)

def get_neighbors(grid: List[List[str]], pos: Position) -> List[Position]:
    """
    Returns passable neighbors (up/down/left/right) of pos.
    Passable cells are anything that is not a wall '#'.
    """
    row, col = pos
    neighbors = []

    # Check each of the four directions
    # A neighbor is valid if it's within bounds and not a wall
    # North
    if row > 0 and grid[row - 1][col] != '#':
        neighbors.append((row - 1, col))
    # South
    if row < len(grid) - 1 and grid[row + 1][col] != '#':
        neighbors.append((row + 1, col))
    # East
    if col < len(grid[0]) - 1 and grid[row][col + 1] != '#':
        neighbors.append((row, col + 1))
    # West
    if col > 0 and grid[row][col - 1] != '#':
        neighbors.append((row, col - 1))

    return neighbors

def reconstruct_path(parent: Dict[Position, Position],
                     start: Position,
                     goal: Position) -> List[Position]:
    """
    Reconstruct path from start to goal using parent dict:
        parent[child] = parent_of_child

    Reconstructs the path by starting at the exit and following
    parent links back to the start.
    """
    path = []
    current = goal

    # work backwards and follow parent links back to start
    while current != start:
        path.append(current)
        current = parent[current] # move to parent

    # finally add the start position
    path.append(start)

    # reverse the path to get it from start to goal
    path.reverse()
    return path

# ============================================================================
# DFS & BFS Solvers (YOU IMPLEMENT)
# ============================================================================

# DFS Solver
def dfs_escape(client: MazeServerClient) -> Optional[List[Position]]:
    """
    Solve the maze using Depth-First Search with a stack.
    Returns the path to the exit as a list of positions, or None if no path found.
    
    DFS explores the maze by going as deep as possible down one path before backtracking.
    It picks a path and follows it until it hits a dead end,
    then backtracks to the last intersection to try a new path.
    """
    print("\n[DFS Solver] Starting DFS escape...")

    # Calls look to see the maze from the server
    maze_lines = client.look()
    # Convert maze lines to grid and find start/exit positions
    grid, start_pos, exit_pos = parse_maze(maze_lines)
    
    # Initialize stack and visited set
    # Push the start position onto the stack
    stack = Stack()
    stack.push(start_pos)
    visited = set()
    visited.add(start_pos)
    
    parent = {} # Dictionary to track parent of each position for path reconstruction

    nodes_explored = 0

    while not stack.is_empty():
        # Pop the most recently added position from the stack
        current_pos = stack.pop()
        nodes_explored += 1

        # Check if we found the exit and end the search
        if current_pos == exit_pos:
            print(f"[DFS Solver] Exit found after exploring {nodes_explored} nodes.")
            # Reconstruct the path from start to exit
            path = reconstruct_path(parent, start_pos, current_pos)
            print("Path length:", len(path))
            return path
        
        # Explore neighbors
        neighbors = get_neighbors(grid, current_pos)

        # For each neighbor, if not visited, mark visited, so we don't go back. Set parent, and push to stack
        for neighbor in neighbors:
            if neighbor not in visited:
                # Mark neighbor as visited
                visited.add(neighbor)
                # Set the parent of the new neighbor to current position
                parent[neighbor] = current_pos
                stack.push(neighbor)

    print("[DFS Solver] No path to exit found.")
    return None

# BFS Solver
def bfs_escape(client: MazeServerClient) -> Optional[List[Position]]:
    """
    Solve the maze using Breadth-First Search with a queue.
    Returns the path to the exit as a list of positions, or None if no path found.
    
    BFS explores the maze level-by-level, checking all neighbors at the current depth.
    First, it explores all positions one step away from the start,
    then all positions two steps away, and so on, until it finds the exit.
    This guarantees the first time we reach the exit, we have found the shortest path.

    When we discover a new position, we add it to the end of the queue.
    This way, positions that were added earlier (closer to the start) are explored first.
    This makes us explore positions in the order we found them, ensuring we find the shortest path.
    """
    print("\n[BFS Solver] Starting BFS escape...")

    # Calls look to see the maze from the server
    maze_lines = client.look()
    # Convert maze lines to grid and find start/exit positions
    grid, start_pos, exit_pos = parse_maze(maze_lines)
    
    # Initialize queue and visited set
    queue = Queue()
    queue.enqueue(start_pos)
    visited = set()
    visited.add(start_pos)
    
    parent = {} # Dictionary to track parent of each position for path reconstruction

    nodes_explored = 0

    while not queue.is_empty():
        # Dequeue the oldest added position from the queue to make sure we exoplore level by level
        current_pos = queue.dequeue()
        nodes_explored += 1

        # Check if we found the exit        
        if current_pos == exit_pos:
            print(f"[BFS Solver] Exit found after exploring {nodes_explored} nodes.")
            # Reconstruct the path from start to exit
            path = reconstruct_path(parent, start_pos, current_pos)
            print("Path length:", len(path))
            return path
        
        # Explore all neighbors of the current position
        neighbors = get_neighbors(grid, current_pos)

        # Look at each neighbor, if not visited, mark visited, set parent, and enqueue
        for neighbor in neighbors:
            if neighbor not in visited:
                # Mark neighbor as visited
                visited.add(neighbor)
                # Set the parent of the new neighbor to current position
                parent[neighbor] = current_pos
                queue.enqueue(neighbor)

    print("[BFS Solver] No path to exit found.")
    return None

# ============================================================================
# Simple Demo (Use to get you started and test server connection)
# ============================================================================

def main():
    client = MazeServerClient()
    maze_selected = 0

    try:
        #1. List mazes
        print("Available mazes:")
        mazes = client.list_mazes()
        print(mazes)
        maze_selected = input("\nChoose a maze to initialize: ")

        #2. Initialize a maze (change "1" to another ID if you want)
        print("\nInitializing maze 1...")
        init_response = client.init_maze(maze_selected)
        print(init_response)

        #3. Look at the maze
        print("\nInitial LOOK:")
        maze_lines = client.look()
        print_maze(maze_lines)

        #At this point, you should implement and test dfs_escape / bfs_escape.

        print("Running DFS solver ...")
        dfs_path = dfs_escape(client)

        #Reset before BFS so position is back at start
        print("\nResetting maze...")
        client.reset()
        print("Maze reset.")

        print("\nRunning BFS solver ...")
        bfs_path = bfs_escape(client)

        #Compare path lengths if both bfs / dfs exist
        print("\nComparison of DFS and BFS paths:")
        if dfs_path and bfs_path:
            print(f"DFS path length: {len(dfs_path)}")
            print(f"BFS path length: {len(bfs_path)}")

    finally:
        #Make sure to shut down the server
        print("\nQuitting maze server...")
        client.quit()


if __name__ == "__main__":
    main()

