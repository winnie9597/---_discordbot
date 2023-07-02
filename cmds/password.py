import discord
from discord.ext import commands
from core import Cog_Extension
import random


class Password(Cog_Extension):
    def __init__(self, bot):
        # self.password為目前猜到的範圍, self.a裡有曾經猜過錯誤答案和正確的答案, self.num為最終的答案
        self.password = [int(1), int(100)]
        self.a = []
        self.num = int()

    @commands.command()
    async def playpassword(self, ctx):
        # 隨機生成一個1-100的數字
        self.num = random.randint(1, 100)
        self.password.append(self.num)
        self.a.append(self.num)
        await ctx.send(f"請輸入一個1-100的數字/")

    @commands.command()
    async def guesspassword(self, ctx, guessnum=int()):
        if self.a == []:
            await ctx.send(f"請先輸入playpassword指令/")
        # 數字不再目前猜的範圍內
        elif guessnum >= max(self.password) or guessnum <= min(self.password):
            await ctx.send(f"請輸入一個從{min(self.password)}到{max(self.password)}的數字/")
        else:
            # 猜的次數小於五次時
            if len(self.a) < 6:
                if self.num == guessnum:
                    self.password = [int(1), int(100)]
                    self.a.clear()
                    await ctx.send(f"猜對了🎊/")
                # 答案大於猜的值時, 請玩家在猜一個由猜的值到目前self.password(目前猜到的範圍)裡最大的值
                elif self.num > guessnum:
                    self.a.append(guessnum)
                    self.password.append(guessnum)
                    self.password.remove(min(self.password))
                    await ctx.send(f"請再猜一個由{guessnum}到{max(self.password)}的數字/")
                # 答案小於猜的值時, 請玩家在猜一個由目前self.password裡最小的值到猜的值
                elif self.num < guessnum:
                    self.a.append(guessnum)
                    self.password.append(guessnum)
                    self.password.remove(max(self.password))
                    await ctx.send(f"請再猜一個由{min(self.password)}到{guessnum}的數字/")
            # 為猜到第五次時(猜最後一次)
            elif len(self.a) == 6:
                if self.num == guessnum:
                    self.a.clear()
                    self.password = [int(1), int(100)]
                    await ctx.send(f"猜對了🎊/")
                else:
                    self.password = [int(1), int(100)]
                    await ctx.send(f"沒猜對，答案是{self.num}/")
                    self.a.clear()

    @commands.command()
    async def replaypassword(self, ctx):
        # 所有東西恢復初始化
        self.password = [int(1), int(100)]
        self.a = []
        self.num = int()


async def setup(bot):
    await bot.add_cog(Password(bot))
