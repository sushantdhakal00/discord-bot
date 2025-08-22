import time
import random
import logging
import discord
from discord.ext import commands

# Import your database helpers (with single-arg can_claim_reward)
from database import (
    can_claim_reward,  # expects (uid) -> bool
    record_reward_claim,  # expects (uid) -> None
    update_balance,  # expects (uid, amount) -> None
    record_transaction,  # expects (uid, type, source, amount, note) -> None
)

log = logging.getLogger(__name__)

FAUCET_AMOUNT = 0.001
ONE_DAY_SECONDS = 24 * 60 * 60


class PerCommandFaucetCache:
    """
    In-memory per-process cache to enforce once-per-day per-command rewards.
    Key: (uid, command_key) -> last_claim_ts (epoch seconds)
    This augments your DB's per-user global throttle so each command
    has its own cooldown even though can_claim_reward(uid) is global.
    """

    def __init__(self):
        self._last_claim = {}  # dict[(int, str), float]

    def can_claim(self, uid: int, command_key: str, now: float = None) -> bool:
        now = now or time.time()
        key = (uid, command_key)
        last = self._last_claim.get(key)
        if last is None:
            return True
        return (now - last) >= ONE_DAY_SECONDS

    def record_claim(self, uid: int, command_key: str, now: float = None):
        now = now or time.time()
        key = (uid, command_key)
        self._last_claim[key] = now


