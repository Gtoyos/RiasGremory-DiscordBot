from .status import Guildcount

def setup(bot):
    bot.add_cog(Guildcount(bot))
