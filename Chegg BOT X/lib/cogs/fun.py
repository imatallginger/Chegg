import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from lib.bot.cheggapi import getLink
from lib.bot.firebaseauth import addUser, getUser, getUserMail, updateMail, deleteUser, addQuestion, updateQuestion, \
    getQuestion, deleteQuestion, fetchAllUsers
from lib.bot.saveMail import findQuestionId
from lib.bot.log import Log

OWNERS = [623772185315639302, 618038532665114624]
ALLOWED = [623772185315639302, 618038532665114624]
MODS = []


class Fun(Cog):
    def __init__(self, bot):
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.bot = bot
        self.log = Log(r"C:\Users\woosal\Desktop\Chegg BOT X", "chegg.log")

    @command(name="commands", aliases=["info", "about"])
    async def help(self, ctx):
        self.log.command(f"{ctx.message.author.id}:commands")
        embed = discord.Embed(title="Chegg BOT", url="https://cheggbot.woosal.com/",
                              description="Unblur the answers of the Chegg questions, and get receive them.",
                              color=0xfbc041)
        embed.set_author(name="woosal", url="https://woosal.com/",
                         icon_url="https://woosal.com/1337/woosal1337-AxcOjfpPCjYo2aMU9s05XvXnLk3SGXC67oJq7CZ6d0TCTRPzMKZ8D9q5g7W4fIdWwmwRVQHdYvffkr16RsEdD0Y1Y.png")
        embed.set_thumbnail(url="https://woosal.com/1337/cheggwpfullblacklogoleftnobg.png")
        embed.add_field(name="Add Your Email", value="+addmail your@mail.com", inline=False)
        embed.add_field(name="Search For The Question", value="+chegg URL", inline=False)
        embed.add_field(name="Commands", value="+commands", inline=False)
        embed.add_field(name="Your Current Mail Info", value="+mymail", inline=False)
        embed.add_field(name="Update Your Mail to New Mail", value="+updatemail newmail@mail.com", inline=False)
        embed.add_field(name="Delete Your Mail Completely", value="+deletemail", inline=False)
        embed.add_field(name="Want a new feature?", value="chegg@woosal.com", inline=False)
        embed.set_footer(text="Star the project on GitHub: https://github.com/woosal1337/Chegg-Discord-BOT")
        await ctx.send(embed=embed)
        return True

    @command(name="addmail", aliases=["adduser"])
    async def add_mail(self, ctx, mail):

            await ctx.message.delete()
            #############################################
            newUser = [str(ctx.message.author.id), mail]
            print("New User: ", newUser)
            newUserRes = getUser(newUser[0])
            # User already registered
            if newUserRes != None:
                newUserResMail = getUserMail(newUser[0])
                print("Such user already registered with the mail of {0}".format(newUserResMail))
                await ctx.author.send("Such user already registered with the mail of {0}".format(newUserResMail))
                return True

            # User is registering for the first time
            else:
                print(addUser(newUser[0], newUser[1]))
                print("Mail has been added successfully!")
                await ctx.author.send("Your mail has been successfully added!")
                print("\n")

                return True

    @command(name="updatemail", aliases=["newmail", "mainmail", "changemail"])
    async def update_mail(self, ctx, mail):
        await ctx.message.delete()

        userid = str(ctx.message.author.id)

        if getUser(userid) != None:
            print(updateMail(userid, mail))
            await ctx.author.send("Your email has been updated to {0}".format(mail))
            return True

        else:
            await ctx.author.send(
                "This user has not registered any mails yet, please use ```+addmail yourmail@mail.com``` to create your account!")
            return True

    @command(name="mymail", aliases=["currentmail", "mycurrentmail", "savedmail", "mysavedmail", "mail"])
    async def current_mail(self, ctx):
        # self.log.command(f"{ctx.message.author.id}:mymail:{getUser(ctx.message.author.id)['mail']}")
        await ctx.message.delete()

        userid = str(ctx.message.author.id)

        if getUser(userid) != None:
            await ctx.author.send(
                "Your current saved mail to your Discord account is ```{0}``` You can update it anytime you want by using ```+updatemail newmail@mail.com```".format(
                    getUserMail(userid)))
            return True
        else:
            await ctx.author.send(
                "This user has not registered any mails yet, please use ```+addmail yourmail@mail.com``` to create your account")
            return True


    @command(name="deletemail", aliases=["purgemail", "delete", "removemail", "removeme", "purgeme", 'deleteuser'])
    async def delete_user(self, ctx):
        await ctx.message.delete()
        print("Delete user request was received.")
        userid = str(ctx.message.author.id)

        if getUser(userid) != None:
            print(deleteUser(userid))
            await ctx.author.send("Dear {0}, your mail was removed!".format(ctx.message.author.name))
            print("{0}'s mail was removed!".format(ctx.message.author))
            return True

        else:
            await ctx.author.send(
                    "Dear {0}, your have not even registered yet, please consider registering at first by using the command: ```+addmail yourmail@mail.com```".format(
                        ctx.message.author.name))
            print("{0} have not registered yet".format(ctx.message.id))
            return True


    @command(name="chegg", aliases=["check", "cheggapi", "search", "c"])
    async def chegg_answer(self, ctx, link):
        await ctx.message.delete()

        userid = str(ctx.message.author.id)
        newUserRes = getUser(userid)

        if newUserRes != None:
            if "chegg.com" in link:
                newUserResMail = newUserRes["mail"]

                await ctx.author.send("I am searching for the answer, please give me a few seconds!")
                await ctx.author.send(
                    "Dear {1}, I am sending the answer to {0}, you will get it in a few minutes!".format(
                        newUserResMail, ctx.message.author.name))

            print("User: {0}; Link:{1}".format(ctx.message.author, link))
            print(getLink(newUserResMail, str(link)))

            return True


    @command(name="cheggdm", aliases=["dmchegg", "pmchegg", "cheggpm"])
    async def chegg_send_dm(self, ctx, *links):
        await ctx.message.delete()
        if len(links) == 1:
            link = links[0]
            self.log.command(f"{ctx.message.author.id}:cheggdm:{link}")

            userid = ctx.message.author.id
            if len(getQuestion(userid)) == 0:
                if ctx.message.author.id in ALLOWED:
                    if "chegg.com" in link:
                        questionid = findQuestionId(link)
                        print(addQuestion(userid, questionid))
                        print(getLink("chegg1337@gmail.com", link))
                        self.log.info(f"{ctx.message.author.id}:question_added:{questionid}")
                        try:
                            await ctx.author.send("You will get your answers in a few minutes!")
                        except:
                            await ctx.send("You have to allow direct messages to get answers!")

                else:
                    try:
                        await ctx.author.send("You do not have permissions to do this action!")
                    except:
                        pass
            else:
                try:
                    await ctx.author.send("Please, wait for your previous request to be sent!")
                    # await ctx.author.send("Please, wait for your previous request to be sent!")
                except:
                    pass
        else:
            try:
                await ctx.author.send(
                    "Dear {0}, Please use only official Chegg links, this link is not recognized!".format(
                        ctx.message.author.name))
            except:
                pass


    @command(name="deletequestion")
    async def delete_question(self, ctx):
        self.log.command(f"{ctx.message.author.id}:deletequestion:{getQuestion(ctx.message.author.id)}")
        await ctx.message.delete()
        userid = ctx.message.author.id
        deleteQuestion(str(userid))
        try:
            await ctx.author.send(
                "Dear {0}, your question request deleted successfully".format(ctx.message.author.name))
        except:
            await ctx.send(
                "Dear {0}, your question request deleted successfully".format(ctx.message.author.name))


    @command(name="usersdb", aliases=["totalusers", "currentusers"])
    async def users_db(self, ctx):
        await ctx.message.delete()
        if ctx.message.author.id in OWNERS:
            for i in OWNERS:
                user = await self.bot.fetch_user(int(i))
                try:
                    await user.send(
                        "There are {0} users saved in the database using the bot!".format(len(fetchAllUsers()),
                                                                                          len(self.bot.guilds)))
                except:
                    pass
        else:
            await ctx.send("You are not the owner of the bot! Only owners can access this command!")
            self.log.alert(f"{ctx.message.author.id}:usersdb_command")


    @command(name="usersdc", aliases=["usersdiscord"])
    async def users_dc(self, ctx):
        await ctx.message.delete()
        if ctx.message.author.id in OWNERS:
            for i in OWNERS:
                user = await self.bot.fetch_user(int(i))
                userCount = 0
                for j in self.bot.guilds:
                    userCount += j.member_count
                try:
                    await user.send(
                        "There are {0} users in {1} servers using the bot!".format(userCount, len(self.bot.guilds)))
                except:
                    pass
        else:
            await ctx.send("You are not the owner of the bot! Only owners can access this command!")
            self.log.alert(f"{ctx.message.author.id}:usersdc_command")


    @command(name="servers", aliases=["server"])
    async def total_servers(self, ctx):
        await ctx.message.delete()
        if ctx.message.author.id in OWNERS:
            for i in OWNERS:
                user = await self.bot.fetch_user(int(i))
                try:
                    await user.send("BOT is currently in {0} servers!".format(len(self.bot.guilds)))
                except:
                    pass
        else:
            await ctx.send("Dear {0}, you are not the owner of the bot! Only owners can access this command!".format(
                ctx.message.author.name))
            self.log.alert(f"{ctx.message.author.id}:servers_command")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
