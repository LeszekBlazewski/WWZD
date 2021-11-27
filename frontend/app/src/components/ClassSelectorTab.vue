<template>
  <n-button-group class="filter-btns" vertical>
    <n-button
      v-for="(value, key) in SubclassLabels"
      :key="key"
      :value="key"
      :class="{ btnenabled: classFilter[key] }"
      size="large"
      @click="select(key)"
    >
      {{ value }}
    </n-button>
  </n-button-group>
  <n-divider />
  <n-button class="filter-btns" size="large" @click="clearSelection">
    Clear
  </n-button>
</template>

<script lang="ts" setup>
  import { watch } from 'vue'
  import { NButtonGroup, NButton, NDivider } from 'naive-ui'
  import { useClassSelection } from '@/composables/useClassSelection'
  import { useCommentsStore } from '@/stores/commentsStore'
  import { SubclassLabels } from '@/models'
  import type { Subclass } from '@/models'

  const { select, clearSelection, classFilter } = useClassSelection()

  const commentsStore = useCommentsStore()

  watch(
    classFilter,
    (state) => {
      for (const key in state) {
        if (state[key as Subclass]) {
          commentsStore.setFilter(key as Subclass)
          return
        }
      }
      commentsStore.setFilter('all')
    },
    { deep: true }
  )
</script>

<style lang="scss" scoped>
  .cls-btns {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .filter-btns {
    width: 80%;
  }

  input {
    font-size: 2rem;
    margin: 10px;
  }

  .btnenabled {
    --text-color: #7fe7c4 !important;
    --border: 1px solid #7fe7c4 !important;
    font-weight: 600 !important;

    :deep(div) {
      --border: 1px solid #7fe7c4 !important;
      border-color: #7fe7c4 !important;
      z-index: 3;
    }
  }
</style>
