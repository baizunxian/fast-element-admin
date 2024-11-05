<script setup lang="ts">
import {nextTick, onMounted, ref, shallowRef, watch} from 'vue';
import {useRouter} from 'vue-router';
import {SearchX, X} from '/@/icons';
import {mapTree, traverseTreeValues, uniqueByField, isHttpUrl} from '/@/utils';
import {onKeyStroke, useLocalStorage, useThrottleFn} from '@vueuse/core';

defineOptions({
  name: 'SearchPanel',
});

const props = withDefaults(
    defineProps<{ keyword: string; menus: any[] }>(),
    {
      keyword: '',
      menus: () => [],
    },
);
const emit = defineEmits<{ close: [] }>();

const router = useRouter();
const searchHistory = useLocalStorage<any[]>(
    `__search-history-${location.hostname}__`,
    [],
);
const activeIndex = ref(-1);
const searchItems = shallowRef<any[]>([]);
const searchResults = ref<any[]>([]);

const handleSearch = useThrottleFn(search, 200);

// 搜索函数，用于根据搜索关键词查找匹配的菜单项
function search(searchKey: string) {
  // 去除搜索关键词的前后空格
  searchKey = searchKey.trim();

  // 如果搜索关键词为空，清空搜索结果并返回
  if (!searchKey) {
    searchResults.value = [];
    return;
  }

  // 使用搜索关键词创建正则表达式
  const reg = createSearchReg(searchKey);

  // 初始化结果数组
  const results: any[] = [];

  // 遍历搜索项
  traverseTreeValues(searchItems.value, (item) => {
    // 如果菜单项的名称匹配正则表达式，将其添加到结果数组中
    if (reg.test(item.title?.toLowerCase()) && !item.meta?.isHide) {
      results.push(item);
    }
  });

  // 更新搜索结果
  searchResults.value = results;

  // 如果有搜索结果，设置索引为 0
  if (results.length > 0) {
    activeIndex.value = 0;
  }

  // 赋值索引为 0
  activeIndex.value = 0;
}

// When the keyboard up and down keys move to an invisible place
// the scroll bar needs to scroll automatically
function scrollIntoView() {
  const element = document.querySelector(
      `[data-search-item="${activeIndex.value}"]`,
  );

  if (element) {
    element.scrollIntoView({block: 'nearest'});
  }
}

// enter keyboard event
async function handleEnter() {
  if (searchResults.value.length === 0) {
    return;
  }
  const result = searchResults.value;
  const index = activeIndex.value;
  if (result.length === 0 || index < 0) {
    return;
  }
  const to = result[index];
  if (to) {
    searchHistory.value.push(to);
    handleClose();
    await nextTick();
    if (isHttpUrl(to.path)) {
      window.open(to.path, '_blank');
    } else {
      router.push({path: to.path, replace: true});
    }
  }
}

// Arrow key up
function handleUp() {
  if (searchResults.value.length === 0) {
    return;
  }
  activeIndex.value--;
  if (activeIndex.value < 0) {
    activeIndex.value = searchResults.value.length - 1;
  }
  scrollIntoView();
}

// Arrow key down
function handleDown() {
  if (searchResults.value.length === 0) {
    return;
  }
  activeIndex.value++;
  if (activeIndex.value > searchResults.value.length - 1) {
    activeIndex.value = 0;
  }
  scrollIntoView();
}

// close search modal
function handleClose() {
  searchResults.value = [];
  emit('close');
}

// Activate when the mouse moves to a certain line
function handleMouseenter(e: MouseEvent) {
  const index = (e.target as HTMLElement)?.dataset.index;
  activeIndex.value = Number(index);
}

function removeItem(index: number) {
  if (props.keyword) {
    searchResults.value.splice(index, 1);
  } else {
    searchHistory.value.splice(index, 1);
  }
  activeIndex.value = activeIndex.value - 1 >= 0 ? activeIndex.value - 1 : 0;
  scrollIntoView();
}

// 存储所有需要转义的特殊字符
const code = new Set([
  '$',
  '(',
  ')',
  '*',
  '+',
  '.',
  '?',
  '[',
  '\\',
  ']',
  '^',
  '{',
  '|',
  '}',
]);

