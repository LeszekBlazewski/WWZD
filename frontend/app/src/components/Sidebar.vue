<template>
  <div class="sidebar-ctn">
    <n-tabs type="segment">
      <n-tab-pane name="load" tab="Load" display-directive="show">
        <n-card title="Load dataset" size="huge">
          <n-dialog-provider>
            <DatasetLoaderTab />
          </n-dialog-provider>
        </n-card>
      </n-tab-pane>

      <n-tab-pane name="filter" tab="Filter" display-directive="show">
        <n-card title="Filters" size="huge">
          <ClassSelectorTab />
        </n-card>
      </n-tab-pane>

      <n-tab-pane name="insert" tab="Insert" display-directive="show">
        <n-card title="Comment insertion" size="huge">
          <CommentInsertionTab />
        </n-card>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script lang="ts" setup>
  import { NCard, NTabs, NTabPane, NDialogProvider } from 'naive-ui'
  import ClassSelectorTab from '@/components/ClassSelectorTab.vue'
  import CommentInsertionTab from '@/components/CommentInsertionTab.vue'
  import DatasetLoaderTab from '@/components/DatasetLoaderTab.vue'
</script>

<style lang="scss" scoped>
  .sidebar-ctn {
    height: calc(100% - 40px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px 0;
  }

  .n-card {
    user-select: none;
    --title-font-size: 1.5rem !important;
  }

  .n-tabs {
    user-select: none;
  }
</style>
