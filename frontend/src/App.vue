<template>
  <div id="app">
    <CaptchaDetector />
  </div>
</template>

<script>
import CaptchaDetector from './components/CaptchaDetector.vue'

export default {
  components: {
    CaptchaDetector
  }
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background: #EDF2F7;
  color: #2D3748;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  line-height: 1.5;
  padding: 20px;
}

#app {
  max-width: 1400px;
  margin: 0 auto;
}
</style>