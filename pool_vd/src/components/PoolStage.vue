<template>
  <div>
    <pocket-row
      :pocket-left="poolState.pockets[0]"
      :pocket-middle="poolState.pockets[1]"
      :pocket-right="poolState.pockets[2]"
    />
    <v-stage ref="stage" :config="stageConfig">
      <v-fast-layer>
        <v-image :config="backgroundConfig" />
        <v-ellipse
          v-for="(pocket, nth) in pockets"
          :key="nth"
          :config="pocket"
        />
      </v-fast-layer>
      <v-layer>
        <ball v-for="ball in balls" :key="ball.number" :ball="ball" />
        <cue v-for="cue in cues" :key="cue.number" :cue="cue" />
      </v-layer>
    </v-stage>
    <pocket-row
      :pocket-left="poolState.pockets[5]"
      :pocket-middle="poolState.pockets[4]"
      :pocket-right="poolState.pockets[3]"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import { poolData } from "../core/models/PoolData";
import Ball from "./Ball.vue";
import Cue from "./Cue.vue";
import PocketRow from "./PocketRow.vue";
import { PoolState } from "../core/models/PoolState/PoolState";
import Konva from "konva";
import pool from "../assets/pool.svg";
import { Vector2i } from "../core/models/PoolState/Vector2i";
import { PoolOptions } from "../core/models/PoolOptions";
@Component({
  name: "PoolStage",
  components: { Ball, Cue, PocketRow }
})
export default class PoolStage extends Vue {
  @Prop({ type: Object }) poolState!: PoolState;
  @Prop({ type: Object }) poolOptions!: PoolOptions;
  backgroundImage = new Image(100, 100);
  stageWidth = 1920;

  readonly leftCorner: Vector2i = new Vector2i(128, 112);

  get stageHeight() {
    return this.stageWidth * poolData.table.ratio;
  }
  readonly shift = this.leftCorner.add(
    new Vector2i(-poolData.ball.size / 2, -poolData.ball.size / 2)
  );
  readonly intBase = this.leftCorner
    .multiply(-2)
    .add(new Vector2i(this.stageWidth, this.stageHeight));

  get balls() {
    return this.poolState.balls.map(ball => {
      ball.position = this.transformPosition(ball.position.clone());
      return ball;
    });
  }

  get cues() {
    return this.poolState.cues.map(cue => {
      cue.positionStart = this.transformPosition(cue.positionStart.clone());
      cue.positionEnd = this.transformPosition(cue.positionEnd.clone());
      return cue;
    });
  }

  get pockets() {
    return this.poolState.pockets.map(p => {
      const r = new Vector2i(p.catchRadius, p.catchRadius)
        .multiply(this.poolOptions.table.shrink.multiply(this.base))
        .multiply(this.intBase)
        .multiply(new Vector2i(0.5, 1));
      return {
        ...this.transformPosition(p.position),
        fill: "white",
        opacity: 0.1,
        radiusY: r.y,
        radiusX: r.x
      };
    });
  }

  readonly base = new Vector2i(0.01, 0.01);
  transformPosition(v: Vector2i) {
    return v
      .multiply(new Vector2i(0.5, 1))
      .multiply(this.poolOptions.table.shrink.multiply(this.base))
      .add(this.poolOptions.table.shift.multiply(this.base))
      .multiply(this.intBase)
      .add(this.shift);
  }

  get backgroundConfig() {
    return {
      image: this.backgroundImage,
      width: this.stageWidth,
      height: this.stageWidth * poolData.table.ratio
    };
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
    window.removeEventListener("resize", this.fitStageIntoParentContainer);
    window.addEventListener("resize", this.fitStageIntoParentContainer);
  }

  fitStageIntoParentContainer() {
    const stage = this.$refs.stage as Vue & Konva.Stage;
    if (stage) {
      const container = stage.$el as HTMLDivElement;
      const containerWidth = container.offsetWidth;

      const scale = containerWidth / this.stageWidth;

      const stageKonva = stage.getStage();
      stageKonva.width(this.stageWidth * scale);
      stageKonva.height(this.stageHeight * scale);
      stageKonva.scale({ x: scale, y: scale });
      this.redraw();
    }
  }

  redraw() {
    const stage = this.$refs.stage as Vue & Konva.Stage;
    const stageKonva = stage.getStage();
    stageKonva.draw();
  }
}
</script>
