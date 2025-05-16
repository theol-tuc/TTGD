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
];

export const updateChallengeInitialBoard = async (challengeId: string) => {
    const challenge = CHALLENGES.find(ch => ch.id === challengeId);
    if (!challenge) return;

    const backendChallenge = await fetchChallengeById(challengeId);
    if (backendChallenge && backendChallenge.initialBoard) {
        challenge.initialBoard = backendChallenge.initialBoard;
    }
};