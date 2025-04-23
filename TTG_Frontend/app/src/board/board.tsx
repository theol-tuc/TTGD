import React, { useEffect, useRef, useState } from "react";
import { ItemType, IMAGE_FILENAMES } from "../parts/constants";
import { Direction, MarblePathGraph } from "../parts/marble_path";
import "./board.css";
import {getBoardState, addComponent, launchMarble, setLauncher, updateBoard, BoardState} from "../services/api";

export type BoardCell = {
    type: ItemType;
    isOccupied?: boolean;
};

const numRows = 17;
const numCols = 15;

interface BoardProps {
    board: BoardCell[][];
    setBoard: React.Dispatch<React.SetStateAction<BoardCell[][]>>;
    isRunning: boolean;
    currentSpeed: number;
}

const Board: React.FC<BoardProps> = ({ board, setBoard, isRunning, currentSpeed }) => {
    const [backendState, setBackendState] = useState<BoardState | null>(null);
    const marblePathGraph = useRef<MarblePathGraph>(new MarblePathGraph(numRows, numCols));
    const updateInterval = useRef<NodeJS.Timeout | null>(null);

    // Initialize the board and sync with backend
    useEffect(() => {
        const initializeBoard = async () => {
            const state = await getBoardState();
            setBackendState(state);
            updateFrontendBoard(state);
        };

        initializeBoard();

        return () => {
            if (updateInterval.current) {
                clearInterval(updateInterval.current);
            }
        };
    }, []);

    // Handle simulation running state
    useEffect(() => {
        if (isRunning) {
            updateInterval.current = setInterval(async () => {
                await updateBoard();
                const state = await getBoardState();
                setBackendState(state);
                updateFrontendBoard(state);
            }, 1000 / currentSpeed);
        } else if (updateInterval.current) {
            clearInterval(updateInterval.current);
        }

        return () => {
            if (updateInterval.current) {
                clearInterval(updateInterval.current);
            }
        };
    }, [isRunning, currentSpeed]);

    // Update the marble path graph when board changes
    useEffect(() => {
        if (board && board.length > 0) {
            for (let row = 0; row < numRows; row++) {
                for (let col = 0; col < numCols; col++) {
                    marblePathGraph.current.updateNode(row, col, board[row][col].type);
                }
            }
        }
    }, [board]);

    const updateFrontendBoard = (state: BoardState) => {
        const newBoard: BoardCell[][] = Array.from({ length: numRows }, () =>
            Array.from({ length: numCols }, () => ({ type: ItemType.Empty }))
        );

        // Map backend components to frontend
        state.components.forEach((row, y) => {
            row.forEach((component, x) => {
                newBoard[y][x] = {
                    type: mapComponentType(component.type),
                    isOccupied: component.is_occupied
                };
            });
        });

        // Add marbles
        state.marbles.forEach(marble => {
            newBoard[marble.y][marble.x].type = marble.color === 'red' ? ItemType.BallRed : ItemType.BallBlue;
            newBoard[marble.y][marble.x].isOccupied = true;
        });

        setBoard(newBoard);
    };

    const mapComponentType = (type: string): ItemType => {
        switch (type) {
            case 'ramp_left': return ItemType.RampLeft;
            case 'ramp_right': return ItemType.RampRight;
            case 'crossover': return ItemType.Crossover;
            case 'interceptor': return ItemType.Intercept;
            case 'bit_left': return ItemType.BitLeft;
            case 'bit_right': return ItemType.BitRight;
            case 'border_vertical': return ItemType.BorderVertical;
            case 'border_horizontal': return ItemType.BorderHorizontal;
            case 'border_diagonal_left': return ItemType.BorderDiagonalLeft;
            case 'border_diagonal_right': return ItemType.BorderDiagonalRight;
            case 'corner_left': return ItemType.CornerLeft;
            case 'corner_right': return ItemType.CornerRight;
            case 'lever_blue': return ItemType.LeverBlue;
            case 'lever_red': return ItemType.LeverRed;
            case 'invalid': return ItemType.Invalid;
            case 'gray_space': return ItemType.GraySpace;
            default: return ItemType.Empty;
        }
    };

    const handleAddComponent = async (type: ItemType, x: number, y: number) => {
        let backendType = '';
        switch(type) {
            case ItemType.RampLeft: backendType = 'ramp_left'; break;
            case ItemType.RampRight: backendType = 'ramp_right'; break;
            case ItemType.BitLeft: backendType = 'bit_left'; break;
            case ItemType.BitRight: backendType = 'bit_right'; break;
            case ItemType.Crossover: backendType = 'crossover'; break;
            case ItemType.Intercept: backendType = 'interceptor'; break;
            default: return;
        }

        await addComponent(backendType, x, y);
        const state = await getBoardState();
        setBackendState(state);
        updateFrontendBoard(state);
    };

    const cloneBoard = (board: BoardCell[][]): BoardCell[][] =>
        board.map((row) => row.map((cell) => ({ ...cell })));

    const handleCellClick = (row: number, col: number) => {
        setBoard((prevBoard) => {
            const newBoard = cloneBoard(prevBoard);
            const cell = newBoard[row][col];
            switch (cell.type) {
                case ItemType.BitLeft:
                    cell.type = ItemType.BitRight;
                    handleAddComponent(ItemType.BitRight, col, row);
                    break;
                case ItemType.BitRight:
                    cell.type = ItemType.BitLeft;
                    handleAddComponent(ItemType.BitLeft, col, row);
                    break;
                case ItemType.RampLeft:
                    cell.type = ItemType.RampRight;
                    handleAddComponent(ItemType.RampRight, col, row);
                    break;
                case ItemType.RampRight:
                    cell.type = ItemType.RampLeft;
                    handleAddComponent(ItemType.RampLeft, col, row);
                    break;
                default:
                    return prevBoard;
            }
            return newBoard;
        });
    };

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

    const handleDrop = async (e: React.DragEvent, row: number, col: number) => {
        e.preventDefault();
        e.stopPropagation();
        const itemType = e.dataTransfer.getData("text/plain") as ItemType;
        const sourceRow = parseInt(e.dataTransfer.getData("source-row"));
        const sourceCol = parseInt(e.dataTransfer.getData("source-col"));

        if (board[row][col].type === ItemType.Empty && isDraggable(itemType)) {
            await handleAddComponent(itemType, col, row);

            if (!isNaN(sourceRow) && !isNaN(sourceCol)) {
                setBoard(prevBoard => {
                    const newBoard = cloneBoard(prevBoard);
                    newBoard[sourceRow][sourceCol].type = ItemType.Empty;
                    return newBoard;
                });
            }
        }
    };

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

    if (!board || board.length === 0) {
        return null;
    }

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