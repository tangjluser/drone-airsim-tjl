import airsim
import time

#这里是我用来测试规划好路径的
# ========== 通用参数 ==========
ALTITUDE = -3.0  # 固定飞行高度（负数表示升高）
SPEED = 1.0      # 飞行速度 m/s
init_v_x=[0,10]  #多个无人机初始的点位，用于后期修正用的，因为每个无人机都会以自己的出生点为原点坐标而采用了相对坐标，而非世界坐标
init_v_y=[0,0]

# ========== 读取路径函数 ==========
def read_path(file_path):
    path = []
    with open(file_path, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split(','))
            path.append((x, y))
    return path

# ========== 主函数 ==========
if __name__ == "__main__":
    # 连接客户端
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # ======================
    # 初始化 Drone1
    # ======================
    client.enableApiControl(True, vehicle_name="Drone1")
    client.armDisarm(True, vehicle_name="Drone1")
    client.takeoffAsync(vehicle_name="Drone1").join()
    client.moveToZAsync(ALTITUDE, SPEED, vehicle_name="Drone1").join()

    # ======================
    # 初始化 Drone2
    # ======================
    client.enableApiControl(True, vehicle_name="Drone2")
    client.armDisarm(True, vehicle_name="Drone2")
    client.takeoffAsync(vehicle_name="Drone2").join()
    client.moveToZAsync(ALTITUDE-1, SPEED, vehicle_name="Drone2").join()

    # ======================
    # 加载路径点
    # ======================
    path1 = read_path("planned_path_output1.txt")
    path2 = read_path("planned_path_output2.txt")

    trajectory1 = []
    trajectory2 = []

    # ======================
    # 飞行逻辑：按最长路径同步执行
    # ======================
    max_len = max(len(path1), len(path2))

    for i in range(max_len):
        tasks = []

        # --- Drone1 ---
        if i < len(path1):
            x1, y1 = path1[i]
            tasks.append(client.moveToPositionAsync(x1-init_v_x[0], y1-init_v_y[0], ALTITUDE, SPEED, vehicle_name="Drone1"))
            trajectory1.append(airsim.Vector3r(x1, y1, ALTITUDE))
            client.simPlotLineStrip(trajectory1,
                                    color_rgba=[0.0, 1.0, 0.0, 1.0],  # 绿色轨迹
                                    thickness=10.0,
                                    duration=120.0,
                                    is_persistent=True)

        # --- Drone2 ---
        if i < len(path2):
            x2, y2 = path2[i]
            tasks.append(client.moveToPositionAsync(x2-init_v_x[1], y2-init_v_y[1], ALTITUDE-1, SPEED, vehicle_name="Drone2"))
            trajectory2.append(airsim.Vector3r(x2, y2, ALTITUDE))
            client.simPlotLineStrip(trajectory2,
                                    color_rgba=[1.0, 0.0, 0.0, 1.0],  # 红色轨迹
                                    thickness=10.0,
                                    duration=120.0,
                                    is_persistent=True)

        for task in tasks:
            task.join()

    # ======================
    # 悬停 + 降落
    # ======================
    client.hoverAsync(vehicle_name="Drone1").join()
    client.hoverAsync(vehicle_name="Drone2").join()

    client.landAsync(vehicle_name="Drone1").join()
    client.landAsync(vehicle_name="Drone2").join()

    client.armDisarm(False, vehicle_name="Drone1")
    client.armDisarm(False, vehicle_name="Drone2")
    client.enableApiControl(False, vehicle_name="Drone1")
    client.enableApiControl(False, vehicle_name="Drone2")

    print("✅ 双无人机飞行任务完成！")


