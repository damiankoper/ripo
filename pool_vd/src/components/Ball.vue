<template>
  <v-group :config="groupConfig">
    <v-rect :config="mainRect" />
    <template v-if="ball.type == BallType.STRIPED">
      <v-rect :config="stripeUpper" />
      <v-rect :config="stripeLower" />
    </template>
    <v-circle :config="circle" />
    <v-text :config="text" />
  </v-group>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { poolData } from "../core/models/PoolData";
import Konva from "konva";
import { Ball } from "../core/models/PoolState/Ball";
import { BallType } from "../core/models/PoolState/Ball";
@Component({
  name: "BallCircle",
  data: () => ({
    BallType
  })
})
export default class BallCircle extends Vue {
  @Prop({ type: Object }) ball!: Ball;

  get text(): Konva.TextConfig {
    const radius = poolData.ball.size * poolData.ball.textSize;
    return {
      text: String(this.ball.number),
      y:
        poolData.ball.size / 2 -
        radius +
        poolData.ball.size * poolData.ball.textSize * 0.4,
      width: poolData.ball.size,
      fontSize: poolData.ball.size * poolData.ball.textSize * 1.45,
      align: "center",
      fontStyle: "bold"
    };
  }

  get circle(): Konva.CircleConfig {
    return {
      x: poolData.ball.size / 2,
      y: poolData.ball.size / 2,
      radius: poolData.ball.size * poolData.ball.textSize,
      fill: "white"
    };
  }

  get groupConfig() {
    return {
      clipFunc(ctx: CanvasRenderingContext2D) {
        const radius = poolData.ball.size / 2;
        ctx.arc(radius, radius, radius, 0, Math.PI * 2, false);
      },
      ...this.ball.position
    };
  }

  get stripeUpper() {
    return {
      fill: "white",
      width: poolData.ball.size,
      height: poolData.ball.size * poolData.ball.stripeSize
    };
  }

  get stripeLower() {
    return {
      fill: "white",
      y: poolData.ball.size - poolData.ball.size * poolData.ball.stripeSize,
      width: poolData.ball.size,
      height: poolData.ball.size * poolData.ball.stripeSize
    };
  }

  get mainRect(): Konva.RectConfig {
    return {
      fill: poolData.balls[this.ball.number].color,
      width: poolData.ball.size,
      height: poolData.ball.size
    };
  }
}
</script>
