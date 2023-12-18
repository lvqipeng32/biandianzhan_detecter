import subprocess
import cv2

def run_yolov5_detection(source, weights_path, detect_script_path):
    # 构建运行命令
    command = ['python', detect_script_path, '--source', source, '--weights', weights_path]

    # 运行命令
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # 打印标准输出和标准错误
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))

