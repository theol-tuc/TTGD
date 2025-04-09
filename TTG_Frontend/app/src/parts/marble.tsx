import { Position, ItemType } from './types';

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

  // Define movement patterns for different items
  switch (itemType) {
    case ItemType.RAMP_GOING_LEFT:
      return {
        x: currentPosition.x - 1,
        y: currentPosition.y + 1
      };
    case ItemType.RAMP_GOING_RIGHT:
      return {
        x: currentPosition.x + 1,
        y: currentPosition.y + 1
      };
    case ItemType.CROSS_OVER:
      return {
        x: currentPosition.x,
        y: currentPosition.y + 2
      };
    case ItemType.GEAR:
      // Gear changes ball direction
      return {
        x: currentPosition.x,
        y: currentPosition.y + 1
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