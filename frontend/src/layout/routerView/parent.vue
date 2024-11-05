<template>
  <div class="layout-parent">
    <router-view v-slot="{ Component, route}">
      <transition :name="setTransitionName" mode="out-in">
        <keep-alive :include="getKeepAliveNames">
          <component :is="formatComponentInstance(Component, route)"
                     class="w100"
                     :key="state.refreshRouterViewKey"
                     v-show="!isIframePage">
          </component>
        </keep-alive>
      </transition>
    </router-view>

    <transition :name="setTransitionName" mode="out-in">
      <Iframes class="w100"
               v-show="isIframePage"
               :refreshKey="state.iframeRefreshKey"
               :name="setTransitionName"
               :list="state.iframeList"/>
    </transition>
  </div>
</template>

<script setup lang="ts" name="layoutParentView">
import {
  computed,
  defineAsyncComponent,
  h,
  markRaw,
  nextTick,
  onBeforeMount,
  onMounted,
  onUnmounted,
  reactive,
  watch
} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {storeToRefs} from "/@/stores";
import {useKeepALiveNames} from '/@/stores/keepAliveNames';
import {useThemeConfig} from '/@/stores/themeConfig';
import {Session} from '/@/utils/storage';
import mittBus from '/@/utils/mitt';

// 引入组件
const Iframes = defineAsyncComponent(() => import('/@/layout/routerView/iframes.vue'));
// 定义变量内容
const route = useRoute();
const router = useRouter();
const storesKeepAliveNames = useKeepALiveNames();
const storesThemeConfig = useThemeConfig();
const {keepAliveNames, cachedViews} = storeToRefs(storesKeepAliveNames);
const {themeConfig} = storeToRefs(storesThemeConfig);
const state = reactive<ParentViewState>({
  refreshRouterViewKey: '', // 非 iframe tagsView 右键菜单刷新时
  iframeRefreshKey: '', // iframe tagsView 右键菜单刷新时
  keepAliveNameList: [],
  iframeList: [],
});

const wrapperMap = new Map()

// 设置主界面切换动画
const setTransitionName = computed(() => {
  return themeConfig.value.animation;
});
// 获取组件缓存列表(name值)
const getKeepAliveNames = computed(() => {
  return themeConfig.value.isTagsview ? cachedViews.value : state.keepAliveNameList;
});
// 设置 iframe 显示/隐藏
const isIframePage = computed(() => {
  return route.meta.isIframe;
});
// 获取 iframe 组件列表(未进行渲染)
const getIframeListRoutes = async () => {
  router.getRoutes().forEach((v: any) => {
    if (v.meta.isIframe) {
      v.meta.isIframeOpen = false;
      v.meta.loading = true;
      state.iframeList.push({...v});
    }
  });
};


const formatComponentInstance = (component: any, route: any) => {
  let wrapper;
  if (component) {
    const wrapperName = route.fullPath;
    if (wrapperMap.has(wrapperName)) {
      wrapper = wrapperMap.get(wrapperName);
    } else {
      wrapper = {
        name: wrapperName,
        render() {
          return h(component);
        },
      };
      wrapperMap.set(wrapperName, wrapper);
    }
    return h(wrapper);
  }
}

// 页面加载前，处理缓存，页面刷新时路由缓存处理
onBeforeMount(() => {
  state.keepAliveNameList = keepAliveNames.value;
  mittBus.on('onTagsViewRefreshRouterView', (fullPath) => {
    state.refreshRouterViewKey = Math.random().toString();
    state.iframeRefreshKey = Math.random().toString();
    state.keepAliveNameList = keepAliveNames.value.filter((name: string) => route.fullPath !== name);
    nextTick(() => {
      state.refreshRouterViewKey = fullPath;
      state.iframeRefreshKey = fullPath;
      if (route.meta.isKeepAlive) {
        const stores = useKeepALiveNames();
        stores.updateCacheKeepAlive(route.fullPath);
      }
      state.keepAliveNameList = keepAliveNames.value;
    });
  });
});
// 页面加载时
onMounted(() => {
  getIframeListRoutes();
  nextTick(() => {
    setTimeout(() => {
      if (themeConfig.value.isCacheTagsView) {
        let tagsViewArr: RouteItem[] = Session.get('tagsViewList') || [];
        cachedViews.value = tagsViewArr.filter((item) => item.meta?.isKeepAlive).map((item) => item.name as string);
      }
    }, 0);
  });
});
// 页面卸载时
onUnmounted(() => {
  mittBus.off('onTagsViewRefreshRouterView', () => {
  });
});
watch(
    () => route.fullPath,
    () => {
      state.refreshRouterViewKey = decodeURI(route.fullPath);
      useKeepALiveNames().addCachedView(route?.meta?.isKeepAlive || false, route.fullPath);
    },
    {
      immediate: true,
    }
);
</script>
