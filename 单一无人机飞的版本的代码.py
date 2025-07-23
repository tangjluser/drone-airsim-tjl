
# path_file = "planned_path_output.txt"  #这里用来保存最短路算法规划好的路径
# # 飞行参数
# ALTITUDE = -3.0      # 固定飞行高度（负值为上升）
# SPEED = 1.0          # 速度 m/s
# PAUSE_TIME = 0.1     # 每步之间的延迟（可选）
# # 上升到指定高度
# client.moveToZAsync(ALTITUDE, SPEED).join()

# trajectory_points = []   #用来绘制无人机飞过的路径
# # 依次飞行经过路径点
# for idx, (x, y) in enumerate(path):
#     print(f"Moving to point {idx+1}/{len(path)}: ({x}, {y})")
#     client.moveToPositionAsync(x, y, ALTITUDE, SPEED,
#                                lookahead=1, adaptive_lookahead=0).join()
#     # time.sleep(PAUSE_TIME)  # 可选暂停以避免震荡
#     trajectory_points.append(airsim.Vector3r(x, y, ALTITUDE))
#     client.simPlotLineStrip(trajectory_points,
#                             color_rgba=[0.0, 1.0, 0.0, 1.0],  # 绿色线条
#                             thickness=10.0,
#                             duration=120.0,  # 显示时间（秒）
#                             is_persistent=True)
# client.hoverAsync().join()
# client.landAsync().join()