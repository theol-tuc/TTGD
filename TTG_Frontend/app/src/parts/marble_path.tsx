import { ItemType } from './constants';

// Define the possible directions a marble can move (only downward due to gravity)
export enum Direction {
    DownLeft = 'down_left',
    DownRight = 'down_right'
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

        // Connect nodes based on the diamond pattern (only downward connections)
        for (let row = 0; row < this.numRows - 1; row++) {
            for (let col = 0; col < this.numCols; col++) {
                const node = graph[row][col];

                // Only connect to nodes below
                if (col > 0) {
                    node.connections.set(Direction.DownLeft, graph[row + 1][col - 1]);
                }
                if (col < this.numCols - 1) {
                    node.connections.set(Direction.DownRight, graph[row + 1][col + 1]);
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
    public getNextNode(row: number, col: number, direction: Direction): GraphNode | null {
        if (row >= 0 && row < this.numRows && col >= 0 && col < this.numCols) {
            const node = this.nodes[row][col];

            // Handle different part types
            switch (node.type) {
                case ItemType.RampRight:
                    // RampRight always sends marble down-right
                    return node.connections.get(Direction.DownRight) || null;

                case ItemType.RampLeft:
                    // RampLeft always sends marble down-left
                    return node.connections.get(Direction.DownLeft) || null;

                case ItemType.BitRight:
                    // BitRight sends marble down-right if set to 1, down-left if set to 0
                    return this.getBitState(row, col) 
                        ? node.connections.get(Direction.DownRight) || null
                        : node.connections.get(Direction.DownLeft) || null;

                case ItemType.BitLeft:
                    // BitLeft sends marble down-left if set to 1, down-right if set to 0
                    return this.getBitState(row, col)
                        ? node.connections.get(Direction.DownLeft) || null
                        : node.connections.get(Direction.DownRight) || null;

                case ItemType.Crossover:
                    // Crossover preserves the incoming direction
                    return node.connections.get(direction) || null;

                case ItemType.Intercept:
                    // Intercept stops the marble
                    return null;

                case ItemType.GraySpace:
                case ItemType.Empty:
                    // Empty spaces and gray spaces stop the marble
                    return null;

                case ItemType.Invalid:
                    // Invalid spaces stop the marble
                    return null;

                default:
                    return null;
            }
        }
        return null;
    }

    // Get all possible paths from a starting position, taking into account the node type
    public getPossiblePaths(startRow: number, startCol: number): Direction[] {
        if (startRow >= 0 && startRow < this.numRows && startCol >= 0 && startCol < this.numCols) {
            const node = this.nodes[startRow][startCol];
            
            switch (node.type) {
                case ItemType.RampRight:
                    return [Direction.DownRight];
                case ItemType.RampLeft:
                    return [Direction.DownLeft];
                case ItemType.BitRight:
                case ItemType.BitLeft:
                    return [Direction.DownLeft, Direction.DownRight];
                case ItemType.Crossover:
                    return Array.from(node.connections.keys());
                default:
                    return [];
            }
        }
        return [];
    }
}