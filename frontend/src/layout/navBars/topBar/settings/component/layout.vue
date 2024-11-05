<script setup lang="ts">
import {
  getThemeConfig,
  onBgColorPickerChange,
  onColumnsMenuBarGradualChange,
  onColumnsMenuHoverPreloadChange,
  onIsBreadcrumbChange,
  onIsFixedHeaderChange,
  onIsShowLogoChange,
  onMenuBarGradualChange,
  onSetLayout,
  onShareTagsViewChange,
  onSortableTagsViewChange,
  onThemeConfigChange,
  onTopBarGradualChange,
  setLocalThemeConfig
} from "../index";
import {type Component, computed, ref} from "vue";
import {
  FullContent,
  HeaderNav,
  MixedNav,
  SidebarMixedNav,
  SidebarNav
} from "/@/layout/navBars/topBar/settings/component/icons";

interface PresetItem {
  name: string;
  tip: string;
  type: string;
  layout: string;
}


const components: Record<string, Component> = {
  'full-content': FullContent,
  'header-nav': HeaderNav,
  'mixed-nav': MixedNav,
  'sidebar-mixed-nav': SidebarMixedNav,
  'sidebar-nav': SidebarNav,
};

const PRESET = computed((): PresetItem[] => [
  {
    name: "垂直",
    tip: "侧边垂直菜单模式",
    type: 'sidebar-nav',
    layout: 'defaults'
  },
  {
    name: "双列菜单",
    tip: "垂直双列菜单模式",
    type: 'sidebar-mixed-nav',
    layout: 'columns'
  },
  {
    name: "水平",
    tip: "水平菜单模式，菜单全部显示在顶部",
    type: 'header-nav',
    layout: 'transverse'
  },
  // {
  //   name: "混合菜单",
  //   tip: "垂直水平菜单共存",
  //   type: 'mixed-nav',
  //   layout: "transverse"
  // },
  // {
  //   name: "内容全屏",
  //   tip: "不显示任何菜单，只显示内容主体",
  //   type: 'full-content',
  // },
]);

const isMobile = ref(false)

function activeClass(theme: string): string[] {
  return theme === getThemeConfig.value.layout ? ['outline-box-active'] : [];
}
</script>

