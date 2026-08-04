import numpy as np
import pinocchio as pin

from anymal_model import URDF, load_anymal_reduced

import pprint

if __name__ == "__main__":
    model = load_anymal_reduced()
    # 作用：加载预定义的 AnyMal 简化模型。
    # 输入：无显式参数，依赖当前项目中的 AnyMal 模型定义与 URDF 资源。
    # 输出：返回一个 Pinocchio 模型对象，包含关节、惯量、碰撞/视觉框架等信息，后续可用于运动学与动力学计算。

    data = model.createData()
    # 作用：为当前模型创建一个数据缓存对象。
    # 输入：Pinocchio 模型对象。
    # 输出：一个包含正向运动学、逆向运动学、质心计算等中间缓存字段的 data 对象；后续调用会复用其中的计算结果。

    q = pin.neutral(model)
    # 作用：生成模型的“中性构型”关节配置向量。
    # 输入：Pinocchio 模型对象。
    # 输出：一个长度为关节自由度数量的 numpy 数组，通常用于初始化姿态或进行基准位姿计算。

    print("frames named *FOOT* :")
    for fid, fr in enumerate(model.frames):
        if "FOOT" in fr.name.upper():
            print("    ", fid, fr.name, fr.type, "| parent:", model.names[fr.parent])

    pin.framesForwardKinematics(model, data, q)
    # 作用：根据给定关节配置 q，计算模型所有 frame 的世界坐标变换。
    # 输入：模型 model、数据缓存 data、关节配置 q。
    # 输出：把结果写入 data.oMf 等字段，后续可以读取每个 frame 的位姿；这是正向运动学的标准接口。

    feet = {}
    sth = {}
    rot = {}
    for fid, fr in enumerate(model.frames):
        if "FOOT" in fr.name.upper() and fr.type == pin.FrameType.BODY:
            feet[fr.name] = data.oMf[fid].translation.copy()
            # 作用：从已完成正向运动学计算的 data 中读取指定 frame 的平移部分。
            # 输入：frame 的索引 fid，以及已经计算好的 data.oMf 变换矩阵。
            # 输出：一个三维 numpy 向量，表示该足端在世界坐标系中的位置；.copy() 可避免后续修改影响缓存数据。
            sth[fr.name] = data.oMf[fid].copy()
            rot[fr.name] = data.oMf[fid].rotation.copy()
    pprint.pprint(feet)
    pprint.pprint(rot)
    # pprint.pprint(sth)
    print("--------\n",sth)

    print("foot positions (neutral q, world == base):")
    for name in sorted(feet):
        print("    ", name, np.round(feet[name], 4))
        # 作用：对数组进行四舍五入，便于打印和观察数值。
        # 输入：numpy 数组、保留的小数位数。
        # 输出：返回一个四舍五入后的新数组，常用于可视化和日志输出。

    com = pin.centerOfMass(model, data, q)
    # 作用：计算当前构型下模型的质心位置。
    # 输入：模型 model、数据缓存 data、关节配置 q。
    # 输出：一个三维 numpy 向量，表示系统重心在世界坐标系中的位置。

    print("CoM (reduced)    :", np.round(com, 4))
    expected = ("LF_FOOT", "RF_FOOT", "LH_FOOT", "RH_FOOT")
    if not all(name in feet for name in expected):
        print("!! foot names differ from expected -- read the table above")
    else:
        LF, RF, LH, RH = (feet[name] for name in expected)
        mirror_y = np.diag([1.0, -1.0, 1.0])
        # 作用：构造一个关于 Y 轴做镜像的 3x3 对角变换矩阵。
        # 输入：一个长度为 3 的对角元素序列。
        # 输出：一个对角矩阵，可用于将左右足端坐标做镜像对称变换。

        mirror_x = np.diag([-1.0, 1.0, 1.0])
        # 作用：构造一个关于 X 轴做镜像的 3x3 对角变换矩阵。
        # 输入：一个长度为 3 的对角元素序列。
        # 输出：一个对角矩阵，可用于检查前后足端之间的对称关系。

        print("L/R mirror LF~RF :", bool(np.allclose(LF, mirror_y @ RF, atol=1e-6)))
        # 作用：判断两个向量是否在容差范围内相等。
        # 输入：两个 numpy 向量/数组，以及容差 atol。
        # 输出：返回布尔值；当数值差异小于阈值时为 True。

        print("L/R mirror LH~RH :", bool(np.allclose(LH, mirror_y @ RH, atol=1e-6)))
        print("F/H mirror LF~LH :", bool(np.allclose(LF, mirror_x @ LH, atol=1e-6)))

        full = pin.buildModelFromUrdf(str(URDF), pin.JointModelFreeFlyer())
        # 作用：从 URDF 文件构建一个完整的 Pinocchio 模型。
        # 输入：URDF 文件路径字符串，以及一个自由飞行器关节模型（用于表示基座为 6 自由度浮动关节）。
        # 输出：返回一个完整模型对象，通常比缩减模型更接近真实机器人结构。

        dfull = full.createData()
        # 作用：为完整模型创建一个新的数据缓存对象。
        # 输入：完整 Pinocchio 模型对象。
        # 输出：对应的 data 对象，供后续完整模型的运动学计算使用。

        qfull = pin.neutral(full)
        # 作用：为完整模型生成一个中性构型配置。
        # 输入：完整 Pinocchio 模型对象。
        # 输出：对应的关节配置向量 qfull。

        pin.framesForwardKinematics(full, dfull, qfull)
        # 作用：计算完整模型所有 frame 的世界坐标变换。
        # 输入：完整模型 full、对应 data dfull、关节配置 qfull。
        # 输出：将结果写入 dfull.oMf 等字段，后续可读取各 frame 的位姿。

        lf_full = dfull.oMf[full.getFrameId("LF_FOOT")].translation
        # 作用：获取指定 frame 在完整模型中的平移向量。
        # 输入：完整模型的 frame ID（由 getFrameId 获得）。
        # 输出：一个三维 numpy 向量，表示该 frame 的位置。

        com_full = pin.centerOfMass(full, dfull, qfull)
        # 作用：计算完整模型在当前构型下的质心。
        # 输入：完整模型 full、data dfull、关节配置 qfull。
        # 输出：一个三维 numpy 向量，表示完整模型的质心位置。

        print("LF_FOOT full==reduced :", bool(np.allclose(LF, lf_full, atol=1e-9)))
        print("CoM     full==reduced :", bool(np.allclose(com, com_full, atol=1e-9)))
