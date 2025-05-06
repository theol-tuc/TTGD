// src/components/ChallengeContext.tsx
import React, { createContext, useContext, useState } from 'react';
import { Challenge, DEFAULT_CHALLENGE } from './challenges';

interface ChallengeContextType {
    currentChallenge: Challenge;
    setCurrentChallenge: (challenge: Challenge) => void;
    resetToDefault: () => void;
}

export const ChallengeContext = createContext<ChallengeContextType>({
    currentChallenge: DEFAULT_CHALLENGE,
    setCurrentChallenge: () => {},
    resetToDefault: () => {}
});

export const ChallengeProvider: React.FC = ({ children }) => {
    const [currentChallenge, setCurrentChallenge] = useState<Challenge>(DEFAULT_CHALLENGE);

    const resetToDefault = () => {
        setCurrentChallenge(DEFAULT_CHALLENGE);
    };

    return (
        <ChallengeContext.Provider value={{ currentChallenge, setCurrentChallenge, resetToDefault }}>
            {children}
        </ChallengeContext.Provider>
    );
};

export const useChallenge = () => useContext(ChallengeContext);