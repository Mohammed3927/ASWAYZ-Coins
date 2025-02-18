const { removeCoins, saveCoinsData } = require('../utils/coinManager');

module.exports = {
    name: 'remove',
    description: 'Remove coins from a user',
    execute(message, args) {
        const user = message.mentions.users.first();
        const amount = parseInt(args[1]);

        if (!user || isNaN(amount)) return message.reply('Usage: !remove @user amount');

        removeCoins(user.id, amount);
        saveCoinsData();
        message.channel.send(`Removed ${amount} coins from ${user.username}.`);
    }
};
