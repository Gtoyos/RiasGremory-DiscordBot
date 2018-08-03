from .akinator import Akinator

def setup(bot):
    bot.add_cog(Akinator(bot))
