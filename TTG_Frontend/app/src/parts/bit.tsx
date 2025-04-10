import { Part } from './part';
import { ItemType, Direction } from './constants';

export class Bit extends Part {
  isLeft: boolean;

  constructor(row: number, col: number, initialLeft: boolean = true) {
    super(row, col, initialLeft ? ItemType.BitLeft : ItemType.BitRight);
    this.isLeft = initialLeft;
  }

  onMarbleEnter(from: Direction): void {
    // Update the internal state (flip the bit)
    this.isLeft = !this.isLeft;
    this.type = this.isLeft ? ItemType.BitLeft : ItemType.BitRight;
  }
}
