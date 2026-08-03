"""Regenerate the stage-1 training-curve figures in docs/ from rsl_rl TensorBoard logs.

Usage:
    python scripts/plot_training_curves.py            # latest run under logs/rsl_rl/stage_1_pure_rl
    python scripts/plot_training_curves.py --run logs/rsl_rl/stage_1_pure_rl/2026-08-03_00-44-21
"""

import argparse
import glob
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

STAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG_ROOT = os.path.join(STAGE_DIR, "logs", "rsl_rl", "stage_1_pure_rl")
DEFAULT_OUT_DIR = os.path.join(STAGE_DIR, "docs")

SERIES = "#2a78d6"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

FIGURES = [
    ("Train/mean_reward", "Mean episode reward", "mean_reward.png"),
    ("Curriculum/terrain_levels", "Terrain curriculum level (mean over envs, 0-9)", "terrain_levels.png"),
]


def latest_run(log_root: str) -> str:
    runs = sorted(p for p in glob.glob(os.path.join(log_root, "*")) if os.path.isdir(p))
    if not runs:
        raise SystemExit(f"No runs found under {log_root}")
    return runs[-1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default=None, help="Run directory (default: latest run)")
    parser.add_argument("--out", default=DEFAULT_OUT_DIR, help="Output directory for the PNGs")
    args = parser.parse_args()

    run = args.run or latest_run(DEFAULT_LOG_ROOT)
    os.makedirs(args.out, exist_ok=True)

    accumulator = EventAccumulator(run, size_guidance={"scalars": 0})
    accumulator.Reload()

    for tag, title, filename in FIGURES:
        events = accumulator.Scalars(tag)
        xs = [e.step for e in events]
        ys = [e.value for e in events]

        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(xs, ys, color=SERIES, linewidth=2)
        ax.plot(xs[-1], ys[-1], "o", color=SERIES, markersize=5)
        ax.annotate(
            f"{ys[-1]:.2f}",
            (xs[-1], ys[-1]),
            xytext=(-6, 10),
            textcoords="offset points",
            ha="right",
            color=INK,
            fontsize=10,
            fontweight="bold",
        )

        ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel("Learning iteration", color=INK_SECONDARY, fontsize=10)
        ax.grid(color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(AXIS)
        ax.tick_params(colors=MUTED, labelsize=9)

        out_path = os.path.join(args.out, filename)
        fig.tight_layout()
        fig.savefig(out_path, facecolor="white")
        plt.close(fig)
        print(f"{tag}  ->  {out_path}  ({len(xs)} points, final {ys[-1]:.3f})")


if __name__ == "__main__":
    main()
