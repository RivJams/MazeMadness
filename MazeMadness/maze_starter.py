"""
Escape Maze Simulator - Final Starter Code

This file will provide example code for:
- Connection to the maze_server.exe file (found on canvas)
- How to start the server and work on your code
- Provides an outline for you to use or not use (your choice)
- Run this code to test your connection and get started coding the required material
- There are 3 maze patterns stored in the server right now
"""

import subprocess
from typing import List, Tuple, Optional, Dict

Position = Tuple[int, int]  # (row, col)

# ============================================================================
# Data Structures: Stack and Queue (YOU COMPLETE CODE) (Class Definitions)
# ============================================================================

class Stack:
    
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Peek from empty stack")

    def is_empty(self):
        return len(self.stack) == 0
    
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Dequeue from empty queue")

    def front(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            raise IndexError("Front from empty queue")

    def is_empty(self):
        return len(self.queue) == 0

# ============================================================================
# Maze Server Client (Don't edit this code)
# ============================================================================

class MazeServerClient:
    """
    Handles communication with the Maze Server.
    You should copy the maze_server.exe file to the same
    project folder as your main python script for this to work.
    """
    SERVER_CMD = ["./maze_server.exe"]

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
        #Write command
        pass

    def list_mazes(self) -> str:
        #Will use send_simple
        pass

    def init_maze(self, maze_id: str) -> str:
        #Will use send_simple to initialize maze 1,2 or 3
        pass

    def move(self, direction: str) -> str:
        """
        direction in {"N", "S", "E", "W"}
        Returns one of:
            "BLOCKED WALL"
            "OK MOVE row=... col=..."
            "EXIT FOUND row=... col=... steps=..."
        """
        #Also use send_simple to command a direction
        pass

    def status(self) -> str:
        #Uses send_simple with STATUS cmd
        pass

    def reset(self) -> str:
        #Uses send_simple with RESET cmd
        pass

    def help(self) -> str:
        #HELP returns multiple lines; we read until no more lines for a moment
        pass

    def quit(self) -> None:
        #QUIT cmd - use try except finally to terminate appropriately
        pass

    # ------------- LOOK command: multi-line response ------------------------

    def look(self) -> List[str]:
        """
        Sends LOOK and returns the maze as a list of strings (rows),
        with 'P' indicating the current player position.
        """
        pass


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
    pass


def print_maze(maze_lines: List[str]) -> None:
    """Pretty-print the maze to the console."""
    pass

def get_neighbors(grid: List[List[str]], pos: Position) -> List[Position]:
    """
    Returns passable neighbors (up/down/left/right) of pos.
    Passable cells are anything that is not a wall '#'.
    """
    pass

def reconstruct_path(parent: Dict[Position, Position],
                     start: Position,
                     goal: Position) -> List[Position]:
    """
    Reconstruct path from start to goal using parent dict:
        parent[child] = parent_of_child
    """
    pass

def follow_path_with_moves(client: MazeServerClient, path: List[Position]) -> None:
    """
    Given a path of positions [p0, p1, ..., pk], send MOVE commands
    to the server to actually walk that path.
    Assumes the server's current position is p0 at the start.
    """
    pass
# ============================================================================
# DFS & BFS Solvers (YOU IMPLEMENT)
# ============================================================================


# ============================================================================
# Simple Demo (Use to get you started and test server connection)
# ============================================================================

def main():
    client = MazeServerClient()

    try:
        #1. List mazes
        print("Available mazes:")
 
        #2. Initialize a maze (change "1" to another ID if you want)
        print("\nInitializing maze 1...")

        #3. Look at the maze
        print("\nInitial LOOK:")

        #At this point, you should implement and test dfs_escape / bfs_escape.

        print("Running DFS solver ...")
        #add your own 

        #Reset before BFS so position is back at start
        print("\nResetting maze...")

        print("\nRunning BFS solver ...")

        #Compare path lengths if both bfs / dfs exist

    finally:
        #Make sure to shut down the server
        client.quit()


if __name__ == "__main__":
    main()
