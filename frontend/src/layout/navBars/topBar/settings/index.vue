<template>
  <div class="layout-breadcrumb-setting">
    <el-drawer title="偏好设置" v-model="getThemeConfig.isDrawer" direction="rtl" destroy-on-close size="390px"
               @close="onDrawerClose">
      <template #header>
        <span>偏好设置</span>
      </template>

      <el-scrollbar>
        <div class="layout-breadcrumb-setting-bar p15">
          <el-segmented v-model="segmentedValue" :options="segmentedOptions" block size="default">
            <template #default="{item}">
              <!--            <el-button>{{ item.label }}</el-button>-->
              <span>{{ item.label }}</span>
            </template>
          </el-segmented>
          <!-- 全局主题 -->
          <div class="m4">
            <Appearance v-if="segmentedValue == 'appearance'"></Appearance>
            <Layout v-if="segmentedValue == 'layout'"></Layout>
            <General v-if="segmentedValue == 'general'"></General>
          </div>
        </div>
      </el-scrollbar>

      <template #footer>
        <div class="copy-config">
          <el-button size="default" class="copy-config-btn" type="primary" ref="copyConfigBtnRef"
                     @click="onCopyConfigClick">
            <el-icon class="mr5">
              <ele-CopyDocument/>
            </el-icon>
            一键复制配置
          </el-button>
          <el-button size="default" class="copy-config-btn-reset" type="info" @click="onResetConfigClick">
            <el-icon class="mr5">
              <ele-RefreshRight/>
            </el-icon>
            一键恢复默认
          </el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import {nextTick, onMounted, onUnmounted, reactive, ref} from 'vue';
import {Local} from '/@/utils/storage';
import other from '/@/utils/other';
import mittBus from '/@/utils/mitt';
import Appearance from "./component/appearance.vue";
import Layout from "./component/layout.vue";
import General from "./component/general.vue";
import {
  getThemeConfig,
  initLayoutChangeFun,
  initSetStyle,
  onAddDarkChange,
  onAddFilterChange,
  onColorPickerChange,
  onCopyConfigClick,
  onDrawerClose,
  onResetConfigClick,
  onWartermarkChange
} from "/@/layout/navBars/topBar/settings/index";

defineOptions({name: "layoutBreadcrumbSetting"})

// 定义变量内容
const state = reactive({
  isMobile: false,
});

const segmentedValue = ref("appearance")
const segmentedOptions = [
  {label: '外观', value: 'appearance'},
  {label: '布局', value: 'layout'},
  {label: '通用', value: 'general'},
]

onMounted(() => {
  nextTick(() => {
    // 判断当前布局是否不相同，不相同则初始化当前布局的样式，防止监听窗口大小改变时，布局配置logo、菜单背景等部分布局失效问题
    if (!Local.get('frequency')) initLayoutChangeFun();
    Local.set('frequency', 1);
    // 监听窗口大小改变，非默认布局，设置成默认布局（适配移动端）
    mittBus.on('layoutMobileResize', (res) => {
      getThemeConfig.value.layout = res.layout;
      getThemeConfig.value.isDrawer = false;
      initLayoutChangeFun();
      state.isMobile = other.isMobile();
    });
    setTimeout(() => {
      // 默认样式
      onColorPickerChange();
      // 灰色模式
      if (getThemeConfig.value.isGrayscale) onAddFilterChange('grayscale');
      // 色弱模式
      if (getThemeConfig.value.isInvert) onAddFilterChange('invert');
      // 深色模式
      if (getThemeConfig.value.isIsDark) onAddDarkChange('dark');
      // 开启水印
      onWartermarkChange();
      // 初始化菜单样式等
      initSetStyle();
    }, 10);
  });
});
onUnmounted(() => {
  mittBus.off('layoutMobileResize', () => {
  });
});


const openDrawer = () => {
  getThemeConfig.value.isDrawer = true;
};
// 暴露变量
defineExpose({
  openDrawer,
});
</script>

<style lang="scss" scoped>
@import "./index";

</style>
