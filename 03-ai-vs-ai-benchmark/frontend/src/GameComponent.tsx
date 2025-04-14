import React, { useEffect, useRef, useState } from 'react';
import { Color, DisplayMode, Engine, FadeInOut } from "excalibur";
import { loader } from "./resources";
import { MyLevel } from "./level";
import { PuppetConfig } from "../../shared/GameState";
import { Player } from "./player";
import { WebSocketManager } from "./webSocketManager";
import './style.css'; // Make sure styles are imported

interface GameComponentProps {
  characterData?: {
    name: string;
    bio: {
      tragicBackstory: string;
      strategyForKilling: string;
      strategyForSurvival: string;
    };
    stats: {
      stealth: number;
      strength: number;
      speed: number;
      perception: number;
      cunning: number;
    };
  };
}

const GameComponent: React.FC<GameComponentProps> = ({ characterData }) => {
  const gameRef = useRef<Engine | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocketManager | null>(null);
  const [gameState, setGameState] = useState<any>(null);

  // Send game state to agents
  const sendGameStateUpdate = (wsManager: WebSocketManager, game: Engine) => {
    if (!wsManager || !game) {
      console.log('Cannot send game state: WebSocketManager or game not initialized');
      return;
    }

    try {
      const level = game.currentScene as MyLevel;

      if (!level || !level.engine) {
        console.log('Game scene not fully initialized yet, skipping state update');
        return;
      }

      console.log('Current scene:', level);

      // Get all players' state - no need to check for human player
      const players = level.actors
        .filter(actor => actor instanceof Player)
        .map(player => {
          const p = player as Player;
          return {
            id: p.id,
            name: p.name,
            position: { x: p.pos.x, y: p.pos.y },
            isAlive: p.active,
            isHuman: false, // All players are AI
            targetId: p.targetId,
            stats: {
              stealth: 1,
              strength: 1,
              speed: 1,
              perception: 1,
              cunning: 1
            }
          };
        });

      if (players.length === 0) {
        console.log('No players found in scene, skipping state update');
        return;
      }

      console.log(`Sending state update with ${players.length} players`);

      // Send the state update to the server using WebSocketManager
      wsManager.socket?.send(JSON.stringify({
        type: 'state_update',
        state: {
          puppets: players, // Use puppets instead of players to match backend expectation
          environment: {
            width: game.drawWidth,
            height: game.drawHeight
          }
        }
      }));
      console.log('State update sent to server');
    } catch (error) {
      console.error('Error sending game state update:', error);
    }
  };

  useEffect(() => {
    // Initialize WebSocket connection using WebSocketManager
    const wsManager = new WebSocketManager('ws://localhost:8080');
    const wsManagerRef = { current: wsManager };

    // Set up callbacks
    wsManager.setConnectionStatusCallback((connected) => {
      console.log(`WebSocket connection status: ${connected ? 'connected' : 'disconnected'}`);
    });

    wsManager.setGameStateUpdateCallback((state) => {
      console.log('Game state update received:', state);
      setGameState(state);

      // Initialize game engine if not already done
      if (!gameRef.current) {
        console.log('Initializing game engine');
        const game = new Engine({
          width: 800,
          height: 600,
          displayMode: DisplayMode.FitScreen, // Changed from FitScreenAndFill to FitScreen
          pixelArt: true,
          backgroundColor: Color.fromHex('#0a0a0a'), // Darker background
          canvasElement: canvasRef.current!
        });

        // Create the game level with character data
        const level = new MyLevel(characterData);

        // Add the level to the game
        game.add('game-level', level);

        // Start the game
        game.start(loader).then(() => {
          console.log('Game started successfully');
          game.goToScene('game-level');

          // Pass WebSocketManager to MyLevel
          const level = game.currentScene as MyLevel;
          if (level) {
            console.log('Setting WebSocketManager in level');
            level.setWebSocketManager(wsManager);

            // Update game state with the latest state
            if (state && typeof level.updateGameState === 'function') {
              console.log('Updating initial game state in level');
              level.updateGameState(state);
            } else {
              console.warn('Level does not have updateGameState method or state is invalid');
            }
          } else {
            console.error('Failed to get level from game scene');
          }

          // Start sending state updates every second
          updateInterval = setInterval(() => {
            sendGameStateUpdate(wsManagerRef.current, game);
          }, 1000);
        });

        gameRef.current = game;
      } else {
        // Update game state in level if needed
        const level = gameRef.current.currentScene as MyLevel;
        if (level && typeof level.updateGameState === 'function') {
          console.log('Updating game state in level');
          level.updateGameState(state);
        } else {
          console.warn('Level does not have updateGameState method or is not properly initialized');
        }
      }
    });

    // Connect to server
    wsManager.connect();

    // Store reference to WebSocketManager
    wsRef.current = wsManager;

    // Start game when connected
    setTimeout(() => {
      if (wsManager) {
        console.log('Starting game with AI agents only');

        // Start game with only AI agents
        wsManager.startGame(['ai', 'ai']);
      }
    }, 1000);

    // Set up periodic state updates
    let updateInterval: NodeJS.Timeout;
    
    // Add resize handler
    const handleResize = () => {
      if (gameRef.current) {
        console.log('Resizing game to fit window');
        gameRef.current.screen.setDimension(window.innerWidth, window.innerHeight);
      }
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      if (wsManager) {
        wsManager.disconnect();
      }
      if (gameRef.current) {
        gameRef.current.stop();
        gameRef.current = null;
      }
      if (updateInterval) {
        clearInterval(updateInterval);
      }
      // Remove resize event listener
      window.removeEventListener('resize', handleResize);
    };
  }, [characterData]);

  return (
    <div className="game-wrapper">
      <div className="game-title">
        <h1>Killer Sock Puppets</h1>
        <p>Hunt or be hunted...</p>
      </div>
      <canvas ref={canvasRef} id="game-canvas"></canvas>
      <button
        className="debug-toggle"
        onClick={() => {
          if (gameRef.current) {
            gameRef.current.toggleDebug();
            console.log('Debug mode toggled');
          }
        }}
      >
        Toggle Debug
      </button>
    </div>
  );
};

export default GameComponent;