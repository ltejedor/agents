import { Actor, Collider, CollisionContact, CollisionType, Color, Engine, Font, GraphicsGroup, ImageSource, PointerEvent, Rectangle, Side, Sprite, Text, vec } from "excalibur";
import { FALLBACK_AVATARS } from "./resources";

// Actors are the main unit of composition you'll likely use, anything that you want to draw and move around the screen
// is likely built with an actor

// They contain a bunch of useful components that you might use
// actor.transform
// actor.motion
// actor.graphics
// actor.body
// actor.collider
// actor.actions
// actor.pointer


export class Player extends Actor {
  private playerColor: Color;
  private targetColor: Color = Color.Yellow;
  public isHumanControlled: boolean;
  private speed: number = 200;
  private isControlledByBackend: boolean = false;
  private avatarUrl: string | null = null;
  private avatarImage: ImageSource | null = null;
  private isAvatarLoaded: boolean = false;
  public id: string; // Add id property
  public targetId?: string; // Add targetId property
  public isAI: boolean = false; // Add isAI property

  constructor(options: {
    id: string,
    name: string,
    pos: { x: number, y: number },
    color: Color,
    isHumanControlled?: boolean,
    isControlledByBackend?: boolean,
    avatarUrl?: string,
    isAI?: boolean
  }) {
    super({
        name: options.name,
        pos: vec(options.pos.x, options.pos.y),
        width: 50,
        height: 50,
        color: options.color,
        collisionType: CollisionType.Active
    });

    this.id = options.id;
    this.playerColor = options.color;
    this.isHumanControlled = options.isHumanControlled || false;
    this.isControlledByBackend = options.isControlledByBackend || !this.isHumanControlled;
    this.isAI = options.isAI || false;

    // Always use the default avatar image
    this.setAvatarUrl(FALLBACK_AVATARS.default);
  }

  public setAvatarUrl(url: string): void {
    this.avatarUrl = url;

    if (!url) return;

    // Create an ImageSource and load it
    console.log('Loading avatar image from:', url);
    this.avatarImage = new ImageSource(url);
    this.avatarImage.load().then(() => {
      this.isAvatarLoaded = true;
      console.log('Avatar loaded');
      this.updateGraphics();
    }).catch(err => {
      console.error('Failed to load avatar image:', err);
    });
  }

  public updateGraphics(): void {
    // Create a text label with the player's name with spookier font
    const nameLabel = new Text({
      text: this.name,
      font: new Font({
        family: 'Creepster, cursive',
        size: 14,
        color: Color.fromHex('#ff1a1a'), // Blood red color
        quality: 4,
        shadow: {
          offset: vec(1, 1),
          color: Color.Black,
          blur: 2
        }
      })
    });

    // Always use the avatar image
    let mainGraphic;
    
    if (this.isAvatarLoaded && this.avatarImage) {
      // Use the avatar image with a slight red tint for a spookier look
      mainGraphic = new Sprite({
        image: this.avatarImage,
        destSize: { width: this.width, height: this.height },
        tint: Color.fromRGB(255, 200, 200, 0.9) // Slight red tint
      });
    } else {
      // Fallback to a rectangle but make it look spooky
      mainGraphic = new Rectangle({
        width: this.width,
        height: this.height,
        color: Color.fromHex('#8a0303'), // Dark blood color
      });
    }

    // Create a graphics group to combine the main graphic and text
    const graphicsGroup = new GraphicsGroup({
      members: [
        {
          graphic: mainGraphic,
          offset: vec(0, 0)
        },
        {
          graphic: nameLabel,
          offset: vec(0, -35) // Position above the player avatar
        }
      ]
    });

    // Use the composite graphic
    this.graphics.use(graphicsGroup);
  }

  // Add method to constrain position to visible area
  private constrainPosition(pos: { x: number, y: number }): { x: number, y: number } {
    if (!this.scene || !this.scene.engine) return pos;
    
    const engine = this.scene.engine;
    const margin = 50; // Keep player at least 50px from the edge
    
    return {
      x: Math.max(margin, Math.min(engine.drawWidth - margin, pos.x)),
      y: Math.max(margin, Math.min(engine.drawHeight - margin, pos.y))
    };
  }

