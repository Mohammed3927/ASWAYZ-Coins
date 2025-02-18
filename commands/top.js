const { getTopUsers } = require('../utils/coinManager');

module.exports = {
    name: 'top',
    description: 'Display the top 5 users with the most coins',
    execute(message) {
        const topUsers = getTopUsers();
        const leaderboard = topUsers.map(([id, coins]) => `<@${id}>: ${coins} coins`).join('\n');

        message.channel.send(`🏆 **Top 5 Users:**\n${leaderboard}`);
    }
};
