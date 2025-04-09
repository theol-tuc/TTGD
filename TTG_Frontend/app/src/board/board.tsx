//put the board and its functions here
import React, {useState, useRef} from "react";


export enum PartType {
    RampRight = "ramp_right",
    RampLeft = "ramp_left",
    BitRight = "bit_right",
    BitLeft = "bit_left",
    Crossover = "crossover",
    Intercept = "intercept",
    Invalid = "invalid",
    GraySpace = "gray_space", //space where only gears can be placed
    Empty = "empty",
}

export type BoardCell = {
    type: PartType;
};

const numRows = 11;
const numCols = 11;


const getColorForPart = (type: PartType): string => {
    switch (type) {
        case PartType.RampRight: return "#60bb46";
        case PartType.RampLeft:  return "#a9ff18";
        case PartType.BitRight:  return "#1649b2";
        case PartType.BitLeft:   return "#006fff";
        case PartType.Crossover: return "#fa9d00";
        case PartType.Intercept: return "#34302f";
        case PartType.GraySpace: return "#e0e0e0";
        case PartType.Invalid: return "#000000";
        case PartType.Empty: return "#ffffff";
    }
};


const Board: React.FC = () => {
    // Initialize the board with empty cells
    const initialBoard: BoardCell[][] = Array.from({length: numRows}, () =>
        Array.from({length: numCols}, () => ({type: PartType.Empty}))
    );
    return(
        <div className="board">

        </div>
    );
}


