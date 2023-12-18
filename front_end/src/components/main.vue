<template>

  <div id="Main">

    <div class="back">
      <div class="header">
        <a href="https://pjreddie.com/darknet/yolo/" target="_blank">
            <img src="../assets/img/YOLOv5.png" width="125" height="50">

        </a>
        <p class="ziti">基于YOLOV5高分卫星影像的变电站识别系统</p>
    </div>


  <div class="shang">
        <div class="camera">
          <a class="cameraa" > <i class="fa-solid fa-camera"></i><router-link to="/Header" style="color: white; text-decoration: none;">实时检测</router-link></a>
        </div>
        <div class="photo">
          <a  class="photoa" > <i class="fa-solid fa-image"></i><router-link to="/Footer" style="color: white; text-decoration: none;">上传图片</router-link></a>
        </div>
        <div class="video">
          <a  class="videoa" > <i class="fa-solid fa-image"></i><router-link to="/video" style="color: white; text-decoration: none;">上传视频</router-link></a>
        </div>
    <div class="router-container">
      <router-view></router-view>
    </div>
    </div>



<div class="more">
        <div class="baidu">
            <a href="https://blog.csdn.net/shibuyiya/article/details/108992880" class="baidua" target="_blank">
                <img src="../assets/img/baidu.jpg"  class="baiduphoto">
                <p class="baidup" >
                    你了解高分卫星影像吗?
                </p>
            </a>

        </div>

        <div class="photo">
            <a href="https://cloud.tencent.com/developer/article/2113139" class="photoa" target="_blank">
                <img src="../assets/img/photo.jpg" class="baiduphoto" >
                <p class="photop" >
                    高分卫星影像拍摄的变电站图片
                </p>
            </a>
        </div>

        <div class="try">
            <a href="https://zhuanlan.zhihu.com/p/334361466" class="trya" target="_blank">
                <img src="../assets/img/try.jpg" class="baiduphoto" >
                <p class="tryp" >
                    带你体验高分卫星视角！
                </p>
            </a>
        </div>

  <div class="future">
            <a href="https://zhuanlan.zhihu.com/p/334361466" class="futurea" target="_blank">
                <img src="../assets/img/future.jpg" class="baiduphoto" >
                <p class="futurep" >
                    高分卫星未来发展
                </p>
            </a>
        </div>



    </div>

<div class="footer">

        <div class="bottom">
            <p>2023@软件项目管理@开发者小组</p>
        </div>
    </div>


</div>
  </div>


</template>
<script>
export default {
  name: "main",

  data() {
    return {
    };
  },
  methods: {},
};
</script>
<style scoped>

.back{
    background-color: #1d72bb;
}

.header{
    height:75px;

    display: flex;

    align-items: center;
    padding-left: 40px;
  background-color: #608ff4;

}

.header  .ziti{

    margin-left: 20px;
    font-size: 25px;
    font-family: "sans-serif";
    color: azure;


}

.imgg{
    width: 100%;
    display: flex;
    margin: 0 auto;
    background-color: green;

    background-repeat: no-repeat;
  background-size: cover;
    background-image:url("../assets/img/gaofenweixing.png");
    flex-direction: column;
    box-sizing: border-box;
    padding-left: 980px;
    padding-top: 170px;

}
.imgg .upp{
    width:300px;
    height:70px;

    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 60px;

}
.imgg .upp .uppp{
    font-size:50px;
    color: white;

}
.imgg .dowwn{
    width:400px;
    height:100px;

    display: flex;
    justify-content: left;
    align-items: center;


}
.imgg .dowwn .dowwwn{
    font-size:35px;
    color: white;
    font-family: "华文行楷";


}
.shang{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-image: url("https://i.imgs.ovh/2023/12/17/6Qe7m.jpeg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding-top: 80px; /* 调整顶部内边距以实现靠上效果 */
  height: 1000px;
}
.router-container {
  position: absolute;
  top: 200px;
  left: 0;
  right: 0;
  bottom: 0;
}
.shang .camera{
    width:120px;
    height:50px;
    border-radius: 10px;
    background-color: #608ff4;

    margin-right: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.shang  .camera .cameraa{
    text-decoration-line: none;
    font-size: 20px;
    color: #1d72bb;
}

.shang  .camera .cameraa .fa-camera{
    margin-right: 10px;
}

.shang .photo{
    width:120px;
    height:50px;
    border-radius: 10px;
    background-color: #608ff4;

    margin-right: 50px;
    display: flex;
    justify-content: center;
    align-items: center;

}
.shang .photo .photoa{
    text-decoration-line: none;
    font-size: 20px;
    color: #1d72bb;
}
.shangchuan  .photo .photoa .fa-image{
    margin-right: 10px;
}

.shang .video{
    width:120px;
    height:50px;
    border-radius: 10px;
    background-color: #608ff4;

    margin-right: 50px;
    display: flex;
    justify-content: center;
    align-items: center;

}
.shang .video .videoa{
    text-decoration-line: none;
    font-size: 20px;
    color: #1d72bb;
}
.shang .video .videoa .fa-video{
    margin-right: 10px;
}

.more{

    display: flex;
    margin: 0 auto;
    justify-content: space-between;
    align-items: center;
    width:100%;
    height:300px;
    flex-wrap: wrap;
}
.baiduphoto {
  width: 300px;
  height: 265px;
}
.more .baidu{
    width:300px;
    height:265px;
    background-color: #608ff4;
    flex-direction: column;
}
.more .baidu .baidua{
    text-decoration: none ;
}
.more .baidu  .baidup{
    text-align: center;
    color: #ffffff;
}

.more .photo{
    width:300px;
    height:265px;
    background-color:antiquewhite;
    flex-direction: column;
}
.more .photo .photoa{
    text-decoration: none ;
}
.more .photo  .photop{
    text-align: center;
    color: #ffffff;
}

.more .try{
    width:300px;
    height:265px;
    background-color:antiquewhite;
    flex-direction: column;

}
.more .try .trya{
    text-decoration: none ;
}
.more .try  .tryp{
    text-align: center;
    color: #ffffff;
}

.more .future{
    width:300px;
    height:265px;
    background-color:antiquewhite;
    flex-direction: column;

}
.more .future .futurea{
    text-decoration: none ;
}
.more .future  .futurep{
    text-align: center;
    color: #ffffff;
}

.footer{
    flex-wrap: wrap;
    margin-top: 100px;
    display:flex;
    text-decoration: none ;
    background-color: #608ff4;
    height:60px;
}

.footer .bottom{
    margin-left:600px;
    margin-bottom: 0px;
    width:700px;
    height:20px;

}

</style>


