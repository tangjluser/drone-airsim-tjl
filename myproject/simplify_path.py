def simplify_path(points):
    simplified = []
    if len(points) < 2:
        return points

    def direction(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        # 化简方向向量（用于判断是否共线）
        if dx == 0 and dy == 0:
            return (0, 0)
        elif dx == 0:
            return (0, dy // abs(dy))
        elif dy == 0:
            return (dx // abs(dx), 0)
        else:
            from math import gcd
            g = gcd(dx, dy)
            return (dx // g, dy // g)

    start = points[0]
    prev_dir = direction(points[0], points[1])

    for i in range(2, len(points)):
        curr_dir = direction(points[i - 1], points[i])
        if curr_dir != prev_dir:
            simplified.append(start)
            start = points[i - 1]
            prev_dir = curr_dir

    simplified.append(start)
    simplified.append(points[-1])
    return simplified


def read_path_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                x, y = map(int, line.strip().split(','))
                points.append((x, y))
    return points


def write_path_to_file(points, filename):
    with open(filename, 'w') as file:
        for x, y in points:
            file.write(f"{x},{y}\n")


if __name__ == "__main__":
    input_file = "planned_path/planned_path_output8.txt"
    output_file = "simplified_path/simplified_path_output8.txt"

    original_path = read_path_from_file(input_file)
    simplified_path = simplify_path(original_path)
    write_path_to_file(simplified_path, output_file)

    print(f"原始点数: {len(original_path)}")
    print(f"简化后点数: {len(simplified_path)}")
    print(f"简化结果已保存至: {output_file}")
