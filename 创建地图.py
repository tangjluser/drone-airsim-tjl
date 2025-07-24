# 初始化 170x170 矩阵
matrix = [[0 for _ in range(170)] for _ in range(170)]

# 给定的坐标点
points = [
    (20,20), (60,20), (100,20), (140,20),
    (20,60), (20,100), (20,140),
    (60,60), (60,100), (60,140),
    (100,60), (100,100), (100,140),
    (140,60), (140,100), (140,140)
]

# 对每个点，设置中心以及周围 7 格范围内的点为1
for x, y in points:
    for dx in range(-9, 10):
        for dy in range(-9, 10):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 170 and 0 <= ny < 170:
                matrix[ny][nx] = 1  # 注意行是y，列是x

# 保存到 map.txt
with open("map.txt", "w") as f:
    for row in matrix:
        f.write(' '.join(map(str, row)) + "\n")
