# KILLER PUPPET - CORE DATA STRUCTURES

## Puppet

```typescript
interface Puppet {
  // Basic Information
  id: string;                     // Unique identifier
  name: string;                   // Player-given name
  avatarImage: string;            // URL or reference to AI-generated image
  personalityBio: string;         // AI strategy guidance text
  
  // Stats
  stats: {
    health: number;               // Current health points
    maxHealth: number;            // Maximum possible health
    stamina: number;              // Current stamina points
    maxStamina: number;           // Maximum possible stamina
    strength: number;             // Base strength (affects damage dealt)
    speed: number;                // Base speed (affects initiative in combat)
    stealth: number;              // Base stealth (affects chance to hide/ambush)
    perception: number;           // Base perception (affects item finding and puppet detection)
    hunger: number;               // Current hunger level
    maxHunger: number;            // Maximum hunger level
  };
  
  // Game State
  currentRoomId: string;          // Current location
  targetId: string;               // Current assassination target
  isAlive: boolean;               // Whether puppet is still in the game
  knownMap: string[];             // List of room IDs the puppet knows about
  
  // Equipment
  equipment: {
    weapon: Item | null;          // Equipped weapon
    armor: Item | null;           // Equipped armor
    tool: Item | null;            // Equipped tool
    consumable: Item | null;      // Equipped consumable
  };
  
  // Stats (for end-game summary)
  killCount: number;              // Number of puppets eliminated
  damageDealt: number;            // Total damage dealt
  damageTaken: number;            // Total damage received
  itemsUsed: number;              // Total items consumed
}
```

## Room

```typescript
interface Room {
  // Basic Information
  id: string;                     // Unique identifier
  name: string;                   // Room name
  description: string;            // Room description
  environment: "mansion" | "factory" | "lair";  // Which game environment
  
  // Connections
  connectedRoomIds: string[];     // IDs of directly connected rooms
  
  // Contents
  items: {
    itemId: string;               // Item in room
    isHidden: boolean;            // Whether item requires searching
    discoveryDifficulty: number;  // Perception check difficulty to find
  }[];
  
  // Environmental Features
  hazards: {
    targetStat: "health" | "stamina";  // Which stat is affected
    checkType: "strength" | "speed" | "stealth" | "perception";  // Skill to avoid
    difficulty: number;           // Skill check difficulty
  }[];
  
  // State
  puppetsPresent: string[];       // IDs of puppets currently in room
  isDiscovered: boolean;          // Whether any puppet has entered this room
}
```

## Item

```typescript
interface Item {
  // Basic Information
  id: string;                     // Unique identifier
  name: string;                   // Item name
  description: string;            // Item description
  
  // Equipment slot
  slot: "weapon" | "armor" | "tool" | "consumable";
  
  // Effect
  affectedStat: "health" | "stamina" | "strength" | "speed" | "stealth" | "perception";
  effectValue: number;            // Amount of boost/restoration
}
```

## Action

```typescript
interface Action {
  // Basic Information
  id: string;                     // Unique identifier
  puppetId: string;               // Puppet performing action
  type: "move" | "search" | "attack" | "use" | "pickup" | "hide" | "rest";  // Action type
  turnNumber: number;             // Game turn when executed
  
  // Target
  subject: string;               // ID of target (room, item, or puppet)
}
```

## Game State

```typescript
interface GameState {
  // Basic Information
  id: string;                     // Game session ID
  startTime: Date;                // When game began
  environment: "mansion" | "factory" | "lair";  // Selected environment
  
  // Turn Information
  currentTurn: number;            // Current turn number
  
  // Participants
  puppets: Puppet[];              // All puppets in game
  targetChain: string[];          // Circular list of puppet IDs (assassination targets)
  
  // Environment
  rooms: Room[];                  // All rooms in the game
  
  // Items
  availableItems: Item[];         // All possible items in this game
  
  // Action History
  actions: Action[];              // All actions taken so far
}
```