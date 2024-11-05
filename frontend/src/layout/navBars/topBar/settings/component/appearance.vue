<script setup lang="ts">
import {getHexColor} from "/@/utils/theme";
import {getThemeConfig, onAddDarkChange, onAddFilterChange, onColorPickerChange} from "../index";
import {computed} from "vue";
import {MoonStar, Sun, SunMoon} from "/@/icons"


defineOptions({name: 'appearance'})


const BUILT_IN_THEME_PRESETS = [
  {
    color: '#409eff',
    type: 'default',
    name: "默认"
  },
  {
    color: 'hsl(245 82% 67%)',
    type: 'violet',
    name: "紫罗兰"
  },
  {
    color: 'hsl(347 77% 60%)',
    type: 'pink',
    name: "樱花粉"
  },
  {
    color: 'hsl(42 84% 61%)',
    type: 'yellow',
    name: '柠檬黄',
  },
  {
    color: 'hsl(231 98% 65%)',
    type: 'sky-blue',
    name: '天蓝色',
  },
  {
    color: 'hsl(161 90% 43%)',
    type: 'green',
    name: '浅绿色',
  },
  {
    color: 'hsl(240 5% 26%)',
    darkPrimaryColor: 'hsl(0 0% 98%)',
    primaryColor: 'hsl(240 5.9% 10%)',
    type: 'zinc',
    name: '锌色灰',
  },

  {
    color: 'hsl(181 84% 32%)',
    type: 'deep-green',
    name: '深绿色',
  },

  {
    color: 'hsl(211 91% 39%)',
    type: 'deep-blue',
    name: '深蓝色',
  },
  {
    color: 'hsl(18 89% 40%)',
    type: 'orange',
    name: '橙黄色',
  },
  {
    color: 'hsl(0 75% 42%)',
    type: 'rose',
    name: '玫瑰红',
  },

  {
    color: 'hsl(0 0% 25%)',
    darkPrimaryColor: 'hsl(0 0% 98%)',
    primaryColor: 'hsl(240 5.9% 10%)',
    type: 'neutral',
    name: '中性色',
  },
  {
    color: 'hsl(215 25% 27%)',
    darkPrimaryColor: 'hsl(0 0% 98%)',
    primaryColor: 'hsl(240 5.9% 10%)',
    type: 'slate',
    name: '石板灰',
  },
  {
    color: 'hsl(217 19% 27%)',
    darkPrimaryColor: 'hsl(0 0% 98%)',
    primaryColor: 'hsl(240 5.9% 10%)',
    type: 'gray',
    name: '中灰色',
  },
  {
    color: '',
    type: 'custom',
  },
];

const isIsDark = computed(() => {
  return getThemeConfig.value.isIsDark;
})


</script>

<template>
  <div class="">

    <el-divider content-position="left"><h3>主题</h3></el-divider>

    <div class="layout-setting-appearance">
      <div class="layout-setting-appearance-item " @click="onAddDarkChange('light')">
        <div class="layout-setting-appearance-item-value outline-box"
             :class="!isIsDark ? 'outline-box-active' :'' ">
          <Sun class="mr36 ml36"></Sun>
        </div>
        <div class="layout-setting-appearance-item-label">浅色</div>
      </div>

      <div class="layout-setting-appearance-item " @click="onAddDarkChange('dark')">
        <div class="layout-setting-appearance-item-value outline-box"
             :class="isIsDark ? 'outline-box-active' :'' ">
          <MoonStar class="mr36 ml36"></MoonStar>
        </div>
        <div class="layout-setting-appearance-item-label">深色</div>
      </div>

      <div class="layout-setting-appearance-item is-disabled">
        <div class="layout-setting-appearance-item-value outline-box">
          <SunMoon class="mr36 ml36"></SunMoon>
        </div>
        <div class="layout-setting-appearance-item-label">跟随系统</div>
      </div>
    </div>

    <el-divider content-position="left"><h3>内置主题</h3></el-divider>

    <div class="layout-setting-appearance">
      <div class="layout-setting-appearance-item"
           v-for="theme in BUILT_IN_THEME_PRESETS"
           :key="theme.type"
           @click="onColorPickerChange(theme.color)">
        <div class="layout-setting-appearance-item-value outline-box p4"
             :class="theme.color && getHexColor(theme.color) == getThemeConfig.primary ? 'outline-box-active' :'' ">
          <div :style="{backgroundColor: theme.color}" style="width: 20px; height: 20px; margin: 8px 40px">

          </div>
        </div>
        <div class="layout-setting-appearance-item-label mb8">{{ theme.name }}</div>
      </div>
    </div>

    <el-divider content-position="left"><h3>其他</h3></el-divider>
    <div class="flex justify-space-between mt15">
      <div class="layout-breadcrumb-setting-bar-flex-label">灰色模式</div>
      <div class="flex">
        <el-switch v-model="getThemeConfig.isGrayscale" size="small"
                   @change="onAddFilterChange('grayscale')"></el-switch>
      </div>
    </div>
    <div class="flex justify-space-between mt15">
      <div class="layout-breadcrumb-setting-bar-flex-label">色弱模式</div>
      <div class="flex">
        <el-switch v-model="getThemeConfig.isInvert" size="small"
                   @change="onAddFilterChange('invert')"></el-switch>
      </div>
    </div>
  </div>

</template>

<style scoped lang="scss">
@import "../index";

.layout-setting-appearance {
  //outline: auto !important;
  //outline: 1px solid black !important;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  width: 100%;


  .layout-setting-appearance-item {
    display: flex;
    cursor: pointer;
    flex-direction: column;

    .layout-setting-appearance-item-value {
      align-items: center;
      display: flex;
      justify-content: center;
      padding: 16px 4px;
      color: var(--el-text-color-primary);
    }

    .layout-setting-appearance-item-label {
      color: #71717a;
      color: var(--el-text-color-primary);
      text-align: center;
      margin-top: 8px;
    }
  }

}

</style>