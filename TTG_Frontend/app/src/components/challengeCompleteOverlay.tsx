import React from 'react';
import { Modal, Typography, Button } from 'antd';

const { Title, Paragraph } = Typography;

interface ChallengeCompleteOverlayProps {
    visible: boolean;
    challengeName: string;
    onClose: () => void;
}

const ChallengeCompleteOverlay: React.FC<ChallengeCompleteOverlayProps> = ({visible, challengeName, onClose}) => {
    return (
        <Modal
            title="Challenge Complete!"
            visible={visible}
            onCancel={onClose}
            footer={[
                <Button key="close" type="primary" onClick={onClose}>
                    Close
                </Button>
            ]}
            centered
            width={600}
        >
            <div style={{ textAlign: 'center', padding: '20px' }}>
                <Title level={2}>🎉 Congratulations! 🎉</Title>
                <Paragraph style={{ fontSize: '18px' }}>
                    You've successfully completed <strong>{challengeName}</strong>!
                </Paragraph>
                <Paragraph>
                    The marble output matched the expected sequence for this challenge.
                </Paragraph>
            </div>
        </Modal>
    );
};

export default ChallengeCompleteOverlay;