import React from "react";
import { BoardCell } from "./board";

interface BoardCellComponentProps {
    cell: BoardCell;
    rowIndex: number;
    colIndex: number;
    onCellClick: (row: number, col: number) => void;
    getColorForPart: (type: string) => string;
}


