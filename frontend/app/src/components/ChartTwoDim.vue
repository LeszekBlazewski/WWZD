<template>
  <div ref="chart" class="chart" />
  <DatasetInfoOverlay />
  <CommentDetailsOverlay :title="tags" :content="comment" />
  <CommentDetailsModal
    v-model:show="showModal"
    :title="tags"
    :content="comment"
    :classification="classification"
  />
</template>

<script setup lang="ts">
  import { ref, computed, watchEffect } from 'vue'
  import Plotly from 'plotly.js-basic-dist'
  import CommentDetailsOverlay from '@/components/CommentDetailsOverlay.vue'
  import CommentDetailsModal from '@/components/CommentDetailsModal.vue'
  import DatasetInfoOverlay from '@/components/DatasetInfoOverlay.vue'
  import { useCommentsStore } from '@/stores/commentsStore'
  import { useCommentData } from '@/composables/useCommentData'
  import { usePlotlyConfiguration } from '@/composables/usePlotlyConfiguration'

  const chart = ref<Plotly.PlotlyHTMLElement>()
  const commentsStore = useCommentsStore()

  const {
    comment,
    tags,
    classification,
    showModal,
    mapToPlotData,
    subscribeToPlotEvents,
  } = useCommentData()

  const { plotLayout, plotConfig, getPlotDataDefaults } =
    usePlotlyConfiguration()

  const plotData = computed<Plotly.Data[]>(() => {
    const notToxic = {
      ...getPlotDataDefaults('notToxic'),
      ...mapToPlotData(commentsStore.notToxic),
    } as Plotly.Data

    const toxic = {
      ...getPlotDataDefaults('toxic'),
      ...mapToPlotData(commentsStore.toxic),
    } as Plotly.Data

    const userAdded = {
      ...getPlotDataDefaults('user'),
      ...mapToPlotData(commentsStore.userComments),
    } as Plotly.Data

    const result = [notToxic, toxic]

    if (commentsStore.filter !== 'all') {
      const filtered = {
        ...getPlotDataDefaults({ filter: commentsStore.filter }),
        ...mapToPlotData(commentsStore.filtered),
      } as Plotly.Data

      result.push(filtered)
    }

    result.push(userAdded)

    return result
  })

  watchEffect(async () => {
    if (chart.value) {
      const plot = await Plotly.newPlot(
        chart.value,
        plotData.value,
        plotLayout,
        plotConfig
      )
      subscribeToPlotEvents(plot)
      Plotly.relayout(plot, {
        'xaxis.autorange': true,
        'yaxis.autorange': true,
      })
    }
  })
</script>

<style lang="scss" scoped>
  .chart {
    height: 100%;
    margin: auto;
  }
</style>
