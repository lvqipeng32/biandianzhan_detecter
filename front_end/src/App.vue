<template>

  <div id="app">
    <app-main></app-main>
  </div>
</template>

<script>
import main from "./components/main";

//import Content from "./components/Content";
export default {
  name: 'App',
  data() {
    return {};
  },
  components: {
    "app-main": main,

    //"app-content": Content,
  },
  methods: {},
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>
