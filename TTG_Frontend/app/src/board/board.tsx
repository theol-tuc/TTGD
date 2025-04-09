import React, {useState, useRef, useEffect} from "react";
import { MarblePathGraph, Direction } from '../parts/marble_path';
import { ItemType, ITEM_COLORS } from '../parts/constants';
import { IMAGE_FILENAMES } from '../parts/constants';
import './board.css';

export type BoardCell = {
    type: ItemType;
};

const numRows = 17;
const numCols = 15;

const Board: React.FC = () => {
    const [board, setBoard] = useState<BoardCell[][]>(() => {
        const initialBoard: BoardCell[][] = Array.from({length: numRows}, () =>
            Array.from({length: numCols}, () => ({type: ItemType.Empty}))
        );

        // Set vertical borders (first and last columns)
        for (let row = 0; row < numRows; row++) {
            initialBoard[row][0].type = ItemType.BorderVertical;
            initialBoard[row][numCols - 1].type = ItemType.BorderVertical;
        }

        // Set horizontal border (last row)
        for (let col = 0; col < numCols; col++) {
            initialBoard[numRows - 1][col].type = ItemType.BorderHorizontal;
        }

        // Set invalid cells and diagonal borders for each row
        // Row 1 (index 0)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || (col >= 3 && col <= 11) || col === 13) {
                initialBoard[0][col].type = ItemType.Invalid;
            } else if (col === 2 ) {
                initialBoard[0][col].type = ItemType.BorderDiagonalLeft;
            }
            else if (col === 12) {
                initialBoard[0][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 2 (index 1)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || col === 2 || (col >= 4 && col <= 10) || col === 12 || col === 13) {
                initialBoard[1][col].type = ItemType.Invalid;
            } else if (col === 3 ) {
                initialBoard[1][col].type = ItemType.BorderDiagonalLeft;
            }
            else if (col === 11) {
                initialBoard[1][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 3 (index 2)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || col === 2 || col === 3 || (col >= 5 && col <= 9) || col === 11 || col === 12 || col === 13) {
                initialBoard[2][col].type = ItemType.Invalid;
            } else if (col === 4 ) {
                initialBoard[2][col].type = ItemType.BorderDiagonalLeft;
            }
            else if (col === 4 || col === 10) {
                initialBoard[2][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 4 (index 3)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || col === 2 || col === 3 || col === 7 || col === 12 || col === 13 || col === 11) {
                initialBoard[3][col].type = ItemType.Invalid;
            }
        }

        // Row 5 (index 4)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 2 || col === 1 || col === 13 || col === 12) {
                initialBoard[4][col].type = ItemType.Invalid;
            }
        }

        // Rows 6-13 (indices 5-12)
        for (let row = 5; row <= 12; row++) {
            initialBoard[row][1].type = ItemType.Invalid;
            initialBoard[row][13].type = ItemType.Invalid;
        }

        // Row 14 (index 13)
        for (let col = 1; col < numCols - 1; col++) {
            if ((col >= 1 && col <= 6) || (col >= 8 && col <= 13)) {
                initialBoard[13][col].type = ItemType.Invalid;
            }
        }

        // Row 15 (index 14)
        for (let col = 1; col < numCols - 1; col++) {
            if ((col >= 1 && col <= 5) || (col >= 9 && col <= 13)) {
                initialBoard[14][col].type = ItemType.Invalid;
            }
        }
        initialBoard[14][6].type = ItemType.LeverBlue;
        initialBoard[14][8].type = ItemType.LeverRed;

        // Row 16 (index 15)
        for (let col = 1; col < numCols - 1; col++) {
            if (col >= 1 && col <= 13) {
                initialBoard[15][col].type = ItemType.Invalid;
            }
        }

        // Create checkerboard pattern for remaining cells
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numCols; col++) {
                // Skip if cell is already set
                if (initialBoard[row][col].type !== ItemType.Empty) continue;

                // Create checkerboard pattern
                if ((row + col) % 2 === 0) {
                    initialBoard[row][col].type = ItemType.Empty;
                } else {
                    initialBoard[row][col].type = ItemType.GraySpace;
                }
            }
        }
        initialBoard[14][7].type = ItemType.Invalid;

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

    return(
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="board-row">
                    {row.map((cell, colIndex) => {
                        const imagePath = IMAGE_FILENAMES[cell.type];
                        console.log(`Cell (${rowIndex},${colIndex}) type: ${cell.type}, image path: ${imagePath}`);

                        return (
                            <div
                                key={`${rowIndex}-${colIndex}`}
                                className="board-cell"
                                style={{
                                    gridColumn: colIndex + 1,
                                    gridRow: rowIndex + 1,
                                    backgroundColor: cell.type === ItemType.GraySpace ? '#e0e0e0' : 'white'
                                }}
                                title={`${cell.type} (${rowIndex},${colIndex})`}
                            >
                                {cell.type !== ItemType.GraySpace && imagePath && (
                                    <img
                                        src={imagePath}
                                        alt={cell.type}
                                        className="cell-image"
                                        onError={(e) => {
                                            console.error(`Failed to load image for ${cell.type} at path: ${imagePath}`);
                                            (e.target as HTMLImageElement).style.display = 'none';
                                        }}
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>
            ))}
        </div>
    );
}

export default Board;