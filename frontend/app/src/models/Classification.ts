import type { Prediction } from '@/models'

export interface Classification {
  toxic: Prediction
  severeToxic: Prediction
  obscene: Prediction
  threat: Prediction
  insult: Prediction
  identityHate: Prediction
}

export type Subclass =
  | 'severeToxic'
  | 'obscene'
  | 'threat'
  | 'insult'
  | 'identityHate'

export const SubclassLabels = {
  severeToxic: 'Severe toxic',
  obscene: 'Obscene',
  threat: 'Threat',
  insult: 'Insult',
  identityHate: 'Identity hate',
}

export const ClassLabels = {
  good: 'Good',
  toxic: 'Toxic',
  ...SubclassLabels,
}
