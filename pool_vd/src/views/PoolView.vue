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
        <pool-options
          v-model="poolOptions"
          @clearPockets="poolDeductionCore.clearPockets()"
        />
      </div>
    </v-navigation-drawer>
    <pool-stage :pool-state="deducedPoolState" :pool-options="poolOptions" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, PropSync, Watch } from "vue-property-decorator";
import PoolStage from "../components/PoolStage.vue";
import PoolOptionsVue from "../components/PoolOptions.vue";
import { PoolDeductionCore } from "../core/PoolDeductionCore";
import { PoolState, IPoolState } from "../core/models/PoolState/PoolState";
import { poolState } from "../../tests/testData/PoolState";
import { Socket } from "vue-socket.io-extended";
import { PoolOptions } from "../core/models/PoolOptions";
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

  beforeMount() {
    this.onPoolState(poolState);
    poolState.pockets.forEach((pocket, i) => {
      this.deducedPoolState.pockets[i].balls = pocket.balls;
    });
  }

  @PropSync("optionsVisible", { type: Boolean })
  syncedOptionsVisible!: boolean;

  @Socket("poolState")
  onPoolState(poolStateReceived: IPoolState) {
    const poolState = new PoolState(poolStateReceived);
    this.poolDeductionCore.addPoolState(poolState);
    this.deducedPoolState = this.poolDeductionCore.getDeductedPoolState();
  }

  @Socket("connect")
  onConnect() {
    this.poolDeductionCore.clearPoolStates();
  }

  @Watch("poolOptions.deduction.precision", { deep: true, immediate: true })
  onPrecisionChange(v: {
    historyStates: number;
    inPocketStates: number;
    velocityStates: number;
  }) {
    this.poolDeductionCore.precision = v;
  }
}
</script>
