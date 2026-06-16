  [English](README.md) | [中文](README.zh-CN.md)

  # isaaclab-drl-mpc-dynamic

  Comparing and combining **Deep Reinforcement Learning (DRL)** and **classical control (MPC / WBC)**
  for quadruped locomotion on rough terrain, built on [Isaac
  Lab](https://github.com/isaac-sim/IsaacLab).

  > 🚧 **Status**: In active development. Long-term research project, delivered in stages.

  ## Motivation

  Most locomotion projects pick a side: either learning-based (PPO/SAC end-to-end) or model-based (MPC
  + WBC). Each has known strengths and weaknesses:

  - **DRL** handles complex terrain and contact-rich dynamics, but is sample-inefficient and hard to
  interpret.
  - **MPC / WBC** provides physical guarantees and is data-efficient, but struggles with unmodeled
  dynamics.

  This project builds **both pipelines on the same robot (Anymal) and same terrain**, then explores
  **principled ways to combine them** — using one to compensate for the other's weakness.

  ## Stages

  | Stage | Scope | Status |
  |---|---|---|
  | **stage_1_pure_rl** | Anymal locomotion on rough terrain, trained with PPO and SAC | 🚧 In progress
   |
  | **stage_2_classical** | MPC + Whole-Body Controller using Pinocchio, no learning | 📋 Planned |
  | **stage_3_hybrid** | Hybrid approaches (e.g. MPC as RL warm start, RL learns residual dynamics for
  MPC) | 📋 Planned |
  | **shared/** | Dynamics wrappers, evaluation tools, visualization utilities | 📋 Planned |

  See [`docs/roadmap.md`](docs/roadmap.md) for the full plan.

  ## Stack

  - **Simulator**: Isaac Lab (Isaac Sim 4.x)
  - **Robot**: Anymal-C
  - **DRL**: PPO, SAC (`rsl_rl`, then custom PyTorch implementation)
  - **Classical control**: Pinocchio for rigid-body dynamics, QP-based MPC + WBC
  - **Hardware**: Ubuntu 22.04, RTX-class GPU

  ## License

  TBD (will be set when repository becomes public).

