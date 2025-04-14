# KILLER PUPPET
## Complete Game Design

## GAME OVERVIEW

Killer Puppet is a text-based game where players create AI-controlled sockpuppet assassins that hunt targets in a haunted mansion. The AI puppets act according to their assigned personalities while players watch the comedic horror unfold. Last puppet standing wins!

## PUPPET CREATION

1. **Name:** Choose a name for your killer sockpuppet

2. **Appearance:** Write a brief description (used to generate an AI avatar)

3. **Personality:** Write a short personality bio (100-200 words) describing your puppet's strategy and behavior patterns. This guides the AI's decision-making.

4. **Stats:** Distribute 10 points across these attributes (all start at 1, max 5):
   - Constitution: Physical resilience
   - Strength: Combat effectiveness
   - Speed: Initiative and action order
   - Perception: Finding items and noticing other puppets
   - Stealth: Ability to hide and avoid detection

5. **Derived Stats:**
   - Health = 20 + (Constitution × 2)
   - Stamina = 20 + (Constitution × 2)

## THE HAUNTED MANSION

### Room Descriptions & Connections

#### 1. Grand Foyer
A once-elegant entrance hall with a cracked marble floor and a massive chandelier dangling precariously overhead. Dusty portraits seem to follow your movements with their eyes.
- **Connects to:** Dining Hall, Library, Grand Staircase

#### 2. Dining Hall
A long table set for a feast that was never served. The silverware is tarnished, and the plates are coated with decades of dust. A foul smell emanates from covered serving dishes.
- **Connects to:** Grand Foyer, Kitchen, Conservatory

#### 3. Kitchen
Rusty knives and cooking implements hang from hooks. The counters are stained with suspicious dark splotches, and an ancient refrigerator emits a low humming sound.
- **Connects to:** Dining Hall, Cellar

#### 4. Library
Floor-to-ceiling bookshelves line the walls, filled with moldering tomes. A ladder on rails provides access to higher shelves, though it creaks dangerously when touched.
- **Connects to:** Grand Foyer, Study, Secret Passage

#### 5. Study
A once-luxurious room with a large desk and leather chair. The walls are decorated with mounted animal heads that seem unnaturally preserved - their glass eyes sometimes blink.
- **Connects to:** Library, Master Bedroom

#### 6. Grand Staircase
A sweeping staircase with rotting banisters. Several steps are missing, creating treacherous gaps. The wallpaper is peeling away to reveal strange symbols carved into the walls.
- **Connects to:** Grand Foyer, Upper Hallway, Cellar

#### 7. Upper Hallway
A long corridor lined with doors, most of which are sealed shut. The faded carpet runner is stained with what might be footprints that appear and disappear at random.
- **Connects to:** Grand Staircase, Master Bedroom, Nursery

#### 8. Master Bedroom
A four-poster bed dominates this room, draped with tattered curtains. A vanity with a cracked mirror sits in the corner, sometimes showing reflections of people who aren't there.
- **Connects to:** Study, Upper Hallway, Conservatory

#### 9. Nursery
Decaying toys are scattered across the floor. A rocking horse moves on its own, and a music box occasionally plays a haunting lullaby without being wound.
- **Connects to:** Upper Hallway

#### 10. Conservatory
Dead plants fill ornate pots, though some seem to twitch and reach out when no one is looking directly at them. A grand piano in the corner occasionally plays a single note.
- **Connects to:** Dining Hall, Master Bedroom, Secret Passage

#### 11. Cellar
A damp underground room with earthen walls and stone floors. Rusty tools hang on the walls, and strange symbols are carved into support beams. The air is thick with the scent of soil and decay.
- **Connects to:** Kitchen, Grand Staircase, Secret Passage

#### 12. Secret Passage
A narrow, hidden corridor behind the walls. The passage is barely wide enough for one person, and strange scratching sounds can be heard coming from inside the walls.
- **Connects to:** Library, Conservatory, Cellar

### Map Layout

```
          [9. NURSERY]
               |
               v
          [7. UPPER HALLWAY]
               |        |
               v        v
[6. GRAND STAIRCASE]    [8. MASTER BEDROOM]
    |      |                   |      |
    |      |                   |      |
    v      v                   v      v
[11. CELLAR]   [1. GRAND FOYER]   [5. STUDY]
    |               |    |             |
    |               |    |             |
    v               v    v             v
[12. SECRET PASSAGE] <- [2. DINING HALL] [4. LIBRARY]
    ^                        |             |
    |                        |             |
    +---------------------+  v             +
                          |  |             |
                          v  v             v
                    [10. CONSERVATORY] <- [3. KITCHEN]
```

