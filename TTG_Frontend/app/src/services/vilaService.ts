import { API_BASE_URL } from '../config';

export interface VilaAnalysis {
    status: string;
    analysis: any;
    recommended_move: string;
    confidence: number;
}

export const captureAndAnalyzeBoard = async (boardElement: HTMLElement): Promise<VilaAnalysis> => {
    try {
        // Create a canvas element to capture the board
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        if (!context) {
            throw new Error('Could not get canvas context');
        }

        // Set canvas size to match board element
        canvas.width = boardElement.offsetWidth;
        canvas.height = boardElement.offsetHeight;

        // Draw the board to canvas
        const boardImage = await html2canvas(boardElement);
        context.drawImage(boardImage, 0, 0);

        // Convert canvas to blob
        const blob = await new Promise<Blob>((resolve) => {
            canvas.toBlob((blob) => {
                if (blob) resolve(blob);
            }, 'image/png');
        });

        // Create form data
        const formData = new FormData();
        formData.append('board_image', blob, 'board.png');

        // Send to backend
        const response = await fetch(`${API_BASE_URL}/api/vila/analyze`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to analyze board with VILA');
        }

        return await response.json();
    } catch (error) {
        console.error('Error analyzing board with VILA:', error);
        throw error;
    }
};

// Helper function to capture HTML element as canvas
const html2canvas = async (element: HTMLElement): Promise<HTMLCanvasElement> => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) {
        throw new Error('Could not get canvas context');
    }

    // Set canvas size
    canvas.width = element.offsetWidth;
    canvas.height = element.offsetHeight;

    // Use html2canvas library to capture the element
    const html2canvas = (await import('html2canvas')).default;
    return await html2canvas(element);
}; 