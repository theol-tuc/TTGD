import React, {useContext} from 'react';
import { Card, Space, Tooltip, Typography } from 'antd';
import { ItemType, IMAGE_FILENAMES } from '../parts/constants';
import { useChallenge } from '../components/challengeContext';

const { Text } = Typography;

interface PartItem {
    type: ItemType;
    name: string;
    count?: number;
}

export const PartsPanel: React.FC = () => {
    const { currentChallenge } = useChallenge();

    const handleDragStart = (e: React.DragEvent, type: ItemType) => {
        e.dataTransfer.setData('text/plain', type);
    };

    const getAvailableParts = (): PartItem[] => {
        const partItems = [
            //{ type: ItemType.BallBlue, name: 'Blue Ball' },
            //{ type: ItemType.BallRed, name: 'Red Ball' },
            { type: ItemType.RampLeft, name: 'Ramp' },
            { type: ItemType.BitLeft, name: 'Bit' },
            { type: ItemType.Crossover, name: 'Crossover' },
            { type: ItemType.Intercept, name: 'Interceptor' },
            { type: ItemType.Gear, name: 'Gear' },
            { type: ItemType.GearBitLeft, name: 'Gear Bit' },
        ];

        if (!currentChallenge?.availableParts) {
            return partItems;
        }

        return partItems.map(part => ({
            ...part,
            count: currentChallenge.availableParts?.[part.type]
        }));
    };

    const partItems = getAvailableParts();

    const isUnlimited = (count: number | undefined): boolean => {
        return count === 999;
    };

    const isPartSpecified = (type: ItemType): boolean => {
        return currentChallenge?.availableParts?.[type] !== undefined;
    };

    return (
        <Card title="Available Parts" bordered={false}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space wrap>
                    {partItems.map((part) => {
                        // A part is available if:
                        // 1. We're in free play mode (no availableParts)
                        // 2. or the part is specified in availableParts and either:
                        //    - has 999 count (unlimited)
                        //    - has count > 0
                        // If the count is = 0 then the aprt in unavailable
                        const isAvailable = !currentChallenge?.availableParts || 
                            (isPartSpecified(part.type) && 
                             (isUnlimited(currentChallenge.availableParts![part.type]) || 
                              currentChallenge.availableParts![part.type]! > 0));

                        const getTooltipText = () => {
                            if (!currentChallenge?.availableParts) return 'Unlimited';
                            if (!isPartSpecified(part.type)) return 'Unavailable';
                            if (isUnlimited(currentChallenge.availableParts[part.type])) return 'Unlimited';
                            if (currentChallenge.availableParts[part.type] === 0) return 'Unavailable';
                            return `Available: ${currentChallenge.availableParts[part.type]}`;
                        };

                        return (
                            <Tooltip
                                key={part.type}
                                title={getTooltipText()}
                            >
                                <Card.Grid
                                    style={{
                                        width: '10vw',
                                        height: '9vh',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        cursor: isAvailable ? 'grab' : 'not-allowed',
                                        opacity: isAvailable ? 1 : 0.5,
                                        borderRadius: '6px',
                                    }}
                                    draggable={isAvailable}
                                    onDragStart={(e) => isAvailable && handleDragStart(e, part.type)}
                                >
                                    <img
                                        src={IMAGE_FILENAMES[part.type]}
                                        alt={part.name}
                                        style={{
                                            width: '80%',
                                            height: '100%',
                                            objectFit: 'contain',
                                            marginBottom: '5px'
                                        }}
                                    />
                                    <div>
                                        <Text style={{ fontSize: '11px' }}>{part.name}</Text>
                                        {isPartSpecified(part.type) && !isUnlimited(currentChallenge.availableParts![part.type]) && currentChallenge.availableParts![part.type]! > 0 && (
                                            <Text style={{ fontSize: '9px', display: 'block' }}>
                                                {currentChallenge.availableParts![part.type]} left
                                            </Text>
                                        )}
                                    </div>
                                </Card.Grid>
                            </Tooltip>
                        );
                    })}
                </Space>
            </Space>
        </Card>
    );
};