import math
import heapq
from itertools import chain

GRID_WIDTH, GRID_HEIGHT = 50, 50


def astar(start, goal, obstacles, snakes_meta):

    snakes = []
    for _, _, _, coords in snakes_meta:
        snake = fill(coords)
        snakes.append(snake)

    # Flatten both snake and obstacles
    snakes = set(chain(*snakes))
    obstacles = set(chain(*obstacles))

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    came_from_ = {}

    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    current = []
    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path
        neighbors = get_neighbors(current, obstacles, snakes)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + \
                1  # Each step has a cost of 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                came_from_[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)

                if not any(n[1] == neighbor and n[0] == f_score[neighbor] for n in open_set):
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points a and b.

    The Manhattan distance is the sum of the absolute differences of 
    their Cartesian coordinates.

    Parameters:
    a (tuple): A tuple representing the x, y coordinates of the first point.
    b (tuple): A tuple representing the x, y coordinates of the second point.

    Returns:
    int: The Manhattan distance between the two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def fill(coords):

    snake = []
    for i in range(len(coords) - 1):
        x0, y0 = coords[i]
        x1, y1 = coords[i + 1]
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                snake.append((x0, y))
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                snake.append((x, y0))
    return snake


def is_valid(neighbor, obstacles, snakes):
    if 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT and neighbor not in obstacles and neighbor not in snakes:
        return True
    return False


def get_neighbors(pos, obstacles, snakes):
    """
    Get valid neighbors of a given position.

    This function generates a list of neighboring positions around the given position 
    and filters out positions that are not valid according to the is_valid function.

    Parameters:
    pos (tuple): The x, y coordinates of the current position.
    obstacles (set): A set of tuples representing the x, y coordinates of the obstacles.

    Returns:
    list: A list of tuples representing the valid neighboring positions.
    """
    x, y = pos
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [neighbor for neighbor in neighbors if is_valid(
        neighbor, obstacles, snakes)]


def head_on_neighbors(heads, obstacles, snakes):
    neighbor_set = set()
    for head in heads:
        neighbor_set.update(get_neighbors(head, obstacles, snakes))
    return neighbor_set


def too_far(start, goal, heads):

    # Calculate the distance to the goal for all the snakes.
    distances_to_goal = [abs(head[0] - goal[0]) +
                         abs(head[1] - goal[1]) for head in heads]
    my_distance = abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    # If my distance to the goal is greater than the average distance to the goal, then my head is too far from the goal compared to other snakes' heads.
    if my_distance > min(distances_to_goal):
        return True
    else:
        return False


def furthest_point(corners, pos):
    distances = [abs(x - pos[0]) + abs(y - pos[1]) for (x, y) in corners]
    return corners[distances.index(max(distances))]


def reconstruct_path(came_from, current):
    """
    Reconstruct the path from the start node to the current node.

    This function backtracks from the current node to the start node 
    by following the parent pointers stored in the came_from dictionary.

    Parameters:
    came_from (dict): A dictionary that maps each node to its parent node.
    current (tuple): The x, y coordinates of the current node.

    Returns:
    list: A list of tuples representing the x, y coordinates of the nodes in the path.
    """
    path = []
    while current in came_from:
        path.insert(0, current)
        current = came_from[current]
    return path
