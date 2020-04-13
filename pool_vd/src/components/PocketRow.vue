<template>
  <v-stage ref="stage" :config="stageConfig">
    <v-layer>
      <ball v-for="(ball, nth) in [...pocketLeftBalls, ...pocketRightBalls, ...pocketMiddleBalls]" :key="nth" :ball="ball" />
    </v-layer>
  </v-stage>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import Ball from "./Ball.vue";
import Konva from "konva";
import { Pocket } from "../core/models/Deduction/Pocket";
import { BallType } from "../core/models/PoolState/Ball";
import { poolData } from "../core/models/PoolData";
import { Vector2i } from "../core/models/PoolState/Vector2i";
@Component({
  name: "PoolStage",
  components: { Ball }
})
export default class PocketRow extends Vue {
  @Prop({ type: Object }) pocketLeft!: Pocket;
  @Prop({ type: Object }) pocketMiddle!: Pocket;
  @Prop({ type: Object }) pocketRight!: Pocket;

  stageWidth = 1920;
  stageHeight = 120;
  readonly margin = 10;
  readonly rowHeight = poolData.ball.size + this.margin;
  readonly ballShift = poolData.ball.size + this.margin;

  get stageConfig() {
    return {
      width: this.stageWidth,
      height: this.stageHeight
    };
  }

  getStriped(pocket: Pocket) {
    return pocket.balls.filter(ball => ball.type === BallType.STRIPED);
  }

  getSolid(pocket: Pocket) {
    return pocket.balls.filter(ball => ball.type === BallType.SOLID);
  }

  mounted() {
    this.fitStageIntoParentContainer();
    window.addEventListener("resize", this.fitStageIntoParentContainer);
  }

  get pocketLeftBalls() {
    const striped = this.getStriped(this.pocketLeft);
    const solid = this.getSolid(this.pocketLeft);
    striped.forEach((ball, i) => {
      ball.position = new Vector2i(i * this.ballShift, 0);
    });

    solid.forEach((ball, i) => {
      ball.position = new Vector2i(i * this.ballShift, this.rowHeight);
    });

    return [...solid, ...striped];
  }

  get pocketRightBalls() {
    const striped = this.getStriped(this.pocketRight);
    const solid = this.getSolid(this.pocketRight);
    striped.forEach((ball, i) => {
      ball.position = new Vector2i(
        this.stageWidth - poolData.ball.size - i * this.ballShift,
        0
      );
    });

    solid.forEach((ball, i) => {
      ball.position = new Vector2i(
        this.stageWidth - poolData.ball.size - i * this.ballShift,
        this.rowHeight
      );
    });

    return [...solid, ...striped];
  }

  get pocketMiddleBalls() {
    const striped = this.getStriped(this.pocketMiddle);
    const solid = this.getSolid(this.pocketMiddle);
    striped.forEach((ball, i) => {
      ball.position = new Vector2i(
         this.stageWidth / 2 -
          poolData.ball.size -
          i * this.ballShift +
          (striped.length * this.ballShift) / 2 -
          this.margin,
        0
      );
    });
    solid.forEach((ball, i) => {
      ball.position = new Vector2i(
        this.stageWidth / 2 -
          poolData.ball.size -
          i * this.ballShift +
          (solid.length * this.ballShift) / 2 -
          this.margin,
        this.rowHeight
      );
    });

    return [...solid, ...striped];
  }

  fitStageIntoParentContainer() {
    const stage = this.$refs.stage as Vue & Konva.Stage;
    const container = stage.$el as HTMLDivElement;
    const containerWidth = container.offsetWidth;

    const scale = containerWidth / this.stageWidth;

    const stageKonva = stage.getStage();
    stageKonva.width(this.stageWidth * scale);
    stageKonva.height(this.stageHeight * scale);
    stageKonva.scale({ x: scale, y: scale });
    this.redraw();
  }

  redraw() {
    const stage = this.$refs.stage as Vue & Konva.Stage;
    const stageKonva = stage.getStage();
    stageKonva.draw();
  }
}
</script>
