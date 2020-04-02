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
        <pool-options> </pool-options>
      </div>
    </v-navigation-drawer>
    <pool-stage :poolState="deducedPoolState" />
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
@Component({
  name: "PoolView",
  components: {
    PoolStage,
    PoolOptions: PoolOptionsVue
  }
})
export default class PoolView extends Vue {
  poolDeductionCore: PoolDeductionCore = new PoolDeductionCore();
  deducedPoolState: PoolState = poolState;

  @PropSync("optionsVisible", { type: Boolean })
  syncedOptionsVisible!: boolean;

  @Socket("poolState")
  onPoolState(poolState: IPoolState) {
    this.poolDeductionCore.addPoolState(new PoolState(poolState));
    this.deducedPoolState = this.poolDeductionCore.getDeductedPoolState();
  }
}
</script>
