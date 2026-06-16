  [English](README.md) | [中文](README.zh-CN.md)

  # isaaclab-drl-mpc-dynamic

  在 [Isaac Lab](https://github.com/isaac-sim/IsaacLab)
  上对比并融合**深度强化学习（DRL）**与**经典控制（MPC / WBC）**，研究四足机器人在粗糙地形上的
  locomotion。

  > 🚧 **状态**：积极开发中。长期研究项目，分 stage 交付。

  ## 动机

  主流 locomotion 项目通常只选一边：要么端到端学习（PPO/SAC），要么基于模型（MPC +
  WBC）。两者各有已知的长短板：

  - **DRL** 能处理复杂地形和富接触动力学，但样本效率低、可解释性差。
  - **MPC / WBC** 提供物理保证、数据效率高，但难以应对未建模动力学。

  本项目在**同一机器人（Anymal）、同一地形**上分别构建两套
  pipeline，然后探索**有原则的融合方式**——让一方弥补另一方的短板。

  ## Stage 划分

  | Stage | 内容 | 状态 |
  |---|---|---|
  | **stage_1_pure_rl** | Anymal 粗地形 locomotion，用 PPO 和 SAC 训练 | 🚧 进行中 |
  | **stage_2_classical** | 基于 Pinocchio 的 MPC + 全身控制器（WBC），不含学习 | 📋 计划中 |
  | **stage_3_hybrid** | 融合方案（如 MPC 作 RL 的 warm start、RL 学习 MPC 的残差动力学） | 📋 计划中 |
  | **shared/** | 动力学封装、评估工具、可视化 | 📋 计划中 |

  完整路线图见 [`docs/roadmap.md`](docs/roadmap.md)。

  ## 技术栈

  - **仿真器**：Isaac Lab（Isaac Sim 4.x）
  - **机器人**：Anymal-C
  - **DRL**：PPO、SAC（先用 `rsl_rl`，后续自己写 PyTorch 实现）
  - **经典控制**：Pinocchio 做刚体动力学，QP 求解 MPC + WBC
  - **硬件环境**：Ubuntu 22.04，RTX 级 GPU

  ## 许可证

  TBD（仓库变 public 时确定）。
