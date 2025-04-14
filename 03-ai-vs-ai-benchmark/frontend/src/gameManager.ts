import { Actor, Color, Engine, Random, Vector, vec } from "excalibur";
import { Player } from "./player";
import { Action } from "../../shared/Action";
import { GameState } from "../../shared/GameState";
import { PuppetState } from "../../shared/Puppet";
import { WebSocketManager } from "./webSocketManager";
import { PuppetWorldView } from "../../shared/Puppet";

// Define the PlayerView interface
interface PlayerView {
  self: string;
  target: string;
  playersRemaining: number;
  selfPosition?: { x: number, y: number };
  targetPosition?: { x: number, y: number };
  environment: { width: number, height: number };
  allPlayers?: Array<{
    id: string;
    position: { x: number, y: number };
    isTarget: boolean;
  }>;
}

export class GameManager {
  private players: Player[] = [];
  private targets: Map<Player, Player> = new Map();
  private isGameOver: boolean = false;
  private winner: Player | null = null;
  private random: Random = new Random();
  private playerMap: Map<string, Player> = new Map();
  private webSocketManager: WebSocketManager | null = null;
  constructor() { }

  // Add this method to GameManager class
  public setWebSocketManager(wsManager: WebSocketManager): void {
    console.log('Setting WebSocketManager in GameManager');
    this.webSocketManager = wsManager;
    
    // Set up callbacks
    this.webSocketManager.setGameStateUpdateCallback(this.handleGameStateUpdate.bind(this));
    this.webSocketManager.setActionReceivedCallback(this.handleAction.bind(this));
  }

  public initializeWebSocket(serverUrl: string = 'ws://localhost:8080'): void {
    // This method is now deprecated, use setWebSocketManager instead
    console.warn('initializeWebSocket is deprecated, use setWebSocketManager instead');
    
    // For backward compatibility, create a new WebSocketManager if one doesn't exist
    if (!this.webSocketManager) {
        console.log('Creating new WebSocketManager');
        this.webSocketManager = new WebSocketManager(serverUrl);
        
        // Set up callbacks
        this.webSocketManager.setGameStateUpdateCallback(this.handleGameStateUpdate.bind(this));
        this.webSocketManager.setActionReceivedCallback(this.handleAction.bind(this));
        this.webSocketManager.setConnectionStatusCallback((connected) => {
            console.log(`WebSocket connection status: ${connected ? 'connected' : 'disconnected'}`);
        });
        
        // Connect to the server
        this.webSocketManager.connect();
    }
  }

  public handleKill(killer: Player, victim: Player): void {
    if (this.isGameOver) return;

    // Check if killer was targeting victim
    if (this.targets.get(killer) === victim) {
      console.log(`${killer.name} killed their target ${victim.name}`);

      // Killer gets victim's target
      const newTarget = this.targets.get(victim);
      if (newTarget) {
        this.targets.set(killer, newTarget);
        killer.setTargetColor(newTarget.getColor());
      }

      // Remove victim from the game
      this.players = this.players.filter(p => p !== victim);
      this.targets.delete(victim);
      victim.kill();

      // Check if game is over (only one player left)
      if (this.players.length === 1) {
        this.isGameOver = true;
        this.winner = this.players[0];
        console.log(`Game over! Winner: ${this.winner.name}`);
      }
    }
  }

  public getTargetFor(player: Player): Player | undefined {
    return this.targets.get(player);
  }

  public isOver(): boolean {
    return this.isGameOver;
  }

  public getWinner(): Player | null {
    return this.winner;
  }

  public getRandomPosition(minX: number, maxX: number, minY: number, maxY: number): Vector {
    return vec(
      this.random.floating(minX, maxX),
      this.random.floating(minY, maxY)
    );
  }

  private handleWebSocketMessage(message: MessageEvent): void {
    const data = JSON.parse(message.data);
    console.log('Received message:', data);

    if (data.type === 'state_update') {
      this.handleGameStateUpdate(data.state);
    }
  }

