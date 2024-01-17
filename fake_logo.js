const fs = require('fs');
const sharp = require('sharp');
const path = require('path');
const csv = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const logoFolder = 'output';
const outputFolder = 'genLogoOutput';
const scaleFactor = 0.8;
const rotationAngle = 30;

const data = [];

// Function to rotate an image
function rotateImage(inputPath, outputPath) {
  const image = sharp(inputPath);
  return image.rotate(rotationAngle).toFile(outputPath);
}

// Function to scale an image
function scaleImage(inputPath, outputPath) {
  const image = sharp(inputPath);
  return image.resize({ width: Math.round(image.options.width * scaleFactor) }).toFile(outputPath);
}

// Process logo images
fs.readdirSync(logoFolder, { withFileTypes: true }).forEach(file => {
  if (file.isFile() && (file.name.endsWith('.jpg') || file.name.endsWith('.png'))) {
    const logoPath = path.join(logoFolder, file.name);
    const brandName = path.basename(path.dirname(logoPath));

    const brandFolder = path.join(outputFolder, brandName);
    if (!fs.existsSync(brandFolder)) {
      fs.mkdirSync(brandFolder, { recursive: true });
    }

    // Rotate image
    rotateImage(logoPath, path.join(brandFolder, file.name)).then(() => {
      data.push({ 'Filename': path.join(brandFolder, file.name), 'Brand Name': brandName, 'Label': 'Fake' });
    });

    // Scale image
    scaleImage(logoPath, path.join(brandFolder, `scal_${file.name}`)).then(() => {
      data.push({ 'Filename': path.join(brandFolder, `scal_${file.name}`), 'Brand Name': brandName, 'Label': 'Fake' });
    });
  }
});

// Read existing CSV file
const fileMap = [];
fs.createReadStream('file_map.csv')
  .pipe(csv())
  .on('data', (row) => {
    fileMap.push(row);
  })
  .on('end', () => {
    // Combine existing data with new data
    const newData = [...fileMap, ...data];

    // Write to new CSV file
    const csvWriter = createCsvWriter({
      path: 'file_mapping.csv',
      header: [
        { id: 'Filename', title: 'Filename' },
        { id: 'Brand Name', title: 'Brand Name' },
        { id: 'Label', title: 'Label' }
      ]
    });

    csvWriter.writeRecords(newData)
      .then(() => console.log('Done'))
      .catch(err => console.error(err));
  });
