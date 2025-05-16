import React, { useState } from 'react';
import { Upload, Button, Spin, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { analyzeWithVila } from '../services/aiService';
import type { AIResponse } from '../services/aiService';

interface AIAssistantProps {
  onAnalysis?: (response: AIResponse) => void;
}

const AIAssistant: React.FC<AIAssistantProps> = ({ onAnalysis }) => {
  const [loading, setLoading] = useState(false);

  const handleVilaClick = async (file: File) => {
    setLoading(true);
    try {
      const response = await analyzeWithVila(file);
      onAnalysis?.(response);
      message.success('Analysis complete');
    } catch (error) {
      console.error('Analysis failed:', error);
      message.error('Failed to analyze board');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-assistant">
      <Upload
        beforeUpload={(file) => {
          handleVilaClick(file);
          return false;
        }}
        accept="image/*"
        showUploadList={false}
      >
        <Button icon={<UploadOutlined />} loading={loading}>
          Analyze with VILA
        </Button>
      </Upload>
      {loading && <Spin />}
    </div>
  );
};

export default AIAssistant;