  public updatePosition(newPos: { x: number, y: number }): void {
    // Log position change for debugging
    console.log(`Player ${this.id} position updating from ${this.pos.x},${this.pos.y} to ${newPos.x},${newPos.y}`);
    
    // Constrain position to visible area
    const constrainedPos = this.constrainPosition(newPos);
    
    // Update the position - use the actual newPos values after constraining
    this.pos.x = constrainedPos.x;
    this.pos.y = constrainedPos.y;
    
    // Force a transform update to ensure position change is applied
    this.transform.pos.x = constrainedPos.x;
    this.transform.pos.y = constrainedPos.y;
    
    // Reset velocity to ensure no residual movement
    this.vel = vec(0, 0);
    
    // Clear any ongoing actions that might interfere with position
    this.actions.clearActions();
    
    // Set this player as controlled by backend
    this.isControlledByBackend = true;
  }

  override onInitialize() {
    // Initialize the graphics
    this.updateGraphics();

    // Set up input handling for human player
    if (this.isHumanControlled) {
      this.on('pointerdown', this.handlePointerDown.bind(this));
    }
  }

  private handlePointerDown(evt: PointerEvent) {
    // Move to clicked position
    this.actions.clearActions();
    this.actions.moveTo(evt.worldPos, this.speed);
  }

  override onPreUpdate(engine: Engine, elapsedMs: number): void {
    // AI movement logic would go here for non-human players
    // Only use random movement if not controlled by backend
    if (!this.isHumanControlled && !this.isControlledByBackend && Math.random() < 0.01) {
      // Occasionally change direction
      const randomX = Math.random() * (engine.drawWidth - 100) + 50;
      const randomY = Math.random() * (engine.drawHeight - 100) + 50;
      this.actions.clearActions();
      this.actions.moveTo(vec(randomX, randomY), this.speed);
    }
    
    // Ensure player stays within bounds
    if (this.pos.x < 50) this.pos.x = 50;
    if (this.pos.y < 50) this.pos.y = 50;
    if (this.pos.x > engine.drawWidth - 50) this.pos.x = engine.drawWidth - 50;
    if (this.pos.y > engine.drawHeight - 50) this.pos.y = engine.drawHeight - 50;
    
    // Add a subtle pulsing effect for a more ominous look
    const pulseAmount = Math.sin(engine.clock.elapsed() / 500) * 0.05 + 0.95;
    this.scale = vec(pulseAmount, pulseAmount);
  }

  override onPostUpdate(engine: Engine, elapsedMs: number): void {
    // Debug position to ensure it's being updated correctly
    if (this.isAI && engine.currentFps % 60 === 0) { // Log once per second approximately
      console.log(`Player ${this.id} current position: ${this.pos.x},${this.pos.y}`);
    }
  }

  override onPreCollisionResolve(self: Collider, other: Collider, side: Side, contact: CollisionContact): void {
    // Called before a collision is resolved, if you want to opt out of this specific collision call contact.cancel()
  }

  override onPostCollisionResolve(self: Collider, other: Collider, side: Side, contact: CollisionContact): void {
    // Called every time a collision is resolved and overlap is solved
  }

  override onCollisionStart(self: Collider, other: Collider, side: Side, contact: CollisionContact): void {
    // Check if collided with another player
    if (other.owner instanceof Player) {
      const otherPlayer = other.owner as Player;

      // Notify game manager of potential kill (will be handled there)
      const scene = this.scene;
      if (scene) {
        scene.emit('player-collision', { killer: this, victim: otherPlayer });
      }
    }
  }

  override onCollisionEnd(self: Collider, other: Collider, side: Side, lastContact: CollisionContact): void {
    // Called when a pair of objects separates
  }

  public getColor(): Color {
    return this.playerColor;
  }

  public setTargetColor(color: Color): void {
    this.targetColor = color;
  }

  public setHumanControlled(isHuman: boolean): void {
    this.isHumanControlled = isHuman;
    if (isHuman) {
      this.isControlledByBackend = false;
    }
  }

  public setBackendControlled(isBackendControlled: boolean): void {
    this.isControlledByBackend = isBackendControlled;
    if (isBackendControlled) {
      this.isHumanControlled = false;
    }
  }
}