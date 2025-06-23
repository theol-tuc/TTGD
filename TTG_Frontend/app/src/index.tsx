import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from "./App";
import {ChallengeProvider} from "./components/challengeContext";

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
    <ChallengeProvider>
        <App/>
    </ChallengeProvider>
);