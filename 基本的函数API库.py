# def airsiminit():
# #初始化无人机
#     client = airsim.MultirotorClient()
#     client.confirmConnection()
#     client.enableApiControl(True)
#     client.armDisarm(True)
#     client.takeoffAsync().join() #起飞

# def show_position():
# #显示无人机当前的位置信息
#     client.hoverAsync().join()
#     state = client.getMultirotorState()
#     position = state.kinematics_estimated.position
#     print(f"位置 (x, y, z): ({position.x_val:.2f}, {position.y_val:.2f}, {position.z_val:.2f})")
# def airsim_hover():
#  #无人机悬停用的
# client.hoverAsync().join()
# def end_airsim():
#  #无人机降落
#  client.landAsync().join()
#  client.armDisarm(False)
#  client.enableApiControl(False)