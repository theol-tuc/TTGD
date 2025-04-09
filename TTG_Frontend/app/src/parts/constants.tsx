// src/constants/index.ts
export enum ItemType {
    Empty = "empty",
    RampRight = "ramp_right",
    RampLeft = "ramp_left",
    BitRight = "bit_right",
    BitLeft = "bit_left",
    Crossover = "crossover",
    Intercept = "intercept",
    Invalid = "invalid",
    GraySpace = "gray_space",
    BallBlue = "ball_blue",
    BallRed = "ball_red",
    LeverBlue = "lever_blue",
    LeverRed = "lever_red",
    BorderVertical = "border_vertical",
    BorderHorizontal = "border_horizontal",
    BorderDiagonal = "border_diagonal_left",
}

// export const IMAGE_FILENAMES: Record<ItemType, string> = {
//     [ItemType.Empty]: '/img/elements/empty.png',
//     [ItemType.RampRight]: '/img/elements/ramp_right.png',
//     [ItemType.RampLeft]: '/img/elements/ramp_left.png',
//     [ItemType.BitRight]: '/img/elements/bit_right.png',
//     [ItemType.BitLeft]: '/img/elements/bit_left.png',
//     [ItemType.Crossover]: '/img/elements/crossover.png',
//     [ItemType.Intercept]: '/img/elements/intercept.png',
//     [ItemType.GraySpace]: '/img/elements/gray_space.png',
//     [ItemType.Invalid]: '/img/elements/invalid.png',
//     [ItemType.BallBlue]: '/img/elements/ball_blue.png',
//     [ItemType.BallRed]: '/img/elements/ball_red.png',
//     [ItemType.LeverBlue]: '/img/elements/lever_blue.png',
//     [ItemType.LeverRed]: '/img/elements/lever_red.png'
//     [ItemType.BorderVertical]: '/img/elements/border.png',
//     [ItemType.BorderHorizontal]: '/img/elements/border.png',
//     [ItemType.BorderDiagonal]: '/img/elements/border.png',
//
// };

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
    [ItemType.BorderDiagonal]: '#88694a'
};