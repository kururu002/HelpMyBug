<template>
  <el-container>
    <el-header>
      <el-image fit="contain" style="height: 60px;width:60px" :src="getImgUrl"/>
      Help my bug
      <a style="float:right" href="https:google.com">登入</a>
    </el-header>
    <el-main>Main</el-main>
  </el-container>
</template>

<script>
export default {
  data () {
    return {}
  },
  computed: {
    getImgUrl () {
      var images = require('@/assets/Pest-insect.png')
      return images
    }
  }
}
</script>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}
</style>
