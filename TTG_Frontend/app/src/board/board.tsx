import React, { useEffect, useRef, useState } from "react";
import { Direction, MarblePathGraph } from "../parts/marble_path";
import { IMAGE_FILENAMES, ItemType } from "../parts/constants";
import "./board.css";

export type BoardCell = {
    type: ItemType;
};

const numRows = 17;
const numCols = 15;

const Board: React.FC = () => {
    // Initialize the board with a function that sets up all cells.
    const [board, setBoard] = useState<BoardCell[][]>(() => {
        const initialBoard: BoardCell[][] = Array.from({ length: numRows }, () =>
            Array.from({ length: numCols }, () => ({ type: ItemType.Empty }))
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

        // Row 1 (index 0)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || (col >= 3 && col <= 11) || col === 13) {
                initialBoard[0][col].type = ItemType.Invalid;
            } else if (col === 2) {
                initialBoard[0][col].type = ItemType.BorderDiagonalLeft;
            } else if (col === 12) {
                initialBoard[0][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 2 (index 1)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || col === 2 || (col >= 4 && col <= 10) || col === 12 || col === 13) {
                initialBoard[1][col].type = ItemType.Invalid;
            } else if (col === 3) {
                initialBoard[1][col].type = ItemType.BorderDiagonalLeft;
            } else if (col === 11) {
                initialBoard[1][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 3 (index 2)
        for (let col = 1; col < numCols - 1; col++) {
            if (
                col === 1 ||
                col === 2 ||
                col === 3 ||
                (col >= 5 && col <= 9) ||
                col === 11 ||
                col === 12 ||
                col === 13
            ) {
                initialBoard[2][col].type = ItemType.Invalid;
            } else if (col === 4) {
                initialBoard[2][col].type = ItemType.BorderDiagonalLeft;
            } else if (col === 4 || col === 10) {
                initialBoard[2][col].type = ItemType.BorderDiagonalRight;
            }
        }

        // Row 4 (index 3)
        for (let col = 1; col < numCols - 1; col++) {
            if (
                col === 1 ||
                col === 2 ||
                col === 3 ||
                col === 7 ||
                col === 12 ||
                col === 13 ||
                col === 11
            ) {
                initialBoard[3][col].type = ItemType.Invalid;
            }
        }

        // Row 5 (index 4)
        for (let col = 1; col < numCols - 1; col++) {
            if (col === 1 || col === 2 || col === 13 || col === 12) {
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

        // Create checkerboard pattern for remaining cells.
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numCols; col++) {
                if (initialBoard[row][col].type !== ItemType.Empty) continue;
                initialBoard[row][col].type = (row + col) % 2 === 0 ? ItemType.Empty : ItemType.GraySpace;
            }
        }

        initialBoard[14][7].type = ItemType.Invalid;
        initialBoard[16][0].type = ItemType.CornerLeft;
        initialBoard[16][14].type = ItemType.CornerRight;

        return initialBoard;
    });

    // Marble path graph setup.
    const marblePathGraph = useRef<MarblePathGraph>(new MarblePathGraph(numRows, numCols));
    useEffect(() => {
        for (let row = 0; row < numRows; row++) {
            for (let col = 0; col < numCols; col++) {
                marblePathGraph.current.updateNode(row, col, board[row][col].type);
            }
        }
    }, [board]);

    // Helper function to deep clone the board.
    const cloneBoard = (board: BoardCell[][]): BoardCell[][] =>
        board.map((row) => row.map((cell) => ({ ...cell })));

    // Only interactive types (for clicks) include bits and ramps.
    const handleCellClick = (row: number, col: number) => {
        setBoard((prevBoard) => {
            const newBoard = cloneBoard(prevBoard);
            const cell = newBoard[row][col];
            switch (cell.type) {
                case ItemType.BitLeft:
                    cell.type = ItemType.BitRight;
                    break;
                case ItemType.BitRight:
                    cell.type = ItemType.BitLeft;
                    break;
                case ItemType.RampLeft:
                    cell.type = ItemType.RampRight;
                    break;
                case ItemType.RampRight:
                    cell.type = ItemType.RampLeft;
                    break;
                default:
                    return prevBoard;
            }
            return newBoard;
        });
    };

    // List of types that should not be draggable.
    const nonDraggableTypes = [
        ItemType.LeverBlue,
        ItemType.LeverRed,
        ItemType.BorderVertical,
        ItemType.BorderHorizontal,
        ItemType.BorderDiagonalLeft,
        ItemType.BorderDiagonalRight,
        ItemType.CornerRight,
        ItemType.CornerLeft,
        ItemType.Empty,
        ItemType.GraySpace,
        ItemType.Invalid,
    ];
    const isDraggable = (type: ItemType): boolean => !nonDraggableTypes.includes(type);

    const handleDragStart = (e: React.DragEvent, row: number, col: number) => {
        const cell = board[row][col];
        if (isDraggable(cell.type)) {
            e.dataTransfer.setData("text/plain", cell.type);
            e.dataTransfer.setData("source-row", row.toString());
            e.dataTransfer.setData("source-col", col.toString());
        } else {
            e.preventDefault();
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    // When dropping on a cell in the board.
    const handleDrop = (e: React.DragEvent, row: number, col: number) => {
        e.preventDefault();
        e.stopPropagation();
        const itemType = e.dataTransfer.getData("text/plain") as ItemType;
        const sourceRow = parseInt(e.dataTransfer.getData("source-row"));
        const sourceCol = parseInt(e.dataTransfer.getData("source-col"));

        // Allow drop only if the target cell is empty and the dragged item is draggable.
        if (board[row][col].type === ItemType.Empty && isDraggable(itemType)) {
            setBoard((prevBoard) => {
                const newBoard = cloneBoard(prevBoard);
                // Clear the source cell.
                if (!isNaN(sourceRow) && !isNaN(sourceCol)) {
                    newBoard[sourceRow][sourceCol].type = ItemType.Empty;
                }
                newBoard[row][col].type = itemType;
                return newBoard;
            });
        }
    };

    // When an item is dropped on the container (outside of any specific cell),
    // clear the source cell so that the item “disappears.”
    const handleContainerDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        const sourceRow = parseInt(e.dataTransfer.getData("source-row"));
        const sourceCol = parseInt(e.dataTransfer.getData("source-col"));
        if (!isNaN(sourceRow) && !isNaN(sourceCol)) {
            setBoard((prevBoard) => {
                const newBoard = cloneBoard(prevBoard);
                newBoard[sourceRow][sourceCol].type = ItemType.Empty;
                return newBoard;
            });
        }
    };

    return (
        <div
            className="board-container"
            onDragOver={handleDragOver}
            onDrop={handleContainerDrop}
        >
            <div className="board">
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                        {row.map((cell, colIndex) => {
                            const imagePath = IMAGE_FILENAMES[cell.type];
                            const draggable = isDraggable(cell.type);
                            // Make cell interactive if it is a bit, ramp, or draggable.
                            const isInteractive =
                                cell.type === ItemType.BitLeft ||
                                cell.type === ItemType.BitRight ||
                                cell.type === ItemType.RampLeft ||
                                cell.type === ItemType.RampRight ||
                                draggable;
                            return (
                                <div
                                    key={`${rowIndex}-${colIndex}`}
                                    className="board-cell"
                                    style={{
                                        gridColumn: colIndex + 1,
                                        gridRow: rowIndex + 1,
                                        cursor: isInteractive ? "move" : "default",
                                    }}
                                    title={`${cell.type} (${rowIndex},${colIndex})`}
                                    onClick={() => handleCellClick(rowIndex, colIndex)}
                                    onDragOver={handleDragOver}
                                    onDrop={(e) => handleDrop(e, rowIndex, colIndex)}
                                    draggable={draggable}
                                    onDragStart={(e) => handleDragStart(e, rowIndex, colIndex)}
                                >
                                    {imagePath && (
                                        <img
                                            src={imagePath}
                                            alt={cell.type}
                                            className="cell-image"
                                            onError={(e) => {
                                                console.error(`Failed to load image for ${cell.type} at path: ${imagePath}`);
                                                (e.target as HTMLImageElement).style.display = "none";
                                            }}
                                        />
                                    )}
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Board;
