import React, { useState } from 'react';
import { Button, Space, Divider, Tooltip, Typography, Card } from 'antd';
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
    RobotOutlined,
    PauseCircleOutlined,
    ReloadOutlined,
    DeleteOutlined,
    RocketOutlined
} from '@ant-design/icons';
import { captureAndAnalyzeBoard, VilaAnalysis } from '../services/vilaService';

const { Text } = Typography;

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
    onRun: () => void;
    onPause: () => void;
    onReset: () => void;
    onClear: () => void;
}

export const Toolbar: React.FC<ToolbarProps> = ({
    onZoomIn,
    onZoomOut,
    onSlowDown,
    onSpeedUp,
    onClearBoard,
    onResetMarbles,
    onTriggerLeft,
    onTriggerRight,
    onToggleAI,
    isRunning,
    currentSpeed,
    isAIVisible,
    onRun,
    onPause,
    onReset,
    onClear
}) => {
    const speedOptions = [0.5, 1, 2, 5];
    const [vilaAnalysisResult, setVilaAnalysisResult] = useState<VilaAnalysis | null>(null);

    const handleVilaAnalysis = async () => {
        try {
            // Get the board element
            const boardElement = document.querySelector('.board-container');
            if (!boardElement) {
                throw new Error('Board element not found');
            }

            // Show loading state
            const button = document.querySelector('.vila-analysis-button');
            if (button) {
                button.setAttribute('disabled', 'true');
                button.textContent = 'Analyzing...';
            }

            // Capture and analyze
            const analysis = await captureAndAnalyzeBoard(boardElement as HTMLElement);

            // Show results
            if (analysis.status === 'success') {
                setVilaAnalysisResult(analysis);
            } else {
                throw new Error('Analysis failed');
            }
        } catch (error) {
            console.error('VILA analysis error:', error);
            alert('Failed to analyze board with VILA. Please try again.');
            setVilaAnalysisResult(null); // Clear previous results on error
        } finally {
            // Reset button state
            const button = document.querySelector('.vila-analysis-button');
            if (button) {
                button.removeAttribute('disabled');
                button.textContent = 'Analyze with VILA';
            }
        }
    };

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
                            type="primary"
                            ghost
                        >
                            Trigger Right
                        </Button>
                    </Tooltip>

                    <Tooltip title="Toggle AI Assistant (experimental)">
                        <Button
                            icon={<RobotOutlined />}
                            block
                            onClick={onToggleAI}
                        >
                            AI Assistant
                        </Button>
                    </Tooltip>

                    <Divider style={{ margin: '12px 0' }} />

                    <Tooltip title="Analyze current board state with NVIDIA VILA">
                        <Button
                            className="vila-analysis-button"
                            onClick={handleVilaAnalysis}
                            type="primary"
                            style={{ backgroundColor: '#76b900' }}  // NVIDIA green
                            block
                        >
                            Analyze with VILA
                        </Button>
                    </Tooltip>

                    {vilaAnalysisResult && (
                        <Card
                            title="VILA Analysis"
                            size="small"
                            style={{ width: '100%', marginTop: '10px' }}
                        >
                            <Text>Recommended Move: {vilaAnalysisResult.recommended_move || 'N/A'}</Text><br/>
                            <Text>Confidence: {vilaAnalysisResult.confidence !== undefined ? `${vilaAnalysisResult.confidence}%` : 'N/A'}</Text>
                        </Card>
                    )}
                </Space>
            </Space>
        </div>
    );
};