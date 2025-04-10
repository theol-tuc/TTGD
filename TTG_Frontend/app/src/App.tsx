import React, { useState, useEffect } from 'react';
import { Layout } from 'antd';
import Board, { BoardCell } from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";
import { ItemType } from './parts/constants';
import {
    getBoardState,
    setLauncher,
    launchMarble,
    resetBoard,
    updateBoard
} from "./services/api";

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
    const [zoomLevel, setZoomLevel] = useState(1);
    const [isRunning, setIsRunning] = useState(false);
    const [currentSpeed, setCurrentSpeed] = useState(1);
    const [board, setBoard] = useState<BoardCell[][]>([]);
    const [activeLauncher, setActiveLauncher] = useState<'left' | 'right'>('left');
    const [marbleCounts, setMarbleCounts] = useState({ red: 0, blue: 0 });

    // Initialize board from backend
    useEffect(() => {
        const initializeBoard = async () => {
            const state = await getBoardState();
            setActiveLauncher(state.active_launcher as 'left' | 'right');
            setMarbleCounts({
                red: state.red_marbles,
                blue: state.blue_marbles
            });
        };
        initializeBoard();
    }, []);

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
        await setLauncher("left");
        await launchMarble("blue");
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
        setActiveLauncher('left');
    };

    const handleTriggerRight = async () => {
        await setLauncher("right");
        await launchMarble("red");
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
        setActiveLauncher('right');
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
            <Header style={{
                textAlign: 'left',
                color: '#fff',
                height: '64px',
                padding: '0 24px',
                lineHeight: '64px',
                backgroundColor: '#4096ff',
                fontSize: '1.2rem',
                fontWeight: 'bold'
            }}>
                Turing Tumble Simulator
                <span style={{
                    float: 'right',
                    fontSize: '0.9rem',
                    fontWeight: 'normal'
                }}>
                    Red: {marbleCounts.red} | Blue: {marbleCounts.blue} |
                    Launcher: {activeLauncher === 'left' ? 'Blue (Left)' : 'Red (Right)'}
                </span>
            </Header>
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