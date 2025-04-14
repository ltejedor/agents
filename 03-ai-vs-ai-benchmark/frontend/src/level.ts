import { BoundingBox, Color, DefaultLoader, Engine, ExcaliburGraphicsContext, Label, Scene, SceneActivationContext, vec } from "excalibur";
import { Player } from "./player";
import { GameManager } from "./gameManager";
import { FALLBACK_AVATARS } from "./resources";
import { WebSocketManager } from "./webSocketManager";

// Character data interface
interface CharacterData {
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
}

export class MyLevel extends Scene {
    private gameManager: GameManager;
    private statusLabel: Label;
    private characterData: CharacterData | null;

    constructor(characterData?: CharacterData) {
        super();
        this.gameManager = new GameManager();
        this.characterData = characterData || null;
    }

    override onInitialize(engine: Engine): void {
        // Create status label
        this.statusLabel = new Label({
            text: 'AI Assassin Game: Two AI agents competing!',
            pos: vec(engine.halfDrawWidth, 30)
        });
        this.add(this.statusLabel);

        // Set camera bounds to ensure players stay visible
        this.camera.strategy.limitCameraBounds(new BoundingBox(0, 0, engine.drawWidth, engine.drawHeight));

        // Listen for player collisions
        this.on('player-collision', (evt) => {
            this.gameManager.handleKill(evt.killer, evt.victim);
            this.updateStatusLabel();
        });
    }

    // Add this method to constrain player positions to the visible area
    private constrainPosition(position: { x: number, y: number }): { x: number, y: number } {
        if (!this.engine) return position;
        
        const margin = 50; // Keep players at least 50px from the edge
        
        return {
            x: Math.max(margin, Math.min(this.engine.drawWidth - margin, position.x)),
            y: Math.max(margin, Math.min(this.engine.drawHeight - margin, position.y))
        };
    }

    // Add this method to MyLevel class
    public setWebSocketManager(wsManager: WebSocketManager): void {
        console.log('Setting WebSocketManager in MyLevel');
        // Pass the WebSocketManager to the GameManager
        this.gameManager.setWebSocketManager(wsManager);
    }

    // Convert server coordinates to screen coordinates
    private convertToScreenCoordinates(serverPos: { x: number, y: number }): { x: number, y: number } {
        if (!this.engine) return serverPos;
        
        // Get the environment dimensions from the game state
        const envWidth = 100; // Default value, should match server's environment width
        const envHeight = 100; // Default value, should match server's environment height
        
        // Calculate scaling factors
        const scaleX = (this.engine.drawWidth - 100) / envWidth; // Leave 50px margin on each side
        const scaleY = (this.engine.drawHeight - 100) / envHeight; // Leave 50px margin on each side
        
        // Convert coordinates
        return {
            x: 50 + serverPos.x * scaleX, // 50px offset from left edge
            y: 50 + serverPos.y * scaleY  // 50px offset from top edge
        };
    }

    // Add this method after onInitialize
    updateGameState(state: any): void {
        console.log('MyLevel.updateGameState called with state:', state);

        if (!state || !state.puppets || !Array.isArray(state.puppets)) {
            console.warn('Invalid game state received:', state);
            return;
        }

        // Update player positions and states based on the game state
        state.puppets.forEach((puppetState: any) => {
            if (!puppetState.id) {
                console.warn('Puppet state missing ID:', puppetState);
                return;
            }

            // Find the corresponding player in the scene
            let player = this.actors.find(
                actor => actor instanceof Player && actor.id === puppetState.id
            ) as Player | undefined;

            if (player) {
                console.log(`Updating player ${puppetState.id} position to:`, puppetState.position);

                // Update player position
                if (puppetState.position && typeof puppetState.position.x === 'number' &&
                    typeof puppetState.position.y === 'number') {
                    // Convert server coordinates to screen coordinates
                    // The server might be using a different coordinate system (e.g., grid-based)
                    // than the client (pixel-based)
                    const screenPos = this.convertToScreenCoordinates(puppetState.position);
                    
                    // Use the new updatePosition method with the converted coordinates
                    player.updatePosition(screenPos);
                }

                // Update player state (alive/dead)
                if (puppetState.isAlive === false && player.active) {
                    console.log(`Player ${puppetState.id} is now dead`);
                    player.kill();
                }

                // Update target if available
                if (puppetState.target) {
                    console.log(`Setting target ${puppetState.target} for player ${puppetState.id}`);
                    player.targetId = puppetState.target;

                    // Find target player to set target color
                    const targetPlayer = this.actors.find(
                        actor => actor instanceof Player && actor.id === puppetState.target
                    ) as Player | undefined;

                    if (targetPlayer) {
                        player.setTargetColor(targetPlayer.getColor());
                    }
                }
            } else {
                console.log(`Player ${puppetState.id} not found in scene, creating new player`);

                // Create a new player if it doesn't exist
                const screenPos = puppetState.position ? 
                    this.convertToScreenCoordinates(puppetState.position) : 
                    { x: 100, y: 100 };
                
                const newPlayer = new Player({
                    id: puppetState.id,
                    name: puppetState.name || `Player ${puppetState.id}`,
                    pos: screenPos,
                    color: Color.Red, // Default color for new players
                    isAI: true, // Assume new players from server are AI
                    avatarUrl: puppetState.avatarUrl
                });

                this.add(newPlayer);
                this.gameManager.addPlayer(newPlayer);
                this.gameManager.registerPlayer(puppetState.id, newPlayer);
            }
        });

        // Update game status
        if (state.completed) {
            console.log('Game is completed');
            this.updateStatusLabel();
        }
    }

    private updateStatusLabel(): void {
        if (this.gameManager.isOver()) {
            const winner = this.gameManager.getWinner();
            if (winner) {
                this.statusLabel.text = `Game Over! ${winner.name} wins!`;
            }
        }
    }

    override onPreLoad(loader: DefaultLoader): void {
        // Add any scene specific resources to load
    }

    override onActivate(context: SceneActivationContext<unknown>): void {
        // Called when Excalibur transitions to this scene
        // Only 1 scene is active at a time
    }

    override onDeactivate(context: SceneActivationContext): void {
        // Called when Excalibur transitions away from this scene
        // Only 1 scene is active at a time
    }

    override onPreUpdate(engine: Engine, elapsedMs: number): void {
        // Called before anything updates in the scene
    }

    override onPostUpdate(engine: Engine, elapsedMs: number): void {
        // Update game state
        if (this.gameManager.isOver()) {
            // Game is over, could add restart logic here
        }
    }

    override onPreDraw(ctx: ExcaliburGraphicsContext, elapsedMs: number): void {
        // Called before Excalibur draws to the screen
    }

    override onPostDraw(ctx: ExcaliburGraphicsContext, elapsedMs: number): void {
        // Debug visualization - draw player positions and IDs
        if (this.engine?.debug?.enabled) {
            this.actors.forEach(actor => {
                if (actor instanceof Player) {
                    // Draw a circle at the player's position
                    ctx.drawCircle(actor.pos, 5, Color.Green);

                    // Draw the player's ID
                    ctx.drawText(`ID: ${actor.id}`, actor.pos.x + 10, actor.pos.y - 10, {
                        color: Color.White,
                        size: 10
                    });

                    // Draw the player's position
                    ctx.drawText(`Pos: ${Math.round(actor.pos.x)},${Math.round(actor.pos.y)}`,
                        actor.pos.x + 10, actor.pos.y + 10, {
                        color: Color.White,
                        size: 10
                    });
                }
            });
        }
    }
}