import discord
from discord.ext import commands
import json
from core import Cog_Extension
import urllib
import random
import requests


class Wordle(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        # self.sol為最終的答案, self.a為猜過的答案, self.wordle裡為五個字的單字
        self.sol = 0
        self.a = []
        # 要擷取資料的網址
        url = "https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt"
        # 取網頁裡的資料
        words = requests.get(url)
        self.wordle = []
        a = 0
        while a <= 14854:  # 14854為五個字單字的數目, 算法為(words.text+1)/6
            # 因為words.text是string, 所以以每五個字母為一個單字
            word = (
                words.text[0 + 6 * a]
                + words.text[1 + 6 * a]
                + words.text[2 + 6 * a]
                + words.text[3 + 6 * a]
                + words.text[4 + 6 * a]
            )
            a += 1
            self.wordle.append(word)
        """
        TODO 
        要在init function 中載入單字庫

        Hint:
        1. 好像有import urllib
        2. data.json中有貼上url了
        """

    @commands.command()
    async def Play(self, ctx):
        # 隨機在self.wordle選一個單字
        self.sol = random.choice(self.wordle)

    @commands.command()
    async def Ask(self, ctx, ans):
        # 初始答案為0, 沒按Play的時候
        if self.sol == 0:
            await ctx.send(f"請先輸入Play指令")
        # 當輸入答案的長度不等於5
        elif len(ans) != 5:
            await ctx.send(f"請輸入一個五個字母的單字")
        # 當答案不在self.wordle裡
        elif ans not in self.wordle:
            await ctx.send(f"這好像不是個單字")
        else:
            # 當猜到五次以內時
            if len(self.a) < 5:
                # 當答案猜對的時候
                if self.sol == ans:
                    self.a.clear
                    await ctx.send(f"恭喜答對!!!")
                else:
                    self.a.append(ans)
                    # 猜的第一個字母與答案的第一個字母相同時, 為粗體
                    if self.sol[0] == ans[0]:
                        letter1 = f"**{ans[0]}**"
                    # 猜的第一個字母有在答案字母裡時, 為藍字
                    elif ans[0] in self.sol:
                        letter1 = f"```fix\n{ans[0]}\n```"
                    else:
                        letter1 = "●"
                    # 依此類推
                    if self.sol[1] == ans[1]:
                        letter2 = f"**{ans[1]}**"
                    elif ans[1] in self.sol:
                        letter2 = f"```fix\n{ans[1]}\n```"
                    else:
                        letter2 = "●"
                    if self.sol[2] == ans[2]:
                        letter3 = f"**{ans[2]}**"
                    elif ans[2] in self.sol:
                        letter3 = f"```fix\n{ans[2]}\n```"
                    else:
                        letter3 = "●"
                    if self.sol[3] == ans[3]:
                        letter4 = f"**{ans[3]}**"
                    elif ans[3] in self.sol:
                        letter4 = f"```fix\n{ans[3]}\n```"
                    else:
                        letter4 = "●"
                    if self.sol[4] == ans[4]:
                        letter5 = f"**{ans[4]}**"
                    elif ans[4] in self.sol:
                        letter5 = f"```fix\n{ans[4]}\n```"
                    else:
                        letter5 = "●"
                    await ctx.send(
                        f"{letter1}\n{letter2}\n{letter3}\n{letter4}\n{letter5}"
                    )
            # 猜到最後一次時
            elif len(self.a) == 5:
                if self.sol == ans:
                    self.a.clear()
                    await ctx.send(f"恭喜答對!!!")
                else:
                    self.a.clear()
                    await ctx.send(f"真可惜, 答案是{self.sol}")

        """
        ans 是使用者傳入的猜測答案

        TODO
        1. 沒有play直接ask : 請先輸入 Play 指令
        2. 不是5個字的單字 : 請輸入5個字母的單字
        3. 不是單字的英文組合(不在單字庫中) : 這好像不是個單字
        4. 答對 : 恭喜答對!!!
        5. 猜太多次了 : 真可惜, 答案是{answer}
        """


async def setup(bot):
    await bot.add_cog(Wordle(bot))