<template>
  <el-divider content-position="left">布局</el-divider>
  <div class="flex w100" style="flex-width: wrap; gap: 1.25rem;">
    <template v-for="theme in PRESET" :key="theme.name">
      <div
          class="flex cursor-pointer"
          style="flex-direction: column; cursor: pointer; flex-wrap: wrap;"
          @click="onSetLayout(theme.layout)"
      >
        <div class="outline-box" :class="activeClass(theme.layout)" style="
    width: 100px;
        align-items: center;
    display: flex;
    justify-content: center;">
          <component :is="components[theme.type]"/>
        </div>
        <div
            class="layout-breadcrumb-setting-bar-flex-label text-muted-foreground flex-center hover:text-foreground mt8 text-center text-xs"
            style="
            text-align: center;
 align-items: center;
    display: flex;
    justify-content: center;"
        >
          {{ theme.name }}
        </div>
      </div>
    </template>
  </div>


  <!-- 顶栏设置 -->
  <el-divider content-position="left">顶栏</el-divider>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">固定顶栏</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isFixedHeader" size="small"
                 @change="onIsFixedHeaderChange"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex">
    <div class="layout-breadcrumb-setting-bar-flex-label">顶栏背景</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-color-picker v-model="getThemeConfig.topBar" size="default"
                       @change="onBgColorPickerChange('topBar')"></el-color-picker>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex">
    <div class="layout-breadcrumb-setting-bar-flex-label">顶栏默认字体颜色</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-color-picker v-model="getThemeConfig.topBarColor" size="default"
                       @change="onBgColorPickerChange('topBarColor')"></el-color-picker>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt10">
    <div class="layout-breadcrumb-setting-bar-flex-label">顶栏背景渐变</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isTopBarColorGradual" size="small"
                 @change="onTopBarGradualChange"></el-switch>
    </div>
  </div>


  <!-- 侧边栏设置 -->
  <el-divider content-position="left">侧边栏</el-divider>

  <div class="layout-breadcrumb-setting-bar-flex mt15"
       :style="{ opacity: getThemeConfig.layout === 'transverse' ? 0.5 : 1 }">
    <div class="layout-breadcrumb-setting-bar-flex-label">折叠侧边栏</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch
          v-model="getThemeConfig.isCollapse"
          :disabled="getThemeConfig.layout === 'transverse'"
          size="small"
          @change="onThemeConfigChange"
      ></el-switch>
    </div>
  </div>

  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边栏 Logo</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isShowLogo" size="small" @change="onIsShowLogoChange"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边背景</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-color-picker v-model="getThemeConfig.menuBar" size="default"
                       @change="onBgColorPickerChange('menuBar')"></el-color-picker>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边默认字体颜色</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-color-picker v-model="getThemeConfig.menuBarColor" size="default"
                       @change="onBgColorPickerChange('menuBarColor')"></el-color-picker>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边高亮背景色</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-color-picker
          v-model="getThemeConfig.menuBarActiveColor"
          size="default"
          show-alpha
          @change="onBgColorPickerChange('menuBarActiveColor')"
      />
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt14">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边背景渐变</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isMenuBarColorGradual" size="small"
                 @change="onMenuBarGradualChange"></el-switch>
    </div>
  </div>

  <div class="layout-breadcrumb-setting-bar-flex mt15"
       :style="{ opacity: getThemeConfig.layout === 'transverse' ? 0.5 : 1 }">
    <div class="layout-breadcrumb-setting-bar-flex-label">侧边手风琴</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch
          v-model="getThemeConfig.isUniqueOpened"
          :disabled="getThemeConfig.layout === 'transverse'"
          size="small"
          @change="setLocalThemeConfig"
      ></el-switch>
    </div>
  </div>

  <template v-if="getThemeConfig.layout !== 'classic' || getThemeConfig.layout !== 'transverse'">
    <!-- 面包屑导航 -->
    <el-divider content-position="left">面包屑导航</el-divider>

    <div
        class="layout-breadcrumb-setting-bar-flex mt15"
        :style="{ opacity: getThemeConfig.layout === 'classic' || getThemeConfig.layout === 'transverse' ? 0.5 : 1 }"
    >
      <div class="layout-breadcrumb-setting-bar-flex-label">开启面包屑</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-switch
            v-model="getThemeConfig.isBreadcrumb"
            :disabled="getThemeConfig.layout === 'classic' || getThemeConfig.layout === 'transverse'"
            size="small"
            @change="onIsBreadcrumbChange"
        ></el-switch>
      </div>
    </div>
    <div class="layout-breadcrumb-setting-bar-flex mt15">
      <div class="layout-breadcrumb-setting-bar-flex-label">开启面包屑图标</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-switch v-model="getThemeConfig.isBreadcrumbIcon" size="small"
                   @change="setLocalThemeConfig"></el-switch>
      </div>
    </div>
  </template>


  <!-- 标签栏 -->
  <el-divider content-position="left">标签栏</el-divider>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">启用标签栏</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isTagsview" size="small" @change="setLocalThemeConfig"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">启用标签栏图标</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isTagsviewIcon" size="small" @change="setLocalThemeConfig"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">启用标签栏缓存</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isCacheTagsView" size="small"
                 @change="setLocalThemeConfig"></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt15" :style="{ opacity: isMobile ? 0.5 : 1 }">
    <div class="layout-breadcrumb-setting-bar-flex-label">启用标签栏拖拽</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch
          v-model="getThemeConfig.isSortableTagsView"
          :disabled="isMobile"
          size="small"
          @change="onSortableTagsViewChange"
      ></el-switch>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">启用标签栏共用</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isShareTagsView" size="small"
                 @change="onShareTagsViewChange"></el-switch>
    </div>
  </div>

  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">标签页风格</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-select v-model="getThemeConfig.tagsStyle" placeholder="请选择" size="default" style="width: 90px"
                 @change="setLocalThemeConfig">
        <el-option label="风格1" value="tags-style-one"></el-option>
        <el-option label="风格4" value="tags-style-four"></el-option>
        <el-option label="风格5" value="tags-style-five"></el-option>
      </el-select>
    </div>
  </div>


  <template v-if="getThemeConfig.layout === 'columns'">
    <!-- 分栏设置 -->
    <el-divider content-position="left" :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
      双列设置
    </el-divider>
    <div class="layout-breadcrumb-setting-bar-flex"
         :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
      <div class="layout-breadcrumb-setting-bar-flex-label">双列菜单背景</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-color-picker
            v-model="getThemeConfig.columnsMenuBar"
            size="default"
            @change="onBgColorPickerChange('columnsMenuBar')"
            :disabled="getThemeConfig.layout !== 'columns'"
        >
        </el-color-picker>
      </div>
    </div>

    <div class="layout-breadcrumb-setting-bar-flex"
         :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
      <div class="layout-breadcrumb-setting-bar-flex-label">双列菜单默认字体颜色</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-color-picker
            v-model="getThemeConfig.columnsMenuBarColor"
            size="default"
            @change="onBgColorPickerChange('columnsMenuBarColor')"
            :disabled="getThemeConfig.layout !== 'columns'"
        >
        </el-color-picker>
      </div>
    </div>
    <div class="layout-breadcrumb-setting-bar-flex mt14"
         :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
      <div class="layout-breadcrumb-setting-bar-flex-label">双列菜单背景渐变</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-switch
            v-model="getThemeConfig.isColumnsMenuBarColorGradual"
            size="small"
            @change="onColumnsMenuBarGradualChange"
            :disabled="getThemeConfig.layout !== 'columns'"
        ></el-switch>
      </div>
    </div>
    <div class="layout-breadcrumb-setting-bar-flex mt14"
         :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
      <div class="layout-breadcrumb-setting-bar-flex-label">双列菜单鼠标悬停预加载</div>
      <div class="layout-breadcrumb-setting-bar-flex-value">
        <el-switch
            v-model="getThemeConfig.isColumnsMenuHoverPreload"
            size="small"
            @change="onColumnsMenuHoverPreloadChange"
            :disabled="getThemeConfig.layout !== 'columns'"
        ></el-switch>
      </div>
    </div>

    <div class="layout-breadcrumb-setting-bar-flex mt15"
       :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
    <div class="layout-breadcrumb-setting-bar-flex-label">分栏高亮风格</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-select
          v-model="getThemeConfig.columnsAsideStyle"
          placeholder="请选择"
          size="default"
          style="width: 90px"
          :disabled="getThemeConfig.layout !== 'columns' ? true : false"
          @change="setLocalThemeConfig"
      >
        <el-option label="圆角" value="columns-round"></el-option>
        <el-option label="卡片" value="columns-card"></el-option>
      </el-select>
    </div>
  </div>
  <div class="layout-breadcrumb-setting-bar-flex mt15 mb27"
       :style="{ opacity: getThemeConfig.layout !== 'columns' ? 0.5 : 1 }">
    <div class="layout-breadcrumb-setting-bar-flex-label">分栏布局风格</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-select
          v-model="getThemeConfig.columnsAsideLayout"
          placeholder="请选择"
          size="default"
          style="width: 90px"
          :disabled="getThemeConfig.layout !== 'columns' ? true : false"
          @change="setLocalThemeConfig"
      >
        <el-option label="水平" value="columns-horizontal"></el-option>
        <el-option label="垂直" value="columns-vertical"></el-option>
      </el-select>
    </div>
  </div>
  </template>

  <!-- 其它设置 -->
  <el-divider content-position="left">其它设置</el-divider>
  <div class="layout-breadcrumb-setting-bar-flex mt15">
    <div class="layout-breadcrumb-setting-bar-flex-label">开启 Footer</div>
    <div class="layout-breadcrumb-setting-bar-flex-value">
      <el-switch v-model="getThemeConfig.isFooter" size="small" @change="setLocalThemeConfig"></el-switch>
    </div>
  </div>

