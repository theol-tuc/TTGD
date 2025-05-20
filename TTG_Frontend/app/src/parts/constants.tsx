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
    [ItemType.Empty]: '#ffffff', // white
    [ItemType.RampRight]: '#60bb46', // green
    [ItemType.RampLeft]: '#a9ff18', // light green
    [ItemType.BitRight]: '#1649b2', // dark blue
    [ItemType.BitLeft]: '#006fff', // blue
    [ItemType.Crossover]: '#fa9d00', // orange
    [ItemType.Intercept]: '#34302f', // dark gray
    [ItemType.GraySpace]: '#e0e0e0', // light gray
    [ItemType.Invalid]: '#000000', // black
    [ItemType.BallBlue]: '#6495ED', // cornflowerblue
    [ItemType.BallRed]: '#FF7F50', // coral
    [ItemType.LeverBlue]: '#87CEFA', // lightskyblue
    [ItemType.LeverRed]: '#FFB6C1', // lightpink
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

