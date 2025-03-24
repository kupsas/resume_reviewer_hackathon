import sharp from 'sharp';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function convertSvgToPng() {
  const inputPath = join(__dirname, '../public/og-image.svg');
  const outputPath = join(__dirname, '../public/og-image.png');
  const faviconPath = join(__dirname, '../public/favicon.svg');
  const faviconPngPath = join(__dirname, '../public/favicon.png');
  const appleTouchPath = join(__dirname, '../public/apple-touch-icon.png');

  try {
    // Convert OG image
    await sharp(inputPath)
      .resize(1200, 630)
      .png()
      .toFile(outputPath);
    console.log('✅ Generated og-image.png');

    // Convert favicon to PNG
    await sharp(faviconPath)
      .resize(32, 32)
      .png()
      .toFile(faviconPngPath);
    console.log('✅ Generated favicon.png');

    // Generate Apple Touch Icon
    await sharp(faviconPath)
      .resize(180, 180)
      .png()
      .toFile(appleTouchPath);
    console.log('✅ Generated apple-touch-icon.png');

  } catch (error) {
    console.error('Error generating images:', error);
    process.exit(1);
  }
}

convertSvgToPng(); 