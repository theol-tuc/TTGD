import React from 'react';
import { Button, Space, Divider, Tooltip } from 'antd';
import {
    ZoomInOutlined,
    ZoomOutOutlined,
    PauseOutlined,
    ForwardOutlined,
    ClearOutlined,
    VerticalAlignTopOutlined,
    CaretLeftOutlined,
    CaretRightOutlined,
    PlayCircleOutlined,
    RobotOutlined
} from '@ant-design/icons';

interface ToolbarProps {
    onZoomIn: () => void;
    onZoomOut: () => void;
    onSlowDown: () => void;
    onSpeedUp: () => void;
    onClearBoard: () => void;
    onResetMarbles: () => void;
    onTriggerLeft: () => void;
    onTriggerRight: () => void;
    onToggleAI: () => void;
    isRunning: boolean;
    currentSpeed: number;
    isAIVisible: boolean;
}

export const Toolbar: React.FC<ToolbarProps> = ({onZoomIn, onZoomOut, onSlowDown, onSpeedUp, onClearBoard, onResetMarbles, onTriggerLeft, onTriggerRight,onToggleAI, isRunning, currentSpeed, isAIVisible}) => {
    const speedOptions = [0.5, 1, 2, 5];
    return (
        <div style={{ padding: '8px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <Tooltip title="Zoom in (Ctrl + Plus)">
                        <Button
                            icon={<ZoomInOutlined />}
                            block
                            onClick={onZoomIn}
                        >
                            Zoom In
                        </Button>
                    </Tooltip>

                    <Tooltip title="Zoom out (Ctrl + Minus)">
                        <Button
                            icon={<ZoomOutOutlined />}
                            block
                            onClick={onZoomOut}
                        >
                            Zoom Out
                        </Button>
                    </Tooltip>

                    <Divider style={{ margin: '12px 0' }} />

                    <Tooltip title={isRunning ? "Pause simulation" : "Start simulation"}>
                        <Button
                            icon={isRunning ? <PauseOutlined /> : <PlayCircleOutlined />}
                            block
                            onClick={isRunning ? onSlowDown : onSpeedUp}
                            type={isRunning ? 'default' : 'primary'}
                        >
                            {isRunning ? 'Pause' : 'Start'}
                        </Button>
                    </Tooltip>

                    <Tooltip title="Increase simulation speed">
                        <Button
                            icon={<ForwardOutlined />}
                            block
                            onClick={onSpeedUp}
                            disabled={currentSpeed >= speedOptions[speedOptions.length - 1]}
                        >
                            Speed Up ({currentSpeed}x)
                        </Button>
                    </Tooltip>

                    <Tooltip title="Decrease simulation speed">
                        <Button
                            icon={<ForwardOutlined rotate={90} />}
                            block
                            onClick={onSlowDown}
                            disabled={currentSpeed <= speedOptions[0]}
                        >
                            Slow Down ({currentSpeed}x)
                        </Button>
                    </Tooltip>

                    <Divider style={{ margin: '12px 0' }} />

                    <Tooltip title="Remove all parts from the board">
                        <Button
                            icon={<ClearOutlined />}
                            block
                            onClick={onClearBoard}
                            danger
                        >
                            Clear Board
                        </Button>
                    </Tooltip>

                    <Tooltip title="Reset all marbles to their starting positions">
                        <Button
                            icon={<VerticalAlignTopOutlined />}
                            block
                            onClick={onResetMarbles}
                        >
                            Reset Marbles
                        </Button>
                    </Tooltip>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Space direction="vertical" size="small" style={{ width: '100%' }}>
                    <Tooltip title="Trigger left lever (Blue)">
                        <Button
                            icon={<CaretLeftOutlined />}
                            block
                            onClick={onTriggerLeft}
                            type="primary"
                            ghost
                        >
                            Trigger Left
                        </Button>
                    </Tooltip>

                    <Tooltip title="Trigger right lever (Red)">
                        <Button
                            icon={<CaretRightOutlined />}
                            block
                            onClick={onTriggerRight}
                            danger
                            ghost
                        >
                            Trigger Right
                        </Button>
                    </Tooltip>

                    <Divider style={{ margin: '12px 0' }} />

                    <Tooltip title={isAIVisible ? "Hide AI Assistant" : "Show AI Assistant"}>
                        <Button
                            icon={<RobotOutlined />}
                            block
                            onClick={onToggleAI}
                            type={isAIVisible ? 'primary' : 'default'}
                            style={{ marginTop: 8 }}
                        >
                            {isAIVisible ? 'Hide AI' : 'AI Assistant'}
                        </Button>
                    </Tooltip>
                </Space>
            </Space>
        </div>
    );
};