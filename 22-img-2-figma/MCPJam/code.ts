// Hide UI but keep plugin alive
figma.showUI(__html__, { visible: false, width: 0, height: 0 });

// ─── command handlers ─────────────────────────────────────────────
// Track created stickies for connector operations
const stickyNodes: StickyNode[] = [];
type Cmd =
  | { op: "create_sticky"; text: string; x: number; y: number }
  | { op: "move_node"; id: string; x: number; y: number }
  | { op: "start_timer"; seconds: number }
  | { op: "create_connector"; start_id?: string; end_id?: string };

figma.ui.onmessage = async (cmd: Cmd) => {
  switch (cmd.op) {
    case "create_sticky": {
      const sticky = figma.createSticky();
      // Load the default sticky font before setting text
      await figma.loadFontAsync({ family: "Inter", style: "Medium" });
      sticky.text.characters = cmd.text;
      sticky.x = cmd.x;
      sticky.y = cmd.y;
      // record sticky for later connector creation
      stickyNodes.push(sticky);
      break;
    }
    case "move_node": {
      const node = figma.getNodeById(cmd.id) as SceneNode | null;
      if (node) {
        node.x = cmd.x;
        node.y = cmd.y;
      }
      break;
    }
    case "start_timer": {
      if (figma.timer) {
        figma.timer.start(cmd.seconds);
      }
      break;
    }
    case "create_connector": {
      // Determine endpoints: use provided IDs or fall back to last two stickies
      let startNode: SceneNode | null = null;
      let endNode: SceneNode | null = null;
      if (cmd.start_id && cmd.end_id) {
        startNode = figma.getNodeById(cmd.start_id) as SceneNode | null;
        endNode = figma.getNodeById(cmd.end_id) as SceneNode | null;
      } else if (stickyNodes.length >= 2) {
        const len = stickyNodes.length;
        startNode = stickyNodes[len - 2];
        endNode = stickyNodes[len - 1];
      }
      if (startNode && endNode) {
        const connector = figma.createConnector();
        connector.connectorStart = { endpointNodeId: startNode.id, magnet: 'AUTO' };
        connector.connectorEnd = { endpointNodeId: endNode.id, magnet: 'AUTO' };
      } else {
        console.warn('create_connector: unable to determine endpoints', cmd);
      }
      break;
    }
  }
};
