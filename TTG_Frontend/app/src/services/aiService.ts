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
    console.log('Sending file to analyze:', file.name, file.size, 'bytes');
    const response = await axios.post(`${API_URL}/analyze-board`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });

    console.log('Received response:', response.data);
    
    if (!response.data || (!response.data.status && !response.data.analysis)) {
      throw new Error('Invalid response format from server');
    }

    return {
      status: response.data.status || 'error',
      analysis: response.data.analysis || 'No analysis available'
    };
  } catch (error) {
    console.error('Error analyzing with VILA:', error);
    if (axios.isAxiosError(error)) {
      const errorMessage = error.response?.data?.detail || error.message;
      console.error('Error details:', errorMessage);
      throw new Error(errorMessage);
    }
    throw error;
  }
};
