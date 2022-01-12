<template>
  <n-space vertical>
    <n-input
      type="textarea"
      :autosize="{ minRows: 3, maxRows: 7 }"
      placeholder="Enter a new comment..."
      clearable
      v-model:value="comment"
    />

    <n-spin size="small" :show="commentsStore.loading">
      <n-button
        size="large"
        @click="addComment"
        :disabled="!datasetsStore.selectedDataset"
      >
        Insert
      </n-button>
    </n-spin>

    <n-divider />

    <n-button size="large" @click="commentsStore.clearUserComments">
      Clear all
    </n-button>
  </n-space>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
  import { NInput, NButton, NSpace, NDivider, NSpin } from 'naive-ui'
  import { useCommentsStore } from '@/stores/commentsStore'
  import { useDatasetsStore } from '@/stores/datasetsStore'

  const commentsStore = useCommentsStore()
  const datasetsStore = useDatasetsStore()

  const comment = ref('')

  const addComment = async () => {
    const dataset = datasetsStore.selectedDataset
    if (dataset) {
      await commentsStore.addComments(dataset.name, dataset.reductionModel, [
        comment.value,
      ])
      comment.value = ''
    }
  }
</script>

<style lang="scss" scoped>
  .n-button {
    width: 80%;
  }

  .n-input {
    text-align: left;
    margin-bottom: 20px;
  }
</style>
