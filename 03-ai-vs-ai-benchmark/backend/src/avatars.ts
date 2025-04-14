import OpenAI from "openai";

import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';

import { PuppetConfig } from '../../shared/GameState';

// Load environment variables from secrets.env
const envPath = path.resolve(__dirname, '../secrets.env');
if (fs.existsSync(envPath)) {
    dotenv.config({ path: envPath });
    console.log('Loaded environment variables from secrets.env for avatar generation');
} else {
    console.warn('secrets.env file not found for avatar generation');
}

const GENERATE_AVATARS = false;

const client = new OpenAI();

/**
 * Generate an avatar image based on the provided prompt using DALL-E 3
 * @param prompt The description of the avatar to generate
 * @returns URL to the generated image
 */
async function generateAvatar(puppetConfig: PuppetConfig): Promise<string> {
    if (!GENERATE_AVATARS) {
        return 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-8Xvqz2Q86mquVqw1Z26O5aEg/user-ObiZKPyVRdJgvOOT30rD3rB1/img-eBJhwzhJJnFbBI5xsw60UeJX.png?st=2025-04-12T22%3A22%3A28Z&se=2025-04-13T00%3A22%3A28Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-12T08%3A02%3A11Z&ske=2025-04-13T08%3A02%3A11Z&sks=b&skv=2024-08-04&sig=9itg1gxfWqCebWK5uRp5jx2MaghBuTB47Exaeyln7VY%3D'
    }

    let prompt = "A sock puppet with a dark gothic background.";
    if (puppetConfig.avatar) {
        prompt = `A ${puppetConfig.avatar.material} sockpuppet with a ${puppetConfig.avatar.pattern} pattern, ${puppetConfig.avatar.eyes}${puppetConfig.avatar.accessories !== 'none' ? `, and ${puppetConfig.avatar.accessories}` : ''}. Dark avatar 3D realistic sockpuppet with haunted gothic background.`;
    }

    const enhancedPrompt = enhancePrompt(prompt);

    try {
        const response = await client.images.generate({
            model: "dall-e-3",
            prompt: enhancedPrompt,
            size: "1024x1024",
            quality: "standard",
            n: 1,
        });

        const imageUrl = response.data[0].url || '';
        console.log(`Avatar generated with prompt: "${prompt}"`);
        console.log(`Image URL: ${imageUrl}`);

        return imageUrl;
    } catch (error) {
        console.error("Error generating avatar:", error);
        throw error;
    }
}

/**
 * Enhance a basic prompt to create better-looking avatars
 * @param basePrompt The original character description
 * @returns An enhanced prompt for DALL-E
 */
function enhancePrompt(basePrompt: string): string {
    // If the prompt already seems detailed enough, use it directly
    if (basePrompt.length > 100) {
        return `${basePrompt}. High quality digital art style for a game avatar, vibrant lighting, character portrait.`;
    }

    // Otherwise enhance it with additional styling instructions
    return `${basePrompt}. High quality digital art style for a game avatar, detailed character portrait, vibrant colors, dynamic lighting, fantasy game art style, isolated on dark background.`;
}

export { generateAvatar };