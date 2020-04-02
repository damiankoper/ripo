<template>
  <v-container>
    <h1>Options</h1>
    <v-form>
        <span class="pr-4">Pool color:</span>
        <color-popover class="mr-2" v-model="poolOptions.table.color.from">
          From
        </color-popover>
        <color-popover class="mr-2" v-model="poolOptions.table.color.to">
          To
        </color-popover>
    </v-form>
  </v-container>
</template>

<script>
import Component from "vue-class-component";
import ColorPopover from "./form/ColorPopover.vue";
import { PoolOptions } from "../core/models/PoolOptions.ts";
import Vue from "vue";
@Component({
  name: "PoolOptions",
  components: {
    ColorPopover
  }
})
export default class PoolOptionsVue extends Vue {
  poolOptions = new PoolOptions();
}
</script>

<style></style>
