import { GameState, Position, GameConfig } from "../../shared/GameState";
import { PuppetState, PuppetWorldView } from "../../shared/Puppet";
import { Action } from "../../shared/Action";
import { BaseAgent } from "./agents/BaseAgent";
import { createAgent } from "./agents/index";
import { WebSocket } from 'ws';

export class Game {
    public state: GameState;
    private agents: Map<string, BaseAgent>;
    public clients: Set<WebSocket>;

    constructor(config: GameConfig) {
        this.clients = new Set();
        this.agents = new Map();
        this.state = new GameState();
        this.state.environment = config.environment;

        for (const puppetConfig of config.puppets) {
            let agentId = "abc" + Math.random();
            let agentState: PuppetState = {
                id: agentId,
                name: "Foo",
                position: { x: 0, y: 0 },
                isAlive: true,
                target: undefined,
                avatarUrl: undefined
            };

            this.state.puppets.push(agentState);
            let agent = createAgent(puppetConfig);
            this.agents.set(agentId, agent);
        }

        // Assign initial targets
        this.reassignTargets();
    }

    public async turn(): Promise<GameState> {
        for (const agent of this.getLivingAgents()) {
            const view = this.getViewForAgent(agent.id);
            const generatedObject = await this.agents.get(agent.id)?.getAction(view);
            const action = generatedObject!.action;
            if (!action) continue;

            switch (action.type) {
                case 'move':
                    const pos = this.getPuppet(agent.id)?.position;
                    if (pos) {
                        pos.x += action.delta.x;
                        pos.y += action.delta.y;
                    }
                    break;

                case 'attack':
                    // TODO: Implement attack
                    break;

                case 'talk':
                    console.log(`Agent ${agent.id} says: "${action.message}"`);
                    // Could broadcast this message to clients
                    break;
            }
        }
        console.log("State after turn", this.state);

        this.state.turnNumber++;
        this.checkGameEndConditions();
        return this.state;
    }

    private calculateDistance(pos1: Position, pos2: Position): number {
        const dx = pos1.x - pos2.x;
        const dy = pos1.y - pos2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    private findTargetForAgent(agentId: string): PuppetState | undefined {
        const agent = this.state.puppets.find(p => p.id === agentId);
        if (!agent || !agent.target) return undefined;

        return this.state.puppets.find(p => p.id === agent.target);
    }

    public getPuppet(agentId: string): PuppetState | undefined {
        return this.state.puppets.find(p => p.id === agentId);
    }

    public getLivingAgents(): PuppetState[] {
        return this.state.puppets.filter(agent => agent.isAlive);
    }

    private reassignTargets(): void {
        const livingAgents = this.getLivingAgents();
        if (livingAgents.length <= 1) return;

        // Create a circular chain of targets
        for (let i = 0; i < livingAgents.length; i++) {
            const nextIndex = (i + 1) % livingAgents.length;
            const agentId = livingAgents[i].id;
            const targetId = livingAgents[nextIndex].id;

            let puppet = this.getPuppet(agentId);
            if (puppet) {
                puppet.target = targetId;
                console.log(`Assigned target ${targetId} to agent ${agentId}`);
            }
        }
    }

    private checkGameEndConditions(): void {
        const livingAgents = this.getLivingAgents();
        if (livingAgents.length <= 1) {
            this.state.completed = true;
        }
    }

    public getViewForAgent(agentId: string): PuppetWorldView {
        const thisPuppet = this.getPuppet(agentId);
        if (!thisPuppet) throw new Error(`Agent ${agentId} not found`);

        return {
            self: thisPuppet,
            nearbyPuppets: [],
            recentMessages: [],
            environment: this.state.environment,
            turnNumber: this.state.turnNumber
        };
    }

    public getState(): GameState {
        return this.state;
    }

    private broadcastAction(action: Action): void {
        // Send action to all connected clients
        this.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({
                    type: 'action',
                    action
                }));
            }
        });
    }

    public updateStateFromFrontend(frontendState: any): void {
        console.log('Updating game state from frontend:', JSON.stringify(frontendState));
        
        // Update environment
        if (frontendState.environment) {
            console.log('Updating environment:', frontendState.environment);
            this.state.environment.width = frontendState.environment.width;
            this.state.environment.height = frontendState.environment.height;
        }

        // Update players
        if (frontendState.players) {
            console.log('Updating players:', frontendState.players);
            frontendState.players.forEach((player: any) => {
                console.log('Processing player:', player);
                const puppet = this.state.puppets.find(p => p.id === player.id);
                if (puppet) {
                    console.log(`Found puppet with id ${player.id}, updating`);
                    // Update position
                    puppet.position = player.position;
                    
                    // Update stats if this is the human player
                    if (player.isHuman) {
                        puppet.stats = {
                            stealth: player.stats.stealth,
                            combat: player.stats.strength,
                            perception: player.stats.perception,
                            speed: player.stats.speed,
                            health: player.stats.health || 100
                        };
                    }
                    
                    // Update target
                    puppet.target = player.targetId;
                    puppet.isAlive = player.isAlive;
                } else {
                    console.log(`No puppet found with id ${player.id}, creating new one`);
                    // Create a new puppet if it doesn't exist
                    const newPuppet: PuppetState = {
                        id: player.id,
                        name: player.name || `Player ${player.id}`,
                        position: player.position,
                        isAlive: player.isAlive,
                        target: player.targetId,
                        avatarUrl: '/images/default.png'
                    };
                    this.state.puppets.push(newPuppet);
                }
            });
        }

        // Update agent views
        console.log('Updating agent views for living agents');
        this.getLivingAgents().forEach(agent => {
            const agentId = agent.id;
            console.log(`Updating view for agent ${agentId}`);
            const agentView = this.getViewForAgent(agentId);
            const agentInstance = this.agents.get(agentId);
            if (agentInstance) {
                console.log(`Found agent instance for ${agentId}, updating view`);
                agentInstance.updateView(agentView);
            } else {
                console.log(`No agent instance found for ${agentId}`);
            }
        });
    }
}