import Vue from "vue";
import App from "./App.vue";
import store from "./store";
import VueKonva from "vue-konva";
import vuetify from "./plugins/vuetify";
import VueSocketIOExt from "vue-socket.io-extended";
import io from "socket.io-client";

Vue.use(VueKonva);
Vue.config.productionTip = false;

const socket = io("localhost:8888");

Vue.use(VueSocketIOExt, socket);
new Vue({
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
