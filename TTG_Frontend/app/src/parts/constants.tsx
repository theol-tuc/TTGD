// src/constants/index.ts
import { ItemType } from './types';

export const IMAGE_FILENAMES: Record<ItemType, string> = {
  [ItemType.EMPTY]: '/img/elements/empty.png',
  [ItemType.EMPTY_GEAR_ONLY]: '/img/elements/empty_gear_only.png',
  [ItemType.RAMP_GOING_LEFT]: '/img/elements/ramp_going_left.png',
  [ItemType.RAMP_GOING_RIGHT]: '/img/elements/ramp_going_right.png',
  [ItemType.BIT_POINTING_LEFT]: '/img/elements/bit_pointing_left.png',
  [ItemType.BIT_POINTING_RIGHT]: '/img/elements/bit_pointing_right.png',
  [ItemType.GEAR_BIT_POINTING_LEFT]: '/img/elements/gear_bit_pointing_left.png',
  [ItemType.GEAR_BIT_POINTING_RIGHT]: '/img/elements/gear_bit_pointing_right.png',
  [ItemType.GEAR]: '/img/elements/gear.png',
  [ItemType.CROSS_OVER]: '/img/elements/crossover.png',
  [ItemType.INTER_CEPTER]: '/img/elements/interceptor.png',
  [ItemType.SPAWN_BALL_BLUE]: '/img/elements/releaser_blue.png',
  [ItemType.SPAWN_BALL_RED]: '/img/elements/releaser_red.png',
  [ItemType.LEVER_BLUE]: '/img/elements/lever_blue.png',
  [ItemType.LEVER_RED]: '/img/elements/lever_red.png',
};

export const ITEM_COLORS: Record<ItemType, string> = {
  [ItemType.EMPTY]: '#FFFFFF', // white
  [ItemType.EMPTY_GEAR_ONLY]: '#FFFFFF', // white
  [ItemType.RAMP_GOING_LEFT]: '#008000', // green
  [ItemType.RAMP_GOING_RIGHT]: '#006400', // darkGreen
  [ItemType.BIT_POINTING_LEFT]: '#0000FF', // blue
  [ItemType.BIT_POINTING_RIGHT]: '#00008B', // darkBlue
  [ItemType.GEAR_BIT_POINTING_LEFT]: '#FF0000', // red
  [ItemType.GEAR_BIT_POINTING_RIGHT]: '#8B0000', // darkRed
  [ItemType.GEAR]: '#FF00FF', // magenta
  [ItemType.CROSS_OVER]: '#FFFF00', // yellow
  [ItemType.INTER_CEPTER]: '#808080', // gray
  [ItemType.SPAWN_BALL_BLUE]: '#6495ED', // cornflowerblue
  [ItemType.SPAWN_BALL_RED]: '#FF7F50', // coral
  [ItemType.LEVER_BLUE]: '#87CEFA', // lightskyblue
  [ItemType.LEVER_RED]: '#FFB6C1', // lightpink
};

export const hasGear = (item: ItemType): boolean => {
  return (
    item === ItemType.GEAR ||
    item === ItemType.GEAR_BIT_POINTING_LEFT ||
    item === ItemType.GEAR_BIT_POINTING_RIGHT
  );
};