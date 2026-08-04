from pathlib import Path

import numpy as np
import pinocchio as pin

URDF = Path.home() / "anymal_d_simple_description/urdf/anymal.urdf"
LOCKED_JOINTS = ["inspection_payload_mount_to_pan",
"inspection_payload_pan_to_tilt"]


def load_anymal_reduced():
    full = pin.buildModelFromUrdf(str(URDF),pin.JointModelFreeFlyer())
    # 从 URDF 文件构建完整的 Pinocchio 机器人模型。
    # 输入: URDF 文件路径字符串，以及根关节类型；这里使用 free-flyer 关节，
    #       使机器人在三维空间中具有平移和旋转自由度。
    # 输出: 返回一个完整的模型对象，包含关节、惯量、几何和约束信息。
    # 特性: 这是后续运动学/动力学计算的基础，通常在模型加载阶段调用一次。

    lock_ids = [full.getJointId(name) for name in LOCKED_JOINTS]
    # 根据关节名称查询对应关节在模型中的索引编号。
    # 输入: 一个或多个关节名字符串；这里从 LOCKED_JOINTS 中逐个提取。
    # 输出: 返回一个列表，包含每个目标关节的  "整数编号"   (joint id)。
    # 特性: 该编号可用于后续锁定关节、构建约简模型或进行关节级操作。
    print("整数ID",lock_ids)

    q_ref = pin.neutral(full)
    # 生成给定模型的中性构型（neutral configuration）。
    # 输入: 一个 Pinocchio 模型对象。
    # 输出: 返回一个长度为 nq 的齐次配置向量，通常表示关节角/位移 "都取零" 的参考状态。
    # 特性: 常用作约简模型构建时的参考配置，以及初始状态或平衡点的基准。
    print("中性位置  :  ",q_ref)

    return pin.buildReducedModel(full, lock_ids, q_ref)
    # 根据原始模型、要锁定的关节索引和参考构型，构建约简模型。
    # 输入: 完整模型对象、锁定关节的 joint id 列表，以及参考构型 q_ref。
    # 输出: 返回一个去掉指定关节自由度后的简化模型对象。
    # 特性: 适用于固定某些关节（如安装的负载或固定部件）后简化系统维数，
    #       便于后续求解和控制器设计。

if __name__ == "__main__":
    model = load_anymal_reduced()
    data = model.createData()
    # 为当前模型创建一个数据对象，用于存放中间计算结果。
    # 输入: 一个 Pinocchio 模型对象。
    # 输出: 返回一个包含状态缓存、计算中间量和几何信息的数据结构。
    # 特性: 大多数动力学/运动学函数都会依赖这个 data 对象保存中间结果。

    print("nq / nv     :", model.nq, "/", model.nv)
    print("total mass  :", round(pin.computeTotalMass(model), 3),
"kg")
    # 计算整个机器人系统的总质量。
    # 输入: Pinocchio 模型对象。
    # 输出: 返回一个标量浮点数，表示模型总质量（单位通常为 kg）。
    # 特性: 该函数基于各刚体的质量和几何信息汇总，常用于系统参数检查。

    print("joint table :")
    for jid, name in enumerate(model.names):
        print("    ", jid, name)
    # model.names 是模型中所有关节/刚体节点的名称列表。
    # 输入: 模型对象本身。
    # 输出: 返回一个字符串序列，表示每个关节或节点的名称。
    # 特性: 适合用来检查模型构建是否正确，或在调试时定位关节编号。

    q = pin.neutral(model)
    # 生成当前模型的中性构型向量。
    # 输入: 一个 Pinocchio 模型对象。
    # 输出: 返回一个与模型自由度对应的配置向量。
    # 特性: 常用于初始化、动力学矩阵计算和重力项计算的参考状态。
    print("reduced ： ",q)

    M = pin.crba(model, data, q)
    # 计算刚体系统的惯性矩阵（Composite Rigid Body Algorithm）。
    # 输入: 模型对象、数据对象以及当前构型 q。
    # 输出: 返回一个大小为 (nv, nv) 的惯性矩阵，描述系统在该构型下的质量分布。
    # 特性: 该矩阵对控制、优化和稳定性分析非常重要，通常是正定的。

    M = np.triu(M) + np.triu(M, 1).T
    # 将惯性矩阵对称化，提取上三角部分后再镜像到下三角部分。
    # 输入: 一个方阵矩阵 M。
    # 输出: 返回一个对称矩阵，便于可视化或检查正定性。
    # 特性: 由于数值误差可能造成 '轻微非对称' ， “使用此方法能得到更稳定的对称形式“ 。

    g = pin.computeGeneralizedGravity(model, data, q)
    # 计算系统在当前构型下的广义重力项。
    # 输入: 模型对象、数据对象以及构型 q。
    # 输出: 返回一个长度为 nv 的向量，表示每个广义坐标上的重力分量。
    # 特性: 在动力学方程中，重力项与惯性矩阵一起决定系统的运动行为。

    print("M shape     :", M.shape)
    print("M pos-def   :", bool(np.linalg.eigvalsh(M).min() > 0))
    # 使用 NumPy 的特征值分解检查惯性矩阵是否正定。
    # 输入: 一个对称方阵 M。
    # 输出: 返回该矩阵的特征值数组；这里取最小特征值并与 0 比较。
    # 特性: 若最小特征值大于零，则说明矩阵正定，通常意味着系统惯性矩阵稳定可逆。

    print("g[2]/9.81   :", round(float(g[2] / 9.81), 3), "kg")