## ITEMS

Three types of consumable items are distributed throughout the mansion:

1. **Medical Kit:** Restores 10 Health
2. **Energy Drink:** Restores 10 Stamina
3. **Puppet Repair Kit:** Restores 5 Health and 5 Stamina

Items have a "hiddenness" score (1d6) determined at game start. Puppets must make successful perception checks to notice them.

## GAME SETUP

1. Place 8 of each item type randomly throughout the mansion
2. Randomly place puppets in different rooms
3. Create a circular assassination chain (A targets B, B targets C, etc.)
4. Inform each puppet who their target is
5. Begin the first turn

## ACTIONS

Each puppet can perform one action per turn:

1. **Move:** Travel to a connected room
2. **Attack:** Fight another puppet in the same room
3. **Chase:** Follow a puppet if they move away
4. **Hide:** Get a stealth bonus until next turn
5. **Grab:** Use an item in the current room (if detected)

## TURN STRUCTURE

### Start of Turn
1. **Automatic Perception Checks**
   - Roll Perception + 1d6 for each puppet
   - Compare against item hiddenness and other puppets' Stealth
   - Hidden puppets get +1d6 to their Stealth

2. **Action Selection**
   - AI chooses actions based on puppet personalities
   - All actions are submitted simultaneously

3. **Initiative Determination**
   - Roll Speed + 1d6 for each puppet
   - Actions resolve in descending order
   - Ties broken by base Speed, then randomly

### Action Resolution
Process each action in initiative order:

1. **Move Action**
   - Relocate to a connected room
   - Other puppets in original room see where you went (if they detect you)

2. **Attack Action**
   - Both attacker and defender roll Strength + 1d6
   - If attacker wins, defender takes damage equal to the difference
   - If defender wins, attacker loses Stamina equal to the difference

3. **Chase Action**
   - If target still in room: Attack them
   - If target moved and was detected: Follow them
   - Otherwise: Chase fails

4. **Hide Action**
   - Gain +1d6 to Stealth until next turn

5. **Grab Action**
   - Use a detected item in the room
   - Gain the item's benefits immediately
   - Item is removed from the game

### End of Turn
1. Reduce all puppets' Stamina by 1
2. Puppets with 0 Stamina lose 1 Health
3. Check for eliminations
4. Generate turn narrative
5. Check for game end

## ELIMINATION

When a puppet's Health reaches 0:
1. The puppet is eliminated from the game
2. The puppet that was hunting them inherits their target
3. If eliminated by another puppet, that puppet gets credit for the kill

## VICTORY

The last puppet standing wins the game!

## GAME OUTPUT

For each turn, the game produces:
1. A global narrative describing all actions and their results
2. Individual perspectives for each puppet (what they see and experience)
3. Updated puppet stats (Health, Stamina)

At game end, a summary shows the order of eliminations and how the winner achieved victory.

## SAMPLE PUPPET TEMPLATES

### "Sneaky Steve"
**Appearance:** A gray sock puppet with shifty button eyes and a stitched-on smile
**Personality:** Prefers stealth over direct confrontation. Will prioritize hiding and only attack when having the advantage. Avoids open spaces and prefers to lurk in corners. Will collect items opportunistically but prioritizes survival over hunting. Only attacks when success is highly likely.

**Stats:**
- Constitution: 2
- Strength: 2
- Speed: 2
- Perception: 3
- Stealth: 5

### "Brute Force Betty"
**Appearance:** A red sock puppet with wild yarn hair and menacing felt teeth
**Personality:** Aggressive and direct. Always goes for the attack when possible. Actively hunts targets and isn't afraid of confrontation. Will use items to maintain fighting ability but won't hide or run away unless critically injured. Prefers direct routes to targets.

**Stats:**
- Constitution: 3
- Strength: 5
- Speed: 3
- Perception: 2
- Stealth: 1

### "Cautious Carl"
**Appearance:** A blue sock puppet with a worried expression and oversized glasses
**Personality:** Risk-averse and methodical. Prioritizes collecting items and maintaining health. Will avoid confrontation when possible and prefers to let others eliminate each other. Always tries to stay at maximum health and stamina. Will only attack when having overwhelming advantage.

**Stats:**
- Constitution: 5
- Strength: 1
- Speed: 1
- Perception: 3
- Stealth: 4

---

This design provides all the necessary components to run a complete game of Killer Puppet. The simplified mechanics maintain the core fun of AI-controlled assassin sockpuppets while being straightforward to implement and understand.