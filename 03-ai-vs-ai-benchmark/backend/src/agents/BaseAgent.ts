import { Action } from "../../../shared/Action";
import { PuppetWorldView } from "../../../shared/Puppet";  // Changed import source

export class BaseAgent {
    constructor(public puppetId: string) { }

    async getAction(worldView: PuppetWorldView): Promise<Action> {
        throw new Error('Method not implemented. Subclasses must override this method.');
    }

    updateView(worldView: PuppetWorldView): void {
        console.log(`BaseAgent ${this.puppetId} received updated world view:`, JSON.stringify(worldView));
        // Base implementation does nothing, subclasses can override
    }
}