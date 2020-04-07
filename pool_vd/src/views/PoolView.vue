<template>
  <v-container>
    <v-navigation-drawer
      v-model="syncedOptionsVisible"
      absolute
      right
      temporary
      :width="512"
    >
      <div>
        <pool-options v-model="poolOptions" />
      </div>
    </v-navigation-drawer>
    <pool-stage :pool-state="finalPoolState" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, PropSync } from "vue-property-decorator";
import PoolStage from "../components/PoolStage.vue";
import PoolOptionsVue from "../components/PoolOptions.vue";
import { PoolDeductionCore } from "../core/PoolDeductionCore";
import { PoolState, IPoolState } from "../core/models/PoolState/PoolState";
import { poolState } from "../../tests/testData/PoolState";
import { Socket } from "vue-socket.io-extended";
import { PoolOptions } from "../core/models/PoolOptions";
import { Vector2i } from "../core/models/PoolState/Vector2i";
import _ from "lodash";
@Component({
  name: "PoolView",
  components: {
    PoolStage,
    PoolOptions: PoolOptionsVue
  }
})
export default class PoolView extends Vue {
  poolDeductionCore: PoolDeductionCore = new PoolDeductionCore();

  poolOptions: PoolOptions = new PoolOptions();
  deducedPoolState: PoolState = new PoolState(poolState);

  get finalPoolState() {
    const base = new Vector2i(0.01, 0.01);
    const finalState = _.cloneDeep(this.deducedPoolState);
    finalState.balls.forEach(b => {
      b.position = b.position.multiply(
        this.poolOptions.table.shrink.multiply(base)
      );
      b.position = b.position.add(this.poolOptions.table.shift.multiply(base));
    });
    finalState.cues.forEach(c => {
      c.positionStart = c.positionStart.multiply(
        this.poolOptions.table.shrink.multiply(base)
      );
      c.positionStart = c.positionStart.add(
        this.poolOptions.table.shift.multiply(base)
      );

      c.positionEnd = c.positionEnd.multiply(
        this.poolOptions.table.shrink.multiply(base)
      );
      c.positionEnd = c.positionEnd.add(
        this.poolOptions.table.shift.multiply(base)
      );
    });
    return finalState;
  }

  beforeMount() {
    this.onPoolState(poolState);
  }

  @PropSync("optionsVisible", { type: Boolean })
  syncedOptionsVisible!: boolean;

  @Socket("poolState")
  onPoolState(poolState: IPoolState) {
    this.poolDeductionCore.addPoolState(new PoolState(poolState));
    this.deducedPoolState = this.poolDeductionCore.getDeductedPoolState();
  }
}
</script>
