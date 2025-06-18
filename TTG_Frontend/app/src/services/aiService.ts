import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface AIMove {
    action: 'add_component' | 'launch_marble' | 'set_launcher';
    parameters: {
        type?: string;
        x?: number;
        y?: number;
        color?: string;
        launcher?: string;
    };
}

export interface AIResponse {
    move: AIMove;
    explanation: string;
}

export const aiService = {
    async getAIMove(): Promise<AIResponse> {
        try {
            const response = await axios.post(`${API_BASE_URL}/ai/move`);
            return response.data;
        } catch (error) {
            console.error('Error getting AI move:', error);
            throw error;
        }
    },

    async executeAIMove(): Promise<void> {
        try {
            await axios.post(`${API_BASE_URL}/ai/execute`);
        } catch (error) {
            console.error('Error executing AI move:', error);
            throw error;
        }
    }
}; 