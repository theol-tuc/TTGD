import {BoardCell} from "../board/board";
import { ItemType } from '../parts/constants';

export interface Challenge {
    id: string;
    name: string;
    description: string;
    objectives: string[];
    initialBoard?: BoardCell[][]; // preset board for the challenge
    availableParts?: {
        [key in ItemType]?: number; // Number available (undefined = unlimited)
    };
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
        name: 'Challenge 1: Basic Ramp',
        description: 'Build a simple ramp that guides the marble from the launcher to the target. Learn how basic components interact with marbles.',
        objectives: [
            'Complete the circuit as described',
            'Test with multiple marbles',
            'Ensure the solution is reliable'
        ],
        availableParts: {
            [ItemType.RampLeft]: 4,
            [ItemType.BallBlue]: 1,
            [ItemType.BallRed]: 1
        },
        initialBoard: [
            // Your board setup here
        ]
    },
    {
        id: '2',
        name: 'Challenge 2: Bit Manipulation',
        description: 'Create a circuit that can store a single bit of information using the gear bits. The marble should flip the bit state each time it passes through.',
        objectives: [
            'Implement a working bit storage',
            'Demonstrate bit flipping',
            'Show reliable operation for 5 consecutive marbles'
        ],
        availableParts: {
            [ItemType.RampLeft]: 4,
            [ItemType.Crossover]: 2,
            [ItemType.RampRight]: 4,
            [ItemType.BitLeft]: 1,
            [ItemType.BitRight]: 1,
            [ItemType.BallBlue]: 1,
            [ItemType.Intercept]: 3
        },
        initialBoard: [
            // Your board setup here
        ]
    },
    // ... other challenges
];

export const getChallengeById = (id: string): Challenge | undefined => {
    return CHALLENGES.find(challenge => challenge.id === id);
};