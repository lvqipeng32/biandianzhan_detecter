import torch
import cv2
from back_end.yolov5.positioning import *

model = torch.hub.load('.', 'custom', path='best.pt', source='local')


# 输入图片路径
image_path = r'E:\xjszt\backend\back_end\yolov5\img.png'
img = image_path

results = model(img)

print(results.xyxy[0])

xyxy = results.xyxy[0]
w = 90  # mm
tensor_data = results.xyxy[0]

# 转换为 Python 列表数据类型
list_data = tensor_data.tolist()

print(list_data)
coordinates = list_data
# 计算中心点坐标和宽高
center_x = (coordinates[0][0] + coordinates[0][2]) / 2
center_y = (coordinates[0][1] + coordinates[0][3]) / 2
width = coordinates[0][2] - coordinates[0][0]
height = coordinates[0][3] - coordinates[0][1]

# 转换为只包含中心点坐标和宽高的列表
transformed_coordinates = [center_x/1000, center_y/1000, width/1000, height/1000]

print(transformed_coordinates)


YOLOdata = transformed_coordinates
camera = Camera1([1920, 1080])
camera.set_inner_matrix([934.423221357734, 934.569525590775, 651.901127267318, 342.276661802914])

X = camera.monocular_positioning(YOLOdata, w)
distance = np.linalg.norm(X)

print(distance)


img = cv2.imread(img)
cv2.rectangle(img, (int(coordinates[0][0]), int(coordinates[0][1])), (int(coordinates[0][2]), int(coordinates[0][3])), (0, 255, 0), 2)
distance_text = f'Distance: {distance:.2f} mm'
cv2.putText(img, distance_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# 显示图片
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()