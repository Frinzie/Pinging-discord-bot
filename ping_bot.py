import sys
import discord


class PingBot(discord.Client):
    ping_roles = {}

    def __init__(self, ping_role, trigger_role, channel_name):
        super(PingBot, self).__init__()
        self._ping_role = ping_role
        self._trigger_role = trigger_role
        self._channel_name = channel_name

    def has_trigger_mention(self, message):
        if discord.utils.find(lambda r: r.name == self._trigger_role,
                              message.role_mentions):
            return True

        for user in message.mentions:
            if discord.utils.find(lambda r: r.name == self._trigger_role,
                                  user.roles):
                return True
        return False

    async def on_ready(self):
        print("What is my purpose other than to ping the illiterate?")
        async for guild in self.fetch_guilds(limit=None):
            roles = await guild.fetch_roles()
            ping_role_id = None
            trigger_role_id = None
            for role in roles:
                if role.name == self._ping_role:
                    ping_role_id = role.id
                elif role.name == self._trigger_role:
                    trigger_role_id = role.id

            if ping_role_id and trigger_role_id:
                PingBot.ping_roles[guild.id] = (ping_role_id, trigger_role_id)
                print(f"Added ping for role ID: {ping_role_id} on trigger:"
                      + f"{trigger_role_id} on guild: {guild.id}")

    async def on_message(self, message):
        has_mention = self.has_trigger_mention(message)
        if (not message.author.bot and has_mention
                and message.guild.id in PingBot.ping_roles):
            channel = next(chan for chan in message.guild.text_channels
                           if chan.name == self._channel_name)
            role_to_tag = PingBot.ping_roles[message.guild.id][0]
            await channel.send(f'<@&{role_to_tag}>')


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Invalid arguments")
        print("Please call ping_bot with <token> <role name>"
              + "<trigger role name> <channel name>")
        exit(0)

    pb = PingBot(sys.argv[2], sys.argv[3], sys.argv[4])
    pb.run(sys.argv[1])
