# CARLA 深度强化学习自动驾驶系统

欢迎来到 CARLA 深度强化学习自动驾驶项目的文档页面！

## 📋 项目概述

本项目使用 CARLA Simulator 实现了一个基于强化学习的自动驾驶控制系统。

## 🚀 快速开始

### 运行演示
```bash
python demo.py
```

### 运行 A2C 算法
```bash
python main.py
```

### 运行 SAC 算法
```bash
python run_sac.py
```

## 📁 项目结构

```
.
├── source/                      # 核心源代码
│   ├── agent.py                 # ActorCar 类，包含传感器
│   ├── carlaenv.py              # CARLA 环境封装
│   ├── model.py                 # A2C Actor-Critic 模型
│   ├── sac.py                   # SAC 实现
│   ├── trainer.py               # A2C 训练循环
│   ├── sac_trainer.py           # SAC 训练循环
│   ├── replaybuffer.py          # 经验回放缓冲区实现
│   └── utility.py               # 工具函数
├── config.yaml                  # 配置文件
├── main.py                      # A2C 入口点
├── run_sac.py                   # SAC 入口点
├── demo.py                      # 演示脚本
└── README.md                    # 项目文档
```

## 🔧 功能特性

### 多视角显示
- **第三人称跟随镜头** - 相机跟随车辆移动
- **俯视视角小窗口** - OpenCV窗口显示车辆上方视角

### HUD 显示
- 实时速度显示（车辆上方绿色数字）
- 档位显示（D/N）
- 平滑镜头跟随效果

## ⚙️ 配置说明

主要配置参数：

| 参数 | 描述 | 默认值 |
| :-------- | :---------- | :------ |
| `host` | CARLA server 主机地址 | localhost |
| `port` | CARLA server 端口 | 2000 |
| `car_num` | NPC 车辆数量 | 10 |
| `lr` | 学习率 | 0.001 |
| `gamma` | 折扣因子 | 0.99 |

## 📐 支持的 RL 算法

- **A2C (Advantage Actor-Critic)** - 离散动作空间
- **SAC (Soft Actor-Critic)** - 连续动作空间

## 📝 许可证

本项目仅供强化学习课程教学使用。