class FunMeters(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._pc_cache = PerCommandFaucetCache()

    # ---------- Internal helpers ----------
    def _award_faucet(
        self,
        ctx: commands.Context,
        embed: discord.Embed,
        command_key: str,
        success_text: str,
        claimed_text: str,
    ):
        """
        Award FAUCET_AMOUNT if:
        - Global per-user DB check allows a claim (can_claim_reward(uid) is True), AND
        - Per-command in-memory cache allows a claim (24h cooldown per command).
        On success, updates balance, records DB claim (global), records transaction (best-effort),
        and records per-command claim in-memory.
        Always appends a field to the embed with the result.
        """
        uid = ctx.author.id

        # Step 1: Global per-user check via DB single-arg function
        try:
            global_ok = can_claim_reward(uid)
        except Exception as e:
            log.exception("can_claim_reward(uid) failed: %s", e)
            embed.add_field(
                name="🎁 Reward",
                value=
                "Reward system is temporarily unavailable. Please try again later.",
                inline=False,
            )
            return

        if not global_ok:
            # Already claimed globally (regardless of command)
            embed.add_field(name="🎁 Reward", value=claimed_text, inline=False)
            return

        # Step 2: Per-command local check for 24h cooldown
        if not self._pc_cache.can_claim(uid, command_key):
            # Command-specific cooldown not elapsed
            embed.add_field(name="🎁 Reward", value=claimed_text, inline=False)
            return

        # Step 3: Perform grant
        try:
            update_balance(uid, FAUCET_AMOUNT)
            # Record DB claim globally — note: this is global, not per-command
            record_reward_claim(uid)
            # Best-effort transaction log
            try:
                record_transaction(
                    uid,
                    "credit",
                    "faucet",
                    FAUCET_AMOUNT,
                    f"Extreme reward from !{command_key}",
                )
            except Exception as log_err:
                log.warning("record_transaction failed (non-critical): %s",
                            log_err)

            # Record per-command claim locally
            self._pc_cache.record_claim(uid, command_key)

            embed.add_field(name="🎁 Reward", value=success_text, inline=False)
        except Exception as e:
            log.exception("Granting faucet failed: %s", e)
            embed.add_field(
                name="🎁 Reward",
                value=
                "Could not deliver reward due to a system error. No balance was changed.",
                inline=False,
            )

    # ---------- !help_fun ----------
    @commands.command(name="help_fun",
                      aliases=["help fun", "fun help", "fun", "funny"])
    async def help_fun(self, ctx: commands.Context):
        """Show help/info for all fun meter commands."""
        embed = discord.Embed(
            title="🎉 Fun Commands Help",
            description=
            "Here’s a list of all fun meter commands you can play with!",
            color=discord.Color.gold(),
        )
        embed.add_field(
            name="🍆 !pp [@user]",
            value=
            (f"Measures someone’s... personality. Get LEGENDARY on yourself to earn "
             f"{FAUCET_AMOUNT} qc (once per day per command)."),
            inline=False,
        )
        embed.add_field(
            name="🏳️‍🌈 !gay [@user]",
            value=
            (f"Calculates someone's Gay‑o‑Meter. Extreme: ULTIMATE GAY (101%) awards "
             f"{FAUCET_AMOUNT} qc (self only, daily)."),
            inline=False,
        )
        embed.add_field(
            name="💘 !simp [@user]",
            value=(
                f"Shows how much of a simp someone is. Extreme: 100% awards "
                f"{FAUCET_AMOUNT} qc (self only, daily)."),
            inline=False,
        )
        embed.add_field(
            name="🕵️ !sus [@user]",
            value=
            (f"Detects suspicious levels. Extreme: IMPOSTOR FOUND (101%) awards "
             f"{FAUCET_AMOUNT} qc (self only, daily)."),
            inline=False,
        )
        embed.add_field(
            name="🍀 !luck [@user]",
            value=(f"Tests luck percentage. Extreme: MAX LUCK (100%) awards "
                   f"{FAUCET_AMOUNT} qc (self only, daily)."),
            inline=False,
        )
        embed.add_field(
            name="🧠 !brain [@user]",
            value=(f"Generates a random IQ. Extreme: ≥140 awards "
                   f"{FAUCET_AMOUNT} qc (self only, daily)."),
            inline=False,
        )
        embed.set_footer(
            text=
            "Tip: Mention someone or leave empty to test yourself. Rewards only when testing yourself."
        )
        await ctx.send(embed=embed)

    # ---------- !pp ----------
    @commands.command()
    async def pp(self, ctx: commands.Context, member: discord.Member = None):
        """Measure someone's... personality."""
        member = member or ctx.author
        length = random.randint(0, 15)
        pp_str = "8" + "=" * length + "D"

        embed = discord.Embed(
            title="🍆 Personality Measurement",
            description=f"{member.mention}'s personality size:",
            color=discord.Color.magenta(),
        )
        embed.add_field(name="Result", value=f"`{pp_str}`", inline=False)

        if length == 0:
            rating = "Microscopic! 🔬"
        elif length < 3:
            rating = "Tiny! 🤏"
        elif length < 7:
            rating = "Average! 👍"
        elif length < 12:
            rating = "Impressive! 😎"
        else:
            rating = "LEGENDARY! 🏆"
        embed.add_field(name="Rating", value=rating, inline=False)

        if length >= 12 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "pp",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for being LEGENDARY! Come back tomorrow.",
                claimed_text=
                "You already claimed your LEGENDARY reward today. 🍀",
            )

        await ctx.send(embed=embed)

    # ---------- !gay ----------
    @commands.command()
    async def gay(self, ctx: commands.Context, member: discord.Member = None):
        """Calculate gay percentage."""
        member = member or ctx.author
        percentage = random.randint(0, 101)
        filled = percentage // 10
        bar = "█" * filled + "░" * (10 - filled)

        embed = discord.Embed(
            title="🏳️‍🌈 Gay-o-Meter",
            description=f"Analyzing {member.mention}...",
            color=discord.Color.from_rgb(255, 0, 255),
        )
        embed.add_field(name="Result",
                        value=f"`{bar}` {percentage}%",
                        inline=False)

        statuses = [
            (0, "Straight as an arrow! 🏹"),
            (25, "Mostly straight! 👫"),
            (50, "Bi-curious! 🤔"),
            (75, "Pretty gay! 🌈"),
            (100, "Very gay! 💅"),
            (101, "ULTIMATE GAY! 🏳️‍🌈✨"),
        ]
        for limit, status in statuses:
            if percentage <= limit:
                embed.add_field(name="Status", value=status, inline=False)
                break

        if percentage == 101 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "gay",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for hitting ULTIMATE GAY! Come back tomorrow.",
                claimed_text=
                "You already claimed your reward for ULTIMATE GAY today. 🌈",
            )

        await ctx.send(embed=embed)

    # ---------- !simp ----------
    @commands.command()
    async def simp(self, ctx: commands.Context, member: discord.Member = None):
        """Measure simping percentage."""
        member = member or ctx.author
        percentage = random.randint(0, 101)
        filled = percentage // 10
        bar = "💗" * filled + "▫" * (10 - filled)

        embed = discord.Embed(
            title="💘 Simp-o-Meter",
            description=f"Analyzing {member.mention}...",
            color=discord.Color.pink(),
        )
        embed.add_field(name="Result",
                        value=f"`{bar}` {percentage}%",
                        inline=False)

        if percentage == 0:
            status = "Stone cold heart! 🧊"
        elif percentage < 25:
            status = "Not really a simp. 😎"
        elif percentage < 50:
            status = "Mildly simpy 😏"
        elif percentage < 75:
            status = "Full-time simp 🥰"
        elif percentage < 100:
            status = "Hopeless romantic 💖"
        else:
            status = "CERTIFIED SIMP 🎓💘"
        embed.add_field(name="Status", value=status, inline=False)

        if percentage == 100 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "simp",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for being a CERTIFIED SIMP! Come back tomorrow.",
                claimed_text=
                "You already claimed your CERTIFIED SIMP reward today. 💘",
            )

        await ctx.send(embed=embed)

    # ---------- !sus ----------
    @commands.command()
    async def sus(self, ctx: commands.Context, member: discord.Member = None):
        """Detect sus level."""
        member = member or ctx.author
        percentage = random.randint(0, 101)
        filled = percentage // 10
        bar = "🔴" * filled + "⚪" * (10 - filled)

        embed = discord.Embed(
            title="🕵️ Sus Detector",
            description=f"Scanning {member.mention}...",
            color=discord.Color.red(),
        )
        embed.add_field(name="Result",
                        value=f"`{bar}` {percentage}%",
                        inline=False)

        if percentage == 0:
            status = "Clean crewmate ✅"
        elif percentage < 50:
            status = "Kind of sus 🤨"
        elif percentage < 75:
            status = "Suspicious 😳"
        elif percentage < 100:
            status = "Super sus 😬"
        else:
            status = "🚨 IMPOSTOR FOUND 🚨"
        embed.add_field(name="Status", value=status, inline=False)

        if percentage == 101 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "sus",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for IMPOSTOR FOUND! Come back tomorrow.",
                claimed_text=
                "You already claimed your IMPOSTOR reward today. 🚨",
            )

        await ctx.send(embed=embed)

    # ---------- !luck ----------
    @commands.command()
    async def luck(self, ctx: commands.Context, member: discord.Member = None):
        """Check someone's luck."""
        member = member or ctx.author
        percentage = random.randint(0, 101)
        filled = percentage // 10
        bar = "🍀" * filled + "▫" * (10 - filled)

        embed = discord.Embed(
            title="🍀 Luck Meter",
            description=f"Testing {member.mention}'s luck...",
            color=discord.Color.green(),
        )
        embed.add_field(name="Result",
                        value=f"`{bar}` {percentage}%",
                        inline=False)

        if percentage == 0:
            status = "Unlucky as hell 😢"
        elif percentage < 25:
            status = "Needs a four-leaf clover 🍀"
        elif percentage < 50:
            status = "Not bad 😉"
        elif percentage < 75:
            status = "Pretty lucky 😎"
        elif percentage < 100:
            status = "Luck is on your side 😏"
        else:
            status = "☘️ MAX LUCK LEVEL ☘️"
        embed.add_field(name="Status", value=status, inline=False)

        if percentage == 100 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "luck",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for MAX LUCK! Come back tomorrow.",
                claimed_text=
                "You already claimed your MAX LUCK reward today. ☘️",
            )

        await ctx.send(embed=embed)

    # ---------- !brain ----------
    @commands.command()
    async def brain(self,
                    ctx: commands.Context,
                    member: discord.Member = None):
        """Test someone's IQ (for fun)."""
        member = member or ctx.author
        iq = random.randint(20, 180)

        embed = discord.Embed(
            title="🧠 IQ Test",
            description=f"Calculating {member.mention}'s IQ...",
            color=discord.Color.blue(),
        )
        embed.add_field(name="IQ Score", value=f"`{iq}`", inline=False)

        if iq < 60:
            status = "Potato brain 🥔"
        elif iq < 90:
            status = "Below average 🤷"
        elif iq < 110:
            status = "Average thinker 🙂"
        elif iq < 140:
            status = "Smart cookie 🍪"
        else:
            status = "Certified Genius 🏆"
        embed.add_field(name="Status", value=status, inline=False)

        if iq >= 140 and member.id == ctx.author.id:
            self._award_faucet(
                ctx,
                embed,
                "brain",
                success_text=
                f"You earned {FAUCET_AMOUNT} qc for being a Certified Genius! Come back tomorrow.",
                claimed_text="You already claimed your Genius reward today. 🧠",
            )

        await ctx.send(embed=embed)





async def setup(bot: commands.Bot):
    await bot.add_cog(FunMeters(bot))
