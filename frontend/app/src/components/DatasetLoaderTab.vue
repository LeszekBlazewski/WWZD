<template>
  <n-divider style="margin: 0" />

  <p>Dataset</p>
  <n-select v-model:value="selDataset" :options="datasetsStore.datasetNames" />

  <p>Feature reduction method</p>
  <n-select
    v-model:value="selModel"
    :options="modelOpts"
    :disabled="!modelOpts.length"
  />

  <n-spin size="small" :show="datasetsStore.loading">
    <n-button size="large" @click="loadDataset" :disabled="selModel === ''">
      Load dataset
    </n-button>
  </n-spin>

  <n-divider style="margin: 30px 0 10px" />

  <p>Number of samples</p>
  <n-slider
    v-model:value="sliderVals"
    :step="100"
    :min="0"
    :max="datasetsStore.selectedDataset?.samplesCount ?? 20000"
    :disabled="samplePickerDisabled"
    range
  />

  <n-grid style="margin-bottom: 30px" :x-gap="12" :y-gap="8" :cols="3">
    <n-grid-item>
      <p class="label">Start</p>
    </n-grid-item>
    <n-grid-item :span="2">
      <n-input-number
        v-model:value="sampleFrom"
        :min="0"
        :max="sampleTo - 1"
        :disabled="samplePickerDisabled"
      />
    </n-grid-item>
    <n-grid-item>
      <p class="label">End</p>
    </n-grid-item>
    <n-grid-item :span="2">
      <n-input-number
        v-model:value="sampleTo"
        :min="sampleFrom + 1"
        :max="datasetsStore.selectedDataset?.samplesCount ?? 20000"
        :disabled="samplePickerDisabled"
      />
    </n-grid-item>
    <n-grid-item>
      <p class="label">Samples</p>
    </n-grid-item>
    <n-grid-item :span="2">
      <n-input-number
        v-model:value="numberOfSamples"
        :show-button="false"
        disabled
      />
    </n-grid-item>
  </n-grid>

  <n-spin size="small" :show="commentsStore.loading">
    <n-button
      size="large"
      @click="loadSamples"
      :disabled="samplePickerDisabled"
    >
      Load samples
    </n-button>
  </n-spin>

  <n-modal
    v-model:show="showModal"
    preset="dialog"
    title="Warning"
    content="Selected range exceeds 20 000 samples. It might have detrimental effect on the chart performance. Are you sure?"
    positive-text="Yes"
    @positive-click="loadSamplesCallback"
    negative-text="No"
  />
</template>

<script lang="ts" setup>
  import { onMounted, ref, watch, computed } from 'vue'
  import {
    NSelect,
    NButton,
    NDivider,
    NSlider,
    NModal,
    NSpin,
    NInputNumber,
    NGrid,
    NGridItem,
  } from 'naive-ui'
  import { useCommentsStore } from '@/stores/commentsStore'
  import { useDatasetsStore } from '@/stores/datasetsStore'
  import type { SelectMixedOption } from 'naive-ui/lib/select/src/interface'
  import type { ReductionModel } from '@/models'

  const commentsStore = useCommentsStore()
  const datasetsStore = useDatasetsStore()

  const selDataset = ref('')
  const selModel = ref('')
  const sliderVals = ref<[number, number]>([0, 5000])
  const modelOpts = ref<SelectMixedOption[]>([])
  const showModal = ref(false)

  const sampleFrom = ref(0)
  const sampleTo = ref(5000)

  const samplePickerDisabled = computed(() => {
    return !datasetsStore.selectedDataset
  })

  const sampleRange = computed(() => {
    return [...sliderVals.value].sort((a, b) => {
      return a - b
    })
  })

  watch([sampleFrom, sampleTo], ([newFrom, newTo]) => {
    if (
      !sliderVals.value.includes(newFrom) ||
      !sliderVals.value.includes(newTo)
    ) {
      sliderVals.value = [newFrom, newTo]
    }
  })

  watch(sampleRange, ([newFrom, newTo]) => {
    if (sampleFrom.value !== newFrom) {
      sampleFrom.value = newFrom
    }
    if (sampleTo.value !== newTo) {
      sampleTo.value = newTo
    }
  })

  const numberOfSamples = computed(() => {
    const [from, to] = sampleRange.value
    return to - from
  })

  watch(selDataset, (datasetName) => {
    const dataset = datasetsStore.datasets.find((x) => x.name === datasetName)
    if (dataset) {
      const options = Array.from(dataset.availableReductionModels)
      modelOpts.value = options.map((mdl) => {
        return {
          label: mdl,
          value: mdl,
        }
      })
    }
  })

  onMounted(async () => {
    await datasetsStore.loadDatasets()
  })

  const loadDataset = () => {
    if (!selDataset.value || !selModel.value) return

    datasetsStore.selectDataset(
      selDataset.value,
      selModel.value as ReductionModel
    )
  }

  const loadSamples = () => {
    if (!datasetsStore.selectedDataset) return

    if (sampleRange.value[1] - sampleRange.value[0] > 20000) {
      showModal.value = true
    } else {
      loadSamplesCallback()
    }
  }

  const loadSamplesCallback = () => {
    if (!datasetsStore.selectedDataset) return
    commentsStore.loadComments(
      datasetsStore.selectedDataset.name,
      datasetsStore.selectedDataset.reductionModel,
      sampleRange.value[0],
      sampleRange.value[1]
    )
  }
</script>

<style lang="scss" scoped>
  p {
    font-size: 1rem;
    font-weight: 700;
  }

  .n-select {
    margin-bottom: 30px;
  }

  .n-slider {
    margin-bottom: 30px;
  }

  .n-input-number {
    display: inline;
    max-width: 50%;
  }

  .label {
    margin: 3px 0 0 0;
    text-align: left;
  }
</style>
