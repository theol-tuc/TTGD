import React, { JSX } from 'react';
import './App.css';
import Board from './board/board';
import { Toolbar } from "./ui/toolbar";

function App(): JSX.Element {
    return (
        <div className="App">
            <header className="App-header">
                <h4>Welcome to Turing Tumble</h4>
            </header>
            <div className="main-content">
                <Board />
                <Toolbar />
            </div>
        </div>
    );
}

export default App;