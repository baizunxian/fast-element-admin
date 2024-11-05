<template>
  <div class="layout-navbars-breadcrumb-user" :style="{ flex: layoutUserFlexNum }">

    <GlobalSearch ref="searchRef" :menus="menuList" class="mr15"/>

<!--    <div class="mr10" style="display: flex; height: 50px; line-height: 50px; align-items: center;">-->
<!--      <TopEnv></TopEnv>-->
<!--    </div>-->


    <div>
      <el-button
          title="布局设置"
          size="default"
          class="layout-navbars-breadcrumb-user-icon rounded-full"
          @click="onLayoutSettingClick"
          text
      >
        <Settings class="icon-size"></Settings>
      </el-button>
    </div>


    <!--    <div class="layout-navbars-breadcrumb-user-icon rounded-full" @click="onLayoutSettingClick">-->
    <!--      <i class="iconfont icon-zhuti" title="布局配置"></i>-->
    <!--    </div>-->


    <div>
      <el-button
          :title="state.isScreenfull ? '关全屏' : '开全屏'"
          class="layout-navbars-breadcrumb-user-icon rounded-full"
          @click="onScreenfullClick"
          text
      >
        <Maximize class="icon-size" v-if="!state.isScreenfull"></Maximize>
        <Minimize class="icon-size" v-else></Minimize>
      </el-button>
    </div>


    <!--    <div class="layout-navbars-breadcrumb-user-icon rounded-full" @click="onScreenfullClick">-->
    <!--      <i-->
    <!--          class="iconfont"-->
    <!--          :title="state.isScreenfull ? '关全屏' : '开全屏'"-->
    <!--          :class="!state.isScreenfull ? 'icon-quanping' : 'icon-tuichuquanping'"-->
    <!--      ></i>-->
    <!--    </div>-->

    <div class="layout-navbars-breadcrumb-user-icon rounded-full mr10">
      <el-popover placement="bottom" trigger="click" transition="el-zoom-in-top" :width="300" :persistent="false">
        <template #reference>
          <el-button
              title="消息"
              size="default"
              class="layout-navbars-breadcrumb-user-icon rounded-full bell-button"
              text
          >
            <el-badge :is-dot="true">
              <Bell class="icon-size shake-animation"></Bell>
            </el-badge>
          </el-button>
        </template>
        <template #default>
          <UserNews/>
        </template>
      </el-popover>
    </div>


    <el-dropdown :show-timeout="70"
                 trigger="click"
                 ref="userInfoDropdownMenuRef"
                 :hide-timeout="50">
      <div class="layout-navbars-breadcrumb-user-link rounded-full">
        <el-avatar class="layout-navbars-breadcrumb-user-link-photo"
                   :src="userInfos.avatar"
                   :size="32"
                   :style="userInfos.avatar ? {'--el-avatar-bg-color': 'transparent'} : {}">
          {{ userInfos.nickname ? userInfos.nickname.slice(0, 1).toUpperCase() : "" }}
        </el-avatar>
      </div>
      <template #dropdown>
        <div class="user-info-dropdown-menu">
          <div class="avatar_box">
            <div class="avatar-box-img">
              <el-avatar
                  :src="userInfos.avatar"
                  :style="userInfos.avatar ? {'--el-avatar-bg-color': 'transparent'} : {}">
                {{ userInfos.nickname ? userInfos.nickname.slice(0, 1).toUpperCase() : "" }}
              </el-avatar>
            </div>
            <div class="avatar-box-name">
              <div class="avatar-box-name-text">{{ userInfos.nickname }}</div>
              <span class="avatar-box-name-des" :title="userInfos?.remarks">{{ userInfos.remarks }}</span>
            </div>
          </div>

          <div class="mb5 mt5" style="height: 1px; background-color: var(--el-border-color)"></div>

          <div class="avatar-box-menu-itme" @click="onMenuClick('doc')">
            <BookOpenText class="icon-size mr5"></BookOpenText>
            文档
          </div>

          <div class="avatar-box-menu-itme" @click="onMenuClick('GitHub')">
            <Github class="icon-size mr5"></Github>
            GitHub
          </div>

          <div class="avatar-box-menu-itme" @click="onMenuClick('lock')">
            <LockKeyhole class="icon-size mr5"></LockKeyhole>
            锁定屏幕
          </div>

          <div class="mb5 mt5 " style="height: 1px; background-color: var(--el-border-color)"></div>
          <div class="avatar-box-menu-itme" @click="onMenuClick('userCenter')">
            <UserRoundPen class="icon-size mr5"></UserRoundPen>
            个人中心
          </div>

          <div class="mb5 mt5 " style="height: 1px; background-color: var(--el-border-color)"></div>
          <div class="avatar-box-menu-itme" @click="onMenuClick('logOut')">
            <LogOut class="icon-size mr5"></LogOut>
            退出登录
          </div>
        </div>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import screenfull from 'screenfull';
