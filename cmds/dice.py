import discord
from discord.ext import commands
from core import Cog_Extension
import random


class Dice(Cog_Extension):
    def __init__(self, bot):
        # self.hostdice為莊家贏的次數, self.guessdice為玩家贏的次數
        # self.point為莊家擲到的點數, self.leopard為莊家擲到豹子(四個數字全同)會有的變數, 只有兩方都擲到豹子才會觸發
        # self.a為判斷是莊家擲還是換到玩家擲, 1是換莊家擲, 2是換玩家擲
        self.hostdice = []
        self.guestdice = []
        self.point = int()
        self.leopard = int()
        self.a = 1

    @commands.command()
    async def Playdice(self, ctx):
        a = 1
        L = []
        # 莊家或玩家獲勝次數等於兩次時即停止遊戲
        if len(self.hostdice) == 2 or len(self.guestdice) == 2:
            a = 2
            await ctx.send(f"遊戲結束,請按指示Lookresult")
        while a == 1:
            # 隨機生成一到六的四個數字
            num1 = random.randint(1, 6)
            L.append(num1)
            num2 = random.randint(1, 6)
            L.append(num2)
            num3 = random.randint(1, 6)
            L.append(num3)
            num4 = random.randint(1, 6)
            L.append(num4)
            # 排列後分別形成b1, b2, b3, b4
            L.sort()
            b1 = L[0]
            b2 = L[1]
            b3 = L[2]
            b4 = L[3]
            if self.a == 1:
                # 四個數相同為豹子
                if b1 == b2 == b3 == b4:
                    self.point = 13
                    self.leopard = b1
                    await ctx.send(f"莊家躑到{b1}{b2}{b3}{b4},為豹子")
                    await ctx.send(f"換你擲骰子")
                    # self.a變為2, 跳出迴圈
                    self.a = 2
                    L.clear()
                    break
                # 前兩相同和後兩相同, 點數(self.point)最大兩數相加
                elif b1 == b2 and b3 == b4:
                    self.point = b3 + b4
                    await ctx.send(f"莊家躑到{b1}{b2}{b3}{b4},點數為{self.point}")
                    await ctx.send(f"換你擲骰子")
                    self.a = 2
                    L.clear()
                    break
                # 前兩相同和後兩不同, 點數相同的兩數相加
                elif b1 == b2 and b3 != b4 and b1 != b3 and b1 != b4:
                    self.point = b1 + b2
                    await ctx.send(f"莊家躑到{b1}{b2}{b3}{b4},點數為{self.point}")
                    await ctx.send(f"換你擲骰子")
                    self.a = 2
                    L.clear()
                    break
                # 前兩不同和後兩相同, 點數相同的兩數相加
                elif b3 == b4 and b1 != b2 and b3 != b1 and b3 != b2:
                    self.point = b3 + b4
                    await ctx.send(f"莊家躑到{b1}{b2}{b3}{b4},點數為{self.point}")
                    await ctx.send(f"換你擲骰子")
                    self.a = 2
                    L.clear()
                    break
                # 第二三數字相同和其餘不同, 點數相同的兩數相加
                elif b2 == b3 and b1 != b4 and b2 != b1 and b2 != b4:
                    self.point = b2 + b3
                    await ctx.send(f"莊家躑到{b1}{b2}{b3}{b4},點數為{self.point}")
                    await ctx.send(f"換你擲骰子")
                    self.a = 2
                    L.clear()
                    break
                # 其餘不合規則的骰子組合則重擲
                else:
                    a = 1
            elif self.a == 2:
                await ctx.send(f"換你擲骰子了,請先按指令Throwdice")
                break

    @commands.command()
    async def Throwdice(self, ctx):
        a = 1
        L = []
        # 莊家或玩家獲勝次數等於兩次時即停止遊戲
        if len(self.hostdice) == 2 or len(self.guestdice) == 2:
            a = 2
            await ctx.send(f"遊戲結束,請按指示Lookresult")
        while a == 1:
            # 隨機生成一到六的四個數字
            num1 = random.randint(1, 6)
            L.append(num1)
            num2 = random.randint(1, 6)
            L.append(num2)
            num3 = random.randint(1, 6)
            L.append(num3)
            num4 = random.randint(1, 6)
            L.append(num4)
            L.sort()
            b1 = L[0]
            b2 = L[1]
            b3 = L[2]
            b4 = L[3]
            if self.a == 2:
                # 玩家擲豹子(四個數字全同)
                if b1 == b2 == b3 == b4:
                    self.a = 1
                    point = b1
                    await ctx.send(f"你躑到{b1}{b2}{b3}{b4},為豹子")
                    # 如果莊家也擲到豹子
                    if self.point == 13:
                        # 比較豹子點數大小
                        if point > self.leopard:
                            self.guestdice.append("win")
                            await ctx.send(f"你的豹子點數大於莊家豹子點數,取下一勝")
                        elif point < self.point:
                            self.hostdice.append("win")
                            await ctx.send(f"你的豹子點數小於莊家豹子點數,拿下一敗")
                        else:
                            await ctx.send(f"你的豹子點數等於莊家豹子點數,平手")
                    # 如果莊家沒擲到豹子, 玩家直接一勝
                    else:
                        self.guestdice.append("win")
                        await ctx.send(f"你躑到無敵星星(豹子),取下一勝")
                    L.clear()
                    break
                # 前兩相同和後兩相同, 點數(self.point)最大兩數相加
                elif b1 == b2 and b3 == b4:
                    self.a = 1
                    point = b3 + b4
                    await ctx.send(f"你躑到{b1}{b2}{b3}{b4},點數為{point}")
                    # 莊家擲到豹子, 但玩家沒擲到
                    if self.point == 13:
                        self.hostdice.append("win")
                        await ctx.send(f"莊家躑到無敵星星(豹子),拿下一敗")
                        L.clear()
                        break
                    # 比較點數大小
                    if point > self.point:
                        self.guestdice.append("win")
                        await ctx.send(f"你的點數{point}大於莊家點數{self.point},取下一勝")
                    elif point < self.point:
                        self.hostdice.append("win")
                        await ctx.send(f"你的點數{point}小於莊家點數{self.point},拿下一敗")
                    else:
                        await ctx.send(f"你的點數{point}等於莊家點數{self.point},平手")
                    L.clear()
                    break
                # 前兩相同和後兩不同, 點數相同的兩數相加
                elif b1 == b2 and b3 != b4 and b1 != b3 and b1 != b4:
                    self.a = 1
                    point = b1 + b2
                    await ctx.send(f"你躑到{b1}{b2}{b3}{b4},點數為{b1+b2}")
                    # 莊家擲到豹子, 但玩家沒擲到
                    if self.point == 13:
                        self.hostdice.append("win")
                        await ctx.send(f"莊家躑到無敵星星(豹子),拿下一敗")
                        L.clear()
                        break
                    # 比較點數大小
                    if point > self.point:
                        self.guestdice.append("win")
                        await ctx.send(f"你的點數{point}大於莊家點數{self.point},取下一勝")
                    elif point < self.point:
                        self.hostdice.append("win")
                        await ctx.send(f"你的點數{point}小於莊家點數{self.point},拿下一敗")
                    else:
                        await ctx.send(f"你的點數{point}等於莊家點數{self.point},平手")
                    L.clear()
                    break
                # 前兩不同和後兩相同, 點數相同的兩數相加
                elif b3 == b4 and b1 != b2 and b3 != b1 and b3 != b2:
                    self.a = 1
                    point = b3 + b4
                    await ctx.send(f"你躑到{b1}{b2}{b3}{b4},點數為{b3+b4}")
                    # 莊家擲到豹子, 但玩家沒擲到
                    if self.point == 13:
                        self.hostdice.append("win")
                        await ctx.send(f"莊家躑到無敵星星(豹子),拿下一敗")
                        L.clear()
                        break
                    # 比較點數大小
                    if point > self.point:
                        self.guestdice.append("win")
                        await ctx.send(f"你的點數{point}大於莊家點數{self.point},取下一勝")
                    elif point < self.point:
                        self.hostdice.append("win")
                        await ctx.send(f"你的點數{point}小於莊家點數{self.point},拿下一敗")
                    else:
                        await ctx.send(f"你的點數{point}等於莊家點數{self.point},平手")
                    L.clear()
                    break
                # 第二三數字相同和其餘不同, 點數相同的兩數相加
                elif b2 == b3 and b1 != b4 and b2 != b1 and b2 != b4:
                    self.a = 1
                    point = b2 + b3
                    await ctx.send(f"你躑到{b1}{b2}{b3}{b4},點數為{b2+b3}")
                    # 莊家擲到豹子, 但玩家沒擲到
                    if self.point == 13:
                        self.hostdice.append("win")
                        await ctx.send(f"莊家躑到無敵星星(豹子),拿下一敗")
                        L.clear()
                        break
                    # 比較點數大小
                    if point > self.point:
                        self.guestdice.append("win")
                        await ctx.send(f"你的點數{point}大於莊家點數{self.point},取下一勝")
                    elif point < self.point:
                        self.hostdice.append("win")
                        await ctx.send(f"你的點數{point}小於莊家點數{self.point},拿下一敗")
                    else:
                        await ctx.send(f"你的點數{point}等於莊家點數{self.point},平手")
                    L.clear()
                    break
                # 其餘不合規則的骰子組合則重擲
                else:
                    a = 1
            elif self.a == 1:
                await ctx.send(f"換莊家擲骰子了,請先按指令Playdice")
                break

    @commands.command()
    async def Lookresult(self, ctx):
        # 獲勝次數相同即平手
        if len(self.guestdice) == 2 and len(self.hostdice) == 2:
            await ctx.send(f"你跟莊家2比2平手")
            self.hostdice.clear()
            self.guestdice.clear()
        # 莊家獲勝次數為2贏
        elif len(self.hostdice) == 2:
            await ctx.send(f"莊家以{len(self.hostdice)}比{len(self.guestdice)}贏了你")
            self.hostdice.clear()
            self.guestdice.clear()
        # 玩家獲勝次數為2贏
        elif len(self.guestdice) == 2:
            await ctx.send(f"你以{len(self.guestdice)}比{len(self.hostdice)}贏了莊家")
            self.hostdice.clear()
            self.guestdice.clear()
        # 一次獲勝次數都沒有 ,要先按Playdice
        elif self.a == 1:
            await ctx.send(f"請先開啟指令Playdice")
        else:
            await ctx.send(f"遊戲未結束,請先按指令Throwdice")


async def setup(bot):
    await bot.add_cog(Dice(bot))
