// Hide UI but keep plugin alive
figma.showUI(__html__, { visible: false, width: 0, height: 0 });

// ─── command handlers ─────────────────────────────────────────────
type Cmd =
  | { op: "create_sticky"; text: string; x: number; y: number }
  | { op: "move_node"; id: string; x: number; y: number }
  | { op: "start_timer"; seconds: number };

figma.ui.onmessage = async (cmd: Cmd) => {
  switch (cmd.op) {
    case "create_sticky": {
      const sticky = figma.createSticky();
      // Load the default sticky font before setting text
      await figma.loadFontAsync({ family: "Inter", style: "Medium" });
      sticky.text.characters = cmd.text;
      sticky.x = cmd.x;
      sticky.y = cmd.y;
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
      if(figma.timer) {
        figma.timer.start(cmd.seconds);
        break;
      }
      else {
        break;
      }
    }
  }
};
