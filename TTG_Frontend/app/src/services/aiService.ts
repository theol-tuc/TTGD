import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const analyzeBoardImage = async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await axios.post(`${API_URL}/analyze-board`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error analyzing board:', error);
        throw error;
    }
};

export interface AIResponse {
  analysis: string;
  status: string;
}

export const analyzeWithVila = async (file: File): Promise<AIResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://localhost:8000/analyze-board', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing with VILA:', error);
    throw error;
  }
};
