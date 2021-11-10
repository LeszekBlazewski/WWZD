<template>
  <div ref="chart" class="chart"></div>
</template>

<script setup lang="ts">
  import { ref, watchEffect } from 'vue'
  import Plotly from 'plotly.js-basic-dist'

  const chart = ref<HTMLElement>()

  const chartData = ref<Plotly.Data[]>([
    {
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 4, 8, 16],
      mode: 'markers',
      type: 'scatter',
    },
  ])

  watchEffect(() => {
    if (chart.value) {
      Plotly.newPlot(chart.value, chartData.value, {
        margin: { t: 0 },
      })
    }
  })
</script>

<style lang="scss" scoped>
  .chart {
    width: 800px;
    height: 600px;
    margin: auto;
  }
</style>
