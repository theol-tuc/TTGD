import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import BoardGrid from './BoardGrid';
import ComponentPalette from './ComponentPalette';
import { dropMarble, resetBoard, getBoard, setBoard } from './services/api';

const BOARD_HEIGHT = 17;
const BOARD_WIDTH = 15;

function App() {
  const [board, setBoardState] = useState(Array(BOARD_HEIGHT).fill(null).map(() => Array(BOARD_WIDTH).fill('.')));
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [animation, setAnimation] = useState({ path: [], finalBoard: null, marbleColor: null, currentStep: 0, isPlaying: false });
  const intervalRef = useRef(null);

  // Sound effect
  const playDropSound = () => {
    const audio = new window.Audio('/marble-drop.mp3');
    audio.play();
  };

  // Fetch board from backend on load
  useEffect(() => {
    (async () => {
      try {
        const result = await getBoard();
        setBoardState(result.board);
      } catch (err) {
        setError('Failed to fetch board from backend.');
      }
    })();
  }, []);

  const handleCellClick = async (row, col) => {
    if (selectedComponent) {
      const newBoard = board.map(r => [...r]);
      newBoard[row][col] = selectedComponent;
      setBoardState(newBoard);
      try {
        await setBoard(newBoard);
      } catch (err) {
        setError('Failed to update board on backend.');
      }
    }
  };

  const handleReset = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await resetBoard();
      setBoardState(result.board);
      setAnimation({ path: [], finalBoard: null, marbleColor: null, currentStep: 0, isPlaying: false });
      clearInterval(intervalRef.current);
    } catch (err) {
      setError('Failed to reset board. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const startAnimation = () => {
    if (!animation.path.length) return;
    setAnimation(a => ({ ...a, isPlaying: true }));
    playDropSound();
    intervalRef.current = setInterval(() => {
      setAnimation(a => {
        if (a.currentStep < a.path.length - 1) {
          return { ...a, currentStep: a.currentStep + 1 };
        } else {
          clearInterval(intervalRef.current);
          setTimeout(() => setBoardState(a.finalBoard), 300);
          return { ...a, isPlaying: false };
        }
      });
    }, 120);
  };

  const pauseAnimation = () => {
    setAnimation(a => ({ ...a, isPlaying: false }));
    clearInterval(intervalRef.current);
  };

  const stepAnimation = () => {
    if (!animation.path.length) return;
    if (animation.currentStep < animation.path.length - 1) {
      setAnimation(a => ({ ...a, currentStep: a.currentStep + 1 }));
    } else {
      setBoardState(animation.finalBoard);
      setAnimation(a => ({ ...a, isPlaying: false }));
      clearInterval(intervalRef.current);
    }
  };

  const handleTrigger = async (side) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await dropMarble(board, side);
      setAnimation({
        path: result.path,
        finalBoard: result.board,
        marbleColor: side === 'left' ? 'B' : 'R',
        currentStep: 0,
        isPlaying: false
      });
      setBoardState(board => {
        const tempBoard = board.map(r => [...r]);
        const [row, col] = result.path[0];
        tempBoard[row][col] = side === 'left' ? 'B' : 'R';
        return tempBoard;
      });
    } catch (err) {
      setError('Failed to drop marble. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Animate marble as currentStep changes
  useEffect(() => {
    if (!animation.path.length) return;
    if (animation.currentStep === 0) return;
    if (animation.currentStep < animation.path.length) {
      setBoardState(board => {
        const tempBoard = board.map(r => [...r]);
        // Clear previous marble
        const [prevRow, prevCol] = animation.path[animation.currentStep - 1];
        if (tempBoard[prevRow][prevCol] === 'O' || tempBoard[prevRow][prevCol] === 'B' || tempBoard[prevRow][prevCol] === 'R') tempBoard[prevRow][prevCol] = '.';
        // Draw current marble
        const [row, col] = animation.path[animation.currentStep];
        tempBoard[row][col] = animation.marbleColor;
        return tempBoard;
      });
    }
  }, [animation.currentStep, animation.path, animation.marbleColor]);

  // Stop interval if animation is paused
  useEffect(() => {
    if (!animation.isPlaying) clearInterval(intervalRef.current);
  }, [animation.isPlaying]);

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'flex-start' }}>
      <ComponentPalette selected={selectedComponent} onSelect={setSelectedComponent} />
      <div>
        <h1>Turing Tumble Game</h1>
        {error && <div className="error-message">{error}</div>}
        <BoardGrid board={board} onCellClick={handleCellClick} />
        <div style={{ display: 'flex', gap: '16px', marginTop: '16px', justifyContent: 'center' }}>
          <button onClick={() => handleTrigger('left')} disabled={isLoading || animation.isPlaying}>Trigger Left</button>
          <button onClick={() => handleTrigger('right')} disabled={isLoading || animation.isPlaying}>Trigger Right</button>
          <button onClick={handleReset} disabled={isLoading || animation.isPlaying}>Reset</button>
        </div>
        {animation.path.length > 0 && (
          <div style={{ display: 'flex', gap: '12px', marginTop: '12px', justifyContent: 'center' }}>
            <button onClick={startAnimation} disabled={animation.isPlaying || animation.currentStep >= animation.path.length - 1}>Play</button>
            <button onClick={pauseAnimation} disabled={!animation.isPlaying}>Pause</button>
            <button onClick={stepAnimation} disabled={animation.isPlaying || animation.currentStep >= animation.path.length - 1}>Step</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