</template>


<style scoped lang="scss">
@import "../index";

.layout-drawer-content-flex {
  overflow: hidden;
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  margin: 0 -5px;

  .layout-drawer-content-item {
    width: 50%;
    height: 70px;
    cursor: pointer;
    border: 1px solid transparent;
    position: relative;
    padding: 5px;

    .el-container {
      height: 100%;

      .el-aside-dark {
        background-color: var(--next-color-seting-header);
      }

      .el-aside {
        background-color: var(--next-color-seting-aside);
      }

      .el-header {
        background-color: var(--next-color-seting-header);
      }

      .el-main {
        background-color: var(--next-color-seting-main);
      }
    }

    .el-circular {
      border-radius: 2px;
      overflow: hidden;
      border: 1px solid transparent;
      transition: all 0.3s ease-in-out;
    }

    .drawer-layout-active {
      border: 1px solid;
      border-color: var(--el-color-primary);
    }

    .layout-tips-warp,
    .layout-tips-warp-active {
      transition: all 0.3s ease-in-out;
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      border: 1px solid;
      border-color: var(--el-color-primary-light-5);
      border-radius: 100%;
      padding: 4px;

      .layout-tips-box {
        transition: inherit;
        width: 30px;
        height: 30px;
        z-index: 9;
        border: 1px solid;
        border-color: var(--el-color-primary-light-5);
        border-radius: 100%;

        .layout-tips-txt {
          transition: inherit;
          position: relative;
          top: 5px;
          font-size: 12px;
          line-height: 1;
          letter-spacing: 2px;
          white-space: nowrap;
          color: var(--el-color-primary-light-5);
          text-align: center;
          transform: rotate(30deg);
          left: -1px;
          background-color: var(--next-color-seting-main);
          width: 32px;
          height: 17px;
          line-height: 17px;
        }
      }
    }

    .layout-tips-warp-active {
      border: 1px solid;
      border-color: var(--el-color-primary);

      .layout-tips-box {
        border: 1px solid;
        border-color: var(--el-color-primary);

        .layout-tips-txt {
          color: var(--el-color-primary) !important;
          background-color: var(--next-color-seting-main) !important;
        }
      }
    }

    &:hover {
      .el-circular {
        transition: all 0.3s ease-in-out;
        border: 1px solid;
        border-color: var(--el-color-primary);
      }

      .layout-tips-warp {
        transition: all 0.3s ease-in-out;
        border-color: var(--el-color-primary);

        .layout-tips-box {
          transition: inherit;
          border-color: var(--el-color-primary);

          .layout-tips-txt {
            transition: inherit;
            color: var(--el-color-primary) !important;
            background-color: var(--next-color-seting-main) !important;
          }
        }
      }
    }
  }
}

</style>