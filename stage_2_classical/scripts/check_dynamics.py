"""检查机器人动力学模型的简单脚本。

本脚本使用 Pinocchio 从 URDF 加载 AnyMal 机器人模型，计算惯性矩阵和重力向量，
并打印模型结构和动力学性质。

用法：
    直接运行脚本：
        python stage_2_classical/scripts/check_dynamics.py

    作为模块导入：
        from stage_2_classical.scripts.check_dynamics import (
            load_anymal_model,
            compute_dynamics_properties,
            print_dynamics_report,
        )
        model, data = load_anymal_model()
        props = compute_dynamics_properties(model, data)
        print_dynamics_report(model, props)

Pinocchio API 说明：
    pin.buildModelFromUrdf(urdf_filename, joint_model)
        - 从 URDF 文件构建机器人模型。
        - 返回一个 Model 对象，包含机器人拓扑、关节类型、惯性、几何信息等。

    pin.JointModelFreeFlyer()
        - 根关节类型，表示机器人基座为自由浮动体。
        - 适用于四足机器人等在空间中可移动的系统。

    model.createData()
        - 为 Model 创建 Data 对象。
        - Data 用于保存 Pinocchio 计算的中间结果，例如重力、惯性矩阵、加速度等。

    pin.computeTotalMass(model)
        - 计算整个模型的总质量。
        - 仅依赖 Model 中每个关节/链接的惯性信息。

    pin.neutral(model)
        - 生成模型的默认中立配置 q。
        - 中立配置通常表示零关节角度、默认姿态或平衡状态。

    pin.crba(model, data, q)
        - 计算质量矩阵 M（Composite Rigid Body Algorithm）。
        - 将结果写入 Data，并返回惯性矩阵上三角部分。

    pin.computeGeneralizedGravity(model, data, q)
        - 计算广义重力向量 g。
        - 结果表示每个自由度受重力作用的广义力。
"""

from pathlib import Path

import numpy as np
import pinocchio as pin

# pathlib 用于跨平台路径处理。
# numpy 用于矩阵操作和数值计算。
# pinocchio 用于机器人动力学建模与计算。

# 默认 URDF 文件路径，指向用户主目录下的 AnyMal 模型描述文件。
# 这里使用 Path.home() 获取当前系统用户的 home 目录。
# 如果当前用户是 lqm，则通常为 /home/lqm。
# 用 Path 的 / 运算符拼接子目录，避免手动字符串拼接错误。
URDF = Path.home() / "anymal_d_simple_description/urdf/anymal.urdf"

# 打印当前 home 目录，帮助确认路径是否指向预期位置。
print("Path.home() : ", Path.home())

def load_anymal_model(urdf_path: Path = URDF):
    """加载 AnyMal 的 Pinocchio 模型并创建数据对象。

    Args:
        urdf_path: AnyMal 机器人 URDF 文件的路径。

    Returns:
        model: Pinocchio 模型对象。
        data: 与模型关联的 Pinocchio 数据对象。

    Usage:
        model, data = load_anymal_model()

    buildModelFromUrdf 用法说明：
        pin.buildModelFromUrdf(urdf_filename, joint_model)

        - urdf_filename: URDF 文件路径字符串。
        - joint_model: 根关节类型。这儿使用 pin.JointModelFreeFlyer()
          表示机器人基的自由度包含 6 个平移/旋转自由度。
    """
    # 从 URDF 加载模型并构建 Pinocchio Model 对象。
    # 该调用返回的 model 包含机器人结构、关节拓扑、惯性数据等。
    model = pin.buildModelFromUrdf(str(urdf_path), pin.JointModelFreeFlyer())

    # 为 model 创建一个 Data 对象，用于后续的动力学计算。
    # Data 存储中间结果，避免每次计算时重新分配内存。
    data = model.createData()

    # 返回 model 和 data，供后续计算函数使用。
    return model, data


