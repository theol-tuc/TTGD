import React, { useState, useEffect } from 'react';
import {Layout, Dropdown, Menu, Space, Button, Drawer, Typography } from 'antd';
import Board, { BoardCell } from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";
import { ItemType } from './parts/constants';
import { CHALLENGES, getChallengeById, Challenge } from './components/challenges';
import {
    getBoardState,
    setLauncher,
    launchMarble,
    resetBoard,
    updateBoard,
    addComponent,
    getMarbleOutput
} from "./services/api";

const { Header, Sider, Content } = Layout;
const { Title, Paragraph, Text } = Typography;

const numRows = 17;
const numCols = 15;

const mapComponentType = (type: string): ItemType => {
    switch (type) {
        case 'ramp_left': return ItemType.RampLeft;
        case 'ramp_right': return ItemType.RampRight;
        case 'crossover': return ItemType.Crossover;
        case 'interceptor': return ItemType.Intercept;
        case 'bit_left': return ItemType.BitLeft;
        case 'bit_right': return ItemType.BitRight;
        case 'border_vertical': return ItemType.BorderVertical;
        case 'border_horizontal': return ItemType.BorderHorizontal;
        case 'border_diagonal_left': return ItemType.BorderDiagonalLeft;
        case 'border_diagonal_right': return ItemType.BorderDiagonalRight;
        case 'corner_left': return ItemType.CornerLeft;
        case 'corner_right': return ItemType.CornerRight;
        case 'lever_blue': return ItemType.LeverBlue;
        case 'lever_red': return ItemType.LeverRed;
        case 'invalid': return ItemType.Invalid;
        case 'gray_space': return ItemType.GraySpace;
        case 'gear': return ItemType.Gear;
        case 'gear_bit_left': return ItemType.GearBitLeft;
        case 'gear_bit_right': return ItemType.GearBitRight;
        default: return ItemType.Empty;
    }
};


