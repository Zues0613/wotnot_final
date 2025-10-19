<template>
  <div id="app">
    <router-view />
    <SpeedInsights />
  </div>
</template>

<script>
import { SpeedInsights } from "@vercel/speed-insights/vue";

export default {
  name: 'App',
  components: {
    SpeedInsights
  }
};
</script>

<style>
.Toastify__toast-container {
  z-index: 99999 !important;
}
</style>