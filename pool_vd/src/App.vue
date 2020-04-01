<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="@/assets/pool.png"
          transition="scale-transition"
          width="50"
        />
      </div>
      <v-toolbar-title>Pool detection</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="optionsVisible=!optionsVisible">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content style="overflow-x: hidden">
      <PoolView :optionsVisible="optionsVisible"/>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import PoolView from "./views/PoolView.vue";

@Component({
  components: { PoolView },
  name: "App"
})
export default class App extends Vue {
  optionsVisible = false;
}
</script>
