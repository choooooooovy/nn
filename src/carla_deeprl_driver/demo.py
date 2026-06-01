import sys
import os
import random
import time
import math
sys.path.insert(0, r'c:\Users\12698\Desktop\carla_deeprl_driver')
os.chdir(r'c:\Users\12698\Desktop\carla_deeprl_driver')

import carla

print("=" * 60)
print("CARLA Demo - Speed Dashboard (Visible!)")
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

print("\n[3] Driving with Speed HUD (in front of car!)")
print("-" * 60)

for i in range(30):
    vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))
    time.sleep(0.15)
    
    # Calculate speed
    velocity = vehicle.get_velocity()
    speed_ms = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
    speed_kmh = speed_ms * 3.6
    
    v_transform = vehicle.get_transform()
    v_loc = v_transform.location
    v_rot = v_transform.rotation
    
    # Update spectator (follow mode)
    spectator = world.get_spectator()
    offset = carla.Location(x=-8, y=0, z=5)
    forward_vec = carla.Vector3D(
        x=v_loc.x + offset.x,
        y=v_loc.y + offset.y,
        z=v_loc.z + offset.z
    )
    spectator.set_transform(carla.Transform(forward_vec, carla.Rotation(pitch=-20, yaw=v_rot.yaw, roll=0)))
    
    # Draw Speed HUD in FRONT of the vehicle (so follow camera can see it!)
    forward_dir = carla.Vector3D(
        x=math.cos(math.radians(v_rot.yaw)) * 10,
        y=math.sin(math.radians(v_rot.yaw)) * 10,
        z=0
    )
    hud_location = carla.Location(
        x=v_loc.x + forward_dir.x,
        y=v_loc.y + forward_dir.y,
        z=v_loc.z + 3
    )
    
    world.debug.draw_string(
        hud_location,
        f"===== SPEED: {speed_kmh:.1f} km/h =====",
        color=carla.Color(255, 255, 0),
        life_time=0.5,
        draw_shadow=True
    )
    
    # Also draw a line from car to HUD for visibility
    world.debug.draw_line(
        v_loc + carla.Location(z=2),
        hud_location,
        thickness=0.1,
        color=carla.Color(255, 200, 0),
        life_time=0.3
    )

    if i % 5 == 0:
        print(f"    Step {i+1}/30: Speed = {speed_kmh:.1f} km/h")

print("\n[DONE] Look IN FRONT of the car!")
vehicle.destroy()