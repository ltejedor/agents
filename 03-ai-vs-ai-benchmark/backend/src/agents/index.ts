import { PuppetConfig } from "../../../shared/GameState";
import { BaseAgent } from "./BaseAgent";
import { AiAgent } from "./AiAgent";

let lastAgentId = 0;

export function createAgent(config: PuppetConfig): BaseAgent {
    return new AiAgent();
}
