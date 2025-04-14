import { z } from 'zod';

import { Action } from './Action';


import {
    PuppetState,
    PuppetPerception,
    PuppetMessage,
    PuppetWorldView,
    PuppetUtils
} from './Puppet';
export class GameState {
    public puppets: PuppetState[];
    public turnNumber: number;
    public completed: boolean;
    public environment: GameEnvironment;
    public messages: PuppetMessage[];
    public events: GameEvent[];

    constructor() {
        this.puppets = [];
        this.turnNumber = 0;
        this.completed = false;
        this.environment = { width: 100, height: 100 };
        this.messages = [];
        this.events = [];
    }


    getPuppetWorldView(puppetId: string): PuppetWorldView {
        const puppet = this.puppets.find(p => p.id === puppetId);
        if (!puppet) throw new Error('Puppet not found');

        return {
            self: puppet,
            nearbyPuppets: this.getNearbyPuppets(puppet),
            recentMessages: this.getRecentMessages(),
            environment: this.environment,
            turnNumber: this.turnNumber
        };
    }

    private getNearbyPuppets(puppet: PuppetState): PuppetPerception[] {
        return this.puppets
            .filter(other => other.id !== puppet.id)
            .map(other => ({
                id: other.id,
                name: other.name,
                position: other.position,
                isAlive: other.isAlive,
                isTarget: puppet.target === other.id,
                lastMessage: other.lastMessage,
                distanceToSelf: PuppetUtils.getDistance(puppet.position, other.position)
            }));
    }

    private getRecentMessages(): PuppetMessage[] {
        // Get last 10 messages
        return this.messages.slice(-10);
    }
}

export interface AvatarConfig {
    material: string;
    pattern: string;
    eyes: string;
    accessories: string;
}

export interface PuppetConfig {
    type: string;
    model: string;
    stats?: PuppetStats;
    avatar: AvatarConfig | undefined;
}

export interface GameConfig {
    puppets: Array<PuppetConfig>;
    environment: GameEnvironment;
}

export interface GameEnvironment {
    width: number;
    height: number;
}

export interface Obstacle {
    position: Position;
    width: number;
    height: number;
}

export interface GameEvent {
    type: string;
    agentId: string;
    timestamp: number;
    data: any;
}

export type Position = {
    x: number;
    y: number;
};

export type PuppetStats = {
    stealth: number;      // Ability to remain undetected
    combat: number;       // Combat effectiveness
    perception: number;   // Ability to detect other agents
    speed: number;        // Movement speed
};
