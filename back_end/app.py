import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import cv2
from back_end.yolov5.positioning import *
import subprocess
import json
import ffmpeg

UPLOAD_FOLDER = r'./uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
video_capture = cv2.VideoCapture(0)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)
# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, 'tmp/ct')

        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext in ['.jpg', '.jpeg', '.png']:

            import torch
            model = torch.hub.load('./yolov5', 'custom', path='best.pt', source='local')
            img =  os.path.join('tmp/ct', file.filename) # or file, PIL, OpenCV, numpy, multiple
        # Inference
            results = model(img)  # <--- TTA inference
        # Results
            results.print()
            results.save(save_dir=r'E:\biandianzhan1\biandianzhan detecter\back_end\tmp\draw')
        # 复制draw文件夹到draw2文件夹
            source_dir = r'E:\biandianzhan1\biandianzhan detecter\back_end\tmp\draw2'
        # 目标文件夹路径
            target_dir = r'E:\biandianzhan1\biandianzhan detecter\back_end\tmp\image'
        # 遍历源文件夹并复制文件或文件夹到目标文件夹
            for item in os.listdir(source_dir):
                item_path = os.path.join(source_dir, item)
                target_path = os.path.join(target_dir, item)
                shutil.copy(item_path, target_path)
        # 删除draw文件夹
            shutil.rmtree(r'E:\biandianzhan1\biandianzhan detecter\back_end\tmp\draw2')
        # 获取文件名和扩展名
            file_name, file_ext = os.path.splitext(file.filename)
        # 组合新的文件名，将扩展名统一修改为".jpg"
            new_file_name = file_name + ".jpg"
            return jsonify({'status': 1,
                            'image_url': 'http://127.0.0.1:5003/tmp/ct/' + file.filename,
                            'draw_url': 'http://127.0.0.1:5003/tmp/image/' + new_file_name
                            })

    return jsonify({'status': 0})

# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response

@app.route('/upload-video', methods=['POST'])
def upload_video():
    print('1111111')

    model = torch.hub.load('./yolov5', 'custom', path='best.pt', source='local')
    model.eval()
    file = request.files['video']
    # 处理上传的视频文件
    uploaded_filename = secure_filename(file.filename)
    # 这里只是简单示例，将视频保存到 static/uploads 目录下
    uploaded_file_path = f'tmp/image/{uploaded_filename}'
    file.save(uploaded_file_path)
    # 处理视频，例如转码、裁剪等
    processed_filename = 'processed_' + uploaded_filename
    # 这里只是简单示例，将处理后的视频保存到 static/uploads 目录下
    processed_file_path = f'tmp/image/{processed_filename}'
    # 在下面添加视频处理代码
    video_path = os.path.join('tmp/image', file.filename)
    output_path = processed_file_path  # 修改输出视频的路径
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # 将frame传递给模型进行推断
        results = model(frame)
        # 在帧上绘制结果
        results.render()
        # 将帧写入视频写入器
        out.write(frame)
        # 按'q'键退出循环
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    input_file1 = os.path.join('tmp/image', file.filename)
    output_file1 = os.path.join('tmp/draw', file.filename)
    ffprobe_command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of',
                       'json', input_file1]
    ffprobe_output = subprocess.check_output(ffprobe_command).decode('utf-8')
    ffprobe_data = json.loads(ffprobe_output)

    # 获取视频的编码器类型
    codec_name = ffprobe_data['streams'][0]['codec_name']
    print(codec_name)

    # 判断编码器类型是否为H.264
    if codec_name != 'h264':
        # 执行转码操作
        if os.path.exists(output_file1):
            os.remove(output_file1)

        ffmpeg.input(input_file1).output(output_file1, codec='libx264').run()
        uploaded_video_url = f'http://127.0.0.1:5003/tmp/draw/' + file.filename
    else:
        print('视频编码是H.264，无需执行转码操作')
        uploaded_video_url = f'http://127.0.0.1:5003/tmp/image/' + file.filename

    input_file = os.path.join('tmp/image', processed_filename)
    output_file =os.path.join('tmp/draw', processed_filename)

    if os.path.exists(output_file):
        os.remove(output_file)
    ffmpeg.input(input_file).output(output_file, codec='libx264').run()
    # 返回上传的视频URL
    processed_video_url =f'http://127.0.0.1:5003/tmp/draw/'+processed_filename # 返回处理后的视频URL
    return jsonify({'videoUrl': uploaded_video_url, 'processedVideoUrl': processed_video_url})

def generate_frames():
    print('11')
    camera0 = cv2.VideoCapture(0)
    while True:
        success, frame = camera0.read()
        if not success :
            break
        else:
            frame_copy = frame.copy()
            # 检测目标
            results = model(frame_copy)
            results.render()
            #绘制距离

            # 绘制距离到视频帧副本上
            frame_encoded = cv2.imencode('.jpg', frame_copy)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')

@app.route('/video_feed')
def video_feed():
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers.add('Access-Control-Allow-Origin', '*')  # 允许跨域访问
    print('1')
    return response

if __name__ == '__main__':
    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
        'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)
    import torch
    model = torch.hub.load('./yolov5', 'custom', path='best.pt', source='local')
    model.eval()
    app.run(host='127.0.0.1', port=5003, debug=True)
