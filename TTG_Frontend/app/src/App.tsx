import React from 'react';
import { Layout } from 'antd';
import Board from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
    return (
        <Layout style={{ minHeight: '100vh', background: '#f0f0f0' }}>
            <Header style={{
                textAlign: 'left',
                color: '#fff',
                height: '64px',
                padding: '0 24px',
                lineHeight: '64px',
                backgroundColor: '#4096ff',
                fontSize: '1.2rem',
                fontWeight: 'bold'}}>
                Welcome to Turing Tumble
            </Header>
            <Layout>
                <Sider
                    width={200}
                    style={{
                        background: '#fff',
                        boxShadow: '2px 0 8px 0 rgba(29, 35, 41, 0.05)',
                        height: 'calc(100vh - 64px)',
                        position: 'fixed',
                        left: 0,
                        top: 64,
                        overflowY: 'auto',
                        padding: '16px'}}>
                    <Toolbar />
                </Sider>
                <Content style={{
                    marginLeft: '200px',
                    marginRight: '300px',
                    padding: '24px',
                    minHeight: 'calc(100vh - 64px)',
                    background: '#f0f0f0',
                    display: 'flex',
                    justifyContent: 'center'}}>
                    <Board />
                </Content>
                <Sider
                    width={300}
                    style={{
                        background: '#fff',
                        boxShadow: '-2px 0 8px 0 rgba(29, 35, 41, 0.05)',
                        height: 'calc(100vh - 64px)',
                        position: 'fixed',
                        right: 0,
                        top: 64,
                        overflowY: 'hidden',
                        padding: '10px'}}>
                    <PartsPanel />
                </Sider>
            </Layout>
        </Layout>
    );
};

export default App;