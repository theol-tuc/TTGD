import { MarbleAction } from "./marble";
import { ItemType, Direction } from "./constants";

export abstract class Part {
    constructor(public row: number, public col: number, public type: ItemType) {}
    abstract onMarbleEnter(from: Direction): MarbleAction;
  }
  