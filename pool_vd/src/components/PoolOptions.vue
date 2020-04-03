<template>
  <v-container>
    <h1>Options</h1>
    <v-form>
      <v-row>
        <v-col>
          <v-row>
            <v-col>
              <h3>Pool</h3>
            </v-col>
          </v-row>
          <span class="pr-4">Color:</span>
          <color-popover class="mr-2" v-model="poolOptions.table.color.from">
            From
          </color-popover>
          <color-popover class="mr-2" v-model="poolOptions.table.color.to">
            To
          </color-popover>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <h3>Init period</h3>

          <v-row>
            <v-col>
              <v-text-field
                v-model="poolOptions.init.duration"
                label="Duration [s]"
                type="number"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-btn @click="sendRerunInitRequest">
                Re-run init
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import Component from "vue-class-component";
import ColorPopover from "./form/ColorPopover.vue";
import { PoolOptions } from "../core/models/PoolOptions";
import Vue from "vue";
import { Socket } from "vue-socket.io-extended";
@Component({
  name: "PoolOptions",
  components: {
    ColorPopover
  }
})
export default class PoolOptionsVue extends Vue {
  poolOptions: PoolOptions = new PoolOptions();

  @Socket()
  connect() {
    console.log("Connection established. Sending config.");
    this.sendPoolColors();
    this.sendInitPeriod();
    this.sendRerunInitRequest();
  }

  sendPoolColors() {
    const colors = [
      this.poolOptions.hsvaColor2Cv(this.poolOptions.table.color.from.hsva),
      this.poolOptions.hsvaColor2Cv(this.poolOptions.table.color.to.hsva)
    ];
    this.$socket.client.emit("poolColorsChange", colors);
  }

  sendInitPeriod() {
    this.$socket.client.emit(
      "initDurationChange",
      this.poolOptions.init.duration
    );
  }

  sendRerunInitRequest() {
    this.$socket.client.emit("rerunInitRequest");
  }
}
</script>

<style></style>
