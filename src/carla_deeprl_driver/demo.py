import sys
import os
import random
import time
import math
import cv2
import numpy as np
sys.path.insert(0, r'c:\Users\12698\Desktop\carla_deeprl_driver')
os.chdir(r'c:\Users\12698\Desktop\carla_deeprl_driver')

import carla

print("CARLA Demo - Main + Top View")
print("=" * 40)

print("\n[1] Connecting...")
client = carla.Client('localhost', 2000)
client.set_timeout(10)
world = client.get_world()

print("\n[2] Spawning vehicle...")
bp = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

vehicle_bp = bp.filter('vehicle.tesla.model3')[0]
vehicle_bp.set_attribute('color', '255, 0, 0')

spawn_point = spawn_points[0]
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

print("\n[3] Setting up top view camera...")

# 创建俯视摄像头（安装在车辆上方15米）
camera_bp = bp.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '320')
camera_bp.set_attribute('image_size_y', '240')
camera_bp.set_attribute('fov', '90')

camera_transform = carla.Transform(carla.Location(x=0, y=0, z=15), carla.Rotation(pitch=-90))
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

# 存储最新图像
latest_image = None

def process_image(image):
    global latest_image
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    latest_image = array

camera.listen(process_image)

print("\n[4] Driving...")
print("    - Main view: Third person follow")
print("    - Top view: Small window on right")

spectator = world.get_spectator()

# 创建OpenCV窗口显示俯视视角
cv2.namedWindow('Top View', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Top View', 320, 240)
cv2.moveWindow('Top View', 1600, 100)  # 移动到右侧

try:
    for i in range(100):
        # 控制车辆
        if i < 30:
            vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))
            gear = 'D'
        elif i < 60:
            steer_angle = math.sin((i-30) * 0.08) * 0.4
            vehicle.apply_control(carla.VehicleControl(throttle=0.4, steer=steer_angle))
            gear = 'D'
        else:
            vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
            gear = 'N'
        
        # 更新主相机（第三人称跟随）
        v_transform = vehicle.get_transform()
        v_loc = v_transform.location
        v_yaw = v_transform.rotation.yaw
        
        yaw_rad = math.radians(v_yaw)
        camera_x = v_loc.x - math.cos(yaw_rad) * 8
        camera_y = v_loc.y - math.sin(yaw_rad) * 8
        camera_z = v_loc.z + 5
        
        spectator.set_transform(carla.Transform(
            carla.Location(x=camera_x, y=camera_y, z=camera_z),
            carla.Rotation(pitch=-20, yaw=v_yaw)
        ))
        
        # 更新显示
        velocity = vehicle.get_velocity()
        speed_kmh = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2) * 3.6
        
        world.debug.draw_string(
            carla.Location(x=v_loc.x, y=v_loc.y, z=v_loc.z + 3),
            f"{int(speed_kmh)} km/h",
            color=carla.Color(0, 255, 0),
            life_time=0.3
        )
        
        gear_color = carla.Color(0, 255, 0) if gear == 'D' else carla.Color(255, 255, 0)
        world.debug.draw_string(
            carla.Location(x=v_loc.x, y=v_loc.y, z=v_loc.z + 2),
            gear,
            color=gear_color,
            life_time=0.3
        )
        
        # 显示俯视视角
        if latest_image is not None:
            cv2.imshow('Top View', latest_image)
            cv2.waitKey(1)
        
        time.sleep(0.05)
        if i % 25 == 0:
            print(f"Step {i+1}")

finally:
    print("\n[5] Cleaning up...")
    camera.stop()
    camera.destroy()
    vehicle.destroy()
    cv2.destroyAllWindows()

print("\n[DONE]")
