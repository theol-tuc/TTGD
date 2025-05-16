import React from 'react';
import './BoardGrid.css';
import RampLeftIcon from './icons/RampLeftIcon';
import RampRightIcon from './icons/RampRightIcon';
import CrossoverIcon from './icons/CrossoverIcon';
import InterceptorIcon from './icons/InterceptorIcon';
import BitLeftIcon from './icons/BitLeftIcon';
import BitRightIcon from './icons/BitRightIcon';
import GearBitIcon from './icons/GearBitIcon';

const MarbleBlue = () => (
  <svg width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="#1976D2" /></svg>
);
const MarbleRed = () => (
  <svg width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="#c62828" /></svg>
);

const ICONS = {
  '\\': <RampLeftIcon />,
  '/': <RampRightIcon />,
  '+': <CrossoverIcon />,
  'X': <InterceptorIcon />,
  '<': <BitLeftIcon />,
  '>': <BitRightIcon />,
  'G': <GearBitIcon />,
  'B': <MarbleBlue />,
  'R': <MarbleRed />,
};

const SYMBOLS = {
  'O': '●', // fallback for generic marble
};

const BoardGrid = ({ board, onCellClick }) => {
  return (
    <div className="board-grid">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className="board-cell"
              onClick={() => onCellClick(rowIndex, colIndex)}
            >
              {ICONS[cell] || SYMBOLS[cell] || ''}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default BoardGrid; 