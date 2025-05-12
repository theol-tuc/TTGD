import React, { useState } from 'react';
import { aiService, AIResponse } from '../services/aiService';
import './AIOverlay.css';

interface AIOverlayProps {
    onAIMove: () => void;
}

export const AIOverlay: React.FC<AIOverlayProps> = ({ onAIMove }) => {
    const [aiResponse, setAIResponse] = useState<AIResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGetAIMove = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await aiService.getAIMove();
            setAIResponse(response);
        } catch (err) {
            setError('Failed to get AI move. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleExecuteAIMove = async () => {
        if (!aiResponse) return;
        
        setIsLoading(true);
        setError(null);
        try {
            await aiService.executeAIMove();
            onAIMove();
            setAIResponse(null);
        } catch (err) {
            setError('Failed to execute AI move. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="ai-overlay">
            <h2>AI Assistant</h2>
            
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <div className="ai-controls">
                <button 
                    onClick={handleGetAIMove}
                    disabled={isLoading}
                >
                    {isLoading ? 'Thinking...' : 'Get AI Move'}
                </button>
                
                {aiResponse && (
                    <button 
                        onClick={handleExecuteAIMove}
                        disabled={isLoading}
                    >
                        Execute Move
                    </button>
                )}
            </div>

            {aiResponse && (
                <div className="ai-response">
                    <h3>AI's Move</h3>
                    <p><strong>Action:</strong> {aiResponse.move.action}</p>
                    <p><strong>Parameters:</strong> {JSON.stringify(aiResponse.move.parameters)}</p>
                    <h3>Explanation</h3>
                    <p>{aiResponse.explanation}</p>
                </div>
            )}
        </div>
    );
}; 