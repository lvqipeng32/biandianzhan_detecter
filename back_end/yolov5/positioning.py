
import numpy as np
from scipy.optimize import minimize


class Camera1:
    def __init__(self, resolution_ration):
        self.inner_matrix = []  # 内参 [fu, fv, u0, v0]
        self.world_camera = []  # 相机在世界坐标系中的坐标
        self.resolution_ration = resolution_ration  # 相机分辨率 [长 * 宽]

    def set_inner_matrix(self, inner_matrix):
        self.inner_matrix = inner_matrix

    def monocular_positioning(self, YOLOdata, width):
        # 获取内参
        fu = self.inner_matrix[0]
        fv = self.inner_matrix[1]
        u0 = self.inner_matrix[2]
        v0 = self.inner_matrix[3]

        # 获取目标像素坐标
        Xyolo = YOLOdata[0]
        Yyolo = YOLOdata[1]
        Wyolo = YOLOdata[2]
        Hyolo = YOLOdata[3]

        u = (Xyolo - Wyolo / 2) * self.resolution_ration[0]
        v = (Yyolo - Hyolo / 2) * self.resolution_ration[1]
        u2 = (Xyolo + Wyolo / 2) * self.resolution_ration[0]

        # 获取目标预设宽度
        w = width

        # 计算相机坐标系
        A = np.array(
            [
                [fu, 0, u0 - u],
                [0, fv, v0 - v],
                [fu, 0, u0 - u2]
            ]
        )
        B = np.array([0, 0, (-1) * w * fu])

        X = np.linalg.solve(A, B)  # [x,y,z]
        # distance = np.linalg.norm(X)
        return X

    def multi_positioning(self, YOLOdata, width):
        # 获得相机坐标系坐标
        X_camera_object = self.monocular_positioning(YOLOdata, width)

        # 转置计算世界坐标系坐标
        rot_matrix = rotation_matrix([1, 0, 0], 0)
        X_world_object = transform_coordinates(X_camera_object, self.world_camera, rot_matrix)

        # 计算方向向量
        world_camera = np.array(self.world_camera)
        world_object = np.array(X_world_object)
        direction_vector = world_object - world_camera

        # 返回相机坐标和方向向量
        return [world_camera, direction_vector]


def multi_positioning(lines):
    initial_guess = np.array([0, 0, 0])  # 初始猜测
    result = minimize(total_distance_to_lines, initial_guess, args=(lines,))
    return result.x


def total_distance_to_lines(point, lines):
    # 计算一个点到一组直线的总距离。
    return sum(line_point_distance(line[0], line[1], point) for line in lines)


def line_point_distance(line_point, line_direction, point):
    # 计算一个点到直线的距离。
    point_vector = point - line_point
    cross_prod = np.cross(line_direction, point_vector)
    return np.linalg.norm(cross_prod) / np.linalg.norm(line_direction)


def rotation_matrix(axis, theta):
    """
    创建一个给定轴和旋转角度（theta）的旋转矩阵。
    使用罗德里格斯旋转公式来进行计算。
    """
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    return np.array([[a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)],
                     [2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)],
                     [2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c]])


def transform_coordinates(point, point_A, rotation_matrix):
    """
    将一个坐标点从一个坐标系转换到另一个坐标系。
    point: 原坐标系中的点坐标（围绕点 A）。
    point_A: 点 A 在新坐标系中的坐标。
    rotation_matrix: 从旧坐标系到新坐标系的旋转矩阵。
    """
    # 旋转点
    rotated_point = np.dot(rotation_matrix, point)
    # 平移点
    transformed_point = rotated_point + point_A
    return transformed_point
