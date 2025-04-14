import { WebSocket, WebSocketServer } from 'ws';
import { AiAgent } from './agents/AiAgent';
import { BaseAgent } from './agents/BaseAgent';
import { Game } from './game';
import { GameState, PuppetConfig } from '../../shared/GameState';
import express from 'express';
import { Request, Response } from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import { generateAvatar } from './avatars';

// Create express app for HTTP endpoints
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Set up WebSocket server for real-time game communication
const wss = new WebSocketServer({ port: 8080 });
const games = new Map<string, Game>();

// API endpoint for avatar generation
app.post('/api/generate-avatar', async (req: Request, res: Response) => {
    try {
        const { prompt } = req.body;

        if (!prompt) {
            res.status(400).json({ error: 'Prompt is required' });
            return;
        }

        console.log(`Generating avatar with prompt: ${prompt}`);
        const imageUrl = await generateAvatar(prompt);

        res.json({ url: imageUrl });
    } catch (error) {
        console.error('Error generating avatar:', error);
        res.status(500).json({ error: 'Failed to generate avatar' });
    }
});

import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';

// Load environment variables from secrets.env
const envPath = path.resolve(__dirname, '../secrets.env');
if (fs.existsSync(envPath)) {
    dotenv.config({ path: envPath });
    console.log('Loaded environment variables from secrets.env');
} else {
    console.warn('secrets.env file not found');
}

console.log('WebSocket server started on port 8080');

wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', async (data) => {
        try {
            const message = JSON.parse(data.toString());
            console.log('Received message type:', message.type);
            console.log('Received message data:', JSON.stringify(message).substring(0, 500) + (JSON.stringify(message).length > 500 ? '...' : ''));

            switch (message.type) {
                case 'start_game':
                    const config = message.config;

                    const game: Game = new Game(config);
                    for (let i = 0; i < config.puppets.length; i++) {
                        let puppetConfig = config.puppets[i];
                        let puppet = game.state.puppets[i];
                        if (puppet && !puppet.avatarUrl) {
                            console.log("Generating avatar for", puppetConfig);
                            puppet.avatarUrl = await generateAvatar(puppetConfig);
                            console.log("Avatar generated : ", puppet.avatarUrl);
                        }
                    }
                    game.clients = new Set([ws]);

                    const gameId = "foo";
                    games.set(gameId, game);

                    // Start game loop
                    startGameLoop(gameId);

                    // Send confirmation
                    ws.send(JSON.stringify({
                        type: 'game_started',
                        gameId,
                        message: `Game ${gameId} started with ${config.puppets.length} agents`
                    }));

                    break;
                    
                case 'state_update':
                    console.log('Received state update from frontend:', message.state);
                    // Find the game this client is connected to
                    let clientGame: Game | undefined;
                    games.forEach((g, id) => {
                        if (g.clients.has(ws)) {
                            clientGame = g;
                        }
                    });
                    
                    if (clientGame) {
                        console.log('Updating game state from frontend');
                        clientGame.updateStateFromFrontend(message.state);
                    } else {
                        console.warn('Received state update but client is not in any game');
                    }
                    break;
            }
        } catch (error) {
            console.error('Error handling message:', error);
            ws.send(JSON.stringify({
                type: 'error',
                message: 'Invalid message format'
            }));
        }
    });

    ws.on('close', () => {
        console.log('Client disconnected');
        // Remove client from all games
        games.forEach((game) => {
            game.clients.delete(ws);
        });
    });
});

async function startGameLoop(gameId: string) {
    const game = games.get(gameId);
    if (!game) {
        console.log(`Game ${gameId} not found, cannot start game loop`);
        return;
    }

    console.log(`Starting game loop for game ${gameId} with ${game.state.puppets.length} puppets`);

    const gameLoop = setInterval(async () => {
        if (!games.has(gameId)) {
            console.log(`Game ${gameId} no longer exists, stopping game loop`);
            clearInterval(gameLoop);
            return;
        }

        console.log(`Running turn for game ${gameId}`);
        // Get moves from all agents
        const state = await game.turn();
        console.log(`Turn completed for game ${gameId}, state:`, JSON.stringify(state).substring(0, 500) + (JSON.stringify(state).length > 500 ? '...' : ''));

        // Broadcast state to all clients
        const stateUpdate = {
            type: 'state_update',
            state
        };

        console.log(`Broadcasting state update to ${game.clients.size} clients`);
        game.clients.forEach((client: WebSocket) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(stateUpdate));
                console.log('State update sent to client');
            } else {
                console.log(`Client not ready, state: ${client.readyState}`);
            }
        });
    }, 2000); // Update every 2 seconds
}

// Start the HTTP server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`HTTP server listening on port ${PORT}`);
});