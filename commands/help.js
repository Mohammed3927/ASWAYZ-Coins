module.exports = {
    name: 'help',
    description: 'List all available commands',
    execute(message) {
        message.channel.send(`Available commands:
        - !coins [@user]
        - !add @user amount
        - !remove @user amount
        - !reset @user
        - !top
        - !help`);
    }
};
