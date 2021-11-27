import { Classification } from '.'
import { Position } from '.'

export interface Comment {
  text: string
  position: Position
  classification: Classification
}
