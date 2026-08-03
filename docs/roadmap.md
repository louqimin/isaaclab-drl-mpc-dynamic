# Roadmap

This project is delivered in three stages on a shared repository. Each stage produces an
independently demoable artifact.

---

## Stage 1 — Pure RL on Anymal (4 weeks)

**Status (2026-08-03): ✅ delivered.** `rsl_rl` PPO baseline trained on Anymal-D rough terrain —
results, curves and demo in [`stage_1_pure_rl/README.md`](../stage_1_pure_rl/README.md).
W2 (from-scratch PPO) and the SAC comparison are deferred as optional follow-ups; the delivered
PPO baseline is what stages 2/3 compare against.

**Goal**: Train a PPO and SAC policy that makes Anymal walk over rough terrain in Isaac Lab. Produce
training curves, evaluation metrics, and a video demo.

| Week | Milestone | Status |
|---|---|---|
| W1 | Run Isaac Lab official examples end-to-end (Cartpole, Ant, Anymal). Familiarize with the task / env / agent abstraction. | ✅ |
| W2 | Implement PPO from scratch in PyTorch (no library). Verify on Pendulum / CartPole. | ⏸ deferred (optional follow-up) |
| W3 | Train Anymal on rough terrain (`rsl_rl` PPO first, then SAC). Tune reward shaping. | ✅ PPO (SAC deferred) |
| W4 | Record demo video, compute evaluation metrics (success rate, energy efficiency, robustness), polish README. | ✅ |

**Deliverables**: trained policy checkpoints ✅, training curves ✅, video ✅, written analysis ✅
(see the stage README).

---

## Stage 2 — Classical Control (≈8 weeks after Stage 1)

**Goal**: Implement a model-based controller for the same robot and terrain — no learning. Show that
the same locomotion can be achieved through dynamics modeling and optimization.

**Key components**:

- Rigid-body dynamics via [Pinocchio](https://github.com/stack-of-tasks/pinocchio)
- Model Predictive Control (MPC) for trajectory optimization
- Whole-Body Controller (WBC) for joint-level execution
- QP solver integration

**Deliverables**: working MPC+WBC pipeline, side-by-side comparison with Stage 1 RL policy (success
rate, energy, computational cost).

---

## Stage 3 — Hybrid (Research)

**Goal**: Investigate principled ways to combine DRL and MPC. Open-ended research stage.

**Candidate directions**:

- MPC as warm-start / safety filter for RL policy
- RL learns residual dynamics correction for MPC
- Diffusion-Policy-style imitation from MPC trajectories, then RL fine-tuning (cf. DPPO)

**Deliverables**: at least one working hybrid pipeline with quantitative comparison against pure RL
(Stage 1) and pure MPC (Stage 2).

---

## Shared infrastructure (`shared/`)

Cross-stage utilities, developed as needed:

- Dynamics wrappers around Pinocchio for use from RL code
- Unified evaluation harness (same metrics across stages)
- Visualization (terrain heatmaps, foot contact traces, reward decomposition)

---

## Stack reference

| Component | Choice | Rationale |
|---|---|---|
| Simulator | Isaac Lab (Isaac Sim 4.x) | Industry-standard for sim-to-real locomotion research |
| Robot | Anymal-D | Strong official support in Isaac Lab (`ANYMAL_D_CFG`), established baseline |
| RL library | `rsl_rl` (stage 1) → custom PyTorch | Match the official Anymal example, then re-implement for understanding |
| Dynamics | Pinocchio | De facto standard for legged MPC/WBC, mature Python bindings |
| Hardware | Ubuntu 22.04 + RTX GPU | Training requires GPU |
