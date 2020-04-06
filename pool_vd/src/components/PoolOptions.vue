<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Pool options
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <span class="pr-4">Color:</span>
                <color-popover
                  v-model="poolOptions.table.color.from"
                  class="mr-2"
                >
                  From
                </color-popover>
                <color-popover
                  v-model="poolOptions.table.color.to"
                  class="mr-2"
                >
                  To
                </color-popover>
              </v-col>
            </v-row>
            <v-row>
              <v-col :cols="4">
                <v-text-field
                  v-model="poolOptions.table.shift.x"
                  label="Horizontal shift [X]"
                  type="number"
                  suffix="%"
                  min="-100"
                  max="100"
                  step="0.1"
                  class="input-right"
                ></v-text-field>
              </v-col>
              <v-col :cols="4">
                <v-text-field
                  v-model="poolOptions.table.shift.y"
                  label="Vertical shift [Y]"
                  type="number"
                  suffix="%"
                  min="-100"
                  max="100"
                  step="0.1"
                  class="input-right"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col :cols="4">
                <v-text-field
                  v-model="poolOptions.table.shrink.x"
                  label="Horizontal shrink [X]"
                  type="number"
                  suffix="%"
                  min="-100"
                  max="100"
                  step="0.1"
                  class="input-right"
                ></v-text-field>
              </v-col>
              <v-col :cols="4">
                <v-text-field
                  v-model="poolOptions.table.shrink.y"
                  label="Vertical shrink [Y]"
                  type="number"
                  suffix="%"
                  min="-100"
                  max="100"
                  step="0.1"
                  class="input-right"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            Init options
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="poolOptions.init.duration"
                      label="Duration [frames]"
                      type="number"
                      @input="sendInitPeriod"
                    ></v-text-field>
                  </v-col>
                  <v-col>
                    <v-btn block color="primary" @click="sendRerunInitRequest">
                      Re-run init
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Component from "vue-class-component";
import ColorPopover from "./form/ColorPopover.vue";
import { PoolOptions } from "../core/models/PoolOptions";
import Vue from "vue";
import { Socket } from "vue-socket.io-extended";
import { Watch, Model } from "vue-property-decorator";
@Component({
  name: "PoolOptions",
  components: {
    ColorPopover
  }
})
export default class PoolOptionsVue extends Vue {
  @Model() poolOptions!: PoolOptions;

  @Socket()
  connect() {
    console.log("Connection established. Sending config.");
    this.sendPoolColors();
    this.sendInitPeriod();
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

  @Watch("poolOptions.table.color", { deep: true })
  onColorChange() {
    this.sendPoolColors();
  }
}
</script>

<style lang="scss">
.input-right input {
  text-align: right;
}
</style>
