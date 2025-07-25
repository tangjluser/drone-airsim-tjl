import airsim


client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True, vehicle_name="Drone1")
client.armDisarm(True, vehicle_name="Drone1")

client.enableApiControl(True, vehicle_name="Drone2")
client.armDisarm(True, vehicle_name="Drone2")
# client.takeoffAsync(vehicle_name="Drone1").join()
# client.moveToZAsync(-3, 1, vehicle_name="Drone1").join()

# client.hoverAsync(vehicle_name="Drone2").join()
# state = client.getMultirotorState(vehicle_name="Drone2")
# position = state.kinematics_estimated.position
# print(f"位置 (x, y, z): ({position.x_val:.2f}, {position.y_val:.2f}, {position.z_val:.2f})")

# client.moveToPositionAsync(2, 0, -2, 1,lookahead=0.5,adaptive_lookahead=0, vehicle_name="Drone1").join()
# client.landAsync(vehicle_name="Drone1").join()

# client.hoverAsync(vehicle_name="Drone1").join()
# state = client.getMultirotorState(vehicle_name="Drone1")
# position = state.kinematics_estimated.position
# print(f"位置 (x, y, z): ({position.x_val:.2f}, {position.y_val:.2f}, {position.z_val:.2f})")

# data = client.getDistanceSensorData(distance_sensor_name="Distance", vehicle_name="Drone1")
# if data.is_valid:
#     print(f"Distance: {data.distance} m")

data = client.getLidarData(lidar_name="Lidar", vehicle_name="Drone1")
points = data.point_cloud
for i in range(0, len(points), 3):
    x, y, z = points[i], points[i+1], points[i+2]
    print(f"Point: x={x}, y={y}, z={z}")
