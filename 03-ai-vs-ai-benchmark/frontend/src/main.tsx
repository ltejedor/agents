import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Import game engine elements but don't start the game immediately
// The game will be started by the CharacterCreator component when needed
import { Color, DisplayMode, Engine, FadeInOut } from "excalibur";
import { loader } from "./resources";
import { MyLevel } from "./level";

// Initialize React app
const container = document.getElementById('root');
if (!container) throw new Error('Failed to find the root element');

const root = createRoot(container);
root.render(<App />);
