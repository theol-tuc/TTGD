import { Position, ItemType } from './constants';
import { Direction} from './constants';

export interface MarbleAction {
    nextRow: number;
    nextCol: number;
    nextDirection: Direction;
}

export const calculateNextPosition = (
  currentPosition: Position,
  itemType: ItemType | undefined,
  boardWidth: number,
  boardHeight: number
): Position | null => {
  // If no item, ball falls straight down
  if (!itemType) {
    return {
      x: currentPosition.x,
      y: currentPosition.y + 1
    };
  }
  switch (itemType) {
    case ItemType.Intercept:
        return {
            x: currentPosition.x,
            y: currentPosition.y
        }
    case ItemType.BitLeft:
        return {
            x: currentPosition.x + 1,
            y: currentPosition.y + 1
        }
    case ItemType.BitRight:
        return {
            x: currentPosition.x - 1,
            y: currentPosition.y + 1
        }
    case ItemType.RampLeft:
      return {
        x: currentPosition.x - 1,
        y: currentPosition.y + 1
      };
    case ItemType.RampRight:
      return {
        x: currentPosition.x + 1,
        y: currentPosition.y + 1
      };
    case ItemType.Crossover:
      return {
        x: currentPosition.x,
        y: currentPosition.y + 2
      };
    default:
      // Default fall straight down
      return {
        x: currentPosition.x,
        y: currentPosition.y + 1
      };
  }
};

export const isOutOfBounds = (
  position: Position,
  boardWidth: number,
  boardHeight: number
): boolean => {
  return (
    position.x < 0 ||
    position.x >= boardWidth ||
    position.y < 0 ||
    position.y >= boardHeight
  );
};
