import React, {useEffect, useRef, useState} from "react";
import {IMAGE_FILENAMES, ItemType} from "../parts/constants";
import "./board.css";
import {addComponent, BoardState, getBoardState, updateBoard, getMarbleOutput} from "../services/api";
import { useChallenge } from "../components/challengeContext";

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

export interface GameState {
    components: Array<Array<{
        type: string;
        is_occupied: boolean;
    }>>;
    marbles: Array<{
        color: string;
        x: number;
        y: number;
        direction: string;
        is_moving: boolean;
    }>;
    red_marbles: number;
    blue_marbles: number;
    active_launcher: string;
}

const unlimitedParts = {
    ramp: Infinity,
    bit: Infinity,
    crossover: Infinity,
    interceptor: Infinity,
    gear: Infinity,
    gearBit: Infinity,
};

const canPlaceComponent = (item: ItemType, target: ItemType) => {
    const isGear = [
        ItemType.Gear,
    ].includes(item);

    if (isGear) {
        // only on gray‐spaces
        return target === ItemType.GraySpace;
    } else {
        // everything else still goes on empty cells
        return target === ItemType.Empty;
    }
};


const Board: React.FC<BoardProps> = ({ board, setBoard, isRunning, currentSpeed }) => {
    const [backendState, setBackendState] = useState<BoardState | null>(null);
    const updateInterval = useRef<NodeJS.Timeout | null>(null);
    const [mode, setMode] = useState("freeplay"); // "freeplay" or "challenge"
    const [selectedChallenge, setSelectedChallenge] = useState(null);
    const [availableParts, setAvailableParts] = useState(unlimitedParts);
    const { decrementPartCount } = useChallenge();

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
            case 'gear': return ItemType.Gear;
            case 'gear_bit_left': return ItemType.GearBitLeft;
            case 'gear_bit_right': return ItemType.GearBitRight;
            default: return ItemType.Empty;
        }
    };

    const handleAddGearBit = async (type: ItemType, x: number, y: number) => {
        const neighbors = [
            board[y-1]?.[x], 
            board[y+1]?.[x], 
            board[y]?.[x-1], 
            board[y]?.[x+1]
        ].filter(Boolean);
        console.log("Neighbors: ", neighbors[0].type, neighbors[1].type, neighbors[2].type, neighbors[3].type);
        const connectedGearBits = neighbors.filter(cell =>
            cell.type === ItemType.GearBitLeft || cell.type === ItemType.GearBitRight
        );
    
        let adjustedType = type;
    
        if (connectedGearBits.length > 0) {
            const neighbor = connectedGearBits[0];
            const neighborState = (neighbor.type === ItemType.GearBitLeft) ? 'left' : 'right';
    
            if (type === ItemType.GearBitLeft && neighborState === 'right') {
                adjustedType = ItemType.GearBitRight;
            } else if (type === ItemType.GearBitRight && neighborState === 'left') {
                adjustedType = ItemType.GearBitLeft;
            }
        }
    
        let backendType = '';
        switch (adjustedType) {
            case ItemType.GearBitLeft: backendType = 'gear_bit_left'; break;
            case ItemType.GearBitRight: backendType = 'gear_bit_right'; break;
        }
    
        await addComponent(backendType, x, y);
        const state = await getBoardState();
        setBackendState(state);
        updateFrontendBoard(state);
    };

    const handleMoveGearBit = async (type: ItemType, x: number, y: number) => {
        // Find connected gear groups for each neighbor
        const gearGroups = [
            findConnectedGearGroup(y - 1, x, board),
            findConnectedGearGroup(y + 1, x, board),
            findConnectedGearGroup(y, x - 1, board),
            findConnectedGearGroup(y, x + 1, board),
        ];

        // Eliminate duplicates by converting to a Set
        const uniqueGearGroups: [number, number][][] = [];
        const seen = new Set<string>();

        for (const group of gearGroups) {
            const serializedGroup = group.map(([row, col]) => `${row},${col}`).sort().join('|');
            if (!seen.has(serializedGroup)) {
                seen.add(serializedGroup);
                uniqueGearGroups.push(group);
            }
        }

        // Determine the largest gear group
        let largestGroup: [number, number][] = [];
        uniqueGearGroups.forEach((group) => {
            if (group.length > largestGroup.length) {
                largestGroup = group;
            }
        });

        // Count the directions in the largest group
        let leftCount = 0;
        let rightCount = 0;
        largestGroup.forEach(([row, col]) => {
            const cell = board[row][col];
            if (cell.type === ItemType.GearBitLeft) {
                leftCount++;
            } else if (cell.type === ItemType.GearBitRight) {
                rightCount++;
            }
        });

        // Choose the majority direction
        const majorityDirection =
            leftCount > rightCount
                ? ItemType.GearBitLeft
                : rightCount > leftCount
                ? ItemType.GearBitRight
                : type; // Default to the current type if equal

        // Place the gear bit with the chosen direction
        let backendType = '';
        switch (majorityDirection) {
            case ItemType.GearBitLeft:
                backendType = 'gear_bit_left';
                break;
            case ItemType.GearBitRight:
                backendType = 'gear_bit_right';
                break;
        }

        await addComponent(backendType, x, y);
        const state = await getBoardState();
        setBackendState(state);
        updateFrontendBoard(state);
    };

    const handleAddGear = async (type: ItemType, x: number, y: number) => {
        const updatedBoard = [...board];
        updatedBoard[y][x].type = ItemType.Gear;
    
        await addComponent('gear', x, y);
    
        const state = await getBoardState();
        setBackendState(state);
        updateFrontendBoard(state);
    
        const gearGroup = findConnectedGearGroup(y, x, updatedBoard);
    
        let leftCount = 0;
        let rightCount = 0;
        gearGroup.forEach(([row, col]) => {
            const cell = updatedBoard[row][col];
            if (cell.type === ItemType.GearBitLeft) {
                leftCount++;
            } else if (cell.type === ItemType.GearBitRight) {
                rightCount++;
            }
        });
    
        const majorityDirection = leftCount > rightCount
            ? ItemType.GearBitLeft
            : rightCount > leftCount
            ? ItemType.GearBitRight
            : ItemType.GearBitRight;
    
        console.log("Majority Direction: ", majorityDirection);
        console.log("Left Count: ", leftCount);
        console.log("Right Count: ", rightCount);
    
        const finalState = await getBoardState();
        setBackendState(finalState);
        updateFrontendBoard(finalState);
    };


    const findConnectedGearGroup = (row: number, col: number, board: BoardCell[][]): [number, number][] => {
        const visited = new Set<string>();
        const queue: [number, number][] = [[row, col]];
        const group: [number, number][] = [];
    
        while (queue.length > 0) {
            const [r, c] = queue.pop()!;
            const key = `${r},${c}`;
            if (visited.has(key)) continue;
            visited.add(key);
    
            const cell = board[r]?.[c];
            if (!cell) continue;
            console.log("Cell: ", cell.type, " at: ", r, c);
            if (cell.type === ItemType.GearBitLeft || cell.type === ItemType.GearBitRight || cell.type === ItemType.Gear) {
                group.push([r, c]);
    
                queue.push([r-1, c]); 
                queue.push([r+1, c]); 
                queue.push([r, c-1]); 
                queue.push([r, c+1]); 
            }
        }
        return group;
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
            case ItemType.GearBitLeft:
            case ItemType.GearBitRight:
                await handleMoveGearBit(type, x, y);
                return;
            case ItemType.Gear:
                await handleAddGear(type, x, y);
                return;
            default:
                return;
        }

        await addComponent(backendType, x, y);

        setBoard(prevBoard => {
            const newBoard = cloneBoard(prevBoard);
            newBoard[y][x] = { type, isOccupied: true };
            return newBoard;
        });
        
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
                case ItemType.GearBitLeft:
                case ItemType.GearBitRight:
                case ItemType.Gear:
                    {
                    const group = findConnectedGearGroup(row, col, newBoard);
                    group.forEach(([r, c]) => {
                        const gearCell = newBoard[r][c];
                        if (gearCell.type === ItemType.GearBitLeft) {
                            gearCell.type = ItemType.GearBitRight;
                            handleAddGearBit(ItemType.GearBitRight, c, r);
                        } else if (gearCell.type === ItemType.GearBitRight) {
                            gearCell.type = ItemType.GearBitLeft;
                            handleAddGearBit(ItemType.GearBitLeft, c, r);
                        }
                    });
                    
                    }
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
        const targetType = board[row][col].type;

        const isMove = !isNaN(sourceRow) && !isNaN(sourceCol) && (row !== sourceRow || col !== sourceCol);

        if (isDraggable(itemType) && canPlaceComponent(itemType, targetType)) {
            await handleAddComponent(itemType, col, row);
            decrementPartCount(itemType);

            if (isMove) {
                if (itemType === ItemType.Gear) {
                    await addComponent('gray_space', sourceCol, sourceRow);
                } else {
                    await addComponent('empty', sourceCol, sourceRow);
                }
            }
        }
        const state = await getBoardState();
        updateFrontendBoard(state);
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