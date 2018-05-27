from .reaction import Reaction
def setup(bot):
    bot.add_cog(Reaction(bot))
