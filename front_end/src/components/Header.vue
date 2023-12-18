<template>


  <div >

    <div class="display">
        <div class="left">
            <img v-if="showVideo" :src="videoSrc" alt="Video Stream" >
        </div>

    </div>

    <div class="header">
      <!--<a href="https://pjreddie.com/darknet/yolo/" target="_blank">
          <img src="../assets/img/logo.png" width="70" class="zhuan">
      </a>
      <p class="ziti">高分卫星影像的变电站识别</p>-->
      <button  class="controll" @click="toggleVideo">{{ showVideo ? '关闭视频流' : '启用视频流' }}</button>

    </div>

  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "Header",

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






     uploadVideo(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append("video", file);


       axios.post("http://127.0.0.1:5003/upload-video", formData).then(response => {
        const videoUrl = response.data.videoUrl;
        this.uploadedVideo = videoUrl; // 显示上传的视频

        const processedVideoUrl = response.data.processedVideoUrl;
        this.processedVideo = processedVideoUrl; // 显示处理后的视频
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

.header{
    /*height:75px;*/

    display: flex;

    align-items: center;
    padding-left: 40px;
  padding-top: 100px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;
}


.header .controll{
    width:100px;
    height:35px;
    margin-left:850px;
    margin-top: 20px;
    background-color: rgb(96, 143, 244);
    border-radius: 20px;
}
.display {
    display: flex;

    width:1330px;
    height:280px;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    margin-top:250px;

}
.display .left{
    height:480px;
    width:640px;
    background-color: rgba(255, 255, 255, 0.81);
    margin-right:50px;
  border-radius: 10px; /* 设置圆角 */
  overflow: hidden; /* 隐藏溢出部分的内容 */
}
.display .right{
    width:640px;
    height:480px;
    background-color: blue;
}
.controll {
  color: white;
  border: none;

}


</style>


