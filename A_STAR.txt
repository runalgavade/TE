# Import heapq module for implementing priority queue (min-heap)
import heapq

# Define the goal state of the 8-puzzle problem
# 0 represents the blank space
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Define possible movement directions for the blank tile
# (-1,0) = Up
# (1,0)  = Down
# (0,-1)= Left
# (0,1) = Right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Heuristic function to count misplaced tiles
# This estimates how far the current state is from goal state
def h_misplaced_tiles(state):

    # Initialize misplaced tile counter
    misplaced = 0

    # Traverse through rows
    for i in range(3):

        # Traverse through columns
        for j in range(3):

            # Check:
            # 1. Tile is not blank
            # 2. Tile is not in correct position
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:

                # Increment misplaced tile count
                misplaced += 1

    # Return total misplaced tiles
    return misplaced

# Function to find blank tile position
def find_blank(state):

    # Traverse rows
    for i in range(3):

        # Traverse columns
        for j in range(3):

            # If blank tile found
            if state[i][j] == 0:

                # Return row and column index
                return i, j

# Function to check whether move is inside puzzle boundary
def is_valid(x, y):

    # Return True if coordinates are valid
    return 0 <= x < 3 and 0 <= y < 3

# Function to convert list into tuple
# Tuples are hashable and can be stored in sets
def state_to_tuple(state):

    # Convert each row into tuple
    return tuple(tuple(row) for row in state)

# Main A* Algorithm function
def a_star(start_state):

    # Convert initial state into tuple format
    start = state_to_tuple(start_state)

    # g(n) = actual cost from start node
    # Initially cost is 0
    g = 0

    # Calculate heuristic value h(n)
    h = h_misplaced_tiles(start_state)

    # Calculate total cost:
    # f(n) = g(n) + h(n)
    f = g + h

    # Create priority queue
    # Stores tuple:
    # (f, g, current_state, path)
    pq = [(f, g, start_state, [])]

    # Create visited set to avoid revisiting states
    visited = set()

    # Continue while priority queue is not empty
    while pq:

        # Remove state with minimum f(n) value
        f, g, current, path = heapq.heappop(pq)

        # Convert current state into tuple
        current_tuple = state_to_tuple(current)

        # If already visited, skip it
        if current_tuple in visited:
            continue

        # Mark current state as visited
        visited.add(current_tuple)

        # Goal Test:
        # If current state equals goal state
        if current == goal_state:

            # Return complete solution path
            return path + [current]

        # Find blank tile position
        x, y = find_blank(current)

        # Try all possible movement directions
        for dx, dy in directions:

            # Calculate new coordinates
            nx, ny = x + dx, y + dy

            # Check if move is valid
            if is_valid(nx, ny):

                # Create deep copy of current state
                # Prevents modifying original state
                new_state = [row[:] for row in current]

                # Swap blank tile with adjacent tile
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                # If new state is not already visited
                if state_to_tuple(new_state) not in visited:

                    # Increment actual path cost
                    new_g = g + 1

                    # Calculate heuristic value for new state
                    new_h = h_misplaced_tiles(new_state)

                    # Calculate total estimated cost
                    new_f = new_g + new_h

                    # Insert new state into priority queue
                    heapq.heappush(
                        pq,
                        (new_f, new_g, new_state, path + [current])
                    )

    # If no solution exists
    return None

# Function to print solution path step-by-step
def print_path(path):

    # Enumerate gives step number and state
    for step, state in enumerate(path):

        # Print step number
        print(f"Step {step}:")

        # Print each row of puzzle
        for row in state:
            print(row)

        # Print blank line for readability
        print()

# Function to take input from user
def get_input_state():

    # Display instructions
    print("Enter the initial state (0 = blank):")

    # Empty list to store puzzle
    state = []

    # Loop for 3 rows
    for i in range(3):

        # Take row input from user
        # split() separates numbers
        # map(int, ...) converts strings to integers
        # list() converts result into list
        row = list(map(int, input(f"Enter row {i+1}: ").split()))

        # Add row into puzzle state
        state.append(row)

    # Return complete puzzle
    return state

# ---------------- MAIN EXECUTION ----------------

# Take initial puzzle input from user
initial_state = get_input_state()

# Call A* algorithm to solve puzzle
solution = a_star(initial_state)

# If solution exists
if solution:

    # Print success message
    print("\nSolution Found:\n")

    # Print all solution steps
    print_path(solution)

# If no solution exists
else:

    # Print failure message
    print("No solution exists.")

# Prevent terminal from closing immediately
input("Press Enter to exit...")
