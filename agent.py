from Astar import *

# Read game initialization data
num_snakes, game_width, game_height, mode = map(int, input().split())
corners = [(0, 0), (49, 0), (0, 49), (49, 49)]
# Main game loop
old_len = 0
old_goal = 0
while True:
    # Read game state data
    game_state = [input() for _ in range(5+num_snakes)]

    # Check for game over
    if game_state[0] == "Game Over":
        break

   # Extract game state data
    apple_x, apple_y = map(int, game_state[0].split())
    obstacle_descriptions = game_state[1:4]
    my_snake_number = int(game_state[4])

    # Parse obstacles
    obstacles = []
    for obstacle_description in obstacle_descriptions:
        obstacles.append([(int(x), int(y)) for x, y in (coord.split(',')
                         for coord in obstacle_description.strip().split())])

    # Parse snake descriptions
    snake_descriptions = game_state[5:]
    snakes = []
    for snake_description in snake_descriptions:
        parts = snake_description.split()
        status, length, kills, *coords = parts
        if status == "alive":
            coords = [(int(x), int(y))
                      for x, y in (coord.split(',') for coord in coords)]
            snakes.append((status, length, kills, coords))

    goal = (apple_x, apple_y)
    start = snakes[my_snake_number][3][0]  # The head of my snake
    neck = snakes[my_snake_number][3][1]  # The neck of my snake
    tail = snakes[my_snake_number][3][-1]  # The tail of my snake
    heads = [snake[3][0] for snake in snakes if not snake[3]
             [0] == start]  # The heads of other snakes
    my_length = int(snakes[my_snake_number][1])
    old_goal = goal
# ---------------------------------------------------------------------------------
    # Find the shortest path to the apple
    possible_moves = head_on_neighbors(heads, obstacles, snakes)
    obstacles.append(list(possible_moves))
    path = astar(start, goal, obstacles, snakes)

    if not path:
        neighbors = get_neighbors(start, obstacles, snakes)
        print(f"log Moving one step at a time! > {neighbors}")
        path = astar(start, neighbors[0], obstacles, snakes)

# ---------------------------------------------------------------------------------
    # Find the furthest point if the goal is too far
    if too_far(start, goal, heads):
        # # print(f"log Goal : Too Far!")
        # if goal == old_goal:
        #     new_goal = old_goal
        # else:
        new_goal = furthest_point(corners, start)
        old_goal = new_goal

        path = astar(start, new_goal, obstacles, snakes)

    # if old_len > int(my_length):
    #     print(f"log ABOVE ", sep='---')
    # print(f"log **********{old_len} > {length} *********")

    # old_len = int(my_length)

    # print(f"log ( {my_snake_number} )")
    # print(f"log {obstacles=}")
    # print(f"log \n\n\n")
    # print(f"log {snakes=}")
    # print(f"log \n\n\n")
    # print(f"log {path=}")
    # print(f"log \n\n\n")
    # print(f"log {start=}")
    # print(f"log {goal=}")
    # print(f"log \n\n\n")
    # print(f"log {possible_moves = }")

    # Update history variables
# ---------------------------------------------------------------------------------

    if path:
        next_move = path[0]
        dx = next_move[0] - start[0]
        dy = next_move[1] - start[1]
        if dx == 1:
            move = 3  # Right/East
        elif dx == -1:
            move = 2  # Left/West
        elif dy == 1:
            move = 1  # Up/North
        elif dy == -1:
            move = 0  # Down/South
    else:
        # If there's no path, just move random for now
        # print(f"log (+DEBUG : no path")
        move = 5

    # Make the move
    print(move)
