import airsim
import time
import os

# ========== 通用参数 ==========
ALTITUDE = -3.0    # 基础飞行高度（负数表示上升）
SPEED = 1          # 飞行速度 m/s
RATIO = 0.1        # 坐标缩放比
NUM_DRONES = 8     # 无人机数量

# 每架无人机出生点偏移（相对坐标转为世界坐标）
# init_v_x = [0 * RATIO + i * 10 * RATIO for i in range(NUM_DRONES)]
# init_v_y = [0 * RATIO for _ in range(NUM_DRONES)]
init_v_x = [0.0,10.0,8.0,12.0,16.0,16.0,4.0,12.0]
init_v_y = [0.0,0.0,8.0,6.0,16.0,10.0,2.0,10.0]
# init_v_z = [-3.0,-4.0,-3.0,-4.0,-3.0,-4.0,-3.0,-4.0]  #会碰撞
init_v_z = [-3.0,-4.0,-5.0,-6.0,-2.0,-7.0,-8.0,-9.0]    #不会碰撞


# ========== 读取路径 ==========
def read_path(file_path):
    path = []
    with open(file_path, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split(','))
            path.append((x, y))
    return path


# ========== 初始化起飞 ==========
def initialize_and_takeoff(client, vehicle_names, altitude, speed):
    tasks = []
    for name in vehicle_names:
        client.enableApiControl(True, vehicle_name=name)
        client.armDisarm(True, vehicle_name=name)
        tasks.append(client.takeoffAsync(vehicle_name=name))
    for task in tasks:
        task.join()

    tasks.clear()
    for i, name in enumerate(vehicle_names):
        # z = altitude - i * 0.5  # 避免垂直冲突
        z = init_v_z[i]
        tasks.append(client.moveToZAsync(z, speed, vehicle_name=name))
    for task in tasks:
        task.join()


# ========== 路径飞行 ==========
def fly_trajectories(client, vehicle_paths, altitude_base, speed, ratio, init_x, init_y):
    max_len = max(len(p) for p in vehicle_paths.values())
    # trajectory_record = {v: [] for v in vehicle_paths.keys()}

    for i in range(max_len):
        tasks = []
        for idx, (vehicle_name, path) in enumerate(vehicle_paths.items()):
            if i < len(path):
                px, py = path[i][0] * ratio, path[i][1] * ratio
                z = altitude_base[idx]
                # 发出移动命令
                task = client.moveToPositionAsync(
                    px - init_x[idx], py - init_y[idx], z, speed, vehicle_name=vehicle_name)
                tasks.append(task)

                # # 记录轨迹
                # trajectory_record[vehicle_name].append(airsim.Vector3r(px, py, z))
                #
                # # 画轨迹
                # client.simPlotLineStrip(
                #     trajectory_record[vehicle_name],
                #     color_rgba=[1.0 - idx * 0.1, 0.5, 0.2 + idx * 0.1, 1.0],
                #     thickness=10.0,
                #     duration=120.0,
                #     is_persistent=True
                # )

        # 在所有任务发出后统一等待
        for task in tasks:
            task.join()


# ========== 悬停并降落 ==========
def hover_and_land(client, vehicle_names):
    tasks = [client.hoverAsync(vehicle_name=v) for v in vehicle_names]
    for t in tasks:
        t.join()
    tasks = [client.landAsync(vehicle_name=v) for v in vehicle_names]
    for t in tasks:
        t.join()
    for v in vehicle_names:
        client.armDisarm(False, vehicle_name=v)
        client.enableApiControl(False, vehicle_name=v)


# ========== 主函数 ==========
if __name__ == "__main__":
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # 生成无人机名列表
    vehicle_names = [f"Drone{i+1}" for i in range(NUM_DRONES)]

    # 加载所有路径
    vehicle_paths = {}
    for i, name in enumerate(vehicle_names):
        filename = f"simplified_path/simplified_path_output{i+1}.txt"
        if os.path.exists(filename):
            vehicle_paths[name] = read_path(filename)
        else:
            print(f"⚠️ 路径文件缺失：{filename}，将跳过该无人机。")

    # 初始化并起飞
    initialize_and_takeoff(client, list(vehicle_paths.keys()), ALTITUDE, SPEED)

    # 执行路径
    fly_trajectories(client, vehicle_paths, init_v_z, SPEED, RATIO, init_v_x, init_v_y)

    # 悬停并降落
    hover_and_land(client, list(vehicle_paths.keys()))

    print("✅ 所有无人机飞行任务完成！")