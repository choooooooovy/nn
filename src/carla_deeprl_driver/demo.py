import sys
import os
import random
import time
import math
sys.path.insert(0, r'c:\Users\12698\Desktop\carla_deeprl_driver')
os.chdir(r'c:\Users\12698\Desktop\carla_deeprl_driver')

import carla

print("=" * 60)
print("CARLA Demo - Vehicle Status Display")
print("=" * 60)

print("\n[1] Connecting...")
client = carla.Client('localhost', 2000)
client.set_timeout(10)
world = client.get_world()
print(f"    Map: {world.get_map().name}")

print("\n[2] Spawning RED Tesla...")
bp = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

vehicle_bp = bp.filter('vehicle.tesla.model3')[0]
vehicle_bp.set_attribute('color', '255, 0, 0')

spawn_point = random.choice(spawn_points)
vehicle = world.spawn_actor(vehicle_bp, spawn_point)
print("    RED Tesla ready!")

print("\n[3] Driving with Vehicle Status Display")
print("-" * 60)

reward = 0
throttle = 0.0
steer = 0.0
for i in range(50):
    # 动态控制车辆：加速、转弯
    if i < 10:
        throttle = min(0.5, throttle + 0.1)
        steer = 0.0
        gear = 'D'
    elif i < 25:
        throttle = 0.5
        steer = math.sin((i-10) * 0.15) * 0.3
        gear = 'D'
    elif i < 35:
        throttle = 0.0
        steer = 0.0
        gear = 'N'
    else:
        throttle = min(0.4, throttle + 0.08)
        steer = -0.2
        gear = 'R'
    
    vehicle.apply_control(carla.VehicleControl(throttle=throttle, steer=steer, reverse=(gear == 'R')))
    time.sleep(0.1)
    
    velocity = vehicle.get_velocity()
    speed_ms = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
    speed_kmh = speed_ms * 3.6
    
    reward += 1
    
    v_transform = vehicle.get_transform()
    v_loc = v_transform.location
    v_rot = v_transform.rotation
    
    # Update spectator (third person view)
    spectator = world.get_spectator()
    behind_offset = carla.Vector3D(
        x=-math.cos(math.radians(v_rot.yaw)) * 8,
        y=-math.sin(math.radians(v_rot.yaw)) * 8,
        z=5
    )
    camera_loc = carla.Location(
        x=v_loc.x + behind_offset.x,
        y=v_loc.y + behind_offset.y,
        z=v_loc.z + behind_offset.z
    )
    spectator.set_transform(carla.Transform(camera_loc, carla.Rotation(pitch=-20, yaw=v_rot.yaw)))
    
    # Draw DIRECTION ARROW
    arrow_start = carla.Location(
        x=v_loc.x + math.cos(math.radians(v_rot.yaw)) * 5,
        y=v_loc.y + math.sin(math.radians(v_rot.yaw)) * 5,
        z=v_loc.z + 0.5
    )
    arrow_end = carla.Location(
        x=v_loc.x + math.cos(math.radians(v_rot.yaw)) * 10,
        y=v_loc.y + math.sin(math.radians(v_rot.yaw)) * 10,
        z=v_loc.z + 0.5
    )
    world.debug.draw_line(arrow_start, arrow_end, thickness=0.3, color=carla.Color(0, 255, 255), life_time=0.5)
    
    # Draw arrow head
    for side in [-1, 1]:
        head_end = carla.Location(
            x=arrow_end.x - math.cos(math.radians(v_rot.yaw + side * 30)) * 2,
            y=arrow_end.y - math.sin(math.radians(v_rot.yaw + side * 30)) * 2,
            z=arrow_end.z
        )
        world.debug.draw_line(arrow_end, head_end, thickness=0.2, color=carla.Color(0, 255, 255), life_time=0.5)
    
    # Vehicle Status Display (right side of the car)
    status_x = v_loc.x + math.cos(math.radians(v_rot.yaw)) * 8
    status_y = v_loc.y + math.sin(math.radians(v_rot.yaw)) * 8
    
    # Title
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z + 5),
        "VEHICLE STATUS",
        color=carla.Color(255, 255, 255),
        life_time=0.3,
        draw_shadow=True
    )
    
    # Speed (color changes based on speed)
    speed_color = carla.Color(0, 255, 0) if speed_kmh < 30 else (carla.Color(255, 255, 0) if speed_kmh < 60 else carla.Color(255, 0, 0))
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z + 4),
        f"Speed: {speed_kmh:.1f} km/h",
        color=speed_color,
        life_time=0.3,
        draw_shadow=True
    )
    
    # Gear
    gear_color = carla.Color(0, 255, 0) if gear == 'D' else (carla.Color(255, 0, 0) if gear == 'R' else carla.Color(255, 255, 0))
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z + 3),
        f"Gear: [{gear}]",
        color=gear_color,
        life_time=0.3,
        draw_shadow=True
    )
    
    # Throttle bar
    throttle_bar = "█" * int(throttle * 10) + "░" * (10 - int(throttle * 10))
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z + 2),
        f"Throttle: [{throttle_bar}]",
        color=carla.Color(0, 255, 0),
        life_time=0.3,
        draw_shadow=True
    )
    
    # Brake bar
    brake = 1.0 if i >= 25 and i < 30 else 0.0
    brake_bar = "█" * int(brake * 10) + "░" * (10 - int(brake * 10))
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z + 1),
        f"Brake:   [{brake_bar}]",
        color=carla.Color(255, 0, 0),
        life_time=0.3,
        draw_shadow=True
    )
    
    # Steering direction
    steer_dir = "←" if steer < -0.1 else ("→" if steer > 0.1 else "↑")
    world.debug.draw_string(
        carla.Location(x=status_x, y=status_y, z=v_loc.z),
        f"Steer: {steer_dir} ({steer:.2f})",
        color=carla.Color(0, 255, 255),
        life_time=0.3,
        draw_shadow=True
    )
    
    if i % 10 == 0:
        print(f"    Step {i+1}/50: Speed={speed_kmh:.1f} km/h, Gear={gear}, Throttle={throttle:.1f}")

print("\n[DONE] Check the Vehicle Status Display on the right side!")
vehicle.destroy()