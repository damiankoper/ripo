<template>
  <v-container>
    <pool-stage :poolState="deducedPoolState" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import PoolStage from "../components/PoolStage.vue";
import { PoolDeductionCore } from "../core/PoolDeductionCore";
import { PoolState, IPoolState } from "../core/models/PoolState/PoolState";

import { poolState } from "../../tests/testData/PoolState";
import { Socket } from "vue-socket.io-extended";
@Component({
  name: "PoolView",
  components: {
    PoolStage
  }
})
export default class PoolView extends Vue {
  poolDeductionCore: PoolDeductionCore = new PoolDeductionCore();
  deducedPoolState: PoolState = poolState;

  @Socket("poolState")
  onPoolState(poolState: IPoolState) {
    this.poolDeductionCore.addPoolState(new PoolState(poolState));
    this.deducedPoolState = this.poolDeductionCore.getDeductedPoolState();
  }
}
</script>
