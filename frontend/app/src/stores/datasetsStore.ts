import { defineStore } from 'pinia'
import axios from 'axios'
import { Dataset, DatasetInfo, ReductionModel } from '@/models'

const apiUrl = import.meta.env.VITE_APP_API_URL

export type DatasetState = {
  datasets: Dataset[]
  loading: boolean
  selectedDataset: null | DatasetInfo
}

export const useDatasetsStore = defineStore('datasets', {
  state: () => {
    return {
      datasets: [],
      loading: false,
      selectedDataset: null,
    } as DatasetState
  },
  getters: {
    datasetNames: (state) =>
      state.datasets.map((x) => {
        return { label: x.name, value: x.name }
      }),
  },
  actions: {
    async loadDatasets() {
      this.loading = true
      try {
        const response = await axios.get('/datasets', {
          baseURL: apiUrl,
        })

        if (response.status === 200 && isDatasetArray(response.data)) {
          this.datasets = response.data
        } else {
          throw new Error('Invalid response')
        }
      } catch (error) {
        console.error('Error loading datasets', error)
      }
      this.loading = false
    },

    async selectDataset(dataset: string, method: ReductionModel) {
      this.loading = true
      try {
        const response = await axios.post(
          '/datasets/load',
          {
            datasetName: dataset,
            availableReductionModel: method,
          },
          {
            baseURL: apiUrl,
          }
        )

        if (response.status === 200 && instanceOfDatasetInfo(response.data)) {
          this.selectedDataset = { ...response.data, reductionModel: method }
        } else {
          throw new Error('Invalid response')
        }
      } catch (error) {
        console.error('Error loading datasets', error)
      }
      this.loading = false
    },
  },
})

function isDatasetArray(value: unknown): value is Dataset[] {
  if (Array.isArray(value)) {
    return value.every((item) => {
      return instanceOfDataset(item)
    })
  }
  return false
}

function instanceOfDataset(value: object): value is Dataset {
  return !!value && 'name' in value && 'availableReductionModels' in value
}

function instanceOfDatasetInfo(value: object): value is DatasetInfo {
  return !!value && 'name' in value && 'samplesCount' in value
}
