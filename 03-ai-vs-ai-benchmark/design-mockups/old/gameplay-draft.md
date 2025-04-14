# KILLER PUPPET
## Game Design Document

### GAME OVERVIEW

**Game Title:** Killer Puppet

**Game Concept:** A comedic horror text adventure where players create sockpuppet characters that are controlled by AI in a deadly game of assassination and survival.

**Genre:** Comedy Horror, Survival, Text Adventure with AI Agents

**Platform:** Video Game

**Target Audience:** Players who enjoy social deduction games, AI behavior, and comedic horror.

### GAME MECHANICS

#### Core Gameplay Loop:
1. Players create and customize their killer sockpuppet
2. Game assigns each puppet a target to eliminate
3. AI-controlled puppets navigate the environment searching for items and hunting targets
4. Last puppet standing wins

#### Game Structure:
- **Session Length:** Approximately 10 minutes per game
- **Player Count:** Up to 12 players
- **Turn System:** Simultaneous turns where all puppets submit their move, then all actions resolve at once

#### Assassination Mechanics:
- Each puppet is assigned a target from a secret circular list
- Players only know their immediate target (next person in the list)
- When a puppet eliminates their target, they inherit that target's next target
- The chain continues until only one puppet remains

### CHARACTER CREATION

#### Character Elements:

1. **Name:** Players choose a name for their sockpuppet

2. **Appearance:** Customize the sockpuppet's visual appearance
   - AI-generated avatar pictures based on customization choices

3. **Personality Bio:** Players write a strategic personality description
   - This text guides how the AI will control the puppet during gameplay
   - Examples: "Cautious but opportunistic," "Aggressive hunter," "Resource hoarder"

4. **Stats:** Players allocate points across six core attributes
   - **Health:** Determines how much damage the puppet can withstand
   - **Stamina:** Affects how many actions can be performed before resting
   - **Strength:** Influences combat effectiveness and carrying capacity
   - **Speed:** Determines movement range per turn
   - **Stealth:** Affects ability to move undetected and ambush others
   - **Perception:** Determines ability to spot hidden items and other puppets

### GAME ENVIRONMENTS

The game features three distinct settings:

1. **Haunted Mansion**
   - Victorian-style haunted house with multiple floors
   - Hidden passages, secret rooms
   - Antique weapons and items fitting the setting

2. **Abandoned Factory**
   - Industrial setting with machinery and hazards
   - More open spaces with fewer hiding spots
   - Modern tools and improvised weapons

3. **Secret Lair**
   - Underground complex with high-tech and mysterious elements
   - Trap rooms and security systems
   - Advanced equipment and experimental items

Each environment is divided into connected rooms that puppets navigate between during turns.

### ITEMS AND RESOURCES

#### Consumables:
- **Food:** Restores hunger meter
- **Medical Items:** Restore health
- **Energy Drinks:** Restore stamina
- **Special Consumables:** Temporary stat boosts

#### Equipment:
- **Weapons:** Increase combat effectiveness
- **Armor:** Reduce damage taken
- **Tools:** Provide special abilities (lock picking, trap detection, etc.)
- **Accessories:** Provide permanent stat boosts

### SURVIVAL MECHANICS

- **Hunger System:** A hunger meter that depletes over time
  - As hunger increases, health and stamina drain accelerates
  - Forces puppets to search for food or risk weakening
  - Creates a time pressure to encourage confrontation

- **Environmental Hazards:**
  - Traps in rooms that can damage unwary puppets
  - Collapsing structures
  - Toxic areas
  - Extreme temperatures

### COMBAT SYSTEM

- **Encounter Resolution:** When puppets encounter each other, combat is resolved through stat-based die rolls
- **Combat Factors:**
  - Base stats (Strength, Speed, Stealth, etc.)
  - Equipment bonuses
  - Current health and stamina levels
  - Environmental factors
  - Random elements (die rolls)

### AI BEHAVIOR SYSTEM

- **Personality-Driven:** AI controls puppets based on player-written personality bios
- **Strategic Decision Making:** AI evaluates:
  - Current health/stamina levels
  - Known locations of other puppets
  - Available routes
  - Inventory status
  - Target location (if known)
  - Environmental threats

- **Learning:** AI may adapt strategies based on game events and observed puppet behaviors

### USER INTERFACE

- **Main Game Screen:** Text-based adventure format with:
  - Room description
  - Available exits
  - Visible items
  - Other puppets present
  - Current status indicators

- **Command Options:** AI selects from available actions:
  - Move to adjacent room
  - Search current room
  - Pick up item
  - Use item/consumable
  - Attack another puppet
  - Hide
  - Set trap
  - Rest

- **Status Display:**
  - Health meter
  - Stamina meter
  - Hunger meter
  - Inventory
  - Current target

### GAME FLOW

1. **Pre-Game:**
   - Players create and customize their puppets
   - Players write personality/strategy bios

2. **Game Start:**
   - Puppets are placed randomly in the environment
   - Target assignments are distributed
   - Initial items are scattered throughout the environment

3. **Gameplay:**
   - AI-controlled puppets take actions based on personality profiles
   - Actions resolve simultaneously each turn
   - Game state updates (health, item locations, puppet positions)

4. **Game End:**
   - Last puppet standing wins
   - Victory screen shows game stats and puppet journey

### TECHNICAL REQUIREMENTS

- **AI System:** Natural language processing to interpret personality bios and generate appropriate puppet behaviors
- **Simultaneous Turn Resolution:** System for collecting all puppet actions and resolving them in a fair order
- **Procedural Content:** Randomized item placement and potentially room layouts
- **AI Image Generation:** System for creating puppet avatars based on customization choices

### MONETIZATION POTENTIAL (Optional)

- **Base Game:** Free or one-time purchase
- **Additional Environments:** New map packs with unique themes
- **Cosmetic Items:** Special puppet customization options
- **AI Personality Templates:** Pre-made strategic AI personalities

### FUTURE EXPANSION POSSIBILITIES

- **Multiplayer Modes:** Allow players to take control during specific moments
- **Campaign Mode:** Connected scenarios with persistent puppets
- **Custom Rule Sets:** Allow players to modify game parameters
- **Puppet Evolution:** Puppets that survive games gain experience and abilities

---

## DEVELOPMENT ROADMAP

### Phase 1: Prototype
- Basic puppet creation
- Simple room navigation
- Fundamental AI behavior system
- Core combat mechanics

### Phase 2: Alpha
- Complete character creation
- All three environments
- Full item system
- Advanced AI behavior

### Phase 3: Beta
- Balance testing
- UI refinement
- Performance optimization
- User testing feedback implementation

### Phase 4: Release
- Final polish
- Launch marketing
- Community building
- Post-launch support planning