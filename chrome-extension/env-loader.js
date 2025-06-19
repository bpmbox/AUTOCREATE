const fs = require('fs');
const path = require('path');

// Load .env file and convert to JSON
const envPath = path.resolve(__dirname, '../.env');
const envContent = fs.readFileSync(envPath, 'utf-8');

const envJson = {};

envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
        envJson[key.trim()] = value.trim();
    }
});

// Write JSON to a file
const outputPath = path.resolve(__dirname, 'env.json');
fs.writeFileSync(outputPath, JSON.stringify(envJson, null, 2));

console.log('✅ .env file converted to env.json');
