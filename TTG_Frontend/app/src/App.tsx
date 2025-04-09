import React, {JSX} from 'react';
import './App.css';
import { Board } from './board/board';

function App(): JSX.Element {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to Turing Tumble</h1>
            </header>
            <main>
                <Board />
            </main>
        </div>
    );
}

export default App;
