import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Paper, Typography, Button } from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [boardState, setBoardState] = useState(null);
  const [selectedComponent, setSelectedComponent] = useState(null);

  useEffect(() => {
    fetchBoardState();
  }, []);

  const fetchBoardState = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/board/state`);
      setBoardState(response.data);
    } catch (error) {
      console.error('Error fetching board state:', error);
    }
  };

  const placeComponent = async (x, y) => {
    if (!selectedComponent) return;
    
    try {
      await axios.post(`${API_BASE_URL}/board/component`, {
        type: selectedComponent,
        x,
        y
      });
      fetchBoardState();
    } catch (error) {
      console.error('Error placing component:', error);
    }
  };

  const dropMarble = async (x) => {
    try {
      await axios.post(`${API_BASE_URL}/board/drop`, { x });
      fetchBoardState();
    } catch (error) {
      console.error('Error dropping marble:', error);
    }
  };

  const getSolution = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/solver/plan`);
      console.log('AI Solution:', response.data);
    } catch (error) {
      console.error('Error getting solution:', error);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Turing Tumble Simulator
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              {/* Board visualization will go here */}
              <Typography variant="h6">Game Board</Typography>
              {boardState && (
                <pre>{JSON.stringify(boardState, null, 2)}</pre>
              )}
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Controls</Typography>
              <Box sx={{ mt: 2 }}>
                <Button 
                  variant="contained" 
                  onClick={() => setSelectedComponent('RAMP_LEFT')}
                  sx={{ mr: 1, mb: 1 }}
                >
                  Ramp Left
                </Button>
                <Button 
                  variant="contained" 
                  onClick={() => setSelectedComponent('RAMP_RIGHT')}
                  sx={{ mr: 1, mb: 1 }}
                >
                  Ramp Right
                </Button>
                <Button 
                  variant="contained" 
                  onClick={() => setSelectedComponent('CROSSOVER')}
                  sx={{ mr: 1, mb: 1 }}
                >
                  Crossover
                </Button>
                <Button 
                  variant="contained" 
                  onClick={() => setSelectedComponent('INTERCEPTOR')}
                  sx={{ mr: 1, mb: 1 }}
                >
                  Interceptor
                </Button>
              </Box>
              
              <Box sx={{ mt: 2 }}>
                <Button 
                  variant="contained" 
                  color="primary"
                  onClick={() => dropMarble(7)}
                  sx={{ mr: 1 }}
                >
                  Drop Blue Marble
                </Button>
                <Button 
                  variant="contained" 
                  color="secondary"
                  onClick={getSolution}
                >
                  Get AI Solution
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default App; 