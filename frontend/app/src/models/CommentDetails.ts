import { Classification } from '@/models'

export interface CommentDetails {
  text: string
  tags: string
  classification: null | Classification
}
