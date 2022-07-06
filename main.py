import copy
import os
from utils.swc import SWCReader
from crop import CropHandler, VoxelCropHandler
import json


# 输入参数，swc node数量 bb size [x_size, y_size, z_size]
def calBaseline(node_cnt, bb_size):
    # n(int) type(int) x(float/double) y(float/double) z(float/double) r(float/double) parent(int)
    # 单位 Byte
    mem_per_node = 28

    volume_total = node_cnt * bb_size[0] * bb_size[1] * bb_size[2]
    mem_total = node_cnt * mem_per_node

    return volume_total, mem_total


# 根据bb计算性能
def calPerformance(bbList):
    # 总体积
    # box 总数
    volume_total = 0
    box_cnt = 0
    nodes_total = 0

    for sbbList in bbList:
        for bb in sbbList:
            volume_total += bb["size"][0] * bb["size"][1] * bb["size"][2]
            box_cnt += 1
            nodes_total += len(bb["nodes"])

    print("-----nodes_total------:", nodes_total)
    return volume_total, box_cnt


def calVoxelGridPerformance(bbList):
    volume_total = 0
    box_cnt = 0
    nodes_total = 0

    for bb in bbList:
        volume_total += bb["size"][0] * bb["size"][1] * bb["size"][2]
        box_cnt += 1
        nodes_total += len(bb["nodes"])

    print("-----nodes_total------:", nodes_total)
    return volume_total, box_cnt


if __name__ == '__main__':
    """------------------------version 1.0 segment crop-------------------------"""
    # swc_path = os.path.join(os.getcwd(), "swc/18454_00158.swc")
    # SWC = SWCReader(swc_path)
    # print("filename:", SWC.getSWCFileName())
    # swc_segments = SWC.getSWCSegments()
    #
    # # crop
    # cropHandler = CropHandler(swc_segments)
    # bb_list = cropHandler.segmentCropWithFixedBB([256, 256, 256])
    #
    # # 计算baseline
    # volume_base, mem_base = calBaseline(SWC.getNodeCnt(), [256, 256, 256])
    # volume_optimize, box_cnt = calPerformance(bb_list)
    # print("baseline volume:", volume_base)
    # print("baseline memory(Byte):", mem_base)
    # print("baseline box cnt", SWC.getNodeCnt())
    #
    # print("\n")
    #
    # print("optimize memory(Byte):", volume_optimize)
    # print("optimize memory(Byte):", mem_base)
    # print("optimize box cnt", box_cnt)

    """------------------------version 2.0 voxel grid crop-------------------------"""
    swc_path = os.path.join(os.getcwd(), "swc/18454_00158.swc")
    SWC = SWCReader(swc_path)
    print("filename:", SWC.getSWCFileName())
    swc_nodes = SWC.getSWCData()

    # crop
    cropHandler = VoxelCropHandler(swc_nodes, voxel_size=128, box_max_size=256)
    bb_list = cropHandler.voxelCrop()

    # 计算baseline
    volume_base, mem_base = calBaseline(SWC.getNodeCnt(), [256, 256, 256])
    volume_optimize, box_cnt = calVoxelGridPerformance(bb_list)
    print("baseline volume:", volume_base)
    print("baseline memory(Byte):", mem_base)
    print("baseline box cnt", SWC.getNodeCnt())

    print("\n")
    print("optimize memory(Byte):", volume_optimize)
    print("optimize memory(Byte):", mem_base)
    print("optimize box cnt", box_cnt)

    # 记录swc node信息
    with open("results/swc.json", 'w') as f:
        json.dump(SWC.getSWCData(), f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行

    # 记录bb list信息
    with open("results/bb_v2.json", 'w') as f:
        json.dump(bb_list, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
