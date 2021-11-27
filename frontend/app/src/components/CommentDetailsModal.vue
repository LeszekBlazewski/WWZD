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
        <tr v-for="(value, name) in props.classification">
          <td>{{ name }}</td>
          <td>{{ value.prediction }}%</td>
        </tr>
      </tbody>
    </n-table>
  </n-modal>
</template>

<script lang="ts" setup>
  import { NModal, NTable, NDivider } from 'naive-ui'
  import type { Classification } from '@/models'

  interface Props {
    content: string
    classification: Classification | null
  }

  const props = withDefaults(defineProps<Props>(), {
    content: '',
  })
</script>
