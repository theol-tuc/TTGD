import { api } from './api';
import { BoardState } from './api';

export interface AIResponse {
    action: string;
    parameters?: any;
    explanation?: string;
    text_representation?: string;
}

export const aiService = {
    async getAIMove(gameState: BoardState, challengeId?: string): Promise<AIResponse> {
        const requestData = {
            gameState,
            challengeId
        };
        console.log('Sending to AI (raw data):', JSON.stringify(requestData, null, 2));
        console.log('Sending to AI (structured):', { 
            components: gameState.components,
            marbles: gameState.marbles,
            red_marbles: gameState.red_marbles,
            blue_marbles: gameState.blue_marbles,
            active_launcher: gameState.active_launcher,
            challengeId 
        });
        const response = await api.post('/ai/move', requestData);
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