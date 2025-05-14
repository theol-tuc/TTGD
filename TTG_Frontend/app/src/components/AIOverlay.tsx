import React, { useState } from 'react';
import { aiService, AIResponse } from '../services/aiService';
import { Button, Card, Space, Typography, Divider, Row, Col, Alert } from 'antd';
import { CloseOutlined, RobotOutlined, ThunderboltOutlined, PlayCircleOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

interface AIOverlayProps {
    onAIMove: () => void;
    onClose: () => void;
}

export const AIOverlay: React.FC<AIOverlayProps> = ({ onAIMove, onClose }) => {
    const [aiResponse, setAIResponse] = useState<AIResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGetAIMove = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await aiService.getAIMove();
            setAIResponse(response);
        } catch (err) {
            setError('Failed to get AI move. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleExecuteAIMove = async () => {
        if (!aiResponse) return;
        
        setIsLoading(true);
        setError(null);
        try {
            await aiService.executeAIMove();
            onAIMove();
            setAIResponse(null);
        } catch (err) {
            setError('Failed to execute AI move. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card
            style={{position: 'fixed', top: 80, left: 220, width: 320, maxHeight: 'calc(100vh - 100px)', borderRadius: 12, boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)', zIndex: 1001, overflow: 'hidden', border: 'none'}}
            title={
                <Space>
                    <RobotOutlined style={{ color: '#722ED1' }} />
                    <Text strong>AI Assistant</Text>
                </Space>
            }
            extra={
                <Button
                    icon={<CloseOutlined />}
                    onClick={onClose}
                    type="text"
                    size="small"
                />
            }
        >
            <div style={{display: 'flex', flexDirection: 'column', gap: 16, maxHeight: 'calc(100vh - 160px)', overflowY: 'auto', padding: 8}}>
                {error && (
                    <Alert
                        message={error}
                        type="error"
                        showIcon
                        closable
                        onClose={() => setError(null)}
                        style={{ marginBottom: 16 }}
                    />
                )}

                <Row gutter={[16, 16]}>
                    <Col span={24}>
                        <Button
                            icon={<ThunderboltOutlined />}
                            onClick={handleGetAIMove}
                            loading={isLoading}
                            block
                            type="primary"
                        >
                            Get AI Suggestion
                        </Button>
                    </Col>

                    {aiResponse && (
                        <Col span={24}>
                            <Button
                                icon={<PlayCircleOutlined />}
                                onClick={handleExecuteAIMove}
                                loading={isLoading}
                                block
                                type="default"
                            >
                                Execute Move
                            </Button>
                        </Col>
                    )}
                </Row>

                {aiResponse && (
                    <>
                        <Divider style={{ margin: '8px 0' }} />

                        <Card
                            title="AI's Move"
                            size="small"
                            style={{ borderRadius: 8 }}
                        >
                            <Space direction="vertical">
                                <Text strong>Action:</Text>
                                <Text code>{aiResponse.move.action}</Text>

                                <Text strong style={{ marginTop: 8 }}>Parameters:</Text>
                                <Text code>
                                    {JSON.stringify(aiResponse.move.parameters, null, 2)}
                                </Text>
                            </Space>
                        </Card>

                        <Card
                            title="Explanation"
                            size="small"
                            style={{ borderRadius: 8 }}
                        >
                            <Text>{aiResponse.explanation}</Text>
                        </Card>
                    </>
                )}
            </div>
        </Card>
    );
};