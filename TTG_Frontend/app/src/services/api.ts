import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface BoardState {
    components: Array<Array<{ type: string; is_occupied: boolean }>>;
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

export const getBoardState = async (): Promise<BoardState> => {
    const response = await axios.get(`${API_BASE_URL}/board`);
    return response.data;
};

export const addComponent = async (type: string, x: number, y: number) => {
    await axios.post(`${API_BASE_URL}/components`, { type, x, y });
};

export const launchMarble = async (color: string) => {
    await axios.post(`${API_BASE_URL}/marbles`, { color });
};

export const setLauncher = async (launcher: string) => {
    await axios.post(`${API_BASE_URL}/launcher`, { launcher });
};

export const updateBoard = async () => {
    await axios.post(`${API_BASE_URL}/update`);
};

export const resetBoard = async () => {
    await axios.post(`${API_BASE_URL}/reset`);
};

export const getMarbleCounts = async () => {
    const response = await axios.get(`${API_BASE_URL}/counts`);
    return response.data;
};

export const getMarbleOutput = async (): Promise<string[]> => {
    const response = await axios.get(`${API_BASE_URL}/output`);
    console.log("Fetched Marbles:", response.data.output);
    return response.data.output || [];
}

export const fetchChallengeById = async (challengeId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/challenge_id`, {
            params: { challenge_id: challengeId }
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching challenge ${challengeId}:`, error);
        return null;
    }
};