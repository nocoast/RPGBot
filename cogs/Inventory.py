#!/usr/bin/env python3
# Copyright (c) 2016-2017, henry232323
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from discord.ext import commands
import discord
from .utils.data import Converter


class Inventory(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=['i', 'inv'], no_pm=True)
    async def inventory(self, ctx, *, member: discord.Member=None):
        """Check your or another users inventory."""
        if member is None:
            member = ctx.message.author

        inv = (await self.bot.di.get_inventory(member))
        if not inv:
            await ctx.send("This inventory is empty!")
            return
        fmap = map(lambda x, y: f"{x} x{y}", inv)
        fmt = "\n".join(fmap)
        embed = discord.Embed(description=fmt)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @inventory.command(no_pm=True, aliases=["take"])
    async def takeitem(self, ctx, item: str, num: int, *members: Converter):
        """Remove an item from a person's inventory"""
        if "everyone" in members:
            members = ctx.guild.members

        num = abs(num)
        for member in members:
            await self.bot.di.take_items(member, (item, num))

    @inventory.command(no_pm=True)
    async def giveitem(self, ctx, item: str, num: int, *members: Converter):
        """Give an item to a person (Not out of your inventory)"""
        if "everyone" in members:
            members = ctx.guild.members

        num = abs(num)
        for member in members:
            await self.bot.di.give_items(member, (item, num))

    @inventory.command(no_pm=True)
    async def give(self, ctx, other: discord.Member, *items: str):
        """Give items ({item}x{#}) to a member; ie: ;give @Henry#6174 pokeballx3"""
        fitems = []
        for item in items:
            split = item.split('x')
            split, num = "x".join(split[:-1]), abs(int(split[-1]))
            fitems.append((split, num))

        try:
            await self.bot.di.take_items(fitems)
            await self.bot.di.give_items(fitems)
        except:
            await ctx.send("You do not have enough to give away!")
