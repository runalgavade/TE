import heapq

# Goal State
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Possible moves (Up, Down, Left, Right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Heuristic Function: Count misplaced tiles
def h_misplaced_tiles(state):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

# Find blank tile position
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Check valid move
def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Convert list to tuple (for hashing)
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# A* Algorithm
def a_star(start_state):
    start = state_to_tuple(start_state)
    g = 0
    h = h_misplaced_tiles(start_state)
    f = g + h

    # Priority Queue (f, g, state, path)
    pq = [(f, g, start_state, [])]
    visited = set()

    while pq:
        f, g, current, path = heapq.heappop(pq)
        current_tuple = state_to_tuple(current)

        if current_tuple in visited:
            continue

        visited.add(current_tuple)

        # Goal Test
        if current == goal_state:
            return path + [current]

        x, y = find_blank(current)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                # Generate new state
                new_state = [row[:] for row in current]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                if state_to_tuple(new_state) not in visited:
                    new_g = g + 1
                    new_h = h_misplaced_tiles(new_state)
                    new_f = new_g + new_h

                    heapq.heappush(pq, (new_f, new_g, new_state, path + [current]))

    return None

# Print solution path
def print_path(path):
    for step, state in enumerate(path):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print()

# Input initial state
def get_input_state():
    print("Enter the initial state (0 = blank):")
    state = []
    for i in range(3):
        row = list(map(int, input(f"Enter row {i+1}: ").split()))
        state.append(row)
    return state

# Main Execution
initial_state = get_input_state()
solution = a_star(initial_state)

if solution:
    print("\nSolution Found:\n")
    print_path(solution)
else:
    print("No solution exists.")

input("Press Enter to exit...")