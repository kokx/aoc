# guessed:
# - 191420
# - 194028
# - 192032
# - 190604
# - 191216 - correct
# part 2:
# - 48050

import sys

grid = []

gnomes = {}
elves = {}

iline = 0
for line in sys.stdin:
    line = line.strip()
    grid.append([])
    ic = 0
    for c in line:
        grid[iline].append(c)
        if c == 'E':
            elves[(iline, ic)] = 200
        if c == 'G':
            gnomes[(iline, ic)] = 200
        ic += 1
    iline += 1

def print_grid(grid):
    for line in grid:
        ln = ''
        for c in line:
            ln += c
        print(ln)

def get_neighbors(grid, vertex):
    neighbors = []
    if vertex[0] > 0 and grid[vertex[0]-1][vertex[1]] == '.':
        neighbors.append((vertex[0]-1, vertex[1]))
    if vertex[0] < len(grid) - 1 and grid[vertex[0]+1][vertex[1]] == '.':
        neighbors.append((vertex[0]+1, vertex[1]))
    if vertex[1] > 0 and grid[vertex[0]][vertex[1] - 1] == '.':
        neighbors.append((vertex[0], vertex[1]-1))
    if vertex[1] < len(grid[vertex[0]]) - 1 and grid[vertex[0]][vertex[1]+1] == '.':
        neighbors.append((vertex[0], vertex[1]+1))
    return neighbors

def bfs_paths(grid, start, goals):
    queue = [(start, [start])]
    shortest = 9999999999
    visited = set()
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(get_neighbors(grid, vertex)):
            if next in visited:
                continue
            visited.add(next)
            if next in goals:
                yield path + [next]
                shortest = len(path) + 1
            else:
                if len(path) + 1 <= shortest:
                    queue.append((next, path + [next]))

def find_enemy_neighbors(grid, enemies):
    all = set()
    for loc in enemies.keys():
        all.update(get_neighbors(grid, loc))
    return all

def check_enemies_near(grid, vertex, enemy):
    neighbors = []
    if vertex[0] > 0 and grid[vertex[0]-1][vertex[1]] == enemy:
        neighbors.append((vertex[0]-1, vertex[1]))
    if vertex[0] < len(grid) - 1 and grid[vertex[0]+1][vertex[1]] == enemy:
        neighbors.append((vertex[0]+1, vertex[1]))
    if vertex[1] > 0 and grid[vertex[0]][vertex[1] - 1] == enemy:
        neighbors.append((vertex[0], vertex[1]-1))
    if vertex[1] < len(grid[vertex[0]]) - 1 and grid[vertex[0]][vertex[1]+1] == enemy:
        neighbors.append((vertex[0], vertex[1]+1))
    return neighbors

def find_best_paths(paths):
    shortest = 9999999999
    ret = []
    for path in paths:
        if len(path) < shortest:
            ret = [path]
            shortest = len(path)
        elif len(path) == shortest:
            ret.append(path)
    return ret

def find_next(paths):
    # FIRST: find best destination square in reading order
    dests = [path[len(path) - 1] for path in paths]
    dests.sort()
    dest = dests[0]
    paths = [path for path in paths if path[len(path) - 1] == dest]
    # THEN: from those, find best step in reading order
    # for each path, get path[1], path[0] = current
    dirs = [path[1] for path in paths]
    dirs.sort()
    return dirs[0]

def get_best_enemy(locations, values):
    lowest = 9999999999
    lowestLocs = []
    for loc in locations:
        if values[loc] < lowest:
            lowest = values[loc]
            lowestLocs = [loc]
        elif values[loc] == lowest:
            lowestLocs.append(loc)
    if len(lowestLocs) > 0:
        return sorted(lowestLocs)[0]
    return None

print_grid(grid)
print()

ended = False

# one round, moves only
for number_round in range(0, 5000):
    print(number_round + 1)
    done = set()
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if (i, j) in done:
                continue
            if grid[i][j] == 'G':
                e_neighbors = find_enemy_neighbors(grid, elves)
                # check if there are enemies left
                if len(elves) == 0:
                    print('G', (i, j), 'no targets left')
                    ended = True
                    break
                # move gnome
                cur = (i, j)
                done.add(cur)
                enemies = check_enemies_near(grid, (i, j), 'E')
                if len(enemies) > 0:
                    print('G', (i, j), 'is where he wants to be')
                else:
                    if len(e_neighbors) > 0:
                        print('G TODO move')
                        paths = list(bfs_paths(grid, (i, j), e_neighbors))
                        print('G TODO haspath')
                        best = find_best_paths(paths)
                        if len(best) > 0:
                            print('G TODO hasbest')
                            next = find_next(best)
                            print('G move', (i, j), next)
                            grid[i][j] = '.'
                            grid[next[0]][next[1]] = 'G'
                            done.add(next)
                            gnomes[next] = gnomes[(i, j)]
                            del gnomes[(i, j)]
                            cur = next
                # attack by gnome
                enemies = check_enemies_near(grid, cur, 'E')
                lowest = get_best_enemy(enemies, elves)
                if lowest:
                    print('G attack', cur, lowest, elves[lowest])
                    elves[lowest] -= 3
                    if elves[lowest] <= 0:
                        del elves[lowest]
                        grid[lowest[0]][lowest[1]] = '.'
            elif grid[i][j] == 'E':
                g_neighbors = find_enemy_neighbors(grid, gnomes)
                # check if there are enemies left
                if len(gnomes) == 0:
                    print('E', (i, j), 'no targets left')
                    ended = True
                    break
                # move elf
                cur = (i, j)
                done.add(cur)
                enemies = check_enemies_near(grid, (i, j), 'G')
                if len(enemies) > 0:
                    print('E', (i, j), 'is where he wants to be')
                else:
                    if len(g_neighbors) > 0:
                        print('E TODO move')
                        paths = list(bfs_paths(grid, (i, j), g_neighbors))
                        print('E TODO haspath')
                        best = find_best_paths(paths)
                        if len(best) > 0:
                            print('E TODO hasbest')
                            next = find_next(best)
                            print('E move', (i, j), next)
                            grid[i][j] = '.'
                            grid[next[0]][next[1]] = 'E'
                            done.add(next)
                            elves[next] = elves[(i, j)]
                            del elves[(i, j)]
                            cur = next
                # attack by elf
                enemies = check_enemies_near(grid, cur, 'G')
                lowest = get_best_enemy(enemies, gnomes)
                if lowest:
                    print('E attack', cur, lowest, gnomes[lowest])
                    gnomes[lowest] -= 3
                    if gnomes[lowest] <= 0:
                        del gnomes[lowest]
                        grid[lowest[0]][lowest[1]] = '.'

    print_grid(grid)
    print('G:', gnomes)
    print('E:', elves)
    print()

    if ended and len(elves) == 0:
        print('Gnomes win')
        total = 0
        for k, v in gnomes.items():
            total += v
        print('%d * %d = %d' % (total, number_round, total * number_round))
        break
    if ended and len(gnomes) == 0:
        print('Elves win')
        total = 0
        for k, v in elves.items():
            total += v
        print('%d * %d = %d' % (total, number_round, total * number_round))
        break
