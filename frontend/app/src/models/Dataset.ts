export interface Dataset {
  name: string
  availableReductionModels: Set<ReductionModel>
}

export interface DatasetInfo {
  name: string
  samplesCount: number
  reductionModel: ReductionModel
}

export type ReductionModel = 'pca' | 'umap'
