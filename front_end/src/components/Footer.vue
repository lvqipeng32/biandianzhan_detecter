<template>

  <div id="Footer">

    <!--<div class="header">
        <a href="https://pjreddie.com/darknet/yolo/" target="_blank">
            <img src="../assets/img/logo.png" width="70" class="zhuan">
        </a>
        <p class="ziti">高分卫星影像的变电站识别</p>

    </div>-->



    <el-dialog
      title="AI预测中"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">请耐心等待约3秒钟</span>
    </el-dialog>
<div class="parent-container">
    <div id="CT" >
      <div id="CT_image">
        <el-card
          id="CT_image_1"
          class="box-card"
          style="
            border-radius: 8px;
            width: 800px;
            height: 360px;
            margin-bottom: -30px;
          "
        >
          <div class="demo-image__preview1">
            <div
              v-loading="loading"
              element-loading-text="上传图片中"
              element-loading-spinner="el-icon-loading"
            >
              <el-image
                :src="url_1"
                class="image_1"
                :preview-src-list="srcList"
                style="border-radius: 3px 3px 0 0"
              >
                <div slot="error">
                  <div slot="placeholder" class="error">
                    <el-button
                      v-show="showbutton"
                      type="primary"
                      icon="el-icon-upload"
                      class="download_bt"
                      v-on:click="true_upload"
                    >
                      上传图像
                      <input
                        ref="upload"
                        style="display: none"
                        name="file"
                        type="file"
                        @change="update"
                      />
                    </el-button>
                  </div>
                </div>
              </el-image>
            </div>
            <div class="img_info_1" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 6px">原始图像</span>
            </div>
          </div>
          <div class="demo-image__preview2">
            <div
              v-loading="loading"
              element-loading-text="处理中,请耐心等待"
              element-loading-spinner="el-icon-loading"
            >
              <el-image
                :src="url_2"
                class="image_1"
                :preview-src-list="srcList1"
                style="border-radius: 3px 3px 0 0"
              >
                <div slot="error">
                  <div slot="placeholder" class="error">{{ wait_return }}</div>
                </div>
              </el-image>



            </div>
            <div class="img_info_1" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 4px">检测结果</span>
            </div>
          </div>
        </el-card>
      </div>
      <div id="info_patient">
        <!-- 卡片放置表格 -->

          <div slot="header" class="clearfix">

            <el-button
              style="margin-left: 35px"
              v-show="!showbutton"
              type="primary"
              icon="el-icon-upload"
              class="download_bt"
              v-on:click="true_upload2"
            >
              重新选择图像
              <input
                ref="upload2"
                style="display: none"
                name="file"
                type="file"
                @change="update"
              />
            </el-button>
          </div>

      </div>
    </div>
 <div>
  </div>
<div>

  </div>


</div>
  </div>



</template>
<script>
import axios from "axios";

export default {
  name: "Footer",
  data() {
    return {
      msg: "",
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
#Footer {
  /*background:#F2F6FC;*/
/*background: url("https://i.imgs.ovh/2023/12/02/wp3oX.jpeg") no-repeat;
  background-size: cover;*/
  width: 100%;
    height: 700px;

}
.header{
    /*height:75px;

    display: flex;*/

    align-items: center;
    padding-left: 40px;

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
    border: 1px solid gray;
    padding: 10px;
}
.container .rightArea {
    width: 45%;
    height: 300px;
    border: 1px solid gray;
    padding: 10px;
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

.choose .left .upload-btn{

    background-color: orangered;
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

#hello p {
  font-size: 15px !important;
  /*line-height: 25px;*/
}

.n1 .el-step__description {
  padding-right: 20%;
  font-size: 14px;
  line-height: 20px;
  /* font-weight: 400; */
}
</style>

<style scoped>


img {
  max-width: 100%;
  max-height: 100%;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}


.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 680px;
  height: 200px;
  border-radius: 8px;
  margin-top: -20px;
}


#CT {
  display: flex;
  height: 100%;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0 auto;
  margin-right: 0px;
  max-width: 1800px;
}

#CT_image_1 {
  width: 90%;
  height: 40%;
  margin: 0px auto;

  margin-right: 180px;
  margin-bottom: 0px;
  border-radius: 4px;
}

#CT_image {
  margin-bottom: 60px;
  margin-left: 30px;
  margin-top: 5px;
}

.image_1 {
  width: 275px;
  height: 260px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #608ff4;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 250px;
  height: 290px;
  margin: 20px 60px;
  float: left;
}

.demo-image__preview2 {
  width: 250px;
  height: 290px;

  margin: 20px 460px;
  /* background-color: green; */
}

.error {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}


.block-sidebar .block-sidebar-item {
  font-size: 50px;
  color: lightblue;
  text-align: center;
  line-height: 50px;
  margin-bottom: 20px;
  cursor: pointer;
  display: block;
}

div {
  display: block;
}

.block-sidebar :hover {
  color: #187aab;
}

.download_bt {
  padding: 10px 16px ;background-color: #608ff4;
}



Content {
  width: 85%;
  height: 800px;
  background-color: #ffffff;
  margin: 15px auto;
  display: flex;
  min-width: 1200px;
}




#info_patient {
  margin-top: 10px;
  margin-right: 160px;
}
.parent-container {
  display: flex;
 margin-top: 200px;
  margin-left: 300px;

}

</style>


