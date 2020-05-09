<template>
  <v-line :config="lineConfig" />
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Konva from "konva";
import { BallType } from "../core/models/PoolState/Ball";
import { Cue } from "../core/models/PoolState/Cue";
import Color from "color";
import { poolData } from "../core/models/PoolData";
@Component({
  name: "CueLine",
  data: () => ({
    BallType
  })
})
export default class CueLine extends Vue {
  @Prop({ type: Object }) cue!: Cue;

  get lineConfig(): Konva.LineConfig {
    return {
      points: [
        this.cue.positionStart.x,
        this.cue.positionStart.y,
        this.cue.positionEnd.x,
        this.cue.positionEnd.y
      ],
      strokeWidth: poolData.cue.width,
      stroke: Color('brown').string()
    };
  }
}
</script>
