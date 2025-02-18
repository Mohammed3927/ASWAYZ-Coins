const { getCoins } = require('../utils/coinManager');

module.exports = {
    name: 'coins',
    description: 'Check user coin balance',
    execute(message, args) {
        const user = args.length ? message.mentions.users.first() : message.author;
        if (!user) return message.reply('Please mention a user.');

        const userCoins = getCoins(user.id);
        message.channel.send(`${user.username} has ${userCoins} coins.`);
    }
};
