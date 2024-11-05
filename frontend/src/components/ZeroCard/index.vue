<script setup lang="ts">
import {ElCard} from "element-plus"
defineOptions({name: "ZeroCard"})

defineSlots<{
  default?: any
  header?: any
  footer?: any
}>()

defineProps({
  borderRadius: {
    type: String,
    default: '15px'
  },
  showTip: {
    type: Boolean,
    default: false
  },
})


</script>

<template>
  <el-card class="zero-card-class" v-bind="$attrs" :class="[showTip? 'zero-card-tip' : '']">
    <template v-for="(item, key) in $slots" :key="key" #[key]="slotProps">
      <slot :name="key" v-bind="slotProps"></slot>
    </template>
  </el-card>
</template>

<style lang="scss" scoped>
.zero-card-class {
  --el-card-border-radius: v-bind(borderRadius);
}

.zero-card-tip {
  border-radius: 10px;
  border-left: 5px solid #409eff;
  border-left: 5px solid var(--el-color-primary);
}

</style>