const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../data/coins.json');
let coinsData = {};

// Load existing coin data
if (fs.existsSync(dataPath)) {
    coinsData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
}

function addCoins(userId, amount) {
    coinsData[userId] = (coinsData[userId] || 0) + amount;
}

function removeCoins(userId, amount) {
    coinsData[userId] = Math.max((coinsData[userId] || 0) - amount, 0);
}

function resetCoins(userId) {
    coinsData[userId] = 0;
}

function getCoins(userId) {
    return coinsData[userId] || 0;
}

function getTopUsers() {
    return Object.entries(coinsData)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5);
}

function saveCoinsData() {
    fs.writeFileSync(dataPath, JSON.stringify(coinsData, null, 2));
}

module.exports = { addCoins, removeCoins, resetCoins, getCoins, getTopUsers, saveCoinsData };
