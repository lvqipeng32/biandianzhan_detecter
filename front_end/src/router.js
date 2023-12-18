import Vue from 'vue';
import VueRouter from 'vue-router';
import Header from "@/components/Header.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Header',
    component: Header // 需要导入对应的组件
  },

  // 其他路由配置...
];

const router = new VueRouter({
  mode: 'history', // 可选项，指定路由模式，可以是history、hash或abstract，默认为hash
  routes
});

export default router;