  // Handle game state updates from the backend
  public handleGameStateUpdate(state: GameState): void {
    console.log('Processing game state update:', state);

    if (!state.puppets || !Array.isArray(state.puppets)) {
      console.error('Invalid game state: puppets is not an array', state);
      return;
    }

    // Create a map to track puppets by ID to handle duplicates
    const puppetIdMap = new Map();
    
    // Update player positions and states based on the game state
    state.puppets.forEach((puppetState: PuppetState, index: number) => {
      // Handle duplicate IDs by appending index if this ID is already processed
      let uniqueId = puppetState.id;
      if (puppetIdMap.has(puppetState.id)) {
        uniqueId = `${puppetState.id}-${index}`;
        console.log(`Found duplicate puppet ID ${puppetState.id}, using ${uniqueId} instead`);
      }
      puppetIdMap.set(puppetState.id, true);
      
      // Use puppet.id as the agent ID
      const player = this.playerMap.get(uniqueId);
      if (player) {
        console.log(`Updating player ${uniqueId} position to:`, puppetState.position);
        
        // Update player position
        if (puppetState.position && typeof puppetState.position.x === 'number' && 
            typeof puppetState.position.y === 'number') {
            // Convert server coordinates to screen coordinates if needed
            const screenPos = this.convertToScreenCoordinates(puppetState.position);
            
            // Use the updatePosition method with the converted coordinates
            player.updatePosition(screenPos);
        }

        // Update player state (alive/dead)
        if (!puppetState.isAlive && player.active) {
          player.kill();
        }
        
        // Update target if available
        if (puppetState.target) {
          player.targetId = puppetState.target;
          
          // Find target player to set target color
          const targetPlayer = this.playerMap.get(puppetState.target);
          if (targetPlayer) {
            player.setTargetColor(targetPlayer.getColor());
          }
        }
      } else {
        console.log(`Creating new player for puppet ${uniqueId}`);
        
        // Create a new player for this puppet
        const screenPos = puppetState.position ? 
            this.convertToScreenCoordinates(puppetState.position) : 
            { x: 100, y: 100 };
            
        const newPlayer = new Player({
          id: uniqueId,
          name: puppetState.name || `Player ${uniqueId}`,
          pos: screenPos,
          color: Color.Red, // Default color for new players
          isAI: true, // Assume new players from server are AI
          avatarUrl: '/images/default.png'
        });
        
        // Add to our collections
        this.players.push(newPlayer);
        this.playerMap.set(uniqueId, newPlayer);
        
        // Note: We can't add to scene here since we don't have access to the scene
        // This will be handled by the level's updateGameState method
      }
    });
  }

  // Convert server coordinates to screen coordinates
  private convertToScreenCoordinates(serverPos: { x: number, y: number }): { x: number, y: number } {
    // Get the environment dimensions from the game state
    const envWidth = 100; // Default value, should match server's environment width
    const envHeight = 100; // Default value, should match server's environment height
    
    // Assume a default screen size if we don't have access to the engine
    const screenWidth = 800;
    const screenHeight = 600;
    
    // Calculate scaling factors
    const scaleX = (screenWidth - 100) / envWidth; // Leave 50px margin on each side
    const scaleY = (screenHeight - 100) / envHeight; // Leave 50px margin on each side
    
    // Convert coordinates
    return {
      x: 50 + serverPos.x * scaleX, // 50px offset from left edge
      y: 50 + serverPos.y * scaleY  // 50px offset from top edge
    };
  }

  private getAgentIdForPlayer(player: Player): string | undefined {
    for (const [agentId, mappedPlayer] of this.playerMap.entries()) {
      if (mappedPlayer === player) {
        return agentId;
      }
    }
    return undefined;
  }

