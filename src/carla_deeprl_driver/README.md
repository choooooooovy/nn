# CARLA 深度强化学习自动驾驶系统

本仓库使用 [`CARLA Simulator (version 0.9.13)`](https://carla.org/) 实现了一个基于强化学习的自动驾驶控制系统。该项目旨在训练一个智能代理，能够通过深度强化学习算法在复杂的城市环境中导航。

## 📋 项目概述

本项目的目标是开发一个健壮的自动驾驶智能代理，能够：
- 在 CARLA 的城市环境中导航
- 避免与其他车辆和障碍物碰撞
- 基于视觉输入做出智能驾驶决策
- 通过强化学习学习最优驾驶策略

## 🛠️ 环境设置

### 前置条件
1. **CARLA Simulator 0.9.13** - 从官方或镜像源下载
2. **Python 3.6+** - 确保与 CARLA Python API 兼容
3. **conda** - 推荐用于环境管理

### 安装步骤

#### 步骤 1: 下载 CARLA Simulator
```bash
# 选项 1: 从 SUSTech 镜像下载（中国推荐）
wget https://mirrors.sustech.edu.cn/carla/carla/0.9.13/CARLA_0.9.13.tar.gz
tar -zxvf CARLA_0.9.13.tar.gz

# 选项 2: 从官方网站下载
# https://github.com/carla-simulator/carla/releases/tag/0.9.13
```

#### 步骤 2: 设置 Python 环境
```bash
# 创建 conda 环境
conda env create -f environment.yml
conda activate carla-rl

# 手动安装依赖（如有需要）
pip install -r requirements.txt
```

#### 步骤 3: 启动 CARLA Server
```bash
# 导航到 CARLA 目录
cd CARLA_0.9.13

# 在屏幕外模式下启动 CARLA server（推荐用于训练）
./CarlaUE4.sh -RenderOffScreen

# 或者带可视化启动（用于测试/演示）
# ./CarlaUE4.sh
```

## 🚀 快速开始

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
│   ├── __init__.py
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
├── requirements.txt             # Python 依赖
├── test.py                      # 测试脚本
├── test_env.py                  # 环境测试
└── README.md                    # 项目文档
```

## ⚙️ 配置说明

所有训练参数都可以在 `config.yaml` 中配置：

| 参数 | 描述 | 默认值 |
| :-------- | :---------- | :------ |
| `host` | CARLA server 主机地址 | localhost |
| `port` | CARLA server 端口 | 2000 |
| `car_num` | NPC 车辆数量 | 50 |
| `lr` | 学习率 | 0.001 |
| `gamma` | 折扣因子 | 0.99 |
| `buffer_size` | 经验回放缓冲区大小 | 1000 |
| `hidden_dim` | 隐藏层维度 | 1024 |
| `epoch` | 训练轮数 | 500 |
| `max_episode_length` | 每回合最大步数 | 3000 |

## 📐 设计细节

### CARLA 世界设置
- 使用默认的 CARLA 城镇环境
- 重置时部署和销毁车辆，而不是重新加载整个世界
- 以同步模式获取 RGB 相机帧
- 将帧转换为张量以高效存储在经验回放缓冲区中

### 智能体配置
- 在随机生成点生成智能体（在 NPC 之后）
- 配备 `sensor.camera.rgb` 和 `sensor.other.collision`
- 观察视觉输入（640x480 RGB）和碰撞事件
- 图像预处理：调整大小到 256x256，中心裁剪到 224x224

### 动作空间

**A2C（离散）:**

| 动作索引 | 动作描述 | 车辆控制 |
| :----------: | :----------------: | :-------------: |
|      0       |     直行     | `(1, 0, 0)`     |
|      1       |      左转     | `(1, -1, 0)`    |
|      2       |     右转     | `(1, 1, 0)`     |
|      3       |       刹车        | `(0, 0, 1)`     |

**SAC（连续）:**
- 仅转向控制：`[-1, 1]`
- 固定油门：`1.0`
- 无刹车

### 奖励函数

**A2C 奖励方案:**

| 奖励 | 事件 |
| :----: | :---- |
|  -200  | 检测到碰撞 |
|  -100  | 执行刹车动作 |
|   +5   | 执行直行动作 |
|   +1   | 执行左转/右转动作 |

**SAC 奖励方案:**

| 奖励 | 事件 |
| :----: | :---- |
|  -200  | 检测到碰撞 |
|   +1   | 所有其他动作 |

### 已实现的 RL 算法
- **A2C (Advantage Actor-Critic)** - 离散动作空间，使用 ResNet50 作为骨干网络
- **SAC (Soft Actor-Critic)** - 连续动作空间，带自动熵调整

## ✅ 进度跟踪

### 核心实现
- [x] CARLA 环境封装（兼容 OpenAI Gym）
- [x] RGB 相机和碰撞传感器集成
- [x] 同步模式模拟
- [x] 高效的世界重置机制

### RL 组件
- [x] A2C 算法实现
- [x] SAC 算法实现
- [x] 带轨迹管理的经验回放缓冲区
- [x] TensorBoard 日志记录

### 测试与调试
- [x] 环境测试脚本
- [x] 连接测试
- [x] 经验回放缓冲区测试

### 未来工作
- [ ] 代码重构和优化
- [ ] 性能改进
- [ ] 高级奖励设计
- [ ] 多智能体场景

## 🧠 模型架构

### A2C Actor-Critic
```
输入 (224x224 RGB)
    ↓
ResNet50 (预训练，冻结)
    ↓
全连接层 (3层，1024 隐藏维度)
    ↓
┌─────────────┬─────────────┐
│  Actor Head │ Critic Head │
├─────────────┼─────────────┤
│ Softmax     │ Linear(1)   │
│ (4 actions) │ (V-value)   │
└─────────────┴─────────────┘
```

### SAC 网络
- **Value Network**: ResNet50 + FC 层 → 标量输出
- **Soft Q Network**: ResNet50 + FC 层（带动作输入）→ 标量 Q 值
- **Policy Network**: ResNet50 + FC 层 → 高斯分布参数

## 💡 训练提示

### 硬件考虑
在有限计算资源上运行（例如 1 RTX 3060）：
- 使用在线 A2C（采样一个回合然后更新）
- 接收帧后直接调整大小和裁剪
- 以 Tensor 类型存储数据以节省内存
- 初始测试时使用较小的回合长度

### 监控训练
```bash
# 启动 TensorBoard
tensorboard --logdir=./log/
```

### 模型检查点
当平均回合帧数改善时自动保存检查点：
- A2C: `checkpoints/a2c/model{epoch}.pt`
- SAC: `checkpoints/sac/{network}{epoch}.pt`

## 📝 许可证
本项目仅供强化学习课程教学使用。

## 🤝 致谢
- [CARLA Simulator](https://carla.org/) 提供模拟环境
- OpenAI Gym 提供环境接口标准

---

## 🔧 功能增强

### 第二视角显示
- 添加了俯视视角摄像头，实时显示车辆上方视角
- 使用 OpenCV 弹出独立窗口显示第二视角
- 支持第三人称跟随镜头和俯视视角同时显示

### HUD 显示
- 实时速度显示（车辆上方绿色数字）
- 档位显示（D/N）
- 平滑镜头跟随效果