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
        description: 'Make all of the blue balls (and only the blue balls) reach the end.',
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
        description: 'Release one blue ball and then all of the red balls.',
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
        description: 'Release one red ball and then all of the blue balls.',
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
        description: 'Create a path for the blue balls to reach the output with only 6 ramps.',
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
        description: 'Flip bits 2 and 5 to the right.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 15,


        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue']
    },
    {
        id: '12',
        name: 'Challenge 12: Duality',
        description: 'Intercept a blue ball. Start with trigger Left',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 3,


        },
        initialBoard: [],
        expectedOutput: ['red']
    },
    {
        id: '13',
        name: 'Challenge 13: Duality - Part 2',
        description: 'Intercept a red ball. Start with trigger Left',
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
        description: 'If the game starts with bit A pointing to the left, intercept a blue ball. Otherwise, intercept a red ball.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 20,


        },
        initialBoard: [],
        expectedOutput: ['blue']
    },
    {
        id: '15',
        name: 'Challenge 15: Inversion',
        description: 'If bit A starts to the left, intercept a blue ball. If bit A starts to the right, intercept a red ball.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 11,
            [ItemType.Crossover]: 2


        },
        initialBoard: [],
        expectedOutput: ['blue']
    },
    // ... other challenges
    {
        id: '16',
        name: 'Challenge 16: Termination',
        description: 'Let only 3 blue balls reach the bottom and catch the 4th ball in the interceptor.',
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
        description: 'Make the pattern blue, blue, blue, red, red, red',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 999
        },
        initialBoard: [],
        expectedOutput: ['blue', 'blue', 'blue', 'red', 'red', 'red']
    },
    {
        id: '18',
        name: 'Challenge 18: Entanglement',
        description: 'If the top bit AND the bottom bit start pointed to the right, put a ball in the left interceptor. Else, put a ball in the right interceptor.',
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
        description: 'If the top bit AND the bottom bit start pointed to the right, intercept a blue ball. Otherwise, intercept a red ball.',
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
        description: 'If the top bit OR the bottom bit start pointed to the right, intercept a blue ball. Otherwise, intercept a red ball.',
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
        description: 'Use register A to count the number of blue balls.',
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
        description: 'Register A starts at 15. Subtract the number of blue balls from the register.',
        objectives: [
            'Complete the circuit as described',
        ],
        availableParts: {
            [ItemType.RampLeft]: 4
        },
        initialBoard: [],
        expectedOutput: []
    }
    
];

export const updateChallengeInitialBoard = async (challengeId: string) => {
    const challenge = CHALLENGES.find(ch => ch.id === challengeId);
    if (!challenge) return;

    const backendChallenge = await fetchChallengeById(challengeId);
    if (backendChallenge && backendChallenge.initialBoard) {
        challenge.initialBoard = backendChallenge.initialBoard;
    }
};