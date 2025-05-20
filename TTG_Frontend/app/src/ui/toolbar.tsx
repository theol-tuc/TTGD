import React, { RefObject } from 'react';
import { analyzeWithVila } from '../services/aiService';

import { Button, Space, Divider, Tooltip, message, Modal } from 'antd';
import {
    ZoomInOutlined,
    ZoomOutOutlined,
    PauseOutlined,
    ForwardOutlined,
    ClearOutlined,
    VerticalAlignTopOutlined,
    CaretLeftOutlined,
    CaretRightOutlined,
    PlayCircleOutlined
} from '@ant-design/icons';
import html2canvas from 'html2canvas';

interface ToolbarProps {
    onZoomIn: () => void;
    onZoomOut: () => void;
    onSlowDown: () => void;
    onSpeedUp: () => void;
    onClearBoard: () => void;
    onResetMarbles: () => void;
    onTriggerLeft: () => void;
    onTriggerRight: () => void;
    isRunning: boolean;
    currentSpeed: number;
    boardRef: RefObject<HTMLDivElement | null>;
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
    isRunning,
    currentSpeed,
    boardRef
}) => {
    const speedOptions = [0.5, 1, 2, 5];

    const handleVilaClick = async () => {
        if (!boardRef.current) {
            message.error('Board reference not found');
            return;
        }

        try {
            message.loading({ content: 'Capturing board image...', key: 'vilaAnalysis' });
            const canvas = await html2canvas(boardRef.current);
            const blob = await new Promise<Blob | null>((resolve) => 
                canvas.toBlob(resolve, 'image/png')
            );

            if (!blob) {
                message.error({ content: 'Failed to create image from board', key: 'vilaAnalysis' });
                return;
            }

            const file = new File([blob], "board.png", { type: "image/png" });
            message.loading({ content: 'Analyzing board with VILA (this may take a few minutes)...', key: 'vilaAnalysis' });
            const result = await analyzeWithVila(file);
            
            message.success({ content: 'Analysis completed', key: 'vilaAnalysis' });
            Modal.info({
                title: 'Board Analysis',
                content: (
                    <div style={{ maxHeight: '60vh', overflow: 'auto' }}>
                        <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                            {result.analysis}
                        </pre>
                    </div>
                ),
                width: 600,
            });
        } catch (err: any) {
            message.destroy();
            message.error({ 
                content: `Analysis failed: ${err.message}`, 
                key: 'vilaAnalysis',
                duration: 5 
            });
        }
    };

    return (
        <div style={{ padding: '8px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Space direction="vertical" style={{ width: '100%' }}>
                    <Tooltip title="Zoom in">
                        <Button icon={<ZoomInOutlined />} onClick={onZoomIn} block>
                            Zoom In
                        </Button>
                    </Tooltip>
                    <Tooltip title="Zoom out">
                        <Button icon={<ZoomOutOutlined />} onClick={onZoomOut} block>
                            Zoom Out
                        </Button>
                    </Tooltip>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Space direction="vertical" style={{ width: '100%' }}>
                    <Tooltip title="Slow down simulation">
                        <Button icon={<PauseOutlined />} onClick={onSlowDown} block>
                            Slow Down
                        </Button>
                    </Tooltip>
                    <Tooltip title="Speed up simulation">
                        <Button icon={<ForwardOutlined />} onClick={onSpeedUp} block>
                            Speed Up ({currentSpeed}x)
                        </Button>
                    </Tooltip>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Space direction="vertical" style={{ width: '100%' }}>
                    <Tooltip title="Clear the board">
                        <Button icon={<ClearOutlined />} onClick={onClearBoard} block>
                            Clear Board
                        </Button>
                    </Tooltip>
                    <Tooltip title="Reset marbles">
                        <Button icon={<VerticalAlignTopOutlined />} onClick={onResetMarbles} block>
                            Reset Marbles
                        </Button>
                    </Tooltip>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Space direction="vertical" style={{ width: '100%' }}>
                    <Tooltip title="Trigger left launcher (Blue)">
                        <Button icon={<CaretLeftOutlined />} onClick={onTriggerLeft} block>
                            Left Trigger
                        </Button>
                    </Tooltip>
                    <Tooltip title="Trigger right launcher (Red)">
                        <Button icon={<CaretRightOutlined />} onClick={onTriggerRight} block>
                            Right Trigger
                        </Button>
                    </Tooltip>
                </Space>

                <Divider style={{ margin: '12px 0' }} />

                <Tooltip title="Analyze the current board layout">
                    <Button 
                        type="primary" 
                        icon={<PlayCircleOutlined />} 
                        onClick={handleVilaClick} 
                        block
                    >
                        Analyze with VILA
                    </Button>
                </Tooltip>
            </Space>
        </div>
    );
};