const App: React.FC = () => {
    const [zoomLevel, setZoomLevel] = useState(1);
    const [isRunning, setIsRunning] = useState(false);
    const [currentSpeed, setCurrentSpeed] = useState(1);
    const [board, setBoard] = useState<BoardCell[][]>([]);
    const [activeLauncher, setActiveLauncher] = useState<'left' | 'right'>('left');
    const [marbleCounts, setMarbleCounts] = useState({ red: 0, blue: 0 });
    const [marbleOutput, setMarbleOutput] = useState<string[]>([]);
    const [challenges, setChallenges] = useState<Challenge[]>(CHALLENGES);
    const [selectedChallenge, setSelectedChallenge] = useState<string | null>(null);
    const [infoPanelVisible, setInfoPanelVisible] = useState(false);
    const [initialComponents, setInitialComponents] = useState<Array<Array<{ type: string; is_occupied: boolean }>>>([]);

    const buildBoard = (state: any): BoardCell[][] => {
        const newBoard: BoardCell[][] = Array.from({ length: numRows }, () =>
            Array.from({ length: numCols }, () => ({ type: ItemType.Empty }))
        );

        // components
        state.components.forEach((row: any[], y: number) => {
            row.forEach((c, x) => {
                newBoard[y][x] = {
                    type: mapComponentType(c.type),
                    isOccupied: c.is_occupied
                };
            });
        });

        // marbles
        state.marbles.forEach((m: any) => {
            newBoard[m.y][m.x].type =
                m.color === 'red' ? ItemType.BallRed : ItemType.BallBlue;
            newBoard[m.y][m.x].isOccupied = true;
        });

        return newBoard;
    };


    const refreshBoard = async () => {
        const state = await getBoardState();
        setBoard(buildBoard(state));
        setActiveLauncher(state.active_launcher as 'left' | 'right');
    };

    // Initialize board from backend
    useEffect(() => {
        const initializeBoard = async () => {
            const state = await getBoardState();
            setInitialComponents(state.components);
            setBoard(buildBoard(state));
            setMarbleCounts({ red: state.red_marbles, blue: state.blue_marbles });
            setActiveLauncher(state.active_launcher as 'left' | 'right');
            setMarbleCounts({
                red: state.red_marbles,
                blue: state.blue_marbles
            });
        };
        initializeBoard();
    }, []);

    const handleChallengeSelect = (challengeId: string) => {
        const challenge = challenges.find(c => c.id === challengeId);
        if (challenge) {
            setSelectedChallenge(challengeId);
            setInfoPanelVisible(true);
            // TODO: Add logic to load the selected challenge from backend
            console.log('Selected challenge:', challengeId);
        }
    };

    const getCurrentChallenge = () => {
        return challenges.find(c => c.id === selectedChallenge);
    };

    const challengesMenu = (
        <Menu>
            {challenges.length > 0 ? (
                challenges.map(challenge => (
                    <Menu.Item
                        key={challenge.id}
                        onClick={() => handleChallengeSelect(challenge.id)}
                    >
                        {challenge.name}
                    </Menu.Item>
                ))
            ) : (
                <Menu.Item disabled>No challenges available</Menu.Item>
            )}
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
        await refreshBoard();
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
        setMarbleOutput([]);
    };

    const handleResetMarbles = async () => {
        setMarbleOutput([]);
        const before = await getBoardState();
        const compTypes = before.components.map(row => row.map(c => c.type));
        const countsBefore = { red: before.red_marbles, blue: before.blue_marbles };
        const launcherBefore = before.active_launcher as 'left' | 'right';

        // reset backend (clears both components & marbles)
        await resetBoard();

        // re-add every component cell
        for (let y = 0; y < compTypes.length; y++) {
            for (let x = 0; x < compTypes[y].length; x++) {
                const type = compTypes[y][x];
                if (type && type !== 'empty') {
                    await addComponent(type, x, y);
                }
            }
        }
        // restore launcher and counts
        await refreshBoard();
        setMarbleCounts(countsBefore);
        setActiveLauncher(launcherBefore);
    };

    const handleMarbleOutput = async () => {
            try {
                const output = await getMarbleOutput();
                console.log("Fetched Marble Outputs:", output); // Debugging
                setMarbleOutput(output || []); // Ensure it sets an array
            } catch (error) {
                console.error("Error fetching marble outputs:", error);
                setMarbleOutput([]); // Fallback to an empty array on error
            }
        };
    
    useEffect(() => {
        if (isRunning) {
            const interval = setInterval(handleMarbleOutput, 1000);
            return () => clearInterval(interval);
        }
    }, [isRunning]);

    const renderMarbleOutputs = () => {
        console.log("Rendering Marble Outputs:", marbleOutput); // Debugging
        if (!Array.isArray(marbleOutput)) {
            console.error("marbleOutput is not an array:", marbleOutput);
            return null;
        }

        return (
            <div className="marble-outputs">
                {marbleOutput.map((color, index) => (
                    <div
                        key={index}
                        className="board-cell"
                        title={`ball_${color}`} 
                        style={{
                            height: `40px`, 
                            width: `40px`, 
                            marginLeft: `1px`, 
                        }}
                    >
                        <img
                            src={`/images/${color}Ball.png`} 
                            alt={`${color} ball`}
                            className="cell-image"
                        />
                    </div>
                ))}
            </div>
        );
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
                    {selectedChallenge && (
                        <Button
                            type="text"
                            style={{ color: '#fff' }}
                            onClick={() => setInfoPanelVisible(!infoPanelVisible)}
                        >
                            {infoPanelVisible ? 'Hide Info' : 'Show Info'}
                        </Button>
                    )}
                    <Dropdown overlay={challengesMenu} placement="bottomRight">
                        <Button type="text" style={{ color: '#fff' }}>
                            ▼ Challenges
                        </Button>
                    </Dropdown>
                </Space>

                <span style={{
                    float: 'right',
                    fontSize: '0.9rem',
                    fontWeight: 'normal'
                }}>
                    Red: {marbleCounts.red} | Blue: {marbleCounts.blue} |
                    Launcher: {activeLauncher === 'left' ? 'Blue (Left)' : 'Red (Right)'}
                </span>
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
                {selectedChallenge ? (
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
                        {renderMarbleOutputs()}
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