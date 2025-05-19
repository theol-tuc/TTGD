import { api } from './api';
import { BoardState } from './api';

export interface AIResponse {
    action: string;
    parameters: Record<string, any>;
    explanation: string;
}

export const aiService = {
    async getAIMove(gameState: BoardState, challengeId?: string): Promise<AIResponse> {
        console.log('Sending to AI:', { gameState, challengeId });
        const response = await api.post('/ai/move', {
            gameState,
            challengeId
        });
        console.log('AI response:', response.data);
        return response.data;
    },

    async executeAIMove(gameState: BoardState, challengeId?: string): Promise<void> {
        await api.post('/ai/execute', {
            gameState,
            challengeId
        });
    }
}; 