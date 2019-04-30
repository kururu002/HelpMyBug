<template>
  <div id="app" class="full-height">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
html,
body {
  height: 100%;
  margin:0;
}
.full-height {
  height: 100%;
}
</style>
