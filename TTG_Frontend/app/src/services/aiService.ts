import { GameState } from '../board/board';
import { api } from './api';

const API_URL = 'http://localhost:8000';

export interface AIMove {
    action: string;
    parameters: any;
}

export interface AIResponse {
    action: string;
    parameters: Record<string, any>;
    explanation: string;
}

export const aiService = {
    async getAIMove(gameState: GameState, challengeId?: string): Promise<AIResponse> {
        const response = await api.post('/ai/move', {
            gameState,
            challengeId
        });
        return response.data;
    },

    async executeAIMove(gameState: GameState, challengeId?: string): Promise<void> {
        await api.post('/ai/execute', {
            gameState,
            challengeId
        });
    }
}; 