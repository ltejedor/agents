// shared/Agent.ts

import { Position, GameEnvironment } from './GameState';
import { Action } from './Action';

export type PuppetId = string;

// Rich context about the agent's current state
export interface PuppetState {
    id: PuppetId;
    name: string;
    position: Position;
    isAlive: boolean;
    lastAction?: Action;    // What they did last
    lastMessage?: string;        // What they last said
    target?: PuppetId;           // Who they're supposed to kill
    avatarUrl?: string;
    stats?: object;
}

// What the agent can perceive about others
export interface PuppetPerception {
    id: PuppetId;
    name: string;
    position: Position;
    isAlive: boolean;
    isTarget: boolean;
    lastMessage?: string;        // What this agent last said
    distanceToSelf: number;      // How far they are from the observing agent
}

// The complete view an agent has of the world
export interface PuppetWorldView {
    self: PuppetState;                       // Own state
    nearbyPuppets: PuppetPerception[];        // Other agents they can see
    recentMessages: PuppetMessage[];         // Recent messages they've heard
    environment: GameEnvironment;           // World boundaries
    turnNumber: number;                     // Current turn
}

// Message structure for communication
export interface PuppetMessage {
    from: PuppetId;
    content: string;
    timestamp: number;
}

// Simplified rules that are easy for LLM to understand
export const PUPPET_RULES = {
    BASIC: {
        MOVEMENT_RANGE: 3,          // How far they can move per turn
        KILL_RANGE: 1,              // Must be touching to kill
        CHAT_RANGE: 5               // How far away they can be heard
    }
} as const;

// Simple utility functions
export const PuppetUtils = {
    getDistance(pos1: Position, pos2: Position): number {
        const dx = pos2.x - pos1.x;
        const dy = pos2.y - pos1.y;
        return Math.sqrt(dx * dx + dy * dy);
    },

    // Create a human-readable description of an agent's surroundings
    describeWorldView(view: PuppetWorldView): string {
        const nearby = view.nearbyPuppets.map(puppet => ({
            name: puppet.name,
            distance: puppet.distanceToSelf,
            lastSaid: puppet.lastMessage
        }));

        return `
            You are ${view.self.name}.
            Your position is (${view.self.position.x}, ${view.self.position.y}).
            ${view.self.target ? `Your target is: ${view.self.target}` : 'You have no specific target.'}
            
            Nearby agents:
            ${nearby.map(a =>
            `- ${a.name} is ${Math.round(a.distance)} units away` +
            (a.lastSaid ? ` and last said: "${a.lastSaid}"` : '')
        ).join('\n')}
            
            Recent messages heard:
            ${view.recentMessages.map(m =>
            `- ${m.from}: "${m.content}"`
        ).join('\n')}
        `;
    },

    // Validate if an action is physically possible
    isActionPossible(
        action: Action,
        puppet: PuppetState,
        worldView: PuppetWorldView
    ): boolean {
        return true;
    }
};