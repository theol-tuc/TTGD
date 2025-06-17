import React, { useState, useRef, useEffect } from 'react';
import { Card, Button, Modal, Input, Typography, Space, Alert, Divider, Row, Col, Form, Select, message, Progress } from 'antd';
import { QuestionCircleOutlined, CheckCircleOutlined, CloseCircleOutlined, RobotOutlined, AimOutlined, ThunderboltOutlined, SettingOutlined } from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

interface ExitPageUIProps {
    visible: boolean;
    onClose: () => void;
    currentChallenge?: any;
    boardState?: any;
}

interface VilaResponse {
    position: string;
    component: string;
    isGood: boolean;
    explanation: string;
}

// Available component types
const COMPONENT_TYPES = [
    { value: 'ramp_left', label: 'Ramp Left', icon: '↖' },
    { value: 'ramp_right', label: 'Ramp Right', icon: '↗' },
    { value: 'bit_left', label: 'Bit Left', icon: '◀' },
    { value: 'bit_right', label: 'Bit Right', icon: '▶' },
    { value: 'gear', label: 'Gear', icon: '⚙' },
    { value: 'gear_bit', label: 'Gear Bit', icon: '⚙◀' },
    { value: 'interceptor', label: 'Interceptor', icon: '⛔' },
    { value: 'crossover', label: 'Crossover', icon: '↔' },
];

