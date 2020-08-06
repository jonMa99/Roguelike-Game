from constant import *

def diagonal_distance(start, end):
    """
    Finds the diagonl distance between start and end

    Args:
        start ((int, int)): Start of line to calculate diagonal distance
        end ((int, int)): End of line to calculate diagonal distance

    Returns:
        distance (int): Diagonal distance between start and end
    """
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    return distance


def round_point(position):
    """
    Rounds float to int

    Args:
        position ((int, int)): Position to round to int

    Returns:
        p ((int, int)): Rounded position
    """
    p = round(position[0]), round(position[1])
    return p


def lerp_point(start, end, t):
    """
    Returns position between start and end,
    depending on t

    Args:
        start ((int, int)): Start point of line
        end ((int, int)): End point of line
        t (int): Number that decides what position to choose

    Returns:
        position ((int, int)): Position between start and end,
        depending on t
    """
    x1, y1 = start
    x2, y2 = end
    c1 = lerp(x1, x2, t)
    c2 = lerp(y1, y2, t)
    position = c1, c2
    return position


def lerp(num1, num2, t):
    """
    Gives number between num1 and num2,
    depending on t
    
    Args:
        num1 (int): First number to choose number between
        num2 (int): Second number to choose number between
        t (int): Number that decides what number to choose

    Returns:
        num (int): Number between num1 and num2, depending on t
    """
    num = num1 + t * (num2 - num1)
    return num


def line(start, end, map):
    """
    Draws line from start to end, stopping at any wall,
    returning the tiles the line passes through

    Args:
        start ((int, int)): Start position of line
        end ((int, int)): End position of line
        map (2D array): Array of map

    Returns:
        points (List): List of points line passed through
    """
    points = []
    num_of_tiles = diagonal_distance(start, end)
    for i in range(num_of_tiles + 1):
        if num_of_tiles == 0:
            t = 0
        else:
            t = i / num_of_tiles
        x, y = round_point(lerp_point(start, end, t))
        if map[y][x] == WALL:
            break
        points.append((x, y))
    return points


def cast_fireball (game, caster, damage, lines):
    # get list of tiles from start to end
    enemies = caster.creature.enemy_group
    creature_hit = False
    for (x, y) in lines:
        if creature_hit:
            break
        # damage first enemy in list of tile
        for obj in game.CREATURES:
            if enemies.has(obj):
                if (obj.x, obj.y) == (x, y):
                    obj.creature.take_damage(damage)
                    creature_hit = True
                    break
