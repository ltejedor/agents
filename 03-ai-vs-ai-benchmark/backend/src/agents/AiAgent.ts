import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { Action, ActionSchema } from '../../../shared/Action';
import { BaseAgent } from './BaseAgent';
import { PuppetWorldView, PuppetState, PuppetUtils } from '../../../shared/Puppet';  // Updated imports

function describeView(view: PuppetWorldView): string {
    let description = `You are: ${view.self}`;

    if (view.self.position) {
        description += `Your position: x=${view.self.position.x.toFixed(2)}, y=${view.self.position.y.toFixed(2)}\n`;
    }

    // if (view.targetPosition) {
    //     description += `Target position: x=${view.targetPosition.x.toFixed(2)}, y=${view.targetPosition.y.toFixed(2)}\n`;
    // }

    if (view.environment) {
        description += `Environment size: width=${view.environment.width}, height=${view.environment.height}\n`;
    }

    // if (view.allPlayers && view.allPlayers.length > 0) {
    //     description += "All players:\n";
    //     view.allPlayers.forEach(player => {
    //         description += `  - Player ${player.id}: position x=${player.position.x.toFixed(2)}, y=${player.position.y.toFixed(2)}${player.isTarget ? ' (YOUR TARGET)' : ''}\n`;
    //     });
    // }

    return description;
}

export class AiAgent extends BaseAgent {
    constructor() {
        super("ai-agent");
    }

    updateView(view: PuppetWorldView): void {
        console.log(`AiAgent ${this.puppetId} received updated world view:`, JSON.stringify(view));
        // Store the latest view for use in getAction
        // This could be used to maintain state between turns
    }

    async getAction(view: PuppetWorldView): Promise<Action> {
        console.log(`AiAgent ${this.puppetId} generating action based on view:`, JSON.stringify(view));
        try {
            const { object } = await generateObject({
                model: openai('gpt-4o-mini'),
                system: `You are an agent in a game where you can:
                    - Move up to 3 units per turn
                    - Kill other agents by touching them
                    - Talk to nearby agents
                
                Make decisions based on your situation.`,
                messages: [
                    {
                        "role": "user",
                        "content": PuppetUtils.describeWorldView(view)  // Using built-in description
                    }
                ],
                schema: ActionSchema
            });

            const action: Action = object;
            console.log(`Agent ${this.puppetId} action:`, JSON.stringify(action));
            return action;
        } catch (error) {
            console.error(`Error generating action for agent ${this.puppetId}:`, error);

            // Fallback to a simple move action if generation fails
            const fallbackAction: Action = {
                "action": {
                    type: 'move',
                    agentId: this.puppetId,
                    timestamp: Date.now(),
                    delta: { x: Math.random() * 10 - 5, y: Math.random() * 10 - 5 }
                }
            };

            console.log(`Puppet ${this.puppetId} fallback action:`, JSON.stringify(fallbackAction));
            return fallbackAction;
        }
    }
}