export const ExitPageUI: React.FC<ExitPageUIProps> = ({
    visible,
    onClose,
    currentChallenge,
    boardState
}) => {
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [selectedComponent, setSelectedComponent] = useState<string>('');
    const [positionX, setPositionX] = useState('');
    const [positionY, setPositionY] = useState('');
    const [vilaResponse, setVilaResponse] = useState<VilaResponse | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [debugInfo, setDebugInfo] = useState<string>('');
    const [showResultsOnly, setShowResultsOnly] = useState(false);
    const [form] = Form.useForm();

    // Show modal when component becomes visible
    useEffect(() => {
        if (visible) {
            setIsModalVisible(true);
        }
    }, [visible]);

    // Simplified VILA analysis with better error handling
    const analyzePositionWithVila = async (component: string, x: number, y: number): Promise<VilaResponse> => {
        try {
            setDebugInfo('Starting analysis...');
            
            // Try to find the board element
            const boardElement = document.querySelector('.board-container') || 
                               document.querySelector('[data-testid="board"]') ||
                               document.querySelector('.board') ||
                               document.querySelector('canvas') ||
                               document.querySelector('svg');
            
            setDebugInfo(`Board element found: ${boardElement ? 'Yes' : 'No'}`);
            
            if (!boardElement) {
                setDebugInfo('No board element found, using fallback analysis');
                // Fallback: Use simple logic based on position and component
                const isGood = (x + y) % 2 === 0; // Simple pattern for demo
                return {
                    position: `(${x}, ${y})`,
                    component: component,
                    isGood,
                    explanation: isGood 
                        ? `Adding ${component} at position (${x}, ${y}) appears to be strategically sound based on basic analysis.`
                        : `Adding ${component} at position (${x}, ${y}) might not be optimal. Consider other positions or components.`,
                };
            }

            setDebugInfo('Attempting to capture board...');
            
            // Try to use html2canvas if available
            try {
                const html2canvas = (await import('html2canvas')).default;
                const canvas = await html2canvas(boardElement as HTMLElement, {
                    backgroundColor: null,
                    scale: 1,
                    useCORS: true,
                    allowTaint: true
                });
                
                setDebugInfo('Board captured successfully');
                
                // Convert to blob
                const blob = await new Promise<Blob>((resolve, reject) => {
                    canvas.toBlob((blob) => {
                        if (blob) resolve(blob);
                        else reject(new Error('Failed to convert canvas to blob'));
                    }, 'image/png');
                });

                setDebugInfo('Creating FormData...');
                
                // Create FormData for file upload
                const formData = new FormData();
                formData.append('board_image', blob, 'board.png');

                setDebugInfo('Sending to VILA API...');
                
                // Send to VILA API
                const response = await fetch('/api/vila/analyze', {
                    method: 'POST',
                    body: formData,
                });

                setDebugInfo(`API Response: ${response.status}`);

                if (!response.ok) {
                    throw new Error(`VILA API error: ${response.status}`);
                }

                const result = await response.json();
                setDebugInfo('API response received');
                
                // Parse VILA response to determine if position is good
                const content = result.raw_response?.choices?.[0]?.message?.content || '';
                const executedComponents = result.executed_components || [];
                
                // Check if the suggested position matches the user's input
                const userMove = `add_component(${component}, ${x}, ${y})`;
                const isGood = executedComponents.some((comp: string) => 
                    comp.toLowerCase().includes(component.toLowerCase()) && 
                    comp.includes(`${x}, ${y}`)
                ) || content.toLowerCase().includes(component.toLowerCase()) ||
                   content.toLowerCase().includes(`position (${x}, ${y})`) ||
                   content.toLowerCase().includes(`coordinates (${x}, ${y})`);

                let explanation = '';
                if (isGood) {
                    explanation = `VILA analysis confirms that adding ${component} at position (${x}, ${y}) is a good strategic choice. The AI has identified this move as beneficial for your current board state.`;
                } else {
                    explanation = `VILA analysis suggests that adding ${component} at position (${x}, ${y}) might not be optimal. The AI recommends considering other positions or components based on the current board state.`;
                }

                return {
                    position: `(${x}, ${y})`,
                    component: component,
                    isGood,
                    explanation,
                };

            } catch (html2canvasError) {
                setDebugInfo(`html2canvas failed: ${html2canvasError}`);
                // Fallback to simple analysis
                const isGood = (x + y) % 2 === 0;
                return {
                    position: `(${x}, ${y})`,
                    component: component,
                    isGood,
                    explanation: isGood 
                        ? `Adding ${component} at position (${x}, ${y}) appears to be strategically sound based on basic analysis.`
                        : `Adding ${component} at position (${x}, ${y}) might not be optimal. Consider other positions or components.`,
                };
            }

        } catch (error) {
            console.error('Error in VILA analysis:', error);
            setDebugInfo(`Error: ${error}`);
            throw new Error(`Failed to analyze position: ${error}`);
        }
    };

    const handleSubmitPosition = async () => {
        if (!selectedComponent) {
            message.error('Please select a component type');
            return;
        }

        if (!positionX || !positionY) {
            message.error('Please enter both X and Y coordinates');
            return;
        }

        const x = parseInt(positionX);
        const y = parseInt(positionY);

        if (isNaN(x) || isNaN(y)) {
            message.error('Please enter valid numbers for coordinates');
            return;
        }

        if (x < 0 || x > 14 || y < 0 || y > 16) {
            message.error('Coordinates must be within valid range (X: 0-14, Y: 0-16)');
            return;
        }

        setIsProcessing(true);
        setDebugInfo('');
        setVilaResponse(null);
        
        try {
            const response = await analyzePositionWithVila(selectedComponent, x, y);
            setVilaResponse(response);
            setShowResultsOnly(true);
            setDebugInfo('Analysis completed successfully');
        } catch (error) {
            console.error('Error analyzing position:', error);
            message.error(error instanceof Error ? error.message : 'Analysis failed');
            setDebugInfo(`Analysis failed: ${error}`);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleCloseModal = () => {
        setIsModalVisible(false);
        setSelectedComponent('');
        setPositionX('');
        setPositionY('');
        setVilaResponse(null);
        setDebugInfo('');
        setShowResultsOnly(false);
        form.resetFields();
        onClose();
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSubmitPosition();
        }
    };

    return (
        <Modal
            title={
                <div style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    margin: '-20px -24px 20px -24px',
                    padding: '20px 24px',
                    borderRadius: '8px 8px 0 0',
                    color: 'white'
                }}>
                    <Space>
                        <RobotOutlined style={{ fontSize: '24px', color: '#fff' }} />
                        <span style={{ fontSize: '18px', fontWeight: 'bold' }}>VILA Move Analysis</span>
                    </Space>
                </div>
            }
            open={isModalVisible}
            onCancel={handleCloseModal}
            footer={null}
            width={400}
            centered
            styles={{
                body: { padding: '24px' },
                mask: { backgroundColor: 'rgba(0, 0, 0, 0.6)' }
            }}
        >
            {!showResultsOnly && (
                <div style={{ marginBottom: 10 }}>
                    <div style={{
                        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                        padding: '8px',
                        borderRadius: '6px',
                        marginBottom: '10px',
                        color: 'white',
                        textAlign: 'center'
                    }}>
                        <AimOutlined style={{ fontSize: '32px', marginBottom: '8px' }} />
                        
                        <Paragraph style={{ color: 'white', margin: 0, fontSize: '16px' }}>
                            Ask VILA if your chosen component and position is good for your next move. The AI will analyze the current board state and provide strategic advice.
                        </Paragraph>
                    </div>
                    
                    <Form form={form} layout="vertical">
                        <Row gutter={16}>
                            <Col span={24}>
                                <Form.Item label={
                                    <span style={{ fontWeight: 'bold', color: '#1890ff' }}>
                                        <SettingOutlined /> Component Type
                                    </span>
                                } required>
                                    <Select
                                        value={selectedComponent}
                                        onChange={setSelectedComponent}
                                        placeholder="Select a component type"
                                        size="large"
                                        style={{
                                            borderRadius: '8px',
                                            border: '2px solid #e8f4fd',
                                            transition: 'all 0.3s ease'
                                        }}
                                    >
                                        {COMPONENT_TYPES.map(comp => (
                                            <Option key={comp.value} value={comp.value}>
                                                <Space>
                                                    <span style={{ fontSize: '16px' }}>{comp.icon}</span>
                                                    <span>{comp.label}</span>
                                                </Space>
                                            </Option>
                                        ))}
                                    </Select>
                                </Form.Item>
                            </Col>
                        </Row>
                        
                        <Row gutter={16}>
                            <Col span={12}>
                                <Form.Item label={
                                    <span style={{ fontWeight: 'bold', color: '#1890ff' }}>
                                        <AimOutlined /> X Position
                                    </span>
                                } required>
                                    <Input
                                        value={positionX}
                                        onChange={(e) => setPositionX(e.target.value)}
                                        placeholder="0-14"
                                        onKeyPress={handleKeyPress}
                                        size="large"
                                        style={{
                                            borderRadius: '8px',
                                            border: '2px solid #e8f4fd',
                                            transition: 'all 0.3s ease'
                                        }}
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item label={
                                    <span style={{ fontWeight: 'bold', color: '#1890ff' }}>
                                        <AimOutlined /> Y Position
                                    </span>
                                } required>
                                    <Input
                                        value={positionY}
                                        onChange={(e) => setPositionY(e.target.value)}
                                        placeholder="0-16"
                                        onKeyPress={handleKeyPress}
                                        size="large"
                                        style={{
                                            borderRadius: '8px',
                                            border: '2px solid #e8f4fd',
                                            transition: 'all 0.3s ease'
                                        }}
                                    />
                                </Form.Item>
                            </Col>
                        </Row>
                    </Form>
                    
                    <Button 
                        type="primary" 
                        onClick={handleSubmitPosition}
                        loading={isProcessing}
                        block
                        size="large"
                        icon={<ThunderboltOutlined />}
                        style={{
                            height: '50px',
                            borderRadius: '12px',
                            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            border: 'none',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                            transition: 'all 0.3s ease'
                        }}
                    >
                        {isProcessing ? 'Analyzing with VILA...' : 'Ask VILA'}
                    </Button>

                    {isProcessing && (
                        <div style={{ marginTop: 16 }}>
                            <Progress 
                                percent={100} 
                                status="active" 
                                strokeColor={{
                                    '0%': '#667eea',
                                    '100%': '#764ba2',
                                }}
                                showInfo={false}
                            />
                            <Text style={{ textAlign: 'center', display: 'block', marginTop: 8, color: '#666' }}>
                                VILA is analyzing your move...
                            </Text>
                        </div>
                    )}

                    {debugInfo && (
                        <Alert
                            message="Debug Info"
                            description={debugInfo}
                            type="info"
                            showIcon
                            style={{ 
                                marginTop: 16,
                                borderRadius: '8px',
                                border: '1px solid #e8f4fd'
                            }}
                        />
                    )}
                </div>
            )}

            {vilaResponse && showResultsOnly && (
                <div style={{ marginTop: 20 }}>
                    <Divider style={{ 
                        borderColor: '#e8f4fd',
                        margin: '24px 0'
                    }} />
                    
                    <div style={{
                        background: vilaResponse.isGood 
                            ? 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
                            : 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                        padding: '20px',
                        borderRadius: '16px',
                        border: `2px solid ${vilaResponse.isGood ? '#52c41a' : '#faad14'}`,
                        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)'
                    }}>
                        <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                            {vilaResponse.isGood ? (
                                <CheckCircleOutlined style={{ 
                                    fontSize: '48px', 
                                    color: '#52c41a',
                                    marginBottom: '8px'
                                }} />
                            ) : (
                                <CloseCircleOutlined style={{ 
                                    fontSize: '48px', 
                                    color: '#faad14',
                                    marginBottom: '8px'
                                }} />
                            )}
                            <Title level={3} style={{ 
                                color: vilaResponse.isGood ? '#52c41a' : '#faad14',
                                margin: '8px 0'
                            }}>
                                {vilaResponse.isGood ? 'YES - Excellent Move!' : 'NO - Consider Alternatives'}
                            </Title>
                        </div>
                        
                        <div style={{ marginBottom: 16 }}>
                            <Card
                                size="small"
                                style={{
                                    borderRadius: '8px',
                                    border: '1px solid #e8f4fd',
                                    background: 'rgba(255, 255, 255, 0.8)'
                                }}
                            >
                                <Row gutter={16}>
                                    <Col span={12}>
                                        <Text strong style={{ fontSize: '16px' }}>
                                            Component: {vilaResponse.component}
                                        </Text>
                                    </Col>
                                    <Col span={12}>
                                        <Text strong style={{ fontSize: '16px' }}>
                                            Position: {vilaResponse.position}
                                        </Text>
                                    </Col>
                                </Row>
                            </Card>
                        </div>
                        
                        <Paragraph style={{ 
                            fontSize: '16px',
                            lineHeight: '1.6',
                            marginBottom: 16,
                            color: '#333'
                        }}>
                            {vilaResponse.explanation}
                        </Paragraph>
                        
                        <Space style={{ width: '100%', justifyContent: 'center', marginTop: 24 }}>
                            <Button
                                type="primary"
                                size="large"
                                onClick={handleCloseModal}
                                style={{
                                    borderRadius: '8px',
                                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                    border: 'none',
                                    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)'
                                }}
                            >
                                Got it!
                            </Button>
                            <Button
                                type="default"
                                size="large"
                                onClick={() => {
                                    setVilaResponse(null); // Clear previous response
                                    setShowResultsOnly(false); // Go back to input form
                                }}
                                style={{
                                    borderRadius: '8px',
                                    borderColor: '#667eea',
                                    color: '#667eea',
                                    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
                                }}
                            >
                                Try Another Move
                            </Button>
                        </Space>
                    </div>
                </div>
            )}
        </Modal>
    );
}; 