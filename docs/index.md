# [神经网络](https://github.com/OpenHUTB/nn)

欢迎使用神经网络文档，该页面包含所有内容的导航。

* [__核心__](#primary)
* [__感知__](#perception)
* [__规划__](#planning)
* [__控制__](#control)
* [__其他__](#other)

---

## 核心 <span id="primary"></span>

[__热身__](warmup.md) - 核心热身样例

[__线性回归__](linear_regression.md)

[__线性回归改进__](linear_regression_improved.md)

[__线性回归修复__](linear_regression_fix.md) - 修复边界未更新bug       

[__softmax回归__](softmax_regression.md)

[__线性回归和softmax回归改进__](softmax_regression_improved.md)

[__支持向量机__](svm.md)

[__支持向量机改进__](svm_improved.md)

[__简单神经网络__](simple_nn.md)

[__卷积神经网络__](CNN.md)

[__循环神经网络__](RNN.md)

[__注意力机制__](attention.md)

[__高斯混合__](gaussian_mixture.md)

[__受限玻尔兹曼机__](RBM.md)

[__强化学习__](RL.md)

---
## 感知 <span id="perception"></span>

[__车道线检测__](./lane_detection/README.md) - 基于 OpenCV 的 Carla 场景车道线检测(分帧实现)

[__carla_CAM__](./carla_CAM/README.md) - 使用孪生网络验证测试场景神经网络

[__手势控制无人机__](./drone_hand_gesture/README.md) - 使用手势识别控制 Airsim 无人机仿真

[__V2X边缘智能感知__](./edge_intelligence_V2X/README.md) - 基于YOLOv8n的V2X边缘智能感知系统优化与实现

[__目标检测__](./test/object_detection.md) - 目标检测与精度评估       

[__CARLA深度强化学习自动驾驶__](./carla_deeprl_driver/index.md)

## 规划 <span id="planning"></span>

[__Carla YOLO规划器__](carla_yolo_planner.md) - Carla场景结合YOLO的自动驾驶路径规划方案

[__双足人形机器人SAC强化学习步态优化__](./mujoco_running/running.md)

[__人形机器人项目__](./mujoco_hci_sim/README.md) - 基于PPO强化学习的Humanoid人形机器人自主行走仿真

[__td3_carracing__](./td3_carracing/README.md) - 基于 TD3 + CNN 的 CarRacing 强化学习自动驾驶系统

[__机器人仿真系统__](ant_robot/机器人仿真系统.md)

[__自动驾驶语义分割__](./auto_drive_seg/README.md)

## 控制  <span id="control"></span>

[__无人机飞行控制系统__](./UVA_flight_control_system.md) - 基于AirSim的无人机飞行控制系统

[__人形机器人平衡控制__](./humanoid_balance/Humanoid_Balance.md) - 基于强化学习的人形机器人平衡控制实现

[__工程优化__](./improve/project.md) - 多机协同仿真与控制优化项目

## 其他  <span id="other"></span>

[__CARLA IMU 数据采集平台__](./carla_imu/carla_imu.md)

[__setup_tool模块开发报告文档__](./setup_tool/report.md)