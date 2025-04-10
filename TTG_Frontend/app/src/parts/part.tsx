import { Direction, ItemType } from "./constants";

export abstract class Part {
    constructor(public row: number, public col: number, public type: ItemType) {}
    abstract onMarbleEnter(from: Direction): void; // No return value
}