def compute_dynamics_properties(model, data):
    """计算模型的质量矩阵、重力向量和总质量。

    Args:
        model: Pinocchio 模型对象。
        data: 与模型关联的 Pinocchio 数据对象。

    Returns:
        dict: 包含以下键值：
            - total_mass: 机器人总质量。
            - M: 对称惯性矩阵（质量矩阵）。
            - g: 广义重力向量。
            - q_neutral: 模型的中立关节状态。

    Usage:
        props = compute_dynamics_properties(model, data)
        print(props['total_mass'])
    """
    # 计算机器人总质量，返回一个标量。
    # 输出是一个浮点数，单位与模型 URDF 中定义的惯性单位一致（通常是 kg）。
    total_mass = pin.computeTotalMass(model)

    # 生成模型的中立配置 q_neutral。
    # 该向量表示默认的关节/基座状态，通常用于静态分析或刚开始的姿态。
    q_neutral = pin.neutral(model)

    # 计算质量矩阵 M（关节空间惯性矩阵）。复合刚体算法。
    # 该矩阵用于动力学方程 M(q) * qdd + ...，描述惯性耦合关系。
    M = pin.crba(model, data, q_neutral)
    # crba 只返回上三角部分，因此需要补全成对称矩阵。
    M = np.triu(M) + np.triu(M, 1).T

    # 计算给定配置下的广义重力向量 g。
    # 输出向量长度等于模型自由度 nv，可用于构造重力项。
    g = pin.computeGeneralizedGravity(model, data, q_neutral)

    # 返回一个字典，包含计算结果和中立配置，便于后续打印或验证。
    return {
        "total_mass": total_mass,
        "M": M,
        "g": g,
        "q_neutral": q_neutral,
    }


def print_dynamics_report(model, properties):
    """打印模型动力学检查报告。

    Args:
        model: Pinocchio 模型对象。
        properties: compute_dynamics_properties 返回的字典。

    Usage:
        print_dynamics_report(model, properties)
    """
    total_mass = properties["total_mass"]
    M = properties["M"]
    g = properties["g"]

    # 打印模型名称，便于确认加载的 URDF 对象正确。
    print("model name  :", model.name)
    try:
        # model.names 是 Pinocchio C++ std::vector<string> 的 Python 包装对象，
        # 直接打印会显示一个 C++ 对象的表示。将其转换为 Python 列表以便可读输出。
        print("joint names : ", list(model.names))
    except Exception:
        # 作为退路，逐项转换为字符串并打印（更稳健）
        print("joint names : ", [str(n) for n in model.names])
    # 打印模型自由度：配置维度 nq 和速度维度 nv。
    print("nq / nv     :", model.nq, "/", model.nv)
    # 打印计算得到的总质量。
    print("total mass  :", round(total_mass, 3), "kg")
    # 打印惯性矩阵维度，确认矩阵尺寸与自由度一致。
    print("M shape     :", M.shape)
    # 检查质量矩阵是否对称。
    print("M symmetric :", bool(np.allclose(M, M.T)))

    # 计算质量矩阵的最小特征值，判断其是否正定。
    min_eig = float(np.linalg.eigvalsh(M).min())
    # 质量矩阵应为正定矩阵，若最小特征值<=0则说明模型或参数可能有问题。
    print(
        "M pos-def   :",
        bool(min_eig > 0),
        "| min eigenvalue =",
        round(min_eig, 6),
    )
    # 打印广义重力向量前 3 个分量，通常对应基座平移方向。
    print("g[0:3]      :", np.round(g[:3], 3))
    # 通过 g[2]/9.81 估算等效质量，检查是否接近总质量。
    print(
        "g[2]/9.81   :",
        round(float(g[2] / 9.81), 3),
        "kg  <- should equal total mass",
    )


def main():
    """脚本入口函数。

    直接运行该脚本时，会加载 URDF 模型、计算动力学属性并打印检查结果。
    """
    # 加载模型与数据对象。
    model, data = load_anymal_model()
    # 计算质量、惯性矩阵和重力信息。
    properties = compute_dynamics_properties(model, data)
    # 打印完整的动力学检查报告。
    print_dynamics_report(model, properties)


if __name__ == "__main__":
    main()
