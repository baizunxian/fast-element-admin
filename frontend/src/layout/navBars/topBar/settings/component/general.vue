<script setup lang="ts">

import {
  getThemeConfig,
  onWartermarkChange,
  onWartermarkTextInput,
  setLocalThemeConfig
} from "/@/layout/navBars/topBar/settings/index";
</script>

<template>

  <el-divider content-position="left">通用</el-divider>

  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">开启水印</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isWartermark" size="small" @change="onWartermarkChange"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt14">
    <div class="layout-breadcrumb-setting-bar-flex-label">水印文案</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-input v-model="getThemeConfig.wartermarkText" size="default" style="width: 90px"
                @input="onWartermarkTextInput($event)"></el-input>
    </div>
  </div>

    <el-divider content-position="left">动画</el-divider>

  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">主页面切换动画</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-select v-model="getThemeConfig.animation"
                 placeholder="请选择" size="default"
                 style="width: 90px"
                 @change="setLocalThemeConfig">
        <el-option label="default" value="default"></el-option>
        <el-option label="slide-right" value="slide-right"></el-option>
        <el-option label="slide-left" value="slide-left"></el-option>
        <el-option label="opacitys" value="opacitys"></el-option>
      </el-select>
    </div>
  </div>

</template>

<style scoped lang="scss">
@import "../index";

</style>