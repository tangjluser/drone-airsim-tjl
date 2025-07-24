import airsim
import time
import os
import threading

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

# ========== 每架无人机完整任务线程 ==========
def run_vehicle_flight_plan(vehicle_name, path, altitude, speed, ratio, init_x, init_y):
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # 起飞
    client.enableApiControl(True, vehicle_name=vehicle_name)
    client.armDisarm(True, vehicle_name=vehicle_name)
    client.takeoffAsync(vehicle_name=vehicle_name).join()
    client.moveToZAsync(altitude, speed, vehicle_name=vehicle_name).join()

    # 路径飞行
    for point in path:
        px, py = point[0] * ratio, point[1] * ratio
        z = altitude
        client.moveToPositionAsync(
            px - init_x, py - init_y, z, speed, vehicle_name=vehicle_name).join()

    # 悬停 + 降落
    client.hoverAsync(vehicle_name=vehicle_name).join()
    client.landAsync(vehicle_name=vehicle_name).join()
    client.armDisarm(False, vehicle_name=vehicle_name)
    client.enableApiControl(False, vehicle_name=vehicle_name)

# ========== 并发执行所有无人机任务 ==========
def run_all_vehicles_parallel(vehicle_paths, altitude_base, speed, ratio, init_x_list, init_y_list):
    threads = []
    for idx, (vehicle_name, path) in enumerate(vehicle_paths.items()):
        thread = threading.Thread(
            target=run_vehicle_flight_plan,
            args=(
                vehicle_name,
                path,
                altitude_base[idx],
                speed,
                ratio,
                init_x_list[idx],
                init_y_list[idx]
            )
        )
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()



# ========== 主函数 ==========
if __name__ == "__main__":
    # 建立初始连接确认（非必要 client，仅用作连接测试）
    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("✅ 连接成功！开始加载路径...")

    # 生成无人机名列表
    vehicle_names = [f"Drone{i + 1}" for i in range(NUM_DRONES)]

    # 加载所有路径
    vehicle_paths = {}
    for i, name in enumerate(vehicle_names):
        filename = f"simplified_path/simplified_path_output{i + 1}.txt"
        if os.path.exists(filename):
            vehicle_paths[name] = read_path(filename)
        else:
            print(f"⚠️ 路径文件缺失：{filename}，将跳过该无人机。")

    # 执行所有无人机完整任务流程（起飞+飞行+降落）
    run_all_vehicles_parallel(vehicle_paths, init_v_z, SPEED, RATIO, init_v_x, init_v_y)

    print("✅ 所有无人机任务已并行完成！")