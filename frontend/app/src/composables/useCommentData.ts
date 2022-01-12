import { ref, watch } from 'vue'
import { ClassLabels } from '@/models'
import type {
  Classification,
  Subclass,
  Comment,
  CommentDetails,
} from '@/models'

export function useCommentData() {
  const comment = ref('')
  const tags = ref('')
  const classification = ref<Classification | null>(null)
  const showModal = ref(false)

  const getTags = (comment: Classification): string => {
    const tags = []

    if (comment.toxic.assigned === false) return ClassLabels.good

    for (const field in comment) {
      if (
        Object.prototype.hasOwnProperty.call(comment, field) &&
        comment[field as Subclass].assigned === true
      )
        tags.push(ClassLabels[field as Subclass])
    }
    return tags.join(', ')
  }

  const mapToPlotData = (comments: Comment[]): Partial<Plotly.Data> => {
    return {
      ids: comments.map((c) => c.id),
      x: comments.map((c) => c.position.x),
      y: comments.map((c) => c.position.y),
      customdata: comments.map((c) =>
        JSON.stringify({
          text: c.text,
          tags: getTags(c.classification),
          classification: c.classification,
        } as CommentDetails)
      ),
    }
  }

  const subscribeToPlotEvents = (chart: Plotly.PlotlyHTMLElement) => {
    chart.on('plotly_hover', (data) => {
      if (!data?.points || data.points.length < 1) return
      const point = data.points[0]
      const pointData = JSON.parse(point.customdata as string) as CommentDetails

      tags.value = pointData.tags
      comment.value = pointData.text
      classification.value = pointData.classification
    })

    chart.on('plotly_click', (data) => {
      if (!data?.points || data.points.length < 1) return
      const point = data.points[0]
      const pointData = JSON.parse(point.customdata as string) as CommentDetails

      tags.value = pointData.tags
      comment.value = pointData.text
      classification.value = pointData.classification
      showModal.value = true
    })

    chart.on('plotly_unhover', () => {
      if (!showModal.value) {
        tags.value = ''
        comment.value = ''
        classification.value = null
      }
    })
  }

  watch(showModal, (newVal, oldVal) => {
    if (oldVal && !newVal) {
      setTimeout(() => {
        tags.value = ''
        comment.value = ''
        classification.value = null
      }, 350)
    }
  })

  return {
    comment,
    tags,
    classification,
    showModal,
    getTags,
    mapToPlotData,
    subscribeToPlotEvents,
  }
}
