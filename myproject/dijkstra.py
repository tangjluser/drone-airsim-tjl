import numpy as np
import time
import heapq

def load_map(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return np.array([[int(ch) for ch in line.strip()] for line in lines])
def dijkstra_with_diagonal(grid, start, goal):
    rows, cols = grid.shape
    visited = np.full((rows, cols), False)
    distance = np.full((rows, cols), np.inf)
    prev = np.full((rows, cols, 2), -1, dtype=int)

    distance[start] = 0
    heap = [(0, start)]

    # 8-connected directions
    directions = [(-1,0), (1,0), (0,-1), (0,1),
                  (-1,-1), (-1,1), (1,-1), (1,1)]

    while heap:
        dist, (x, y) = heapq.heappop(heap)
        if visited[x, y]:
            continue
        visited[x, y] = True

        if (x, y) == goal:
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and
                not visited[nx, ny] and grid[nx, ny] == 0):
                cost = np.sqrt(2) if dx != 0 and dy != 0 else 1
                new_dist = dist + cost
                if new_dist < distance[nx, ny]:
                    distance[nx, ny] = new_dist
                    prev[nx, ny] = [x, y]
                    heapq.heappush(heap, (new_dist, (nx, ny)))

    # reconstruct path
    path = []
    cur = goal
    while tuple(cur) != (-1, -1):
        path.append(tuple(cur))
        cur = prev[cur[0], cur[1]]
    path.reverse()

    if path[0] != start:
        return []  # no path found
    return path

def save_path_txt(path, filename="planned_path_output.txt"):
    with open(filename, 'w') as f:
        for pt in path:
            f.write(f"{pt[0]},{pt[1]}\n")
    print(f"📁 路径已保存至 {filename}")



if __name__ == "__main__":
    # 地图路径 & 起终点
    map_file = "map.txt"
    output_file = "planned_path_output2.txt"
    start = (10, 0)
    goal = (17, 16)
    # 加载地图
    grid_map = load_map(map_file)
    # 路径规划
    print("⏳ Planning path...")
    path = dijkstra_with_diagonal(grid_map, start, goal)
    if not path:
        print("❌ 无法找到从起点到终点的可行路径。")
        exit(1)
    print(f"✅ 路径规划完成！共 {len(path)} 个点")
    save_path_txt(path, output_file)

