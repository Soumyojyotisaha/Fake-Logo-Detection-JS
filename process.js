const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const logoFolder = 'logos';
const targetSize = { width: 70, height: 70 };
const outputFolder = 'output';

const data = [];

function processLogo(logoPath, brandName) {
    return sharp(logoPath)
        .resize(targetSize.width, targetSize.height)
        .toFile(path.join(outputFolder, brandName, path.basename(logoPath)))
        .then(() => {
            data.push({
                Filename: path.join(outputFolder, brandName, path.basename(logoPath)),
                'Brand Name': brandName,
                Label: 'Genuine',
            });
        });
}

function processLogos() {
    fs.readdirSync(logoFolder, { withFileTypes: true }).forEach((entry) => {
        if (entry.isDirectory()) {
            const brandName = entry.name;
            const brandPath = path.join(logoFolder, brandName);

            fs.readdirSync(brandPath).forEach((filename) => {
                if (filename.endsWith('.jpg') || filename.endsWith('.png')) {
                    const logoPath = path.join(brandPath, filename);
                    processLogo(logoPath, brandName);
                }
            });
        }
    });
}

function saveToFileMap() {
    const csvData = data.map((entry) => `${entry.Filename},${entry['Brand Name']},${entry.Label}`).join('\n');
    fs.writeFileSync('file_map.csv', csvData);
}

// Start the processing
processLogos();
saveToFileMap();

console.log('Done');
