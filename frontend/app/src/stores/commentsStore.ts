import { defineStore } from 'pinia'
import axios from 'axios'
import type { Comment, Subclass, ReductionModel, DatasetInfo } from '@/models'

const apiUrl = import.meta.env.VITE_APP_API_URL

export type CommentState = {
  comments: Comment[]
  userComments: Comment[]
  filter: 'all' | Subclass
  loading: boolean
  dataset: null | DatasetInfo
  sampleRange: [number, number]
}

export const useCommentsStore = defineStore('comments', {
  state: () => {
    return {
      comments: [],
      userComments: [],
      filter: 'all',
      loading: false,
      dataset: null,
      sampleRange: [0, 0],
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
      stop: number,
      clearUserComments: boolean = true
    ) {
      if (!dataset || !method) return
      this.loading = true

      const datasetChanged =
        this.dataset?.name !== dataset || this.dataset.reductionModel !== method

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
          this.comments = []
          if (datasetChanged) {
            this.dataset = {
              name: dataset,
              reductionModel: method,
              samplesCount: stop - start,
            }
            if (clearUserComments) {
              this.clearUserComments()
            } else {
              const userAdded = this.userComments.map((c) => {
                return c.text
              })
              this.clearUserComments()
              await this.addComments(dataset, method, userAdded)
              this.loading = true
            }
          }
          this.sampleRange = [start, stop]
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

    async addComments(
      dataset: string,
      reductionMethod: ReductionModel,
      comments: string[]
    ) {
      this.loading = true

      try {
        const response = await axios.post(
          '/classification/',
          {
            datasetName: dataset,
            availableReductionModel: reductionMethod,
            textSamples: comments,
          },
          {
            baseURL: apiUrl,
          }
        )

        if (response.status === 200 && isCommentArray(response.data)) {
          const results = response.data.map((c) => {
            return {
              ...c,
              id: tinySimpleHash(c.text),
            }
          })
          this.userComments.push(...results)
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
    'id' in value &&
    'text' in value &&
    'position' in value &&
    'classification' in value
  )
}

function tinySimpleHash(s: string) {
  for (var i = 0, h = 9; i < s.length; )
    h = Math.imul(h ^ s.charCodeAt(i++), 9 ** 9)
  return ((h ^ (h >>> 9)) >>> 0).toString(16).padStart(8, '0')
}
