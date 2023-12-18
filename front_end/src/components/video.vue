<template>

 <div id="Header">


    <div class="display">
        <div class="left">
            <h3 style="color: #ffffff">上传视频</h3>
        </div>
        <div class="right">
          <h3 style="color: #ffffff">识别结果</h3>
        </div>
    </div>
    <div class="container">
        <div class="leftArea">
            <video v-if="uploadedVideo" ref="uploadedVideoPlayer" :src="uploadedVideo" controls width="100%" ></video>
        </div>
        <div class="rightArea">
            <video v-if="processedVideo" ref="processedVideoPlayer" :src="processedVideo" controls  width="100%" ></video>
        </div>
    </div>

    <div class="choose">
        <div class="left">
            <label for="uploadInput" class="custom-file-upload">
                上传视频
              <input type="file" id="uploadInput" @change="uploadVideo" accept="video/*" />
            </label>
        </div>

    </div>

 <div v-if="loading" class="loading-overlay">
      <div class="loading-text">请等待1分钟左右...</div>
    </div>
 </div>

</template>
<script>
import axios from "axios";

export default {
  name: "Video",

  data() {
    return {


showVideo: false,
      videoSrc: '',
      uploadedVideo: '',
      processedVideo: '',
      server_url: "http://127.0.0.1:5003",
      activeName: "first",
      active: 0,
      centerDialogVisible: true,
      url_1: "",
      url_2: "",
      textarea: "",
      srcList: [],
      srcList1: [],
      feature_list: [],
      feature_list_1: [],
      feat_list: [],
      url: "",
      visible: false,
      wait_return: "等待上传",
      wait_upload: "等待上传",
      loading: false,
      table: false,
      isNav: false,
      showbutton: true,
      percentage: 0,
      fullscreenLoading: false,
      opacitys: {
        opacity: 0,
      },
      dialogTableVisible: false,
    };
  },

    created: function () {
    document.title = "YOLOv5目标检测WEB端";
  },

  methods: {
       toggleVideo() {
      this.showVideo = !this.showVideo;

      if (this.showVideo) {
        this.videoSrc = 'http://127.0.0.1:5003/video_feed'; // 根据实际的后端地址进行修改
         axios.post('http://127.0.0.1:5003/update_show_video', { showVideo: this.showVideo })
      } else {
        this.videoSrc = '';
          axios.post('http://127.0.0.1:5003/update_show_video', { showVideo: this.showVideo })
      }
    },






      showLoading() {
      this.loading = true;
    },
    uploadVideo(event) {
      this.showLoading(); // 显示加载提示

      const file = event.target.files[0];
      const formData = new FormData();
      formData.append("video", file);

      axios.post("http://127.0.0.1:5003/upload-video", formData).then(response => {
        const videoUrl = response.data.videoUrl;
        this.uploadedVideo = videoUrl; // 显示上传的视频

        const processedVideoUrl = response.data.processedVideoUrl;
        this.processedVideo = processedVideoUrl; // 显示处理后的视频

        this.loading = false; // 隐藏加载提示
      });
    },


    true_upload() {
      this.$refs.upload.click();
    },
    true_upload2() {
      this.$refs.upload2.click();
    },
    next() {
      this.active++;
    },
    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
    // 上传文件
    update(e) {
      this.percentage = 0;
      this.dialogTableVisible = true;
      this.url_1 = "";
      this.url_2 = "";
      this.srcList = [];
      this.srcList1 = [];
      this.wait_return = "";
      this.wait_upload = "";
      this.feature_list = [];
      this.feat_list = [];
      this.fullscreenLoading = true;
      this.loading = true;
      this.showbutton = false;
      let file = e.target.files[0];
      this.url_1 = this.$options.methods.getObjectURL(file);
      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据
      var timer = setInterval(() => {
        this.myFunc();
      }, 30);
      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      }; //添加请求头
      axios
        .post(this.server_url + "/upload", param, config)
        .then((response) => {
          this.percentage = 100;
          clearInterval(timer);
          this.url_1 = response.data.image_url;
          this.srcList.push(this.url_1);
          this.url_2 = response.data.draw_url;
          this.srcList1.push(this.url_2);
          this.fullscreenLoading = false;
          this.loading = false;


          this.feature_list.push(response.data.image_info);
          this.feature_list_1 = this.feature_list[0];
          this.dialogTableVisible = false;
          this.percentage = 0;
          this.notice1();
        });
    },
    myFunc() {
      if (this.percentage + 33 < 99) {
        this.percentage = this.percentage + 33;
      } else {
        this.percentage = 99;
      }
    },
    drawChart() {},
    notice1() {
      this.$notify({
        title: "预测成功",
        message: "点击图片可以查看大图",
        duration: 0,
        type: "success",
      });
    },
  },
  mounted() {
    this.drawChart();

  },
};
</script>
<style scoped>
#Header {

  width: 100%;
    height: 960px;
}
.header{
    height:75px;

    display: flex;

    align-items: center;
    padding-left: 40px;

}

.header  .img{


}
.header  .ziti{

    margin-left: 20px;
    font-size: 25px;
    font-family: "sans-serif";

}

.display{
    display: flex;
    padding-left:450px;
    align-items: center;
    margin-top: 100px;
}
.display .left{

}
.display .right{
    margin-left: 430px;
}
.container {
    width:1000px;
    display: flex;

    margin: 0 auto;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
}
.container .leftArea{
    width: 45%;
    height: 300px;
    border: 1px solid #ffffff;
    padding: 10px;
  border-radius: 10px; /* 设置圆角 */
  overflow: hidden; /* 隐藏溢出部分的内容 */
}
.container .rightArea {
    width: 45%;
    height: 300px;
    border: 1px solid #ffffff;
    padding: 10px;
  border-radius: 10px; /* 设置圆角 */
  overflow: hidden; /* 隐藏溢出部分的内容 */
}
.container .leftArea .front{
    max-width: 100%;
    max-height: 100%;
}
.container .rightArea .back{
    max-width: 100%;
    max-height: 100%;
}
.choose{
    margin-top: 50px;
    display:flex;
}
.choose .left{
    display:flex;
    margin-left: 420px;
}

.choose .left .custom-file-upload{

    background-color: #608ff4;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 4px;
    height:23px;
}
.choose .right{

    display:flex;
    margin-left: 444px;
}
.choose .right .recognize-btn{
    background-color: sandybrown;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 4px;
}
input[type="file"] {
    display: none;
}
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-text {
  font-size: 24px;
  color: white;
}

</style>


