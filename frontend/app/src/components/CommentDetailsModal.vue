<template>
  <n-modal
    :style="{
      maxWidth: '50%',
      width: 'auto',
      textAlign: 'justify',
      whiteSpace: 'pre-line',
    }"
    bordered
    preset="card"
    size="huge"
  >
    {{ props.content }}

    <n-divider />

    <n-table v-if="props.classification != null">
      <thead>
        <tr>
          <th>Class</th>
          <th>Probability</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="[name, value] in sortedClasses">
          <td>{{ name }}</td>
          <td>{{ value }}%</td>
        </tr>
      </tbody>
    </n-table>
  </n-modal>
</template>

<script lang="ts" setup>
  import { computed } from 'vue'
  import { NModal, NTable, NDivider } from 'naive-ui'
  import type { Classification, Prediction } from '@/models'

  interface Props {
    content: string
    classification: Classification | null
  }

  const props = withDefaults(defineProps<Props>(), {
    content: '',
    classification: null,
  })

  const sortedClasses = computed(() => {
    return Object.entries(props.classification)
      .map(([key, value]) => {
        return [key, value.prediction]
      })
      .sort(([aKey, aVal], [bKey, bVal]) => {
        return bVal - aVal
      })
  })
</script>
