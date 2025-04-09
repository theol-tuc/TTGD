import React from 'react';
import { Button, Space, Divider } from 'antd';
import {
    ZoomInOutlined,
    ZoomOutOutlined,
    PauseOutlined,
    ForwardOutlined,
    ClearOutlined,
    VerticalAlignTopOutlined,
    CaretLeftOutlined,
    CaretRightOutlined
} from '@ant-design/icons';

export const Toolbar: React.FC = () => {
    const handleClick = (action: string) => {
        console.log(`Action: ${action}`);
    };

    return (
        <div style={{ padding: '8px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <Button
                        icon={<ZoomInOutlined />}
                        block
                        onClick={() => handleClick('zoom-in')}
                    >
                        Zoom In
                    </Button>
                    <Button
                        icon={<ZoomOutOutlined />}
                        block
                        onClick={() => handleClick('zoom-out')}
                    >
                        Zoom Out
                    </Button>
                    <Button
                        icon={<PauseOutlined />}
                        block
                        onClick={() => handleClick('slow-down')}
                    >
                        Slow Down
                    </Button>
                    <Button
                        icon={<ForwardOutlined />}
                        block
                        onClick={() => handleClick('speed-up')}
                    >
                        Speed Up
                    </Button>
                    <Button
                        icon={<ClearOutlined />}
                        block
                        onClick={() => handleClick('clear-board')}
                    >
                        Clear Board
                    </Button>
                    <Button
                        icon={<VerticalAlignTopOutlined />}
                        block
                        onClick={() => handleClick('reset-marbles')}
                    >
                        Move Marbles to Top
                    </Button>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <Button
                        icon={<CaretLeftOutlined />}
                        block
                        onClick={() => handleClick('trigger-left')}
                    >
                        Trigger Left
                    </Button>
                    <Button
                        icon={<CaretRightOutlined />}
                        block
                        onClick={() => handleClick('trigger-right')}
                    >
                        Trigger Right
                    </Button>
                </Space>
            </Space>
        </div>
    );
};