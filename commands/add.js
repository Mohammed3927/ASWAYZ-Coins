const { addCoins, saveCoinsData } = require('../utils/coinManager');

module.exports = {
    name: 'add',
    description: 'Add coins to a user',
    execute(message, args) {
        const user = message.mentions.users.first();
        const amount = parseInt(args[1]);

        if (!user || isNaN(amount)) return message.reply('Usage: !add @user amount');

        addCoins(user.id, amount);
        saveCoinsData();
        message.channel.send(`Added ${amount} coins to ${user.username}.`);
    }
};
