import { Action } from "../../shared/Action";
import { GameState, GameEnvironment, PuppetConfig } from "../../shared/GameState";

export type GameStateUpdateCallback = (state: GameState) => void;
export type ActionReceivedCallback = (action: Action) => void;
export type ConnectionStatusCallback = (connected: boolean) => void;

export class WebSocketManager {
  public socket: WebSocket | null = null;
  private gameId: string | null = null;
  private onGameStateUpdate: GameStateUpdateCallback | null = null;
  private onActionReceived: ActionReceivedCallback | null = null;
  private onConnectionStatus: ConnectionStatusCallback | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: number | null = null;

  constructor(private serverUrl: string = 'ws://localhost:8080') { }

  public connect(): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    console.log(`Connecting to WebSocket server at ${this.serverUrl}`);
    this.socket = new WebSocket(this.serverUrl);

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
      this.reconnectAttempts = 0;
      if (this.onConnectionStatus) {
        this.onConnectionStatus(true);
      }
    };

    this.socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log('Received WebSocket message:', message);

        switch (message.type) {
          case 'state_update':
            if (this.onGameStateUpdate && message.state) {
              console.log('Processing state update:', message.state);
              
              // Validate state structure before processing
              if (!message.state.puppets || !Array.isArray(message.state.puppets)) {
                console.warn('Invalid state format: puppets is not an array', message.state);
              } else if (message.state.puppets.length === 0) {
                console.warn('Empty puppets array in state update');
              } else {
                // Check for duplicate puppet IDs
                const puppetIds = new Set();
                const duplicateIds = new Set();
                message.state.puppets.forEach(puppet => {
                  if (puppetIds.has(puppet.id)) {
                    duplicateIds.add(puppet.id);
                  } else {
                    puppetIds.add(puppet.id);
                  }
                });
                
                if (duplicateIds.size > 0) {
                  console.warn('Found duplicate puppet IDs:', Array.from(duplicateIds));
                }
                
                // Convert Map-like objects back to actual Maps
                const state = this.deserializeGameState(message.state);
                this.onGameStateUpdate(state);
              }
            } else {
              console.warn('No game state update callback registered or invalid state');
            }
            break;
          case 'game_started':
            console.log(`Game started: ${message.gameId}`);
            this.gameId = message.gameId;
            break;
          case 'action':
            if (this.onActionReceived && message.action) {
              console.log('Received action:', message.action);
              this.onActionReceived(message.action);
            }
            break;
          case 'error':
            console.error('Server error:', message.message);
            break;
          default:
            console.warn(`Unknown message type: ${message.type}`);
        }
      } catch (error) {
        console.error('Error parsing message:', error, 'Raw data:', event.data);
      }
    };

    this.socket.onclose = (event) => {
      console.log(`WebSocket connection closed: ${event.code} ${event.reason}`);
      if (this.onConnectionStatus) {
        this.onConnectionStatus(false);
      }

      // Attempt to reconnect
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

        this.reconnectTimeout = window.setTimeout(() => {
          this.connect();
        }, delay);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  public disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  public startGame(agents: string[] = ['ai', 'ai', 'ai']): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('Cannot start game: WebSocket not connected');
      return;
    }

    console.log('Starting new game with agents:', agents);
    const env: GameEnvironment = {
      width: 800,
      height: 600
    }
    
    // Create puppet configs based on agent types
    const puppets: PuppetConfig[] = agents.map(agentType => {
      const puppet: PuppetConfig = {
        type: agentType,
        model: agentType === 'ai' ? "gpt-4o-mini" : "player",
        stats: undefined,
        avatar: undefined
      };
      console.log('Created puppet config:', puppet);
      return puppet;
    });
    
    const config = {
      puppets: puppets,
      environment: env
    };
    
    console.log('Sending start_game message with config:', config);
    this.socket.send(JSON.stringify({
      type: 'start_game',
      config: config,
    }));
  }

  public sendAction(action: Action): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('Cannot send action: WebSocket not connected');
      return;
    }

    console.log('Sending action:', action);
    this.socket.send(JSON.stringify({
      type: 'action',
      gameId: this.gameId,
      action
    }));
  }

  public setGameStateUpdateCallback(callback: GameStateUpdateCallback): void {
    this.onGameStateUpdate = callback;
  }

  public setActionReceivedCallback(callback: ActionReceivedCallback): void {
    this.onActionReceived = callback;
  }

  public setConnectionStatusCallback(callback: ConnectionStatusCallback): void {
    this.onConnectionStatus = callback;
  }

  private deserializeGameState(state: any): GameState {
    // Create a new GameState instance
    const gameState = new GameState();
    
    // Copy over the basic properties
    if (state.puppets) {
      gameState.puppets = state.puppets;
    }
    
    if (state.turnNumber !== undefined) {
      gameState.turnNumber = state.turnNumber;
    }
    
    if (state.completed !== undefined) {
      gameState.completed = state.completed;
    }
    
    if (state.environment) {
      gameState.environment = state.environment;
    }
    
    if (state.messages) {
      gameState.messages = state.messages;
    }
    
    if (state.events) {
      gameState.events = state.events;
    }
    
    return gameState;
  }
}