import { storeToRefs } from "/@/stores";
import { useUserStore } from '/@/stores/user';
import { useAuthStore } from '/@/stores/auth';
import { useThemeConfig } from '/@/stores/themeConfig';
import mittBus from '/@/utils/mitt';
import { Local } from '/@/utils/storage';
import { Bell, BookOpenText, Github, LockKeyhole, LogOut, Maximize, Minimize, Settings, UserRoundPen } from "/@/icons"
import { useMenuInfo } from "/@/stores/menu";

defineOptions({ name: "layoutBreadcrumbUser" })

// 引入组件
const UserNews = defineAsyncComponent(() => import('/src/layout/navBars/topBar/userNews.vue'));
const GlobalSearch = defineAsyncComponent(() => import('/src/layout/navBars/global-search/global-search.vue'));

// 定义变量内容
const router = useRouter();
const storesUser = useUserStore();
const authStore = useAuthStore();
const { userInfos } = storeToRefs(storesUser);
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

const searchRef = ref();
const userInfoDropdownMenuRef = ref();

const useMenuState = useMenuInfo()

const menuList = computed(() => {
  return useMenuState.getMenuList()
})

const state = reactive({
  isScreenfull: false,
  disabledSize: 'large',
});

// 设置分割样式
const layoutUserFlexNum = computed(() => {
  let num = '';
  const { layout, isClassicSplitMenu } = themeConfig.value;
  const layoutArr = ['defaults', 'columns'];
  if (layoutArr.includes(layout) || (layout === 'classic' && !isClassicSplitMenu)) num = '1';
  else num = '';
  return num;
});

// 菜单点击操作
const onMenuClick = (command: string) => {
  switch (command) {
    case "doc":
      onDocClick()
      break
    case "logOut":
      onLogOutClick()
      break
    case "GitHub":
      onGithubClick()
      break
    case "lock":
      onLockScreen()
      break
    case "userCenter":
      onUserCenterClick()
      break
    default:
      break
  }
  userInfoDropdownMenuRef.value?.handleClose()
}

// 全屏点击时
const onScreenfullClick = () => {
  if (!screenfull.isEnabled) {
    ElMessage.warning('暂不不支持全屏');
    return false;
  }
  screenfull.toggle();
  screenfull.on('change', () => {
    if (screenfull.isFullscreen) state.isScreenfull = true;
    else state.isScreenfull = false;
  });
};
// 布局配置 icon 点击时
const onLayoutSettingClick = () => {
  mittBus.emit('openSettingsDrawer');
};
// 布局配置 icon 点击时
const onLockScreen = () => {
  themeConfig.value.isLockScreen = true
  themeConfig.value.lockScreenTime = 0
  // mittBus.emit('lockScreen');
};
// 退出登录
const onLogOutClick = () => {
      ElMessageBox({
        closeOnClickModal: false,
        closeOnPressEscape: false,
        title: '提示',
        message: '此操作将退出登录, 是否继续?',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        buttonSize: 'default',
        beforeClose: async (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true;
            instance.confirmButtonText = '退出中';
            try {
              await authStore.Logout()
            } catch (e) {
              console.log('退出失败，错误信息： ', e)
            } finally {
              done();
              instance.confirmButtonLoading = false;
            }
          } else {
            done();
          }
        },
      })
          .then(async () => {
            // 使用 reload 时，不需要调用 resetRoute() 重置路由
            window.location.reload();
          })
          .catch(() => {
          });
    }
;
// 菜单搜索点击
const onSearchClick = () => {
  searchRef.value.toggleOpen();
};

// git仓库
const onGithubClick = () => {
  window.open('https://github.com/baizunxian/zerorunner');
}
// doc文档
const onDocClick = () => {
  window.open('https://zerorunner.cn/docs');
}
// 个人中心
const onUserCenterClick = () => {
  router.push({ path: "/system/personal" })
}
// 组件大小改变
const onComponentSizeChange = (size: string) => {
  Local.remove('themeConfig');
  themeConfig.value.globalComponentSize = size;
  Local.set('themeConfig', themeConfig.value);
  initI18nOrSize('globalComponentSize', 'disabledSize');
  window.location.reload();
};
// 初始化组件大小/i18n
const initI18nOrSize = (value: string, attr: string) => {
  state[attr] = Local.get('themeConfig')[value];
};

