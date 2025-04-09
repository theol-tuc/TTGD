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

export const IMAGE_FILENAMES: Record<ItemType, string> = {
    [ItemType.Empty]: '/images/PartLocation-t.png',
    [ItemType.RampRight]: '/images/Ramp-t.png',
    [ItemType.RampLeft]: '/images/Ramp-t.png',
    [ItemType.BitRight]: '/images/Ramp-t.png',
    [ItemType.BitLeft]: '/images/Ramp-t.png',
    [ItemType.Crossover]: '/images/Crossover-t.png',
    [ItemType.Intercept]: '/images/Interceptor-t.png',
    [ItemType.GraySpace]: '',
    [ItemType.Invalid]: '',
    [ItemType.BallBlue]: '/images/Ball-m.png',
    [ItemType.BallRed]: '/images/Ball-m.png',
    [ItemType.LeverBlue]: '/images/Turnstile-t.png',
    [ItemType.LeverRed]: '/images/Turnstile-t.png',
    [ItemType.BorderVertical]: '/images/Side-t.png',
    [ItemType.BorderHorizontal]: '/images/Side-horizontal-t.png',
    [ItemType.BorderDiagonal]: '/images/Slope-t.png',
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
    [ItemType.BorderDiagonal]: '#88694a'
};