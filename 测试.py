import airsim


client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True, vehicle_name="Drone2")
client.armDisarm(True, vehicle_name="Drone2")
client.takeoffAsync(vehicle_name="Drone2").join()
client.moveToZAsync(-3, 1, vehicle_name="Drone2").join()

client.hoverAsync(vehicle_name="Drone2").join()
state = client.getMultirotorState(vehicle_name="Drone2")
position = state.kinematics_estimated.position
print(f"位置 (x, y, z): ({position.x_val:.2f}, {position.y_val:.2f}, {position.z_val:.2f})")

client.moveToPositionAsync(10, 1, -3, 1,lookahead=0.5,adaptive_lookahead=0, vehicle_name="Drone2").join()

client.hoverAsync(vehicle_name="Drone2").join()
state = client.getMultirotorState(vehicle_name="Drone2")
position = state.kinematics_estimated.position
print(f"位置 (x, y, z): ({position.x_val:.2f}, {position.y_val:.2f}, {position.z_val:.2f})")