import React from 'react';
import { Card, Space, Typography } from 'antd';
import { ItemType, IMAGE_FILENAMES } from '../parts/constants';
import { addComponent } from '../services/api';

const { Title } = Typography;

const partItems = [
//    { type: ItemType.BallBlue, name: 'Blue Ball' },
 //   { type: ItemType.BallRed, name: 'Red Ball' },
    { type: ItemType.RampLeft, name: 'Ramp' },
    { type: ItemType.BitLeft, name: 'Bit' },
    { type: ItemType.Crossover, name: 'Crossover' },
    { type: ItemType.GearBitLeft, name: 'Gear Bit' },
    { type: ItemType.Gear, name: 'Gear' },
    { type: ItemType.Intercept, name: 'Interceptor' },
];

export const PartsPanel: React.FC = () => {
    const handleDragStart = (e: React.DragEvent, type: ItemType) => {
        e.dataTransfer.setData('text/plain', type);
    };

    return (
        <Card title="Parts" bordered={false}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space wrap>
                    {partItems.map((part) => (
                        <Card.Grid
                            key={part.type}
                            style={{
                                width: '10vw',
                                height: '9vh',
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'grab',
                                borderRadius: '6px',
                            }}
                            draggable
                            onDragStart={(e) => handleDragStart(e, part.type)}
                        >
                            <img 
                                src={IMAGE_FILENAMES[part.type]} 
                                alt={part.name}
                                style={{
                                    width: '100%',
                                    height: '150%',
                                    objectFit: 'contain',
                                    marginBottom: '5px'
                                }}
                            />
                            <span style={{fontSize: '11px'}}>{part.name}</span>
                        </Card.Grid>
                    ))}
                </Space>
            </Space>
        </Card>
    );
};