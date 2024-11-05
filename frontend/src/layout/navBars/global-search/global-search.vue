<script setup lang="ts">

import {nextTick, onMounted, onUnmounted, ref, watch} from 'vue';

import {
  ArrowDown,
  ArrowUp,
  CornerDownLeft,
  MdiKeyboardEsc,
  Search,
} from '/@/icons';
import {isWindowsOs} from '/@/utils/inference';

import {useMagicKeys, whenever} from '@vueuse/core';

import SearchPanel from './search-panel.vue';

defineOptions({
  name: 'GlobalSearch',
});

const props = withDefaults(
    defineProps<{ enableShortcutKey?: boolean; menus: any[] }>(),
    {
      enableShortcutKey: true,
      menus: () => [],
    },
);


const keyword = ref('');
const GlobalSearchRef = ref('');
const searchInputRef = ref<HTMLInputElement>();
const isOpen = ref(false);

function handleClose() {
  keyword.value = '';
  isOpen.value = false
}

const keys = useMagicKeys();
const cmd = isWindowsOs() ? keys['ctrl+k'] : keys['cmd+k'];
whenever(cmd!, () => {
  if (props.enableShortcutKey) {
    toggleOpen();
  }
});

whenever(isOpen, () => {
  nextTick(() => {
    setTimeout(() => {
      searchInputRef.value?.focus();
    }, 0)
  });
});

const preventDefaultBrowserSearchHotKey = (event: KeyboardEvent) => {
  if (event.key?.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey)) {
    event.preventDefault();
  }
};

const toggleKeydownListener = () => {
  if (props.enableShortcutKey) {
    window.addEventListener('keydown', preventDefaultBrowserSearchHotKey);
  } else {
    window.removeEventListener('keydown', preventDefaultBrowserSearchHotKey);
  }
};

const toggleOpen = () => {
  isOpen.value = !isOpen.value
};


watch(() => props.enableShortcutKey, toggleKeydownListener);

onMounted(() => {
  toggleKeydownListener();

  onUnmounted(() => {
    window.removeEventListener('keydown', preventDefaultBrowserSearchHotKey);
  });
});

defineExpose({
  toggleOpen
})
</script>

<template>
  <div>
    <el-dialog v-model="isOpen"
               ref="GlobalSearchRef"
               width="600"
    >
      <template #header>
        <div class="search-header">
          <Search class="search-icon"/>
          <input
              ref="searchInputRef"
              v-model="keyword"
              placeholder="搜索导航菜单"
              class="search-input"
          />
        </div>
      </template>

      <SearchPanel :keyword="keyword" :menus="menus" @close="handleClose"/>
      <template #footer>
        <div class="search-footer">
          <div class="search-footer-item">
            <CornerDownLeft class="search-footer-item-icon"/>
            选择
          </div>
          <div class="mr5 search-footer-item">
            <ArrowUp class="search-footer-item-icon"/>
            <ArrowDown class="search-footer-item-icon"/>
            导航
          </div>
          <div class="mr5 search-footer-item">
            <MdiKeyboardEsc class="search-footer-item-icon"/>
            关闭
          </div>
        </div>
      </template>
    </el-dialog>
    <div
        class=" bg-none px-2 py-0.5 outline-none"
        style="
background-color: #f4f4f5;
background-color: var(--next-bg-color);
display: flex;
height: 30px;
cursor: pointer !important;
align-items: center;
justify-items: center;
place-items: center;
gap:.75rem;
border-radius: 1rem;
border-style: none;
background-image: none;
padding-left: .5rem;
padding-right: .5rem;
padding-bottom: .125rem;
padding-top: .125rem;
outline: 2px solid transparent;
outline-offset: 2px;
"
        @click="toggleOpen"
    >
      <Search style="width: 16px; height: 16px"
              class="text-muted-foreground group-hover:text-foreground size-4 group-hover:opacity-100"
      />
      <span
          class="text-muted-foreground group-hover:text-foreground hidden text-xs duration-300 md:block"
          style="white-space: nowrap"
      >搜索
      </span>
      <span
          style="
          padding: 4px 6px;
white-space: nowrap;
background-color: #FFF;
background-color: var(--el-color-white);
border-color:#32363999;
border-bottom-right-radius: calc(0.5rem + 4px);
border-top-right-radius: calc(0.5rem + 4px);
font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji';
"
          v-if="enableShortcutKey"
          class="bg-background border-foreground/60 text-muted-foreground group-hover:text-foreground relative hidden rounded-sm rounded-r-xl px-1.5 py-1 text-xs leading-none group-hover:opacity-100 md:block"
      >
        {{ isWindowsOs() ? 'Ctrl' : '⌘' }}
        <kbd>K</kbd>
      </span>
      <span v-else></span>
    </div>
  </div>
</template>


<style lang="scss" scoped>

.search-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e4e4e7;
  border-bottom: 1px solid var(--el-border-color);

  .search-input {
    font-weight: 400;
    font-size: .875rem;
    line-height: 1.25rem;
    padding-left: 0;
    background-color: transparent;
    border-style: none;
    border-width: 1px;
    border-radius: calc(var(0.5rem) - 2px);
    width: 80%;
    padding: .5rem;
    //color: var(--next-color-white);
  }

  .search-icon {
    color: #71717a;
    height: 1rem;
    width: 1rem
  }
}


.search-footer {
  color: #323639;
  display: flex;
  width: 100%;
  justify-content: flex-start;
  font-size: .75rem;
  line-height: 1rem;
  border-top: 1px solid #e4e4e7;
  border-top: 1px solid var(--el-border-color);
  padding-top: 16px;

  .search-footer-item {
    display: flex;
    align-items: center;
    margin-right: .5rem;
    //color: var(--el-color-white);

    .search-footer-item-icon {
      margin-right: 5px;
      height: 18px;
      width: 18px;

    }

    .search-footer-item-text {

    }
  }
}

:deep(.el-dialog__header.show-close) {
  padding-right: 0;
}


.group:hover .group-hover\:text-foreground {
  color: #323639;
  color: hsl(var(--foreground))
}

.group:hover .group-hover\:opacity-100 {
  opacity: 1
}

.text-muted-foreground {
  color: #71717a;
}

.bg-background {
  background-color: #fff;
  background-color: hsl(var(--background))
}

.border-foreground\/60 {
  border-color: #32363999;
  border-color: hsl(var(--foreground)/.6)
}

.relative {
  position: relative
}

.hidden {
  display: none
}

.md\:block {
  display: block
}

.leading-none {
  line-height: 1
}

.rounded-r-xl {
  border-bottom-right-radius: calc(.5rem + 4px);
  border-bottom-right-radius: calc(var(--radius) + 4px);
  border-top-right-radius: calc(.5rem + 4px);
  border-top-right-radius: calc(var(--radius) + 4px)
}
</style>
