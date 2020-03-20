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
    </v-app-bar>

    <v-content>
      <PoolView />
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
export default class App extends Vue {}
</script>
