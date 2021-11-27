import { ref, reactive, watch } from 'vue'
import { SubclassLabels } from '@/models'
import type { Classification, Subclass } from '@/models'

export function useClassSelection(limit = 1) {
  const selection = ref<string[]>([])

  const select = (value: string) => {
    if (value in SubclassLabels) {
      if (selection.value.length < limit) {
        selection.value.push(value)
      } else {
        selection.value.shift()
        selection.value.push(value)
      }
    }
  }

  const clearSelection = () => {
    selection.value = []
  }

  const classFilter = reactive<Classification>({
    toxic: false,
    severeToxic: false,
    obscene: false,
    threat: false,
    insult: false,
    identityHate: false,
  })

  watch(
    selection,
    (selected) => {
      for (const key in classFilter) {
        classFilter[key as Subclass] = selected.includes(key)
      }
    },
    {
      deep: true,
    }
  )

  return {
    selection,
    select,
    clearSelection,
    classFilter,
  }
}
