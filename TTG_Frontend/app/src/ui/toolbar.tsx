import React from 'react';
import './toolbar.css';

export const Toolbar: React.FC = () => {
    const handleClick = (action: string) => () => {
        console.log(`Action: ${action}`);
        //Button logic here
    };

    return (
        <div className="toolbar">
            <div className="toolbar-button">
                <button onClick={handleClick('zoom-in')}>Zoom In</button>
                <button onClick={handleClick('zoom-out')}>Zoom Out</button>
                <button onClick={handleClick('slow-down')}>Slow Down</button>
                <button onClick={handleClick('speed-up')}>Speed Up</button>
                <button onClick={handleClick('clear-board')}>Clear Board</button>
                <button onClick={handleClick('reset-marbles')}>Move Marbles to Top</button>
            </div>
            <div className="toolbar-bottom">
                <button onClick={handleClick('trigger-left')}>Trigger Left</button>
                <button onClick={handleClick('trigger-right')}>Trigger Right</button>
            </div>
        </div>
    );
};
