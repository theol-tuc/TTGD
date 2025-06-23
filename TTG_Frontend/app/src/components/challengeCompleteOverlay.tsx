import React from 'react';
import { Modal, Typography, Button, Space, Row, Col } from 'antd';
import { RedoOutlined, ArrowRightOutlined, TrophyOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

interface ChallengeCompleteOverlayProps {
    visible: boolean;
    challengeName: string;
    onClose: () => void;
    onRestart?: () => void;
    onNextChallenge?: () => void;
    hasNextChallenge: boolean;
}

const ChallengeCompleteOverlay: React.FC<ChallengeCompleteOverlayProps> = ({visible, challengeName, onClose, onRestart, onNextChallenge, hasNextChallenge}) => {
    return (
        <Modal
            title={
                <Space>
                    <TrophyOutlined style={{ color: '#faad14', fontSize: '24px' }} />
                    <span>Challenge Complete!</span>
                </Space>
            }
            visible={visible}
            onCancel={onClose}
            footer={null}
            centered
            width={600}
            bodyStyle={{
                textAlign: 'center',
                padding: '24px'
            }}
            maskClosable={false}
            closable={true}
        >
            <div style={{ marginBottom: 32 }}>
                <Title level={2} style={{ color: '#389e0d' }}>🎉 Congratulations! 🎉</Title>
                <Paragraph style={{ fontSize: '18px', marginBottom: 8 }}>
                    You've successfully completed <strong>{challengeName}</strong>!
                </Paragraph>
            </div>

            <Row gutter={16} justify="center">
                <Col>
                    <Button
                        icon={<RedoOutlined />}
                        size="large"
                        onClick={onRestart}
                        style={{
                            borderRadius: '8px',
                            padding: '0 24px',
                            height: '40px'
                        }}
                    >
                        Restart Challenge
                    </Button>
                </Col>
                {hasNextChallenge && (
                    <Col>
                        <Button
                            type="primary"
                            icon={<ArrowRightOutlined />}
                            size="large"
                            onClick={onNextChallenge}
                            style={{
                                borderRadius: '8px',
                                padding: '0 24px',
                                height: '40px'
                            }}
                        >
                            Next Challenge
                        </Button>
                    </Col>
                )}
            </Row>
        </Modal>
    );
};

export default ChallengeCompleteOverlay;