const API_BASE_URL = 'http://localhost:8000';

export const dropMarble = async (board, side) => {
  try {
    const response = await fetch(`${API_BASE_URL}/drop-marble`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ board, side }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to drop marble');
    }
    
    return await response.json(); // { board, path }
  } catch (error) {
    console.error('Error dropping marble:', error);
    throw error;
  }
};

export const resetBoard = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/reset-board`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      throw new Error('Failed to reset board');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error resetting board:', error);
    throw error;
  }
};

export const getBoard = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/board`);
    if (!response.ok) {
      throw new Error('Failed to fetch board');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching board:', error);
    throw error;
  }
};

export const setBoard = async (board) => {
  try {
    const response = await fetch(`${API_BASE_URL}/set-board`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ board }),
    });
    if (!response.ok) {
      throw new Error('Failed to set board');
    }
    return await response.json();
  } catch (error) {
    console.error('Error setting board:', error);
    throw error;
  }
}; 