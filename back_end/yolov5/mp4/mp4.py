import cv2

def convert_video_to_frames(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    frame_count = 0

    while success:
        output_frame_path = "{}\\frame1_{}.jpg".format(output_path, frame_count)
        cv2.imwrite(output_frame_path, frame)  # 将帧保存为图像文件
        success, frame = video.read()
        frame_count += 1

    video.release()

# 调用函数进行视频到图片的转换
video_path = "test7.mp4"  # 输入视频路径
output_path = "output"  # 图片输出路径

convert_video_to_frames(video_path, output_path)