import React, { useState } from 'react';
import CharacterCreator from './CharacterCreator';
import GameComponent from './GameComponent';
import './style.css';

// Define the character data interface
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

function App() {
    const [gameStarted, setGameStarted] = useState(true); // Start game immediately
    const [characterData, setCharacterData] = useState<CharacterData | null>(null);

    const handleStartGame = (data: CharacterData) => {
        setCharacterData(data);
        setGameStarted(true);
    };

    return (
        <div className="App">
            {!gameStarted ? (
                <CharacterCreator onStartGame={handleStartGame} />
            ) : (
                <GameComponent characterData={null} />
            )}
        </div>
    );
}

export default App;