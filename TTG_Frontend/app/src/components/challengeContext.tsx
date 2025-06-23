// src/components/ChallengeContext.tsx
import React, { createContext, useContext, useState } from 'react';
import { Challenge, DEFAULT_CHALLENGE } from './challenges';
import { ItemType } from '../parts/constants';

interface ChallengeContextType {
    currentChallenge: Challenge;
    setCurrentChallenge: (challenge: Challenge) => void;
    resetToDefault: () => void;
    decrementPartCount: (type: ItemType) => void;
}

export const ChallengeContext = createContext<ChallengeContextType>({
    currentChallenge: DEFAULT_CHALLENGE,
    setCurrentChallenge: () => {},
    resetToDefault: () => {},
    decrementPartCount: () => {}
});

export const ChallengeProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [currentChallenge, setCurrentChallenge] = useState<Challenge>(DEFAULT_CHALLENGE);

    const resetToDefault = () => {
        setCurrentChallenge(DEFAULT_CHALLENGE);
    };

    const decrementPartCount = (type: ItemType) => {
        setCurrentChallenge(prevChallenge => {
            if (!prevChallenge.availableParts || prevChallenge.availableParts[type] === undefined) {
                return prevChallenge;
            }

            const currentCount = prevChallenge.availableParts![type]!;
            if (currentCount <= 0) {
                return prevChallenge;
            }

            return {
                ...prevChallenge,
                availableParts: {
                    ...prevChallenge.availableParts,
                    [type]: currentCount - 1
                }
            };
        });
    };

    return (
        <ChallengeContext.Provider value={{ currentChallenge, setCurrentChallenge, resetToDefault, decrementPartCount }}>
            {children}
        </ChallengeContext.Provider>
    );
};

export const useChallenge = () => useContext(ChallengeContext);