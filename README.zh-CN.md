[English](README.md) | [中文](README.zh-CN.md)

# isaaclab-drl-mpc-dynamic

在 [Isaac Lab](https://github.com/isaac-sim/IsaacLab)
上对比并融合**深度强化学习（DRL）**与**经典控制（MPC / WBC）**，研究四足机器人在粗糙地形上的
locomotion。

> **状态**：Stage 1（纯 RL）✅ 已交付——PPO 基线训练完成并归档。下一步是 Stage 2（经典控制）。
> 长期研究项目，分 stage 交付。

## 动机

主流 locomotion 项目通常只选一边：要么端到端学习（PPO/SAC），要么基于模型（MPC +
WBC）。两者各有已知的长短板：

- **DRL** 能处理复杂地形和富接触动力学，但样本效率低、可解释性差。
- **MPC / WBC** 提供物理保证、数据效率高，但难以应对未建模动力学。

本项目在**同一机器人（Anymal-D）、同一地形**上分别构建两套
pipeline，然后探索**有原则的融合方式**——让一方弥补另一方的短板。

## Stage 划分

| Stage | 内容 | 状态 |
|---|---|---|
| **[stage_1_pure_rl](stage_1_pure_rl/README.md)** | Anymal-D 粗地形 locomotion，PPO（`rsl_rl`） | ✅ **已交付**——[结果与 demo](stage_1_pure_rl/README.md) |
| **stage_2_classical** | 基于 Pinocchio 的 MPC + 全身控制器（WBC），不含学习 | 📋 计划中（下一个） |
| **stage_3_hybrid** | 融合方案（如 MPC 作 RL 的 warm start、RL 学习 MPC 的残差动力学） | 📋 计划中 |
| **shared/** | 动力学封装、评估工具、可视化 | 📋 计划中 |

完整路线图见 [`docs/roadmap.md`](docs/roadmap.md)。

## Stage 1 成果速览

![Anymal-D 粗地形 demo](stage_1_pure_rl/docs/stage1_demo.gif)

4096 个并行环境 × 1500 次迭代（约 1.47 亿环境步，单张 RTX 5070 Ti 上 58 分钟）：
平均回报 **17.56**，**92.5%** 的 episode 以超时正常结束（而非摔倒），速度跟踪奖励达到 ≈1.0
上限的 **0.83**，地形课程收敛在 **5.9 / 9** 档。完整指标、训练曲线与复现命令见
[stage_1_pure_rl/README.md](stage_1_pure_rl/README.md)。

## 技术栈

- **仿真器**：Isaac Lab（Isaac Sim 4.x）
- **机器人**：Anymal-D
- **DRL**：PPO（`rsl_rl`，stage 1 已交付）；SAC 与自研 PyTorch PPO 作为可选延伸
- **经典控制**：Pinocchio 做刚体动力学，QP 求解 MPC + WBC
- **硬件环境**：Ubuntu 22.04，RTX 级 GPU（stage 1 在 RTX 5070 Ti 16 GB 上训练）

## 许可证

TBD（仓库变 public 时确定）。

## 致谢

本项目的部分文档与工具脚本在 AI 辅助下完成。
