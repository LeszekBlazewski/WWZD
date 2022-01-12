<template>
  <n-alert :class="alertClass" type="default" :show-icon="false">
    Displaying <b>{{ commentsStore.dataset?.name }}</b> dataset, using
    <b>{{ commentsStore.dataset?.reductionModel.toUpperCase() }}</b> algorithm,
    samples <b>{{ commentsStore.sampleRange[0] }}</b> to
    <b>{{ commentsStore.sampleRange[1] }}</b>
  </n-alert>
</template>

<script lang="ts" setup>
  import { computed } from 'vue'
  import { NAlert } from 'naive-ui'
  import { useCommentsStore } from '@/stores/commentsStore'

  const commentsStore = useCommentsStore()

  const alertClass = computed(() => {
    return {
      hidden: commentsStore.dataset === null,
    }
  })
</script>

<style lang="scss" scoped>
  .n-alert {
    background-color: rgba(24, 24, 28, 0.95);
    position: fixed;
    top: 75px;
    left: 10px;
    text-align: left;
  }

  .hidden {
    display: none;
  }
</style>