  private createEnhancedPlayerView(state: GameState, agentId: string): PuppetWorldView {
    // Find the puppet with the matching ID
    const puppet = state.puppets.find(p => p.id === agentId);
    if (!puppet) {
      throw new Error(`Agent ${agentId} not found in game state`);
    }

    // Create a basic view
    const view: PuppetWorldView = {
      self: puppet,
      nearbyPuppets: [],
      recentMessages: state.messages || [],
      environment: state.environment,
      turnNumber: state.turnNumber
    };

    // Add information about nearby puppets
    state.puppets.forEach(otherPuppet => {
      if (otherPuppet.id !== agentId && otherPuppet.isAlive) {
        view.nearbyPuppets.push({
          id: otherPuppet.id,
          name: otherPuppet.name,
          position: otherPuppet.position,
          isAlive: otherPuppet.isAlive,
          isTarget: puppet.target === otherPuppet.id,
          distanceToSelf: this.getDistance(puppet.position, otherPuppet.position)
        });
      }
    });

    return view;
  }

  // Helper method to calculate distance between two positions
  private getDistance(pos1: { x: number, y: number }, pos2: { x: number, y: number }): number {
    const dx = pos2.x - pos1.x;
    const dy = pos2.y - pos1.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  private requestActionFromAI(view: PuppetWorldView): void {
    // In a real implementation, this would send the view to the backend
    // For now, we'll simulate AI behavior by moving toward the target
    if (view.self && view.targetPosition && view.selfPosition) {
      const selfPos = view.selfPosition;
      const targetPos = view.targetPosition;

      // Calculate direction to target
      const dx = targetPos.x - selfPos.x;
      const dy = targetPos.y - selfPos.y;

      // Normalize and scale
      const distance = Math.sqrt(dx * dx + dy * dy);
      const moveSpeed = 10; // Units per move

      let moveX = 0;
      let moveY = 0;

      if (distance > 0) {
        moveX = (dx / distance) * moveSpeed;
        moveY = (dy / distance) * moveSpeed;
      }

      // Create a move action
      const action: Action = {
        action: {
          type: 'move',
          agentId: view.self,
          timestamp: Date.now(),
          delta: { x: moveX, y: moveY }
        }
      };

      // Handle the action locally - pass the inner action object
      this.handleAction(action.action);

      // Send the action to the server - send the full action object
      if (this.webSocketManager) {
        this.webSocketManager.sendAction(action);
      }
    }
  }

  public handleAction(action: any): void {
    console.log('Handling action:', action);
    
    if (!action || !action.type) {
      console.error('Invalid action received:', action);
      return;
    }

    // Find the player associated with this agent
    const player = this.playerMap.get(action.agentId);
    if (!player) {
      console.error(`No player found for agent ID: ${action.agentId}`);
      return;
    }

    switch (action.type) {
      case 'move':
        if (action.delta) {
            // Calculate new position
            const newPos = {
                x: player.pos.x + action.delta.x,
                y: player.pos.y + action.delta.y
            };
            // Update player position using the new method
            player.updatePosition(newPos);
        }
        break;
        
      case 'attack':
        if (action.targetId) {
          const targetPlayer = this.playerMap.get(action.targetId);
          if (targetPlayer) {
            // Move toward target at increased speed
            const direction = targetPlayer.pos.sub(player.pos).normalize();
            player.vel = direction.scale(200); // Faster attack speed
          }
        }
        break;
        
      case 'talk':
        if (action.message) {
          console.log(`${player.name} says: ${action.message}`);
          // Could display this message in the UI
        }
        break;
        
      default:
        console.warn(`Unknown action type: ${action.type}`);
    }
  }

  public addPlayer(player: Player): void {
    this.players.push(player);
  }

  public registerPlayer(agentId: string, player: Player): void {
    this.playerMap.set(agentId, player);
  }

  public assignTargets(): void {
    if (this.players.length < 2) return;
    
    // Create a circular targeting system
    for (let i = 0; i < this.players.length; i++) {
      const player = this.players[i];
      const target = this.players[(i + 1) % this.players.length];
      this.targets.set(player, target);
      
      // Set target color for visual indication
      player.setTargetColor(target.getColor());
    }
    
    console.log('Targets assigned');
  }
}