import { defineStore } from 'pinia'
import axios from 'axios'
import type { Comment, Subclass, ReductionModel } from '@/models'

const apiUrl = import.meta.env.VITE_APP_API_URL

export type CommentState = {
  comments: Comment[]
  userComments: Comment[]
  filter: 'all' | Subclass
  loading: boolean
}

export const useCommentsStore = defineStore('comments', {
  state: () => {
    return {
      comments: [],
      userComments: [],
      filter: 'all',
      loading: false,
    } as CommentState
  },
  getters: {
    notToxic: (state) =>
      state.comments.filter((x) => !x.classification.toxic.assigned),
    allToxic: (state) =>
      state.comments.filter((x) => x.classification.toxic.assigned),
    toxic: (state) =>
      state.comments.filter(
        (x) =>
          x.classification.toxic.assigned &&
          (state.filter === 'all' || !x.classification[state.filter].assigned)
      ),
    filtered: (state) =>
      state.comments.filter(
        (x) => state.filter !== 'all' && x.classification[state.filter].assigned
      ),
  },
  actions: {
    setFilter(filter: 'all' | Subclass) {
      this.filter = filter
    },

    async loadComments(
      dataset: string,
      method: ReductionModel,
      start: number,
      stop: number
    ) {
      if (!dataset || !method) return
      this.loading = true
      try {
        const response = await axios.get(`/datasets/${dataset}`, {
          baseURL: apiUrl,
          params: {
            availableReductionModel: method,
            start,
            stop,
          },
        })

        if (response.status === 200 && isCommentArray(response.data)) {
          this.comments = response.data
        } else {
          throw new Error('Invalid response')
        }
      } catch (error) {
        console.log(error)
        console.error(error)
        console.error('Error loading comments')
      }
      this.loading = false
    },

    // async loadHardcodedComments(algo: 'pca' | 'tsne' = 'tsne') {
    //   this.loading = true
    //   switch (algo) {
    //     case 'pca':
    //       this.comments = (await import('@/assets/samples_pca.json')).default
    //       break
    //     case 'tsne':
    //       this.comments = (await import('@/assets/samples_tsne.json')).default
    //       break
    //   }
    //   this.loading = false
    // },

    async addComment(
      dataset: string,
      reductionMethod: ReductionModel,
      comment: string
    ) {
      this.loading = true

      try {
        const response = await axios.post(
          '/classification/',
          {
            datasetName: dataset,
            availableReductionModel: reductionMethod,
            textSamples: [comment],
          },
          {
            baseURL: apiUrl,
          }
        )

        if (response.status === 200 && isCommentArray(response.data)) {
          this.userComments.push(...response.data)
        } else {
          throw new Error('Invalid response')
        }
      } catch (error) {
        console.error('Error adding new comment', error)
      }

      this.loading = false
    },

    clearUserComments() {
      this.userComments = []
    },
  },
})

function isCommentArray(value: unknown): value is Comment[] {
  if (Array.isArray(value)) {
    return value.every((item) => {
      return instanceOfComment(item)
    })
  }
  return false
}

function instanceOfComment(value: object): value is Comment {
  return (
    !!value &&
    'text' in value &&
    'position' in value &&
    'classification' in value
  )
}
