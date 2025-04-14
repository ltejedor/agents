import { ImageSource, Loader } from "excalibur";

export const FALLBACK_AVATARS = {
  default: '/images/default.png'
}

// It is convenient to put your resources in one place
export const Resources = {
  Sword: new ImageSource("./images/sword.png"), // Vite public/ directory serves the root images
  Background: new ImageSource("./images/background.png"),
  HealthBar: new ImageSource("./images/health-bar.png"),
  GameOver: new ImageSource("./images/game-over.png"),

  // Fallback avatars - ensure these are always loaded
  PlayerAvatar: new ImageSource(FALLBACK_AVATARS.default),
  EnemyAvatar1: new ImageSource(FALLBACK_AVATARS.default),
  EnemyAvatar2: new ImageSource(FALLBACK_AVATARS.default)
} as const; // the 'as const' is a neat typescript trick to get strong typing on your resources. 
// So when you type Resources.Sword -> ImageSource

export const loader = new Loader();
for (const res of Object.values(Resources)) {
  loader.addResource(res);
  // Preload all resources to avoid flickering
  res.load().catch(err => console.error('Failed to load resource:', err));
}
loader.suppressPlayButton = true;