export enum ItemType {
    Empty = "empty",
    RampRight = "ramp_right",
    RampLeft = "ramp_left",
    BitRight = "bit_right",
    BitLeft = "bit_left",
    Crossover = "crossover",
    Intercept = "interceptor",
    Invalid = "invalid",
    GraySpace = "gray_space",
    BallBlue = "ball_blue",
    BallRed = "ball_red",
    LeverBlue = "lever_blue",
    LeverRed = "lever_red",
    BorderVertical = "border_vertical",
    BorderHorizontal = "border_horizontal",
    BorderDiagonalLeft = "border_diagonal_left",
    BorderDiagonalRight = "border_diagonal_right",
    CornerRight = "corner_right",
    CornerLeft = "corner_left",
    Gear = "gear",
    GearBitRight = "gear_bit_right",
    GearBitLeft = "gear_bit_left",
}

export const IMAGE_FILENAMES: Record<ItemType, string> = {
    [ItemType.Empty]: '/images/PartLocation-t.png',
    [ItemType.RampRight]: '/images/Ramp-t.png',
    [ItemType.RampLeft]: '/images/Ramp-t.png',
    [ItemType.BitRight]: '/images/Bit-t.png',
    [ItemType.BitLeft]: '/images/Bit-t.png',
    [ItemType.Crossover]: '/images/Crossover-t.png',
    [ItemType.Intercept]: '/images/Interceptor-t.png',
    [ItemType.GraySpace]:'/images/GraySpace.png',
    [ItemType.Invalid]: '',
    [ItemType.BallBlue]: '/images/blueBall.png',
    [ItemType.BallRed]: '/images/redBall.png',
    [ItemType.LeverBlue]: '/images/bluelever.png',
    [ItemType.LeverRed]: '/images/redlever.png',
    [ItemType.BorderVertical]: '/images/Side-t.png',
    [ItemType.BorderHorizontal]: '/images/Side-horizontal-t.png',
    [ItemType.BorderDiagonalLeft]: '/images/Slope-t.png',
    [ItemType.BorderDiagonalRight]: '/images/Slope-t.png',
    [ItemType.CornerLeft]: '/images/corner.png',
    [ItemType.CornerRight]: '/images/corner_right.png',
    [ItemType.Gear]: '/images/Gear-t.png',
    [ItemType.GearBitRight]: '/images/Gearbit-t.png',
    [ItemType.GearBitLeft]: '/images/Gearbit-t.png',
};

export const ITEM_COLORS: Record<ItemType, string> = {
    [ItemType.Empty]: '#ffffff',
    [ItemType.RampRight]: '#60bb46',
    [ItemType.RampLeft]: '#a9ff18',
    [ItemType.BitRight]: '#1649b2',
    [ItemType.BitLeft]: '#006fff',
    [ItemType.Crossover]: '#fa9d00',
    [ItemType.Intercept]: '#34302f',
    [ItemType.GraySpace]: '#e0e0e0',
    [ItemType.Invalid]: '#000000',
    [ItemType.BallBlue]: '#6495ED',
    [ItemType.BallRed]: '#FF7F50',
    [ItemType.LeverBlue]: '#87CEFA',
    [ItemType.LeverRed]: '#FFB6C1',
    [ItemType.BorderVertical]: '#946635',
    [ItemType.BorderHorizontal]: '#49331b',
    [ItemType.BorderDiagonalLeft]: '#88694a',
    [ItemType.BorderDiagonalRight]: '#88694a',
    [ItemType.CornerRight]: '#946635',
    [ItemType.CornerLeft]: '#946635',
    [ItemType.Gear]: '#a9ff18',
    [ItemType.GearBitLeft]: '#006fff',
    [ItemType.GearBitRight]: '#006fff',
};

export const ASCII_SYMBOLS: Record<ItemType, string> = {
    [ItemType.Empty]: '.', //
    [ItemType.RampRight]: '\\', //
    [ItemType.RampLeft]: '/',//
    [ItemType.BitRight]: 'R', //
    [ItemType.BitLeft]: 'L', //
    [ItemType.Crossover]: 'X', //
    [ItemType.Intercept]: 'I', //
    [ItemType.GraySpace]:'#', //
    [ItemType.Invalid]: 'i',
    [ItemType.BallBlue]: 'b',
    [ItemType.BallRed]: 'r',
    [ItemType.LeverBlue]: 'B', //
    [ItemType.LeverRed]: 'R', //
    [ItemType.BorderVertical]: '|', //
    [ItemType.BorderHorizontal]: '_', //
    [ItemType.BorderDiagonalLeft]: '-', //
    [ItemType.BorderDiagonalRight]: '-', //
    [ItemType.CornerLeft]: '<', //
    [ItemType.CornerRight]: '>', //
    [ItemType.Gear]: 'G', //
    [ItemType.GearBitRight]: 'GR', //
    [ItemType.GearBitLeft]: 'GL' //
};
