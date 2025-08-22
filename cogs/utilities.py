# cogs/utilities.py
import math
import re
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, available_timezones

import discord
from discord.ext import commands

CALC_ALLOWED = re.compile(r"^[0-9\.\+\-\*\/\^\(\)\s%]+$")  # simple guard

def _safe_eval(expr: str) -> float:
    # Very conservative calculator: convert ^ to ** and evaluate using math-only namespace
    expr = expr.replace("^", "**")
    if not CALC_ALLOWED.match(expr):
        raise ValueError("Expression contains unsupported characters.")
    # Limit builtins and allow math functions/constants
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed.update({"__builtins__": {}})
    return eval(expr, allowed, {})  # expression already guarded

class utilities(commands.Cog):
    """General-purpose utilities: calculator, time zones, formatting, and more."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 1) Calculator
    @commands.command(name="calc", aliases=["calculate", "eval"])
    async def calc_cmd(self, ctx: commands.Context, *, expression: str):
        """
        Evaluate a math expression safely.
        Examples:
          !calc 2+2
          !calc (3^4 + 5) / 2
          !calc sin(pi/2) + sqrt(49)
        """
        try:
            # expose select math names to user—not full Python
            expression = expression.replace("π", "pi")
            value = _safe_eval(expression)
            await ctx.send(f"🧮 `{expression}` = `{value}`")
        except Exception as e:
            await ctx.send(f"❌ {e}")

    # 2) Time zone convert
    @commands.command(name="tz", aliases=["timezone"])
    async def timezone_convert(self, ctx: commands.Context, time_str: str, from_tz: str, to_tz: str):
        """
        Convert a time between IANA time zones.
        Usage:
          !tz "2025-08-19 21:15" Asia/Kathmandu UTC
          !tz "2025-08-19 09:30" America/New_York Europe/London
        Notes:
          - Use quotes around the timestamp if it has spaces.
          - Format: YYYY-MM-DD HH:MM (24h)
          - Time zones must be IANA (e.g., Asia/Kathmandu, Europe/London)
        """
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            src = ZoneInfo(from_tz)
            dst = ZoneInfo(to_tz)
            localized = dt.replace(tzinfo=src)
            converted = localized.astimezone(dst)
            await ctx.send(
                "⏱️ Timezone Conversion\n"
                f"• From: {from_tz} → {localized:%Y-%m-%d %H:%M %Z}\n"
                f"• To:   {to_tz} → {converted:%Y-%m-%d %H:%M %Z}"
            )
        except Exception as e:
            await ctx.send(f"❌ {e}\nTip: Use IANA names (e.g., America/New_York). List with `!tz_list`.")

    @commands.command(name="tz_list", aliases=["timezones"])
    async def tz_list(self, ctx: commands.Context, query: str | None = None):
        """
        List IANA time zones, optionally filter by query.
        Examples:
          !tz_list
          !tz_list asia
          !tz_list kath
        """
        tzs = sorted(available_timezones())
        if query:
            q = query.lower()
            tzs = [t for t in tzs if q in t.lower()]
        if not tzs:
            return await ctx.send("No matching time zones.")
        preview = "\n".join(tzs[:50])
        more = f"\n… and {len(tzs)-50} more" if len(tzs) > 50 else ""
        await ctx.send(f"🗺️ Time zones ({len(tzs)}):\n{preview}{more}")

    # 3) Timestamp helper (Discord inline)
    @commands.command(name="ts", aliases=["timestamp"])
    async def discord_timestamp(self, ctx: commands.Context, *, when: str):
        """
        Create Discord-friendly timestamps.
        Usage:
          !ts 2025-08-19 21:15 UTC
          !ts +2h
          !ts +3d
        Outputs multiple formats like <t:epoch:R>, <t:epoch:f>, etc.
        """
        try:
            now = datetime.utcnow()
            # relative like +2h, +3d, +45m
            if when.startswith(("+", "-")):
                sign = 1 if when[0] == "+" else -1
                num = int(re.findall(r"\d+", when))
                unit = re.findall(r"[a-zA-Z]+", when).lower()
                mult = {"s":1, "sec":1, "m":60, "min":60, "h":3600, "d":86400, "w":604800}.get(unit, None)
                if mult is None:
                    raise ValueError("Use s/sec/m/min/h/d/w for relative units.")
                epoch = int((now.timestamp() + sign * num * mult))
            else:
                # absolute: "YYYY-MM-DD HH:MM ZONE"
                # fallback to UTC if zone omitted
                parts = when.split()
                if len(parts) >= 3:
                    dt = datetime.strptime(" ".join(parts[:2]), "%Y-%m-%d %H:%M")
                    zone = ZoneInfo(parts[2])
                else:
                    dt = datetime.strptime(" ".join(parts[:2]) if len(parts)>=2 else " ".join(parts), "%Y-%m-%d")
                    zone = ZoneInfo("UTC")
                epoch = int(dt.replace(tzinfo=zone).timestamp())

            styles = {
                "Short time": "t",
                "Long time": "T",
                "Short date": "d",
                "Long date": "D",
                "Short dt": "f",
                "Long dt": "F",
                "Relative": "R",
            }
            lines = [f"{name}: <t:{epoch}:{code}>" for name, code in styles.items()]
            await ctx.send("🧷 Discord Timestamps\n" + "\n".join(lines))
        except Exception as e:
            await ctx.send(f"❌ {e}\nExamples:\n• !ts +2h\n• !ts 2025-08-19 21:15 UTC")

    # 4) Unit converter (length/mass/temp quick picks)
    @commands.command(name="convertu", aliases=["unit"])
    async def convert_units(self, ctx: commands.Context, value: float, from_unit: str, to_unit: str):
        """
        Convert common units (length, mass, temperature).
        Examples:
          !convertu 10 km mi
          !convertu 5 kg lb
          !convertu 100 c f
        """
        try:
            fu = from_unit.lower()
            tu = to_unit.lower()

            # length (meters as base)
            length = {
                "m":1.0, "km":1000.0, "cm":0.01, "mm":0.001,
                "mi":1609.344, "yd":0.9144, "ft":0.3048, "in":0.0254
            }
            # mass (kg as base)
            mass = {
                "kg":1.0, "g":0.001, "mg":1e-6,
                "lb":0.45359237, "oz":0.028349523125
            }

            # temperature special cases
            def to_c(x, u):
                if u in ("c", "°c"): return x
                if u in ("f", "°f"): return (x-32)*5/9
                if u in ("k",): return x-273.15
                raise ValueError

            def from_c(xc, u):
                if u in ("c", "°c"): return xc
                if u in ("f", "°f"): return xc*9/5+32
                if u in ("k",): return xc+273.15
                raise ValueError

            # temperature path
            if fu in ("c","°c","f","°f","k") and tu in ("c","°c","f","°f","k"):
                out = from_c(to_c(value, fu), tu)
                return await ctx.send(f"🌡️ {value:g}{fu.upper()} = {out:g}{tu.upper()}")

            # length path
            if fu in length and tu in length:
                meters = value * length[fu]
                out = meters / length[tu]
                return await ctx.send(f"📏 {value:g} {fu} = {out:g} {tu}")

            # mass path
            if fu in mass and tu in mass:
                kg = value * mass[fu]
                out = kg / mass[tu]
                return await ctx.send(f"⚖️ {value:g} {fu} = {out:g} {tu}")

            await ctx.send("❌ Unsupported units. Try: m, km, mi, ft, in | kg, g, lb, oz | C/F/K")
        except Exception:
            await ctx.send("❌ Failed to convert. Example: `!unit 10 km mi`")

    # 5) Text tools: case/snake/camel
    @commands.command(name="case", aliases=["textcase"])
    async def text_case(self, ctx: commands.Context, mode: str, *, text: str):
        """
        Change text case/style.
        Usage:
          !case upper Hello world
          !case lower Hello WORLD
          !case title hello world
          !case snake Hello world again
          !case camel hello_world_again
        """
        mode = mode.lower()
        if mode == "upper":
            return await ctx.send(text.upper())
        if mode == "lower":
            return await ctx.send(text.lower())
        if mode == "title":
            return await ctx.send(text.title())

        tokens = re.split(r"[\s_\-]+", text.strip())
        if mode == "snake":
            return await ctx.send("_".join(t.lower() for t in tokens if t))
        if mode in ("camel","camelcase"):
            parts = [t for t in tokens if t]
            if not parts:
                return await ctx.send("")
            return await ctx.send(parts[0].lower() + "".join(t.title() for t in parts[1:]))

        await ctx.send("❌ Modes: upper, lower, title, snake, camel")

    # 6) Reminder (lightweight)
    @commands.command(name="remindme", aliases=["remind"])
    async def remind_me(self, ctx: commands.Context, delta: str, *, note: str):
        """
        Set a simple reminder.
        Usage:
          !remindme 10m Drink water
          !remindme 2h Finish report
        """
        try:
            m = re.fullmatch(r"(\d+)\s*([smhdw])", delta.strip().lower())
            if not m:
                return await ctx.send("❌ Use formats like 30s, 10m, 2h, 1d, 1w.")
            n = int(m.group(1))
            unit = m.group(2)
            mult = {"s":1, "m":60, "h":3600, "d":86400, "w":604800}[unit]
            await ctx.send(f"⏰ Ok! I’ll remind you in {n}{unit}: {note}")
            await asyncio.sleep(n * mult)
            try:
                await ctx.reply(f"🔔 Reminder: {note}")
            except Exception:
                await ctx.author.send(f"🔔 Reminder from #{ctx.channel.name}: {note}")
        except Exception as e:
            await ctx.send(f"❌ {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(utilities(bot))
