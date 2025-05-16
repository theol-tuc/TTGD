import React from 'react';
import { analyzeWithVila } from '../services/aiService';

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
    boardRef: React.RefObject<HTMLDivElement>;
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
        if (!boardRef.current) return;

        const canvas = await html2canvas(boardRef.current);
        const blob = await new Promise<Blob | null>((resolve) =>
            canvas.toBlob(resolve, 'image/png')
        );
        if (!blob) return;

        const file = new File([blob], "board.png", { type: "image/png" });
        const formData = new FormData();
        formData.append("file", file);

        const result = await analyzeWithVila(file);  // فراخوانی از ماژول
        alert(JSON.stringify(result));

        try {
            const response = await fetch("http://localhost:8000/analyze-board/", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            alert(data.choices?.[0]?.message?.content || data.description || "No response from VILA");
        } catch (err) {
            console.error("VILA error:", err);
            alert("Failed to analyze with VILA.");
        }
    };

    return (
        <div style={{ padding: '8px' }}>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                {/* All other buttons as before... */}
                <Button type="primary" block onClick={handleVilaClick}>
                    Analyze with VILA
                </Button>
            </Space>
        </div>
    );
};
