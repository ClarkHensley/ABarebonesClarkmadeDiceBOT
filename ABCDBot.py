import discord
from discord.channel import DMChannel
from discord.ext import commands
import asyncio
import random

bot = discord.ext.commands.Bot(command_prefix = "!")

async def main():

    with open ("Token.txt", "r", encoding="utf-8") as tokenDoc:
        TOKEN = tokenDoc.readline()

    await bot.start(TOKEN)
    return

@bot.command()
async def quit(ctx):
    """quit() takes no arguments, returns nothing, and simply closes the bot, as well as ending relevant processes"""

    await ctx.reply("Logging Off!")
    await bot.close()
    loop.stop()
    return

def dice_roll(dice, id, modifier = None):
    """dice_roll() takes two arguments, dice and modifier. Dice is an integer, and  modifier is either None or an integer. It returns a dice roll result."""

    # Parse the integer value of dice and get the random roll, store that base value
    output = ""
    roll = random.randint(1, dice) # Generate the actual roll
    base = str(roll) 

    # Determine the modifier, and if it exists, add it to the output
    if modifier is None:
        output += base
    else:
        if modifier >= 0:
            output += (base + " + " + str(modifier))
        elif modifier <= -1:
            output += (base + " - " + str(modifier)[1:]) # strip the negative sign off of the modifier

        roll += modifier
        output += "\n" + str(roll)

    output += "\n"
    return output

@bot.command(name = "roll")
async def parse_roll(ctx, dice, modifier = None):
    """parse_roll() takes two arguments, a string dice and a string modifier, both with specifics formats, and return nothing. Parses the dice string, and gets the values for a dice roll with that modifier"""

    # If the modifier exists, it must be an integer
    if modifier is not None:
        try:
            modifier = modifier.strip()
            if modifier[0] == "+":
                modifier = int(modifier[1:])
            else:
                modifier = int(modifier)
        except ValueError:
            await ctx.reply("Modifier must be some integer. Please enter a valid modifier.")
            return

    # Assume a negative location to start
    locationOfD = -1

    # Find the d or D if relevant
    for i in range(len(dice)):
        if dice[i] in ["d", "D"]:
            locationOfD = i
            break

    try:
        final = int(dice[locationOfD + 1:])
        if final <= 0:
            raise ValueError
    except ValueError:
        await ctx.reply("Dice to be rolled must be a positive integer.")
        return

    output = ""

    # If there is no d or no number before the D, roll that number
    if dice[0:locationOfD] == "" or locationOfD == -1:
       output += dice_roll(int(dice[locationOfD + 1:]), ctx.author.id, modifier)

       await ctx.reply(output)

    # If there is a number in front of the D, roll that many Dice
    else: # If there is a value before the d or D (That is, !roll Xd20)

        try:
            numberOfRolls = int(dice[0:locationOfD])
            if numberOfRolls <= 0:
                raise ValueError
        except ValueError:
            await ctx.reply("Number of dice to be rolled must be a positive integer.")
            return

        for _ in range(numberOfRolls):
            output += dice_roll(int(dice[locationOfD + 1:]), ctx.author.id, modifier))
       
        await ctx.reply(output)

    return

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = "Dungeons and Dragons"))
    print("Bot is logged in as {0.user}".format(bot))
    print("All systems are online. Awaiting Orders.")
    return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())