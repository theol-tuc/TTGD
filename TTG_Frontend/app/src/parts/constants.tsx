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
    [ItemType.Empty]: 'TTG_Frontend/app/docs/images/PartLocation-t.png',
    [ItemType.RampRight]: 'TTG_Frontend/app/docs/images/Ramp-t.png',
    [ItemType.RampLeft]: 'TTG_Frontend/app/docs/images/Ramp-t.png',
    [ItemType.BitRight]: './docs/images/Ramp-t.png',
    [ItemType.BitLeft]: './docs/images/Ramp-t.png',
    [ItemType.Crossover]: './docs/images/Crossover-t.png',
    [ItemType.Intercept]: './docs/images/Interceptor-t.png',
    [ItemType.GraySpace]: '',
    [ItemType.Invalid]: '',
    [ItemType.BallBlue]: './docs/images/Ball-m.png',
    [ItemType.BallRed]: './docs/images/Ball-m.png',
    [ItemType.LeverBlue]: './docs/images/Turnstile-t.png',
    [ItemType.LeverRed]: './docs/images/Turnstile-t.png',
    [ItemType.BorderVertical]: 'TTG_Frontend/app/docs/images/Side-t.png',
    [ItemType.BorderHorizontal]: './docs/images/Side-horizontal-t.png',
    [ItemType.BorderDiagonal]: './docs/images/Slope-t.png',
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