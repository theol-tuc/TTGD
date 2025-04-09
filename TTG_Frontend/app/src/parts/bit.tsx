import { Part } from './part';
import { ItemType, Direction } from './constants';
import { MarbleAction } from './marble';

export class Bit extends Part {
  isLeft: boolean;

  constructor(row: number, col: number, initialLeft: boolean = true) {
    const initialType = initialLeft ? ItemType.BitLeft : ItemType.BitRight;
    super(row, col, initialType);
    this.isLeft = initialLeft;
  }

  onMarbleEnter(from: Direction): MarbleAction {
    const nextDirection = this.isLeft ? 'left' : 'right';

    // Flip the bit
    this.isLeft = !this.isLeft;

    // Update the type after flipping
    this.type = this.isLeft
      ? ItemType.BitLeft
      : ItemType.BitRight;

    return {
      nextRow: this.row + 1,
      nextCol: nextDirection === 'left' ? this.col - 1 : this.col + 1,
      nextDirection,
    };
  }
}
