import discord
from discord.ext import commands
import json
from core import Cog_Extension


class TodoList(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.todo = []

    # Add todolist
    # item 是要增加的待辨事項
    @commands.command()
    async def AddTodoList(self, ctx, item):
        if item in self.todo:
            await ctx.send("此待辨事項已存在/")
        else:
            self.todo.append(item)
            await ctx.send("此待辨事項已儲存/")

    # Remove todolist
    # item 是要移除的待辨事項
    @commands.command()
    async def RemoveTodoList(self, ctx, item):
        if item in self.todo:
            self.todo.remove(item)
            await ctx.send("此待辨事項已刪除")
        else:
            await ctx.send("此待辨事項不存在")

    # Sort todolist
    @commands.command()
    async def SortTodoList(self, ctx):
        if self.todo != []:
            self.todo.sort()
            for item in self.todo:
                await ctx.send(item)
        else:
            pass

    # Clear todolist
    @commands.command()
    async def ClearTodoList(self, ctx):
        if self.todo != []:
            self.todo.clear()
            await ctx.send("沒有任何待辨事項")
        else:
            pass


async def setup(bot):
    await bot.add_cog(TodoList(bot))
