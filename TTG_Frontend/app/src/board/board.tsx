import React, {useState, useRef, useEffect} from "react";
import { MarblePathGraph, Direction } from './marble_path';
import './board.css';

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
    // Initialize the board with the specified pattern
    const [board, setBoard] = useState<BoardCell[][]>(() => {
        const initialBoard: BoardCell[][] = Array.from({length: numRows}, () =>
            Array.from({length: numCols}, () => ({type: PartType.Empty}))
        );

        // Set invalid cells
        const invalidCells = [
            [0,0], [0,1], [0,5], [0,9], [0,10],
            [1,0], [1,10]
        ];

        // Set invalid cells in row 10
        for (let col = 0; col <= 4; col++) {
            invalidCells.push([10, col]);
        }
        for (let col = 6; col <= 10; col++) {
            invalidCells.push([10, col]);
        }

        // Apply invalid cells
        invalidCells.forEach(([row, col]) => {
            initialBoard[row][col].type = PartType.Invalid;
        });

        // Create checkerboard pattern for valid cells
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numCols; col++) {
                // Skip invalid cells
                if (initialBoard[row][col].type === PartType.Invalid) continue;

                // Create checkerboard pattern
                if ((row + col) % 2 === 0) {
                    initialBoard[row][col].type = PartType.GraySpace;
                } else {
                    initialBoard[row][col].type = PartType.Empty;
                }
            }
        }

        return initialBoard;
    });

    // Initialize the marble path graph
    const marblePathGraph = useRef<MarblePathGraph>(new MarblePathGraph(numRows, numCols));

    // Update the graph when the board changes
    useEffect(() => {
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numCols; col++) {
                marblePathGraph.current.updateNode(row, col, board[row][col].type);
            }
        }
    }, [board]);

    // Function to handle marble movement
    const moveMarble = (startRow: number, startCol: number, direction: Direction) => {
        const nextNode = marblePathGraph.current.getNextNode(startRow, startCol, direction);
        if (nextNode) {
            // Handle marble movement logic here
            console.log(`Marble moving from (${startRow},${startCol}) to (${nextNode.row},${nextNode.col})`);
        }
    };

    return (
        <div className="board-container">
            <div className="board" style={{ transform: 'rotate(90deg)' }}>
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                        {row.map((cell, colIndex) => (
                            <div
                                key={`${rowIndex}-${colIndex}`}
                                className="board-cell"
                                style={{
                                    backgroundColor: getColorForPart(cell.type),
                                    gridColumn: colIndex + 1,
                                    gridRow: rowIndex + 1
                                }}
                            />
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Board;
