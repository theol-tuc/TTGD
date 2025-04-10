import React from 'react';
import { Card, Space, Typography } from 'antd';
import { ItemType, IMAGE_FILENAMES } from '../parts/constants';

const { Title } = Typography;

const partItems = [
    { type: ItemType.BallBlue, name: 'Blue Ball' },
    { type: ItemType.BallRed, name: 'Red Ball' },
    { type: ItemType.RampLeft, name: 'Ramp Left' },
    { type: ItemType.RampRight, name: 'Ramp Right' },
    //{ type: ItemType.Gear, name: 'Gear' },
    //{ type: ItemType.GearBit, name: 'Gear Bit' },
    { type: ItemType.Intercept, name: 'Interceptor' },
    { type: ItemType.BitLeft, name: 'Bit Left' },
    { type: ItemType.BitRight, name: 'Bit Right' },
    //{ type: ItemType.Gearbox, name: 'Gearbox' },
    { type: ItemType.Crossover, name: 'Crossover' },
];

export const PartsPanel: React.FC = () => {
    const handlePartClick = (type: ItemType) => {
        console.log('Selected part:', type);
        // Add logic to handle part selection
    };

    return (
        <Card title="Parts to use" bordered={false}>
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
                                cursor: 'pointer',
                                borderRadius: '6px',
                                overflow: "hidden"}}
                            onClick={() => handlePartClick(part.type)}>
                            <img
                                src={IMAGE_FILENAMES[part.type]}
                                alt={part.name}
                                style={{
                                    width: '40px',
                                    height: '40px',
                                    objectFit: 'contain',
                                    marginBottom: '8px'}}/>
                            <span style={{fontSize: '11px'}}>{part.name}</span>
                        </Card.Grid>
                    ))}
                </Space>
            </Space>
        </Card>
    );
};