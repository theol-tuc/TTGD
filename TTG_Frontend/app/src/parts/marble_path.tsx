import { ItemType } from './constants';


// Define the possible directions a marble can move (only downward due to gravity)
export enum Direction {
    DownLeft = 'down_left',
    DownRight = 'down_right',
    Down = 'down'
}

// Define a node in our graph
export interface GraphNode {
    row: number;
    col: number;
    type: ItemType;
    connections: Map<Direction, GraphNode | null>;
}

// Create a diamond-shaped graph for the board
export class MarblePathGraph {
    private nodes: GraphNode[][];
    private numRows: number;
    private numCols: number;
    private bitStates: Map<string, boolean>; // Track bit states using "row,col" as key

    constructor(numRows: number, numCols: number) {
        this.numRows = numRows;
        this.numCols = numCols;
        this.bitStates = new Map();
        this.nodes = this.initializeGraph();
    }

    private initializeGraph(): GraphNode[][] {
        const graph: GraphNode[][] = [];

        // Create nodes for each cell in the board
        for (let row = 0; row < this.numRows; row++) {
            graph[row] = [];
            for (let col = 0; col < this.numCols; col++) {
                graph[row][col] = {
                    row,
                    col,
                    type: ItemType.Empty,
                    connections: new Map<Direction, GraphNode | null>()
                };
            }
        }

        // Connect nodes based on possible marble movements (only downward)
        for (let row = 0; row < this.numRows - 1; row++) {
            for (let col = 0; col < this.numCols; col++) {
                const node = graph[row][col];

                // Connect to node below (default gravity)
                if (row < this.numRows - 1) {
                    node.connections.set(Direction.Down, graph[row + 1][col]);
                }

                // Connect to diagonal nodes (for ramps)
                if (col > 0) {
                    node.connections.set(Direction.DownLeft, graph[row][col - 1]);
                }
                if (col < this.numCols - 1) {
                    node.connections.set(Direction.DownRight, graph[row][col + 1]);
                }
            }
        }

        return graph;
    }

    // Update a node's type (e.g., when a part is placed)
    public updateNode(row: number, col: number, type: ItemType): void {
        if (row >= 0 && row < this.numRows && col >= 0 && col < this.numCols) {
            this.nodes[row][col].type = type;
            // Reset bit state when type changes
            this.bitStates.delete(`${row},${col}`);
        }
    }

    // Toggle a bit's state
    public toggleBit(row: number, col: number): void {
        const key = `${row},${col}`;
        const currentState = this.bitStates.get(key) || false;
        this.bitStates.set(key, !currentState);
    }

    // Get a bit's current state
    public getBitState(row: number, col: number): boolean {
        return this.bitStates.get(`${row},${col}`) || false;
    }

    // Get the next node a marble should move to based on its current position and direction
    public getNextNode(row: number, col: number, direction: Direction): {
        node: GraphNode | null,
        newDirection: Direction
    } {
        if (row < 0 || row >= this.numRows || col < 0 || col >= this.numCols) {
            return {node: null, newDirection: direction};
        }

        const node = this.nodes[row][col];

        // Handle different component types
        switch (node.type) {
            case ItemType.RampLeft:
                // RampLeft changes direction to left and moves down-left
                return {
                    node: this.nodes[row + 1]?.[col - 1] || null,
                    newDirection: Direction.DownLeft
                };

            case ItemType.RampRight:
                // RampRight changes direction to right and moves down-right
                return {
                    node: this.nodes[row + 1]?.[col + 1] || null,
                    newDirection: Direction.DownRight
                };

            case ItemType.BitLeft:
                // BitLeft flips direction (handled by backend)
                // Just pass through to next node in current direction
                return {
                    node: direction === Direction.DownLeft
                        ? this.nodes[row + 1]?.[col - 1] || null
                        : this.nodes[row + 1]?.[col + 1] || null,
                    newDirection: direction
                };

            case ItemType.BitRight:
                // BitRight flips direction (handled by backend)
                // Just pass through to next node in current direction
                return {
                    node: direction === Direction.DownLeft
                        ? this.nodes[row + 1]?.[col - 1] || null
                        : this.nodes[row + 1]?.[col + 1] || null,
                    newDirection: direction
                };

            case ItemType.Crossover:
                // Crossover preserves direction
                return {
                    node: direction === Direction.DownLeft
                        ? this.nodes[row + 1]?.[col - 1] || null
                        : this.nodes[row + 1]?.[col + 1] || null,
                    newDirection: direction
                };

            case ItemType.Intercept:
                // Interceptor stops the marble
                return {node: null, newDirection: direction};

            case ItemType.LeverBlue:
            case ItemType.LeverRed:
                // Levers trigger actions but don't affect marble path directly
                return {node: null, newDirection: direction};

            case ItemType.Invalid:
            case ItemType.BorderVertical:
            case ItemType.BorderHorizontal:
                // Invalid spaces and borders stop the marble
                return {node: null, newDirection: direction};

            default:
                // For empty spaces and gray spaces, continue in current direction
                if (direction === Direction.DownLeft) {
                    return {
                        node: this.nodes[row + 1]?.[col - 1] || null,
                        newDirection: direction
                    };
                } else if (direction === Direction.DownRight) {
                    return {
                        node: this.nodes[row + 1]?.[col + 1] || null,
                        newDirection: direction
                    };
                } else {
                    // Default downward movement
                    return {
                        node: this.nodes[row + 1]?.[col] || null,
                        newDirection: Direction.Down
                    };
                }
        }
    }
    // Get all possible paths from a starting position (for visualization)
    public getPossiblePaths(startRow: number, startCol: number): Direction[] {
        if (startRow < 0 || startRow >= this.numRows || startCol < 0 || startCol >= this.numCols) {
            return [];
        }
        const node = this.nodes[startRow][startCol];
        const possibleDirections: Direction[] = [];

        // Check all possible directions based on component type
        switch (node.type) {
            case ItemType.RampLeft:
                possibleDirections.push(Direction.DownLeft);
                break;
            case ItemType.RampRight:
                possibleDirections.push(Direction.DownRight);
                break;
            case ItemType.BitLeft:
            case ItemType.BitRight:
            case ItemType.Crossover:
                possibleDirections.push(Direction.DownLeft, Direction.DownRight);
                break;
            default:
                possibleDirections.push(Direction.Down);
        }
        return possibleDirections;
    }
}