// 转换函数，用于转义特殊字符
function transform(c: string) {
  // 如果字符在特殊字符列表中，返回转义后的字符
  // 如果不在，返回字符本身
  return code.has(c) ? `\\${c}` : c;
}

// 创建搜索正则表达式
function createSearchReg(key: string) {
  // 将输入的字符串拆分为单个字符
  // 对每个字符进行转义
  // 然后用'.*'连接所有字符，创建正则表达式
  const keys = [...key].map((item) => transform(item)).join('.*');
  // 返回创建的正则表达式
  return new RegExp(`.*${keys}.*`);
}

watch(
    () => props.keyword,
    (val) => {
      if (val) {
        handleSearch(val);
      } else {
        searchResults.value = [...searchHistory.value];
      }
    },
);

onMounted(() => {
  console.log(props.menus, 'menusmenus')
  searchItems.value = mapTree(props.menus, (item) => {
    return {
      ...item,
      name: item?.name,
    };
  });
  if (searchHistory.value.length > 0) {
    searchResults.value = searchHistory.value;
  }
  // enter search
  onKeyStroke('Enter', handleEnter);
  // Monitor keyboard arrow keys
  onKeyStroke('ArrowUp', handleUp);
  onKeyStroke('ArrowDown', handleDown);
  // esc close
  onKeyStroke('Escape', handleClose);
});
</script>

<template>
  <el-scrollbar>
    <div class="h100 pr10 pl10"
         style="max-height: 450px; justify-content: center;display: flex !important"
    >
      <!-- 无搜索结果 -->
      <div
          v-if="keyword && searchResults.length === 0"
          class="search-empty-box"
      >
        <SearchX class="search-empty-box-icon mx-auto mt-4 size-12"/>
        <p class="mb10 mt6 font14">
          未找到搜索结果
          <span style="color: #323639; font-weight: 500;">
            "{{ keyword }}"
          </span>
        </p>
      </div>
      <!-- 历史搜索记录 & 没有搜索结果 -->
      <div
          v-if="!keyword && searchResults.length === 0"
          style="color: #71717a;text-align: center"
      >
        <p class="mb10 mt10 font14">
          没有搜索历史
        </p>
      </div>

      <ul v-show="searchResults.length > 0" class="w100">
        <li
            v-if="searchHistory.length > 0 && !keyword"
            class="text-muted-foreground mb10 font14"
            style="color: #71717a;"
        >
          搜索历史
        </li>
        <li
            v-for="(item, index) in uniqueByField(searchResults, 'path')"
            :key="item.path"
            :class="
            activeIndex === index
              ? 'active bg-primary text-primary-foreground'
              : ''
          "
            :data-index="index"
            :data-search-item="index"
            style="
            background-color: #f4f4f5;
               cursor: pointer;
               border-radius: 0.5rem;
                align-items: center;
                display: flex;
                justify-content: center;"
            class="mb10 w100  pl4 pr4 pb5 pt5"
            @click="handleEnter"
            @mouseenter="handleMouseenter"
        >
          <el-icon
              :icon="item.icon"
              style="flex-shrink: 0"
              class="mr5 font14"
              fallback
          />

          <span style="flex: 1 1 0%">{{ item.title }}</span>
          <div
              class="p5 p-1 hover:scale-110"
              style="align-items: center;
    display: flex;
    justify-content: center;
     border-radius: 9999px
"
              @click.stop="removeItem(index)"
          >
            <X class="font14"/>
          </div>
        </li>
      </ul>
    </div>
  </el-scrollbar>
</template>


<style lang="scss" scoped>
.search-empty-box {
  color: #71717a;
  text-align: center;

  .search-empty-box-icon {
    margin-left: auto;
    margin-right: auto;
    height: 3rem;
    width: 3rem;
  }
}

.hover\:scale-110:hover {
  --tw-translate-y: .25rem;
  --tw-rotate: 180deg;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1.1;
  --tw-scale-y: 1.1;
  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(1.1) scaleY(1.1);
  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skew(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))
}

.bg-primary {
  background-color: var(--el-color-primary) !important;
}

.text-primary-foreground {
  color: #fafafa;
}

.active\:text-primary-active:active {
  color: hsl(var(--primary-700))
}
</style>