<template>
  <div>
    <v-stage ref="stage" :config="stageConfig">
      <v-fast-layer>
        <v-image :config="backgroundConfig" />
      </v-fast-layer>
      <v-layer>
        <ball v-for="ball in balls" :key="ball.number" :ball="ball" />
      </v-layer>
    </v-stage>
    {{ balls }}
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { poolData } from "../core/models/PoolData";
import Ball from "./Ball.vue";
import { PoolState } from "../core/models/PoolState/PoolState";
import Konva from "konva";
import pool from "../assets/pool.svg";
import { Vector2i } from "../core/models/PoolState/Vector2i";
import _ from "lodash";
@Component({
  name: "PoolStage",
  components: { Ball }
})
export default class PoolStage extends Vue {
  @Prop({ type: Object }) poolState!: PoolState;

  backgroundImage = new Image(100, 100);
  stageWidth = 1920;

  readonly leftCorner: Vector2i = {
    x: 128,
    y: 112
  };
  get balls() {
    return this.poolState.balls.map(ball => {
      ball = _.cloneDeep(ball);
      const shift = {
        x: -poolData.ball.size / 2 + this.leftCorner.x,
        y: -poolData.ball.size / 2 + this.leftCorner.y
      };

      const intBase = {
        x: this.stageWidth - 2 * this.leftCorner.x,
        y: this.stageHeight - 2 * this.leftCorner.y
      };
      console.log(shift, intBase);

      ball.position.x = ball.position.x * intBase.x + shift.x;
      ball.position.y = ball.position.y * intBase.y + shift.y;
      return ball;
    });
  }

  get backgroundConfig() {
    return {
      image: this.backgroundImage,
      width: this.stageWidth,
      height: this.stageWidth * poolData.table.ratio
    };
  }

  get stageHeight() {
    return this.stageWidth * poolData.table.ratio;
  }

  get stageConfig() {
    return {
      width: this.stageWidth,
      height: this.stageHeight
    };
  }
  beforeMount() {
    this.backgroundImage.onload = this.redraw;
    this.backgroundImage.src = pool;
  }
  mounted() {
    this.fitStageIntoParentContainer();
    window.addEventListener("resize", this.fitStageIntoParentContainer);
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
