import React from 'react';
import { Card, Space, Typography } from 'antd';
import { ItemType } from '../parts/constants';

const { Title } = Typography;

const partItems = [
    { type: ItemType.RampLeft, name: 'Ramp Left' },
    { type: ItemType.RampRight, name: 'Ramp Right' },
    //{ type: ItemType.Gear, name: 'Gear' },
    //{ type: ItemType.GearBit, name: 'Gear Bit' },
    //{ type: ItemType.Interceptor, name: 'Interceptor' },
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
        <Card title="Parts" bordered={false}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Title level={5} style={{ margin: 0 }}>Parts</Title>
                <Space wrap>
                    {partItems.map((part) => (
                        <Card.Grid
                            key={part.type}
                            style={{
                                width: '13vw',
                                height: '12vh',
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'pointer',
                                overflow: "hidden"
                            }}
                            onClick={() => handlePartClick(part.type)}
                        >
                            <div style={{
                                width: '10vw',
                                height: '10vh',
                                backgroundColor: '#f0f0f0',
                                borderRadius: '4px',
                                marginBottom: '8px'
                            }} />
                            <span style={{ fontSize: '12px' }}>{part.name}</span>
                        </Card.Grid>
                    ))}
                </Space>
            </Space>
        </Card>
    );
};