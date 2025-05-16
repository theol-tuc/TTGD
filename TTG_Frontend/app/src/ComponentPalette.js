import React from 'react';
import './ComponentPalette.css';
import RampLeftIcon from './icons/RampLeftIcon';
import RampRightIcon from './icons/RampRightIcon';
import CrossoverIcon from './icons/CrossoverIcon';
import InterceptorIcon from './icons/InterceptorIcon';
import BitLeftIcon from './icons/BitLeftIcon';
import BitRightIcon from './icons/BitRightIcon';
import GearBitIcon from './icons/GearBitIcon';

const COMPONENTS = [
  { name: 'Ramp Left', symbol: '\\', icon: <RampLeftIcon /> },
  { name: 'Ramp Right', symbol: '/', icon: <RampRightIcon /> },
  { name: 'Crossover', symbol: '+', icon: <CrossoverIcon /> },
  { name: 'Interceptor', symbol: 'X', icon: <InterceptorIcon /> },
  { name: 'Bit Left', symbol: '<', icon: <BitLeftIcon /> },
  { name: 'Bit Right', symbol: '>', icon: <BitRightIcon /> },
  { name: 'Gear Bit', symbol: 'G', icon: <GearBitIcon /> },
];

const ComponentPalette = ({ selected, onSelect }) => (
  <div className="component-palette">
    {COMPONENTS.map((comp) => (
      <button
        key={comp.symbol}
        className={`palette-btn${selected === comp.symbol ? ' selected' : ''}`}
        onClick={() => onSelect(comp.symbol)}
      >
        <span className="palette-symbol">{comp.icon}</span>
        <span className="palette-label">{comp.name}</span>
      </button>
    ))}
  </div>
);

export default ComponentPalette; 