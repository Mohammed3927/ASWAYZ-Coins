const { resetCoins, saveCoinsData } = require('../utils/coinManager');

module.exports = {
    name: 'reset',
    description: 'Reset coins for a user',
    execute(message, args) {
        const user = message.mentions.users.first();
        if (!user) return message.reply('Usage: !reset @user');

        resetCoins(user.id);
        saveCoinsData();
        message.channel.send(`Reset coins for ${user.username}.`);
    }
};
