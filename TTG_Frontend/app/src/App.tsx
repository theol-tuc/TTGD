import React, { useState, useEffect } from 'react';
import {Layout, Dropdown, Menu, Space, Button, Drawer, Typography, notification } from 'antd';
import Board, { BoardCell } from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";
import { ItemType } from './parts/constants';
import { CHALLENGES, getChallengeById, Challenge, DEFAULT_CHALLENGE } from './components/challenges';
import {
    getBoardState,
    setLauncher,
    launchMarble,
    resetBoard,
    updateBoard
} from "./services/api";
import {useChallenge} from "./components/challengeContext";

const { Header, Sider, Content } = Layout;
const { Title, Paragraph, Text } = Typography;

const App: React.FC = () => {
    const [zoomLevel, setZoomLevel] = useState(1);
    const [isRunning, setIsRunning] = useState(false);
    const [currentSpeed, setCurrentSpeed] = useState(1);
    const [board, setBoard] = useState<BoardCell[][]>([]);
    const [activeLauncher, setActiveLauncher] = useState<'left' | 'right'>('left');
    const [marbleCounts, setMarbleCounts] = useState({ red: 0, blue: 0 });
    const { currentChallenge, setCurrentChallenge, resetToDefault } = useChallenge();
    const [infoPanelVisible, setInfoPanelVisible] = useState(false);
    const [api, contextHolder] = notification.useNotification();

    // Initialize board and challenge from backend
    useEffect(() => {
        const initializeApp = async () => {
            try {
                // Initialize with default challenge
                setCurrentChallenge(DEFAULT_CHALLENGE);

                // Get initial board state
                const state = await getBoardState();
                setActiveLauncher(state.active_launcher as 'left' | 'right');
                setMarbleCounts({
                    red: state.red_marbles,
                    blue: state.blue_marbles
                });

                // Initialize frontend board
                const initialBoard: BoardCell[][] = Array.from({ length: 17 }, () =>
                    Array.from({ length: 15 }, () => ({ type: ItemType.Empty })))
                //setBoard(initialBoard);
            } catch (error) {
                console.error('Initialization error:', error);
                api.error({
                    message: 'Initialization Error',
                    description: 'Failed to initialize the application. Please try again.',
                });
            }
        };

        initializeApp();
    }, []);

    const handleChallengeSelect = async (challengeId: string) => {
        try {
            const challenge = getChallengeById(challengeId);
            if (!challenge) return;

            setCurrentChallenge(challenge);
            setInfoPanelVisible(true);
            await resetBoard();

            // Load initial board if defined
            if (challenge.initialBoard) {
                setBoard(challenge.initialBoard);
            } else {
                const state = await getBoardState();
                // Convert backend state to frontend board format
                const newBoard: BoardCell[][] = Array.from({ length: 17 }, () =>
                    Array.from({ length: 15 }, () => ({ type: ItemType.Empty }))
                );
                setBoard(newBoard);
            }

            api.success({
                message: 'Challenge Loaded',
                description: `${challenge.name} has been selected.`,
            });
        } catch (error) {
            console.error('Challenge selection error:', error);
            api.error({
                message: 'Error Loading Challenge',
                description: 'Failed to load the selected challenge. Please try again.',
            });
        }
    };

    const getCurrentChallenge = () => {
        return currentChallenge;
    };

    const handleResetChallenge = async () => {
        try {
            resetToDefault();
            await resetBoard();
            const state = await getBoardState();
            setMarbleCounts({
                red: state.red_marbles,
                blue: state.blue_marbles
            });
            setActiveLauncher(state.active_launcher as 'left' | 'right');

            api.info({
                message: 'Reset Complete',
                description: 'Reset to default Free Play mode.',
            });
        } catch (error) {
            console.error('Reset error:', error);
            api.error({
                message: 'Reset Error',
                description: 'Failed to reset the board. Please try again.',
            });
        }
    };

    const challengesMenu = (
        <Menu>
            {CHALLENGES.map(challenge => (
                <Menu.Item
                    key={challenge.id}
                    onClick={() => handleChallengeSelect(challenge.id)}
                >
                    {challenge.name}
                </Menu.Item>
            ))}
        </Menu>
    );

    const handleZoomIn = () => {
        setZoomLevel(prev => Math.min(prev + 0.1, 2));
    };

    const handleZoomOut = () => {
        setZoomLevel(prev => Math.max(prev - 0.1, 0.5));
    };

    const handleSlowDown = () => {
        const speedOptions = [0.5, 1, 2, 5];
        const currentIndex = speedOptions.indexOf(currentSpeed);
        if (currentIndex > 0) {
            setCurrentSpeed(speedOptions[currentIndex - 1]);
        }
        setIsRunning(false);
    };

    const handleSpeedUp = () => {
        const speedOptions = [0.5, 1, 2, 5];
        const currentIndex = speedOptions.indexOf(currentSpeed);
        if (currentIndex < speedOptions.length - 1) {
            setCurrentSpeed(speedOptions[currentIndex + 1]);
        }
        setIsRunning(true);
    };

    const handleClearBoard = async () => {
        await resetBoard();
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
    };

    const handleResetMarbles = async () => {
        await resetBoard();
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
    };

    const handleTriggerLeft = async () => {
        try {
            console.log('Setting launcher to left...');
            await setLauncher("left");
            console.log('Launcher set, launching blue marble...');
            await launchMarble("blue");
            console.log('Marble launched, getting board state...');
            const state = await getBoardState();
            console.log('Board state updated:', state);
            setMarbleCounts({
                red: state.red_marbles,
                blue: state.blue_marbles
            });
            setActiveLauncher('left');
        } catch (error) {
            console.error('Error in handleTriggerLeft:', error);
        }
    };

    const handleTriggerRight = async () => {
        try {
            console.log('Setting launcher to right...');
            await setLauncher("right");
            console.log('Launcher set, launching red marble...');
            await launchMarble("red");
            console.log('Marble launched, getting board state...');
            const state = await getBoardState();
            console.log('Board state updated:', state);
            setMarbleCounts({
                red: state.red_marbles,
                blue: state.blue_marbles
            });
            setActiveLauncher('right');
        } catch (error) {
            console.error('Error in handleTriggerRight:', error);
        }
    };

    // Update marble counts periodically when running
    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (isRunning) {
            interval = setInterval(async () => {
                const state = await getBoardState();
                setMarbleCounts({
                    red: state.red_marbles,
                    blue: state.blue_marbles
                });
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isRunning]);

    return (
        <Layout style={{ minHeight: '100vh', background: '#f0f0f0', overflow: 'hidden' }}>
            {contextHolder}
            <Header style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                color: '#fff',
                height: '64px',
                padding: '0 24px',
                backgroundColor: '#4096ff',
            }}>
                <Space>
                    <Text strong style={{ color: '#fff', fontSize: '1.2rem' }}>
                        Turing Tumble Simulator
                    </Text>
                </Space>

                <Space>
                    <Text style={{ color: '#fff' }}>
                        Red: {marbleCounts.red} | Blue: {marbleCounts.blue} |
                        Launcher: {activeLauncher === 'left' ? 'Blue (Left)' : 'Red (Right)'}
                    </Text>
                </Space>

                <Space>
                    <Button
                        type="text"
                        style={{ color: '#fff' }}
                        onClick={() => setInfoPanelVisible(!infoPanelVisible)}
                    >
                        {infoPanelVisible ? 'Hide Info' : 'Show Info'}
                    </Button>
                    <Dropdown
                        overlay={
                            <Menu>
                                {CHALLENGES.map(challenge => (
                                    <Menu.Item
                                        key={challenge.id}
                                        onClick={() => handleChallengeSelect(challenge.id)}
                                    >
                                        {challenge.name}
                                    </Menu.Item>
                                ))}
                            </Menu>
                        }
                        placement="bottomRight"
                    >
                        <Button type="text" style={{ color: '#fff' }}>
                            ▼ Challenges
                        </Button>
                    </Dropdown>
                    <Button
                        type="text"
                        style={{ color: '#fff' }}
                        onClick={handleResetChallenge}
                    >
                        Reset
                    </Button>
                </Space>
            </Header>
            <Drawer
                title={getCurrentChallenge()?.name || 'Challenge Info'}
                placement="right"
                closable={true}
                onClose={() => setInfoPanelVisible(false)}
                visible={infoPanelVisible}
                width={400}
                bodyStyle={{ padding: 20 }}
            >
                {currentChallenge ? (
                    <>
                        <Title level={4}>Description</Title>
                        <Paragraph>{getCurrentChallenge()?.description}</Paragraph>
                        <Title level={4}>Objectives</Title>
                        <Paragraph>
                            <ul>
                                {getCurrentChallenge()?.objectives?.map((obj, i) => (
                                    <li key={i}>{obj}</li>
                                ))}
                            </ul>
                        </Paragraph>
                    </>
                ) : (
                    <Paragraph>No challenge selected</Paragraph>
                )}
            </Drawer>
            <Layout style={{ overflow: 'hidden' }}>
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
                        padding: '16px'
                    }}>
                    <Toolbar
                        onZoomIn={handleZoomIn}
                        onZoomOut={handleZoomOut}
                        onSlowDown={handleSlowDown}
                        onSpeedUp={handleSpeedUp}
                        onClearBoard={handleClearBoard}
                        onResetMarbles={handleResetMarbles}
                        onTriggerLeft={handleTriggerLeft}
                        onTriggerRight={handleTriggerRight}
                        isRunning={isRunning}
                        currentSpeed={currentSpeed}
                    />
                </Sider>
                <Content style={{
                    marginLeft: '200px',
                    marginRight: '200px',
                    padding: '24px',
                    height: 'calc(100vh - 64px)',
                    background: '#f0f0f0',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    overflow: 'hidden'
                }}>
                    <div style={{
                        transform: `scale(${zoomLevel})`,
                        transformOrigin: 'center'
                    }}>
                        <Board
                            board={board}
                            setBoard={setBoard}
                            isRunning={isRunning}
                            currentSpeed={currentSpeed}
                        />
                    </div>
                </Content>
                <Sider
                    width={200}
                    style={{
                        background: '#fff',
                        boxShadow: '-2px 0 8px 0 rgba(29, 35, 41, 0.05)',
                        height: 'calc(100vh - 64px)',
                        position: 'fixed',
                        right: 0,
                        top: 64,
                        overflowY: 'auto',
                        padding: '10px'
                    }}>
                    <PartsPanel />
                </Sider>
            </Layout>
        </Layout>
    );
};

export default App;