import React, { useState, useEffect } from 'react';
import { GameConfig, PuppetConfig, PuppetStats } from '../../shared/GameState';
import { Color, DisplayMode, Engine, FadeInOut } from "excalibur";
import { loader } from "./resources";
import { MyLevel } from "./level";

interface CharacterData {
  name: string;
  bio: {
    tragicBackstory: string;
    strategyForKilling: string;
    strategyForSurvival: string;
  };
  stats: {
    stealth: number;
    strength: number;
    speed: number;
    perception: number;
    cunning: number;
  };
}

interface CharacterCreatorProps {
  onStartGame: (characterData: CharacterData) => void;
}

const CharacterCreator: React.FC<CharacterCreatorProps> = ({ onStartGame }) => {
  const TOTAL_POINTS = 15;
  const [pointsLeft, setPointsLeft] = useState(TOTAL_POINTS);
  const [showJson, setShowJson] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  const [webSocket, setWebSocket] = useState<WebSocket | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    material: '',
    pattern: '',
    eyes: '',
    accessories: '',
    backstory: '',
    killStyle: '',
    catchphrase: '',
    stealth: 1,
    strength: 1,
    speed: 1,
    perception: 1,
    cunning: 1
  });

  const [characterJson, setCharacterJson] = useState<CharacterData | null>(null);

  // Calculate points left
  useEffect(() => {
    const { stealth, strength, speed, perception, cunning } = formData;
    const total = stealth + strength + speed + perception + cunning;
    setPointsLeft(TOTAL_POINTS - total);
  }, [formData.stealth, formData.strength, formData.speed, formData.perception, formData.cunning]);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle stat changes
  const handleStatChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const numValue = parseInt(value) || 1;

    // Calculate what the new total would be
    const stats = ['stealth', 'strength', 'speed', 'perception', 'cunning'];
    const currentTotal = stats.reduce((sum, stat) => {
      return sum + (stat === name ? numValue : formData[stat as keyof typeof formData] as number);
    }, 0);

    // Only update if the total is valid or we're decreasing
    if (currentTotal <= TOTAL_POINTS || numValue < formData[name as keyof typeof formData]) {
      setFormData(prev => ({
        ...prev,
        [name]: Math.min(Math.max(numValue, 1), 5) // Clamp between 1 and 5
      }));
    }
  };

  // Handle stat button clicks
  const handleStatButton = (stat: string, action: 'increase' | 'decrease') => {
    const currentValue = formData[stat as keyof typeof formData] as number;
    let newValue = currentValue;

    if (action === 'increase' && currentValue < 5 && pointsLeft > 0) {
      newValue = currentValue + 1;
    } else if (action === 'decrease' && currentValue > 1) {
      newValue = currentValue - 1;
    } else {
      return; // Don't update if invalid
    }

    setFormData(prev => ({
      ...prev,
      [stat]: newValue
    }));
  };

  // Generate random stats that add up to TOTAL_POINTS
  const generateRandomStats = (): Partial<typeof formData> => {
    const stats = ['stealth', 'strength', 'speed', 'perception', 'cunning'];
    const randomStats = stats.reduce((acc, stat) => {
      // Generate a random number between 1 and 5
      const value = Math.floor(Math.random() * 5) + 1;
      acc[stat] = value;
      return acc;
    }, {} as Partial<typeof formData>);

    // Adjust the stats to ensure they add up to TOTAL_POINTS
    const currentTotal = Object.values(randomStats).reduce((sum, val) => sum + val, 0);
    const diff = TOTAL_POINTS - currentTotal;

    // Distribute the difference among the stats
    if (diff !== 0) {
      const statsToAdjust = stats.filter(stat => randomStats[stat] < 5);
      const adjustment = Math.min(Math.abs(diff), statsToAdjust.length);
      
      for (let i = 0; i < adjustment; i++) {
        const stat = statsToAdjust[i % statsToAdjust.length];
        randomStats[stat] = Math.min(5, randomStats[stat] + (diff > 0 ? 1 : -1));
      }
    }

    return randomStats;
  };

  // Handle randomization
  const handleRandomize = () => {
    const randomStats = generateRandomStats();
    
    // Generate random appearance options
    const materials = ['cotton', 'wool', 'nylon', 'silk'];
    const patterns = ['striped', 'polkadot', 'argyle', 'solid'];
    const eyes = ['button', 'googly', 'googly', 'googly']; // More googly eyes for fun
    const accessories = ['none', 'scarf', 'hat', 'glasses'];

    setFormData({
      name: `Sock ${Math.floor(Math.random() * 1000) + 1}`,
      material: materials[Math.floor(Math.random() * materials.length)],
      pattern: patterns[Math.floor(Math.random() * patterns.length)],
      eyes: eyes[Math.floor(Math.random() * eyes.length)],
      accessories: accessories[Math.floor(Math.random() * accessories.length)],
      backstory: `Once a ${formData.material} sock, now a ruthless killer.`,
      killStyle: `Uses ${formData.pattern} patterns to confuse victims.`,
      catchphrase: `I'm just a sock!`,
      ...randomStats
    });
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (pointsLeft < 0) {
      alert('Please make sure your stat points add up to 15!');
      return;
    }

    const characterData: CharacterData = {
      name: formData.name,
      bio: {
        tragicBackstory: formData.backstory,
        strategyForKilling: formData.killStyle,
        strategyForSurvival: formData.catchphrase
      },
      stats: {
        stealth: formData.stealth,
        strength: formData.strength,
        speed: formData.speed,
        perception: formData.perception,
        cunning: formData.cunning
      }
    };

    setCharacterJson(characterData);
    onStartGame(characterData);
  };

  return (
    <div className="container">
      <h1>Killer Sockpuppet Creator</h1>
      <form id="characterForm" onSubmit={handleSubmit}>
        <button 
          type="button" 
          onClick={handleRandomize} 
          className="randomize-button"
          style={{ marginBottom: '20px' }}
        >
          Randomize Character
        </button>
        <section className="form-section">
          <h2>Appearance</h2>
          <div className="form-group">
            <label>Name
              <input
                type="text"
                name="name"
                required
                className="name-input"
                placeholder="Enter your sockpuppet's name"
                value={formData.name}
                onChange={handleInputChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label>Base Material</label>
            <div className="radio-group">
              {['cotton', 'wool', 'nylon', 'silk'].map(material => (
                <label key={material}>
                  <input
                    type="radio"
                    name="material"
                    value={material}
                    required
                    checked={formData.material === material}
                    onChange={handleInputChange}
                  />
                  {material.charAt(0).toUpperCase() + material.slice(1)} Sock
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Pattern</label>
            <div className="radio-group">
              {['striped', 'polkadot', 'argyle', 'solid'].map(pattern => (
                <label key={pattern}>
                  <input
                    type="radio"
                    name="pattern"
                    value={pattern}
                    required
                    checked={formData.pattern === pattern}
                    onChange={handleInputChange}
                  />
                  {pattern === 'polkadot' ? 'Polka Dot' :
                    pattern.charAt(0).toUpperCase() + pattern.slice(1) + (pattern === 'solid' ? ' Color' : '')}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Eyes</label>
            <div className="radio-group">
              {[
                { value: 'button', label: 'Button Eyes' },
                { value: 'googly', label: 'Googly Eyes' },
                { value: 'glowing', label: 'Glowing Eyes' },
                { value: 'void', label: 'Void-like Eyes' }
              ].map(eye => (
                <label key={eye.value}>
                  <input
                    type="radio"
                    name="eyes"
                    value={eye.value}
                    required
                    checked={formData.eyes === eye.value}
                    onChange={handleInputChange}
                  />
                  {eye.label}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Accessories</label>
            <div className="radio-group">
              {[
                { value: 'bow', label: 'Evil Bow Tie' },
                { value: 'hat', label: 'Tiny Top Hat' },
                { value: 'eyepatch', label: 'Eyepatch' },
                { value: 'none', label: 'No Accessories' }
              ].map(accessory => (
                <label key={accessory.value}>
                  <input
                    type="radio"
                    name="accessories"
                    value={accessory.value}
                    required
                    checked={formData.accessories === accessory.value}
                    onChange={handleInputChange}
                  />
                  {accessory.label}
                </label>
              ))}
            </div>
          </div>
        </section>

        <section className="form-section">
          <h2>Bio</h2>
          <div className="bio-fields">
            <label>
              Tragic Backstory
              <textarea
                name="backstory"
                maxLength={256}
                value={formData.backstory}
                onChange={handleInputChange}
              ></textarea>
              <span className="char-count">{formData.backstory.length}/256</span>
            </label>

            <label>
              Strategy for Killing
              <textarea
                name="killStyle"
                maxLength={256}
                value={formData.killStyle}
                onChange={handleInputChange}
              ></textarea>
              <span className="char-count">{formData.killStyle.length}/256</span>
            </label>

            <label>
              Strategy for Staying Alive
              <textarea
                name="catchphrase"
                maxLength={256}
                value={formData.catchphrase}
                onChange={handleInputChange}
              ></textarea>
              <span className="char-count">{formData.catchphrase.length}/256</span>
            </label>
          </div>
        </section>

        <section className="form-section">
          <h2>Stats (Total Points: <span id="pointsLeft">{pointsLeft}</span>)</h2>
          <div className="stat-group">
            {['stealth', 'strength', 'speed', 'perception', 'cunning'].map(stat => (
              <label key={stat}>
                {stat.charAt(0).toUpperCase() + stat.slice(1)}
                <button
                  type="button"
                  className="stat-button"
                  onClick={() => handleStatButton(stat, 'decrease')}
                >-</button>
                <input
                  type="number"
                  name={stat}
                  min="1"
                  max="5"
                  value={formData[stat as keyof typeof formData]}
                  onChange={handleStatChange}
                />
                <button
                  type="button"
                  className="stat-button"
                  onClick={() => handleStatButton(stat, 'increase')}
                >+</button>
              </label>
            ))}
          </div>
        </section>

        <div className="buttons">
          <button
            type="submit"
            disabled={isConnecting}
            className={isConnecting ? "loading" : ""}
          >
            {isConnecting ? "Connecting..." : "Start Game"}
          </button>
        </div>

        {connectionStatus === 'connecting' && (
          <div className="connection-status">
            Connecting to game server...
          </div>
        )}

        {connectionStatus === 'connected' && (
          <div className="connection-status success">
            Connected! Starting game...
          </div>
        )}
      </form>
    </div>
  );
};

export default CharacterCreator;