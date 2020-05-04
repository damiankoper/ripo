<template>
  <v-container>
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
                  min="0"
                  max="200"
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
                  min="0"
                  max="200"
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
            Ball options
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <v-row>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="poolOptions.ball.radiusLower"
                      label="Lower radius"
                      type="number"
                      suffix="px"
                      min="0"
                      max="100"
                      step="1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="poolOptions.ball.radiusUpper"
                      label="Upper radius"
                      type="number"
                      suffix="px"
                      min="0"
                      max="100"
                      step="1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="4">
                    <v-text-field
                      v-model="poolOptions.ball.threshold"
                      label="Cut threshold"
                      type="number"
                      min="0"
                      max="100"
                      step="1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-row>
                  <v-col :cols="3">
                    <v-text-field
                      v-model="poolOptions.ball.dp"
                      label="Acc. inv. ratio"
                      type="number"
                      min="1"
                      max="10"
                      step="1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="3">
                    <v-text-field
                      v-model="poolOptions.ball.minDist"
                      label="Min distance"
                      type="number"
                      suffix="px"
                      min="1"
                      max="100"
                      step="1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="3">
                    <v-text-field
                      v-model="poolOptions.ball.param1"
                      label="Hough P1"
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="3">
                    <v-text-field
                      v-model="poolOptions.ball.param2"
                      label="Hough P2"
                      type="number"
                      min="0"
                      max="100"
                      step="0.1"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                </v-row>
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
            Deduction options
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col>
                <v-row>
                  <v-col :cols="6">
                    <v-text-field
                      v-model="poolOptions.deduction.precision.historyStates"
                      label="History [states]"
                      type="number"
                      min="0"
                      max="100"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="6">
                    <v-btn block color="primary" @click="$emit('clearPockets')">
                      Clear pockets
                    </v-btn>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col :cols="6">
                    <v-text-field
                      v-model="poolOptions.deduction.precision.inPocketStates"
                      label="In pocket [states]"
                      type="number"
                      min="0"
                      max="100"
                      class="input-right"
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="6">
                    <v-text-field
                      v-model="poolOptions.deduction.precision.velocityStates"
                      label="Velocity analysis [states]"
                      type="number"
                      min="0"
                      max="100"
                      class="input-right"
                    ></v-text-field>
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
  async connect() {
    console.log("Connection established. Sending config.");
    this.sendPoolColors();
    this.sendInitPeriod();
    await new Promise(r => setTimeout(r, 500));
    this.sendBallLowerRadius();
    this.sendBallUpperRadius();
    await new Promise(r => setTimeout(r, 500));
    this.sendBallThreshold();
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

  sendBallLowerRadius() {
    this.$socket.client.emit(
      "ballLowerRadiusChange",
      this.poolOptions.ball.radiusLower
    );
  }

  sendBallUpperRadius() {
    this.$socket.client.emit(
      "ballUpperRadiusChange",
      this.poolOptions.ball.radiusUpper
    );
  }

  sendBallThreshold() {
    this.$socket.client.emit(
      "ballThresholdChange",
      this.poolOptions.ball.threshold
    );
  }

  sendBallDP() {
    this.$socket.client.emit("balldpChange", this.poolOptions.ball.dp);
  }

  sendBallMinDist() {
    this.$socket.client.emit(
      "ballMinDistChange",
      this.poolOptions.ball.minDist
    );
  }

  sendBallParam1() {
    this.$socket.client.emit("ballParam1Change", this.poolOptions.ball.param1);
  }

  sendBallParam2() {
    this.$socket.client.emit("ballParam2Change", this.poolOptions.ball.param2);
  }

  @Watch("poolOptions.table.color", { deep: true })
  onColorChange() {
    this.sendPoolColors();
  }

  @Watch("poolOptions.ball.radiusLower")
  onBallLowerRadiusChange() {
    this.sendBallLowerRadius();
  }

  @Watch("poolOptions.ball.radiusUpper")
  onBallUpperRadiusChange() {
    this.sendBallUpperRadius();
  }

  @Watch("poolOptions.ball.threshold")
  onBallThresholdChange() {
    this.sendBallThreshold();
  }

  @Watch("poolOptions.ball.dp")
  onBallDPChange() {
    this.sendBallDP();
  }

  @Watch("poolOptions.ball.minDist")
  onBallMinDistChange() {
    this.sendBallMinDist();
  }

  @Watch("poolOptions.ball.param1")
  onBallParam1Change() {
    this.sendBallParam1();
  }

  @Watch("poolOptions.ball.param2")
  onBallParam2Change() {
    this.sendBallParam2();
  }
}
</script>

<style lang="scss">
.input-right input {
  text-align: right;
}
</style>
