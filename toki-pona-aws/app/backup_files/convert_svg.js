const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const svgDir = path.join(__dirname, 'img', 'sitelen_pona', 'svg');
const pngDir = path.join(__dirname, 'img', 'sitelen_pona', 'png');

// Create directories if they don't exist
if (!fs.existsSync(pngDir)) {
    fs.mkdirSync(pngDir, { recursive: true });
}

// Get all SVG files
const svgFiles = fs.readdirSync(svgDir).filter(file => file.endsWith('.svg'));

// Convert each SVG to PNG
svgFiles.forEach(svgFile => {
    const svgPath = path.join(svgDir, svgFile);
    const pngPath = path.join(pngDir, svgFile.replace('.svg', '.png'));
    
    sharp(svgPath)
        .resize(64, 64)
        .toFile(pngPath)
        .then(() => console.log(`✓ Converted ${svgFile} to PNG`))
        .catch(err => console.error(`✗ Error converting ${svgFile}:`, err));
});
