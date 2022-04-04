FourStepPhaseShifting

# 0. 简介

这个项目使用"互补格雷码+相移码"实现物体的三维重建，整个重建过程可以分为六个步骤：

1. 生成格雷码图像
2. 生成四步相移图像
3. 求解相对相位
4. 求解绝对相位
5. 获得相机-投影仪像素坐标之间的对应关系
6. 根据标定参数获得重建点云信息

# 1. 生成格雷码图像