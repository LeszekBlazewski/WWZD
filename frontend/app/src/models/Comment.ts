import { Classification } from '.'
import { Position } from '.'

export interface Comment {
  id: string
  text: string
  position: Position
  classification: Classification
}
