import {BoardCell} from "../board/board";

export interface Challenge {
    id: string;
    name: string;
    description: string;
    objectives: string[];
    initialBoard?: BoardCell[][]; // preset board for the challenge
}

export const CHALLENGES: Challenge[] = [
    {
        id: '1',
        name: 'Challenge 1: Basic Ramp',
        description: 'Build a simple ramp that guides the marble from the launcher to the target. Learn how basic components interact with marbles.',
        objectives: [
            'Complete the circuit as described',
            'Test with multiple marbles',
            'Ensure the solution is reliable'
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
        ]
    },
    // ... other challenges
];

export const getChallengeById = (id: string): Challenge | undefined => {
    return CHALLENGES.find(challenge => challenge.id === id);
};