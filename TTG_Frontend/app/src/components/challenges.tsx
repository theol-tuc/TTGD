import {BoardCell} from "../board/board";
import { ItemType } from '../parts/constants';
import { fetchChallengeById } from "../services/api";

export interface Challenge {
    id: string;
    name: string;
    description: string;
    objectives: string[];
    initialBoard?: BoardCell[][]; // preset board for the challenge
    availableParts?: {
        [key in ItemType]?: number; // Number available (undefined = unlimited)
    };
    expectedOutput?: string[];

}

export const DEFAULT_CHALLENGE: Challenge = {
    id: 'default',
    name: 'Free Play',
    description: 'Unlimited parts available for creative building',
    objectives: [
        'Build anything you want',
        'Experiment with different components',
        'Create your own puzzles'
    ],
    // No part restrictions
};

export const CHALLENGES: Challenge[] = [
    DEFAULT_CHALLENGE,
    {
        id: '1',
        name: 'Challenge 1: Gravity',
        description: 'Make all of the blue marbles (and only the blue marbles) reach the end.',
        objectives: [
            'Complete the circuit as described',
            'Test with multiple marbles',
            'Ensure the solution is reliable'
        ],
        availableParts: {
            [ItemType.RampLeft]: 4

        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    },
    {
        id: '2',
        name: 'Challenge 2: Re-Entry',
        description: 'Make all of the blue marbles (and only the blue marbles) reach the end.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 5,

        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue','blue', 'blue', 'blue','blue', 'blue']
    },
    {
        id: '3',
        name: 'Challenge 3: Ignition',
        description: 'Release one blue marble and then all of the red marbles.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 6,

        },
        initialBoard: [],
        expectedOutput: ['red', 'red', 'red','red', 'red', 'red', 'red', 'blue']
    },
    {
        id: '4',
        name: 'Challenge 4: Fusion',
        description: 'Release one red marble and then all of the blue marbles.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 13,

        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue','blue', 'blue', 'blue','blue', 'red']
    },
    {
        id: '5',
        name: 'Challenge 5: Entropy',
        description: 'Make the pattern blue, red, blue, red, blue, red...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 9,

        },
        initialBoard: [],
        expectedOutput: ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue']
    },
    {
        id: '6',
        name: 'Challenge 6: Total Internal Reflection',
        description: 'Make the pattern blue, red, blue, red, blue, red...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 2,
            [ItemType.Crossover]: 5,

        },
        initialBoard: [],
        expectedOutput: ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue']
    },
    {
        id: '7',
        name: 'Challenge 7: Path of Least Resistance',
        description: 'Create a path for the blue marbles to reach the output with only 6 ramps.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 6,


        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue','blue', 'blue', 'blue','blue','blue']
    },
    {
        id: '8',
        name: 'Challenge 8: Depolarization',
        description: 'Make the pattern blue, red, blue, red, blue, red...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 14,


        },
        initialBoard: [],
        expectedOutput: ['red','blue', 'red', 'blue', 'red', 'blue', 'red','blue']
    },
    {
        id: '9',
        name: 'Challenge 9: Dimers',
        description: 'Make the pattern blue, blue, red, blue, blue, red...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 18,


        },
        initialBoard: [],
        expectedOutput: ['red','blue','blue', 'red','blue', 'blue']
    },
    {
        id: '10',
        name: 'Challenge 10: Double Bond',
        description: 'Make the pattern blue, blue, red, red, blue, blue, red, red...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 22,


        },
        initialBoard: [],
        expectedOutput: ['red','red','blue','blue', 'red','red','blue', 'blue']
    },
    {
        id: '11',
        name: 'Challenge 11: Selectivity',
        description: 'Flip the bits with the coordinates (3,9) and (11,9) to the right.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 15,
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '12',
        name: 'Challenge 12: Duality',
        description: 'Intercept a blue marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 3,


        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '13',
        name: 'Challenge 13: Duality - Part 2',
        description: 'Intercept a red marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 12,


        },
        initialBoard: [],
        expectedOutput: ['blue']
    },
    {
        id: '14',
        name: 'Challenge 14: Duality - Part 3',
        description: 'If the challege starts with the bit pointing to the left, intercept a blue marble. Otherwise, intercept a red marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 20,


        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '15',
        name: 'Challenge 15: Inversion',
        description: 'If the bit with the coordinates (7,11) starts to the left, intercept a blue marble. Otherwise, intercept a red marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 11,
            [ItemType.Crossover]: 2


        },
        initialBoard: [],
        expectedOutput: []
    },
    // ... other challenges
    {
        id: '16',
        name: 'Challenge 16: Termination',
        description: 'Let only 3 blue marbles reach the bottom and catch the 4th marble in the interceptor.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 10
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue']
    },
    {
        id: '17',
        name: 'Challenge 17: Fixed Ratio',
        description: 'Make the pattern red, red, red, blue, blue, blue...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999
        },
        initialBoard: [],
        expectedOutput: ['red', 'red', 'red', 'blue', 'blue', 'blue',]
    },
    {
        id: '18',
        name: 'Challenge 18: Entanglement',
        description: 'If the top bit AND the bottom bit start pointed to the right, put a marble in the left interceptor. Else, put a marble in the right interceptor.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 7
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '19',
        name: 'Challenge 19: Entanglement',
        description: 'If the top bit AND the bottom bit start pointed to the right, intercept a blue marble. Otherwise, intercept a red marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999,
            [ItemType.Crossover]: 2
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '20',
        name: 'Challenge 20: Symbiosis',
        description: 'If the top bit OR the bottom bit start pointed to the right, intercept a blue marble. Otherwise, intercept a red marble.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999,
            [ItemType.Crossover]: 2
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '21',
        name: 'Challenge 21: Quantum Number',
        description: 'On a Turing Tumble board, each bit component has two states—left and right—which represent binary 0 and 1. When you align multiple bits vertically and let marbles flow through them from top to bottom, the structure behaves like a binary register. You can simulate binary increment and decrement using vertical bit registers on a Turing Tumble board. Each operation involves flipping bits from the LSB upward, with carry for incrementing and borrow for decrementing, just like in standard binary arithmetic. Use the marble’s path and bit flipping behavior to implement these transformations physically. Use the register formed by the bits on the board to count the number of blue marbles.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 5
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '22',
        name: 'Challenge 22: Depletion',
        description: 'On a Turing Tumble board, each bit component has two states—left and right—which represent binary 0 and 1. When you align multiple bits vertically and let marbles flow through them from top to bottom, the structure behaves like a binary register. You can simulate binary increment and decrement using vertical bit registers on a Turing Tumble board. Each operation involves flipping bits from the LSB upward, with carry for incrementing and borrow for decrementing, just like in standard binary arithmetic. Use the marble’s path and bit flipping behavior to implement these transformations physically. The register formed by the bits on the board starts at the value 15. Subtract the number of blue marbles from the register.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 4
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '23',
        name: 'Challenge 23: Tetrad',
        description: 'Let exactly 4 blue marbles reach the end. (Intercept the 5th.)',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue']
    },
    {
        id: '24',
        name: 'Challenge 24: Ennead',
        description: 'Let exactly 9 blue marbles reach the end. (Intercept the 10th.)',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 14,
            [ItemType.Intercept]: 1
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    },
    {
        id: '25',
        name: 'Challenge 25: Regular Expression',
        description: 'Generate the required pattern: red, red, red, blue, blue, blue, blue, blue, blue...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999, 
            [ItemType.Intercept]: 1, 
            [ItemType.BitLeft]: 5
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    },
    {
        id: '26',
        name: 'Challenge 26: Nucleus',
        description: 'Generate the required pattern: blue, blue, blue, blue, red, blue, blue, blue, blue...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999, 
            [ItemType.Crossover]: 2, 
            [ItemType.BitLeft]: 2
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue']
    },
    {
        id: '27',
        name: 'Challenge 27: Reflection',
        description: 'Reverse the direction of each of the 9 starting bits, regardless of the direction they point to start.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999, 
            [ItemType.Intercept]: 1, 
            [ItemType.BitLeft]: 1
        },
        initialBoard: [],
        expectedOutput: []
    },
    {
        id: '28',
        name: 'Challenge 28: Latch',
        description: 'Release only the blue marbles.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 1, 
            [ItemType.Gear]: 1, 
            [ItemType.GearBitLeft]: 1
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'red', 'red']
    },
    {
        id: '29',
        name: 'Challenge 29: One-Shot Switch',
        description: 'Generate the required pattern: blue, blue, blue, blue, blue, blue, red, blue...',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999, 
            [ItemType.Crossover]: 1, 
            [ItemType.GearBitLeft]: 1,
            [ItemType.Gear]: 1
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'red', 'blue']
    },
    {
        id: '30',
        name: 'Challenge 30: Overflow',
        description: 'Count the blue marbles in the register formed by the three bits. If there are more than 7, gear bit that already exists on the board at the start of the challenge must flip right (and stay right) to indicate the overflow.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 14, 
            [ItemType.GearBitLeft]: 1, 
            [ItemType.Gear]: 1
        },
        initialBoard: [],
        expectedOutput: []
    },
    
];

export const updateChallengeInitialBoard = async (challengeId: string) => {
    const challenge = CHALLENGES.find(ch => ch.id === challengeId);
    if (!challenge) return;

    const backendChallenge = await fetchChallengeById(challengeId);
    if (backendChallenge && backendChallenge.initialBoard) {
        challenge.initialBoard = backendChallenge.initialBoard;
    }
};