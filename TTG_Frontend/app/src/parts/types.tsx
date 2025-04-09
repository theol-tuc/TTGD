export enum ItemType {
    EMPTY = 'EMPTY',
    EMPTY_GEAR_ONLY = 'EMPTY_GEAR_ONLY',
    RAMP_GOING_LEFT = 'RAMP_GOING_LEFT',
    RAMP_GOING_RIGHT = 'RAMP_GOING_RIGHT',
    BIT_POINTING_LEFT = 'BIT_POINTING_LEFT',
    BIT_POINTING_RIGHT = 'BIT_POINTING_RIGHT',
    GEAR_BIT_POINTING_LEFT = 'GEAR_BIT_POINTING_LEFT',
    GEAR_BIT_POINTING_RIGHT = 'GEAR_BIT_POINTING_RIGHT',
    GEAR = 'GEAR',
    CROSS_OVER = 'CROSS_OVER',
    INTER_CEPTER = 'INTER_CEPTER',
    SPAWN_BALL_BLUE = 'SPAWN_BALL_BLUE',
    SPAWN_BALL_RED = 'SPAWN_BALL_RED',
    LEVER_BLUE = 'LEVER_BLUE',
    LEVER_RED = 'LEVER_RED',
  }
  
  export interface Position {
    x: number;
    y: number;
  }
  
  export interface BoardItem {
    id: string;
    type: ItemType;
    position: Position;
    rotation: number;
  }
  
  export interface Ball {
    id: string;
    color: 'BLUE' | 'RED';
    position: Position;
  }
