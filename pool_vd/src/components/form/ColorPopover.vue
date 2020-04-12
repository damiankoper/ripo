<template>
  <span>
    <v-menu v-model="menu" :close-on-content-click="false" :nudge-width="200">
      <template v-slot:activator="{ on }">
        <v-btn :color="valueHex" :dark="isDark" v-on="on">
          <slot />
        </v-btn>
      </template>
      <v-card>
        <v-color-picker
          :value="value.hsva"
          class="ma-2"
          canvas-height="300"
          mode="hsla"
          flat
          @update:color="colorInput"
        ></v-color-picker>
      </v-card>
    </v-menu>
  </span>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import { Model } from "vue-property-decorator";
import Color from "color";
import { HSVA } from "../../core/models/PoolOptions";
@Component({
  name: "ColorPopover"
})
export default class ColorPopover extends Vue {
  @Model() readonly value!: { hsva: HSVA };
  menu = false;

  colorInput(v: { hsva: { h: number; s: number; v: number; a: number } }) {
    this.value.hsva = v.hsva;
  }

  get isDark() {
    const c = this.value.hsva;
    return Color.hsv([c.h, c.s * 100, c.v * 100]).isDark();
  }

  get valueHex() {
    const c = this.value.hsva;
    return Color.hsv([c.h, c.s * 100, c.v * 100]).hex();
  }
}
</script>

<style></style>
