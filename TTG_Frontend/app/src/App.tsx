import React, { useState, useEffect } from 'react';
import {Layout, Dropdown, Menu, Space, Button, Drawer, Typography, notification, Empty } from 'antd';
import Board, { BoardCell } from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";
import { ItemType } from './parts/constants';
import { CHALLENGES, updateChallengeInitialBoard, Challenge, DEFAULT_CHALLENGE } from './components/challenges';
import { AIOverlay } from './components/AIOverlay';
import {
    getBoardState,
    setLauncher,
    launchMarble,
    resetBoard,
    updateBoard,
    addComponent,
    getMarbleOutput,
    fetchChallengeById,
    getMarbleCounts
} from "./services/api";
import {useChallenge} from "./components/challengeContext";
import ChallengeCompleteOverlay from "./components/challengeCompleteOverlay";

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
    const [marbleCounts, setMarbleCounts] = useState({ red: 8, blue: 8 });
    const [marbleCountsAux, setMarbleCountsAux] = useState({ red: 0, blue: 0 });
    const [marbleOutput, setMarbleOutput] = useState<string[]>([]);
    const [challenges, setChallenges] = useState<Challenge[]>(CHALLENGES);
    const [selectedChallenge, setSelectedChallenge] = useState<string | null>(null);
    const [infoPanelVisible, setInfoPanelVisible] = useState(false);
    const [initialComponents, setInitialComponents] = useState<Array<Array<{ type: string; is_occupied: boolean }>>>([]);
    const [challengeComplete, setChallengeComplete] = useState(false);
    const [isAIVisible, setIsAIVisible] = useState(false);
    const [completedChallenges, setCompletedChallenges] = useState<Set<string>>(new Set());
    const [showCompletion, setShowCompletion] = useState(false);

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
    const { currentChallenge, setCurrentChallenge, resetToDefault } = useChallenge();
    const [api, contextHolder] = notification.useNotification();

    // Initialize board and challenge from backend
    useEffect(() => {
        const initializeApp = async () => {
            try {
                // Fetch the default challenge from the backend
                const backendChallenge = await fetchChallengeById('default');
                //console.log("Backend Challenge:", backendChallenge); // Debugging
                if (!backendChallenge) {
                    throw new Error('Failed to fetch default challenge');
                }

                // Set the default challenge and board
                setCurrentChallenge(DEFAULT_CHALLENGE);
                setBoard(backendChallenge.initialBoard);

                // Get initial board state
                const state = await getBoardState();
                setActiveLauncher(state.active_launcher as 'left' | 'right');
                setMarbleCounts({
                    red: backendChallenge.red_marbles,
                    blue: backendChallenge.blue_marbles
                });
                setMarbleCountsAux({
                    red: backendChallenge.red_marbles,
                    blue: backendChallenge.blue_marbles
                });
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
            // Fetch the backend challenge data
            const backendChallenge = await fetchChallengeById(challengeId);
            if (!backendChallenge) return;
    
            // Find the frontend metadata for the challenge
            const frontendChallenge = CHALLENGES.find(challenge => challenge.id === challengeId);
            if (!frontendChallenge) return;
    
            // Merge the backend data with the frontend metadata
            const mergedChallenge = {
                ...frontendChallenge,
                initialBoard: backendChallenge.initialBoard
            };

            // Update backend with new board
            await resetBoard(); // clear old board

            // Add components one-by-one to backend
            for (let y = 0; y < mergedChallenge.initialBoard.length; y++) {
                for (let x = 0; x < mergedChallenge.initialBoard[y].length; x++) {
                    const cell = mergedChallenge.initialBoard[y][x];
                    if (cell.type && cell.type !== ItemType.Empty) {
                        await addComponent(cell.type, x, y);
                    }
                }
            }

            setCurrentChallenge(mergedChallenge);
            setBoard(mergedChallenge.initialBoard); 
            setMarbleCounts({
                red: backendChallenge.red_marbles,
                blue: backendChallenge.blue_marbles
            });


    
            api.success({
                message: 'Challenge Loaded',
                description: `${mergedChallenge.name} has been selected.`,
            });
        } catch (error) {
            console.error('Error loading challenge:', error);
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
        setMarbleCounts(marbleCountsAux);
        setActiveLauncher(launcherBefore);
    };

    const handleMarbleOutput = async () => {
            try {
                const output = await getMarbleOutput();
                //console.log("Fetched Marble Outputs:", output); // Debugging
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
        //console.log("Rendering Marble Outputs:", marbleOutput); // Debugging
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

    useEffect(() => {
        if (currentChallenge?.expectedOutput && currentChallenge.expectedOutput.length > 0 && marbleOutput.length > 0 && !completedChallenges.has(currentChallenge.id)) {
            const outputStr = marbleOutput.join(',');
            const expectedStr = currentChallenge.expectedOutput.join(',');

            if (outputStr.includes(expectedStr)) {
                setCompletedChallenges(prev => new Set(prev).add(currentChallenge.id));
                setShowCompletion(true);
            }
        }
    }, [marbleOutput, currentChallenge, completedChallenges]);

    const handleCloseOverlay = () => {
        setShowCompletion(false);
    };

    const handleRestartChallenge = async () => {
        if (!currentChallenge) return;

        setShowCompletion(false);
        await handleChallengeSelect(currentChallenge.id);
    };

    const handleNextChallenge = () => {
        if (!currentChallenge) return;

        setShowCompletion(false);
        const currentIndex = CHALLENGES.findIndex(c => c.id === currentChallenge.id);
        if (currentIndex < CHALLENGES.length - 1) {
            handleChallengeSelect(CHALLENGES[currentIndex + 1].id);
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

    const handleAIMove = async () => {
        await refreshBoard();
        const state = await getBoardState();
        setMarbleCounts({
            red: state.red_marbles,
            blue: state.blue_marbles
        });
    };

    const handleToggleAI = () => {
        setIsAIVisible(!isAIVisible);
    };

    const handleCloseAI = () => {
        setIsAIVisible(false);
    };

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
                        overlay={challengesMenu}
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
                        onToggleAI={handleToggleAI}
                        isAIVisible={isAIVisible}
                    />
                    {isAIVisible && <div style={{ position: 'relative' }}> <AIOverlay onAIMove={handleAIMove} onClose={handleCloseAI}/></div>}
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
            <ChallengeCompleteOverlay
                visible={showCompletion}
                challengeName={currentChallenge?.name || ''}
                onClose={handleCloseOverlay}
                onRestart={handleRestartChallenge}
                onNextChallenge={handleNextChallenge}
                hasNextChallenge={
                    currentChallenge ?
                        CHALLENGES.findIndex(c => c.id === currentChallenge.id) < CHALLENGES.length - 1 :
                        false
                }
            />
        </Layout>
    );
};

export default App;