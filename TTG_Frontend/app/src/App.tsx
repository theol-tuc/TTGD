import React, {useState} from 'react';
import { Layout } from 'antd';
import Board, { BoardCell } from "./board/board";
import { Toolbar } from "./ui/toolbar";
import { PartsPanel } from "./ui/partsPanel";
import { ItemType } from './parts/constants';

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
    const [zoomLevel, setZoomLevel] = useState(1);
    const [isRunning, setIsRunning] = useState(false);
    const [currentSpeed, setCurrentSpeed] = useState(1);
    const [board, setBoard] = useState<BoardCell[][]>([]);

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

    const shouldPreserveCell = (cellType: ItemType): boolean => {
        const preservedTypes = [
            ItemType.BorderVertical,
            ItemType.BorderHorizontal,
            ItemType.BorderDiagonalLeft,
            ItemType.BorderDiagonalRight,
            ItemType.CornerLeft,
            ItemType.CornerRight,
            ItemType.Invalid,
            ItemType.LeverBlue,
            ItemType.LeverRed
        ];
        return preservedTypes.includes(cellType);
    };

    const handleClearBoard = () => {
        setBoard(prevBoard => {
            const newBoard = prevBoard.map(row => 
                row.map(cell => {
                    // Only clear interactive parts, preserve board structure
                    if (cell.type === ItemType.BitLeft || 
                        cell.type === ItemType.BitRight || 
                        cell.type === ItemType.RampLeft || 
                        cell.type === ItemType.RampRight || 
                        cell.type === ItemType.Crossover || 
                        cell.type === ItemType.Intercept) {
                        return { type: ItemType.Empty };
                    }
                    return { ...cell };
                })
            );
            return newBoard;
        });
    };

    const handleResetMarbles = () => {
        console.log("Resetting marbles - functionality to be implemented");
        // This will be implemented when we have marble state management
    };

    const handleTriggerLeft = () => {
        console.log("Triggering left lever - functionality to be implemented");
        // This will be implemented when we have lever functionality
    };

    const handleTriggerRight = () => {
        console.log("Triggering right lever - functionality to be implemented");
        // This will be implemented when we have lever functionality
    };

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
                fontWeight: 'bold'}}>
                Welcome to Turing Tumble
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
                        padding: '16px'}}>
                    <Toolbar onZoomIn={handleZoomIn}
                             onZoomOut={handleZoomOut}
                             onSlowDown={handleSlowDown}
                             onSpeedUp={handleSpeedUp}
                             onClearBoard={handleClearBoard}
                             onResetMarbles={handleResetMarbles}
                             onTriggerLeft={handleTriggerLeft}
                             onTriggerRight={handleTriggerRight}
                             isRunning={isRunning}
                             currentSpeed={currentSpeed}/>
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
                    overflow: 'hidden'}}>
                    <div style={{
                        transform: `scale(${zoomLevel})`,
                        transformOrigin: 'center'
                    }}>
                        <Board board={board} setBoard={setBoard} />
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
                        padding: '10px'}}>
                    <PartsPanel />
                </Sider>
            </Layout>
        </Layout>
    );
};

export default App;