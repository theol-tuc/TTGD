import axios from 'axios';

export const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface BoardState {
    components: Array<Array<{
        type: string;
        is_occupied: boolean;
        is_gear?: boolean;
        gear_rotation?: number;
        is_gear_bit?: boolean;
        gear_bit_state?: boolean;
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
    width: number;
    height: number;
}

export const getBoardState = async (): Promise<BoardState> => {
    try {
        const response = await api.get('/board/state');
        console.log('Board state from backend:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error fetching board state:', error);
        // Return a default board state if the backend is not available
        return {
            components: Array(12).fill(Array(12).fill({ 
                type: 'EMPTY', 
                is_occupied: false 
            })),
            marbles: [],
            red_marbles: 3,
            blue_marbles: 3,
            active_launcher: 'left',
            width: 12,
            height: 12
        };
    }
};

export const addComponent = async (type: string, x: number, y: number) => {
    try {
        await api.post('/components', { type, x, y });
    } catch (error) {
        console.error('Error adding component:', error);
    }
};

export const launchMarble = async (color: string) => {
    try {
        await api.post('/marbles', { color });
    } catch (error) {
        console.error('Error launching marble:', error);
    }
};

export const setLauncher = async (launcher: string) => {
    try {
        await api.post('/launcher', { launcher });
    } catch (error) {
        console.error('Error setting launcher:', error);
    }
};

export const updateBoard = async () => {
    try {
        await api.post('/update');
    } catch (error) {
        console.error('Error updating board:', error);
    }
};

export const resetBoard = async () => {
    try {
        await api.post('/reset');
    } catch (error) {
        console.error('Error resetting board:', error);
    }
};

export const getMarbleCounts = async () => {
    try {
        const response = await api.get('/counts');
        console.log("Fetched Marble Counts:", response.data);
        return response.data;
    } catch (error) {
        console.error('Error getting marble counts:', error);
        return { red: 3, blue: 3 };
    }
};

export const getMarbleOutput = async (): Promise<string[]> => {
    try {
        const response = await api.get('/output');
        console.log("Fetched Marbles:", response.data.output);
        return response.data.output || [];
    } catch (error) {
        console.error('Error getting marble output:', error);
        return [];
    }
};

export const fetchChallengeById = async (challengeId: string) => {
    try {
        const response = await api.get('/challenge_id', {
            params: { challenge_id: challengeId }
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching challenge ${challengeId}:`, error);
        return null;
    }
};

export const updateBoardState = async (gameState: any) => {
    const response = await api.post('/board/state', gameState);
    return response.data;
};

export const getChallenges = async () => {
    const response = await api.get('/challenges');
    return response.data;
};

export const getChallenge = async (id: string) => {
    const response = await api.get(`/challenges/${id}`);
    return response.data;
};