// 页面加载时
onMounted(() => {
  if (Local.get('themeConfig')) {
    initI18nOrSize('globalComponentSize', 'disabledSize');
  }
});
</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb-user {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-right: .5rem;

  &-link {
    cursor: pointer;
    display: flex;
    align-items: center;
    white-space: nowrap;
    padding: 5px;

    &:hover {
      background-color: #f4f4f5;
      background-color: var(--el-fill-color-light);
    }

    &-photo {
      border-radius: 100%;
    }
  }

  &-icon {
    cursor: pointer;
    color: var(--next-bg-topBarColor);
    line-height: 50px;
    display: flex;
    align-items: center;
    justify-items: center;
    width: 2rem;
    height: 2rem;
    //margin-right: .25rem;

    .iconfont {
      margin-right: 0;
    }

    //&:hover {
    //  background: var(--next-color-user-hover);
    //
    //  i {
    //    display: inline-block;
    //    animation: logoAnimation 0.3s ease-in-out;
    //  }
    //
    //}
  }

  :deep(.el-dropdown) {
    color: var(--next-bg-topBarColor);
  }

  :deep(.el-badge) {
    height: 40px;
    line-height: 40px;
    display: flex;
    align-items: center;
  }

  :deep(.el-badge__content.is-fixed) {
    top: 10px;
  }
}

.rounded-full {
  border-radius: 9999px;
}

.icon-size {
  width: 1.25rem;
  height: 1.25rem;
}

.user-info-dropdown-menu {
  width: 248px;
  padding-bottom: 5px;

  .avatar_box {
    padding: 12px 12px 7px 12px;
    display: flex;
    height: 64px;
    line-height: 64px;
    align-items: center; /* 确保图片垂直居中 */
    box-sizing: border-box; /* 确保padding不会影响到整体宽度 */

    .avatar-box-img {
      display: inline-block;
      height: 45px;
      width: 45px;

      //margin-right: 5px;
      box-sizing: border-box; /* 包括padding和border在内 */
      span {
        height: 45px;
        width: 45px;
      }
    }

    .avatar-box-name {
      display: flex;
      align-content: space-around;
      flex-wrap: wrap;
      margin-left: .5rem;
      overflow: hidden;

      .avatar-box-name-text {
        color: #323639;
        color: var(--el-text-color);
        font-weight: 500;
        font-size: 1.25rem;
        line-height: 1.25rem;
        margin-bottom: 5px;
      }

      .avatar-box-name-des {
        width: 180px; /* 容器的宽度 */
        color: #9daab6;
        //color: var(--el-text-color-);
        font-size: .875rem;
        line-height: 1.25rem;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        white-space: nowrap; /* 确保文本在一行内显示 */
        overflow: hidden; /* 隐藏溢出容器的文本 */
        text-overflow: ellipsis; /* 超出部分显示为省略号 */
      }
    }
  }

  .avatar-box-menu-itme {
    font-size: 14px;
    line-height: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    transition-duration: .15s;
    transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
    transition-timing-function: cubic-bezier(.4, 0, .2, 1);
    outline: 2px solid transparent;
    outline-offset: 2px;
    margin: 0 4px;
    padding: 4px 8px;
    color: #606266;
    color: var(--el-text-color-primary);
    cursor: pointer;
    border-radius: 4px;

    &:hover {
      background-color: #f4f4f5;
      color: #606266;
      color: var(--el-color-black);
    }
  }
}

</style>

<style lang="scss">
// 定义晃动动画
@keyframes shake {
  0%, 100% {
    transform-origin: top;
  }
  15% {
    transform: rotate(10deg);
  }
  30% {
    transform: rotate(-10deg);
  }
  45% {
    transform: rotate(5deg);
  }
  60% {
    transform: rotate(-5deg);
  }
  75% {
    transform: rotate(2deg);
  }
}


.bell-button {
  // 晃动动画类
  &:hover {
    .shake-animation {
      transition: all 0.1s; // 添加过渡效果
      animation: shake 1s ease-in-out; // 动画持续时间为1秒
    }
  }
}

</style>
