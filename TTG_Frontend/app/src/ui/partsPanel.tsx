import React, {useContext} from 'react';
import { Card, Space, Tooltip, Typography } from 'antd';
import { ItemType, IMAGE_FILENAMES } from '../parts/constants';
import { ChallengeContext } from '../components/challengeContext';

const { Text } = Typography;

interface PartItem {
    type: ItemType;
    name: string;
    count?: number;
}

export const PartsPanel: React.FC = () => {
    const { currentChallenge } = useContext(ChallengeContext);

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

    return (
        <Card title="Available Parts" bordered={false}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space wrap>
                    {partItems.map((part) => (
                        <Tooltip
                            key={part.type}
                            title={part.count !== undefined ? `Available: ${part.count}` : 'Unlimited'}
                        >
                            <Card.Grid
                                style={{
                                    width: '10vw',
                                    height: '9vh',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    cursor: part.count === 0 ? 'not-allowed' : 'grab',
                                    opacity: part.count === 0 ? 0.5 : 1,
                                    borderRadius: '6px',
                                }}
                                draggable={part.count !== 0}
                                onDragStart={(e) => part.count !== 0 && handleDragStart(e, part.type)}
                            >
                                <img
                                    src={IMAGE_FILENAMES[part.type]}
                                    alt={part.name}
                                    style={{
                                        width: '80%',
                                        height: '60%',
                                        objectFit: 'contain',
                                        marginBottom: '5px'
                                    }}
                                />
                                <div>
                                    <Text style={{ fontSize: '11px' }}>{part.name}</Text>
                                    {part.count !== undefined && (
                                        <Text style={{ fontSize: '9px', display: 'block' }}>
                                            {part.count} left
                                        </Text>
                                    )}
                                </div>
                            </Card.Grid>
                        </Tooltip>
                    ))}
                </Space>
            </Space>
        </Card>
    );
};