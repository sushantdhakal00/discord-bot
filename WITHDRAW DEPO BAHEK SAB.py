@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="👑 Queen Bot — Command Guide",
        description=
        ("Welcome to the royal hub for **Quanta Coin (QC)** on Solana.\n"
         "Deposit SOL → get QC, play provably‑fair games, join lotteries and airdrops.\n"
         "Rate: 1 QC = 0.001 SOL"),
        color=discord.Color.gold())
    embed.set_thumbnail(url="https://cryptologos.cc/logos/solana-sol-logo.png")
    embed.set_footer(text="Quanta Coin • Powered by Solana ⚡")

    # Wallet & On-chain
    embed.add_field(
        name="💰 Wallet & On‑Chain",
        value=
        ("`!deposit` — DM your unique SOL deposit address\n"
         "`!balance` — Show QC balance and SOL equivalent\n"
         "`!withdraw <amount> <sol_address>` — Withdraw QC → SOL on‑chain\n"
         "`!tip @user <amount>` — Send QC to another user\n"
         "`!convert <amount> <QC|SOL>` — Live QC/SOL to 20+ fiats (+NPR via INR×1.6)\n"
         "`!profile [@user]` — View a QC profile (balance, stats, SOL info)\n"
         "`!profile_restrict` — Toggle profile privacy"),
        inline=False)

    # Airdrop
    embed.add_field(
        name="🎁 Airdrop",
        value=
        ("`!airdrop <amount> [unit] <duration> [public]` — Create an airdrop from treasury\n"
         "  • Examples: `!airdrop 0.1$ 10s`, `!airdrop 0.5 qc 2 h`, `!airdrop 1$ sol 10 m public`\n"
         "`!join_airdrop <ID>` — Join an open airdrop (or press the Join button)\n"
         "`!airdrop_status` — See open airdrops or recent results\n"
         "`!airdrop_verify <ID>` — Verify details and claimants of an airdrop\n"
         "`!airdrop_cancel <ID>` — Cancel an open airdrop (creator/admin)"),
        inline=False)

    # Casino & Games (provably fair)
    embed.add_field(
        name="🎮 Casino & Games (Provably Fair)",
        value=(
            "`!games` — List all available games and rules\n"
            "`!tictactoe @user [wager]` — Button-based duel\n"
            "`!keno` — 6 picks, 8 draws, up to 800× minus 1%\n"
            "`!limbo <amount>` — Pick multiplier, win chance scales\n"
            "`!coinflip <amount> <heads|tails>` — 50/50 double or nothing\n"
            "`!dice <amount> <2-100>` — Roll-under; payout by odds (−1%)\n"
            "`!blackjack <amount>` — Auto 17+, push refunds\n"
            "`!hilo <amount> <higher|lower>` — Higher/lower than 7\n"
            "`!roulette <amount> <red|black|odd|even|0-36>` — Wheel of fate\n"
            "`!slots <amount>` — 3-reel slots; 3× & 2× pay\n"
            "`!wheel <amount>` — Land a multiplier (uniform segments)\n"
            "`!mines <amount> [picks]` — 5×5, 5 mines; inverse-odds payout"),
        inline=False)

    # Lottery
    embed.add_field(
        name="🎟️ Lottery",
        value=(
            "`!lottery [entry_cost] [duration]` — Start a flexible lottery\n"
            "`!join` — Enter the open lottery\n"
            "`!lottery_status` — Check current or last result"),
        inline=False)

    # System & Admin
    embed.add_field(name="📊 System & Admin",
                    value=("`!bot_stats` — Global stats (admin only)\n"
                           "`!about` — Learn about Queen Bot & Quanta Coin\n"
                           "`!help` — Show this menu"),
                    inline=False)

    # Pointers to lists instead of inlining
    embed.add_field(name="📚 More Lists",
                    value=("Use `!games` for the list of available games.\n"
                           "Use `!fun` for the list of fun commands."),
                    inline=False)

    # Tips
    embed.add_field(
        name="💡 Tips",
        value=("• Minimum deposit: `0.001 SOL` (=1 QC)\n"
               "• Deposits credited automatically; withdrawals are on‑chain\n"
               "• Games are provably fair (HMAC seeds and nonces shown)\n"
               "• Enable DMs for deposit/lottery/airdrop/game notifications"),
        inline=False)

    await ctx.send(embed=embed)


@bot.command(name="about")
async def about_cmd(ctx):
    e = discord.Embed(
        title="👑 About Queen Bot",
        description=
        ("Queen Bot is the all‑in‑one wallet and casino companion for **Quanta Coin (QC)**.\n\n"
         "With Queen Bot you can:\n"
         "• Deposit SOL and receive QC automatically (1 QC = 0.001 SOL)\n"
         "• Check balances, tip friends, and withdraw SOL on‑chain\n"
         "• Play provably‑fair games (Keno, Limbo, Dice, Blackjack, Roulette, Slots, Wheel, Mines, TicTacToe)\n"
         "• Join flexible lotteries with auto‑settlement and DM notices\n"
         "• Enjoy fun meters that sometimes award small QC faucet bonuses"),
        color=discord.Color.purple())
    e.add_field(
        name="Quick Start",
        value=(
            "1) `!deposit` to get your SOL address\n"
            "2) Send SOL → QC is auto‑credited\n"
            "3) `!balance` to view QC and SOL equivalent\n"
            "4) Try games: `!games` or e.g. `!keno`, `!limbo 1`, `!dice 1 50`"
        ),
        inline=False)
    e.add_field(
        name="Popular Commands",
        value=
        ("`!help` • `!convert <amount> <QC|SOL>` • `!tip @user <amount>`\n"
         "`!profile` • `!lottery` • `!join` • `!lottery_status` • `!help_fun`"
         ),
        inline=False)
    e.set_footer(text="Welcome to Quanta Coin • Powered by Solana ⚡")
    await ctx.send(embed=e)


@bot.event
async def on_guild_join(guild: discord.Guild):
    # Pick a channel the bot can speak in (system channel preferred)
    target = None
    try:
        if guild.system_channel and guild.system_channel.permissions_for(
                guild.me).send_messages:
            target = guild.system_channel
        else:
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    target = ch
                    break
    except Exception:
        target = None

    if target:
        try:
            e = discord.Embed(
                title=f"👑 Hello {guild.name} — I’m Queen Bot!",
                description=
                ("Thanks for inviting me! I manage **Quanta Coin (QC)** and run a suite of provably‑fair games.\n\n"
                 "• `!deposit` to get your SOL address (1 QC = 0.001 SOL)\n"
                 "• `!balance`, `!withdraw <amount> <address>`, `!tip @user <amount>`\n"
                 "• `!convert <amount> <QC|SOL>` for live fiat values\n"
                 "• `!games` for all game commands\n"
                 "• `!lottery` to start a lottery; `!join` to enter\n"
                 "• `!help_fun` for faucets via fun meters"),
                color=discord.Color.gold())
            e.set_footer(
                text="Use !help to see everything • Powered by Solana ⚡")
            await target.send(embed=e)
        except Exception:
            pass


#==================end of withdraw

from datetime import datetime, timezone
import aiohttp
import discord

# 20 supported fiats (request these from your price source)
SUPPORTED_FIATS = [
    "usd",
    "eur",
    "gbp",
    "inr",
    "aud",
    "cad",
    "nzd",
    "sgd",
    "jpy",
    "krw",
    "chf",
    "hkd",
    "cny",
    "brl",
    "zar",
    "mxn",
    "try",
    "rub",
    "sek",
    "dkk",
]

# Symbols for display (fallback to code if not found)
FIAT_SYMBOLS = {
    "usd": "$",
    "eur": "€",
    "gbp": "£",
    "inr": "₹",
    "aud": "A$",
    "cad": "C$",
    "nzd": "NZ$",
    "sgd": "S$",
    "jpy": "¥",
    "krw": "₩",
    "chf": "CHF ",
    "hkd": "HK$",
    "cny": "¥",
    "brl": "R$",
    "zar": "R",
    "mxn": "MX$",
    "try": "₺",
    "rub": "₽",
    "sek": "kr",
    "dkk": "kr",
    # NPR is derived from INR below; symbol here for rendering:
    "npr": "रु",
}

# Choose an on-brand color for the embed
EMBED_COLOR = discord.Color.blue()


@bot.command(name="convert")
async def convert_cmd(ctx, amount: float, unit: str):
    """
    Convert QC or SOL to 20 real-world currencies using live SOL price.
    NPR is derived from INR by multiplier 1.6.
    Usage: !convert <amount> <QC|SOL>
    """
    unit_norm = unit.strip().upper()
    if amount <= 0 or unit_norm not in {"QC", "SOL"}:
        return await ctx.send(
            "❌ Usage: `!convert <amount> <QC|SOL>` (example: `!convert 25 QC`)"
        )

    # Convert input to SOL (1 QC = 0.001 SOL)
    sol_amount = amount * 0.001 if unit_norm == "QC" else amount

    # Fetch live prices (expects a mapping like {"usd": 123.45, "inr": 9999.0, ...})
    try:
        async with aiohttp.ClientSession() as session:
            prices = await fetch_sol_price(session, SUPPORTED_FIATS)
    except Exception as e:
        return await ctx.send(f"❌ Failed to fetch SOL price: {e}")

    if not prices:
        return await ctx.send("❌ Price lookup returned no data.")

    # Prepare values
    lines = []
    missing = []
    for fiat in SUPPORTED_FIATS:
        p = prices.get(fiat)
        if p is None:
            missing.append(fiat.upper())
            continue
        value = sol_amount * float(p)
        symbol = FIAT_SYMBOLS.get(fiat, "")
        lines.append((fiat.upper(), f"{symbol}{value:,.2f}"))

    # NPR derived from INR × 1.6
    inr_price = prices.get("inr")
    if inr_price is not None:
        inr_value = sol_amount * float(inr_price)
        npr_value = inr_value * 1.6
        lines.append(("NPR", f"{FIAT_SYMBOLS['npr']}{npr_value:,.2f}"))
    else:
        lines.append(("NPR", "Unavailable (INR missing)"))

    # Build a polished embed
    qc_equiv = sol_amount / 0.001
    title = f"🔁 Conversion for {amount:g} {unit_norm}"
    description = (
        f"• Equivalent: `{sol_amount:.6f} SOL` ≈ `{qc_equiv:.3f} QC`\n"
        "• Based on live SOL price")

    embed = discord.Embed(
        title=title,
        description=description,
        color=EMBED_COLOR,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name="Currency Converter")
    embed.set_thumbnail(
        url="https://cryptologos.cc/logos/solana-sol-logo.png")  # optional

    # Format into 2 columns for readability
    half = (len(lines) + 1) // 2
    left_block = "\n".join(f"• {code}: {val}" for code, val in lines[:half])
    right_block = "\n".join(f"• {code}: {val}" for code, val in lines[half:])

    embed.add_field(name="Fiat Values (A)",
                    value=left_block or "—",
                    inline=True)
    embed.add_field(name="Fiat Values (B)",
                    value=right_block or "—",
                    inline=True)

    if missing:
        embed.add_field(name="Missing prices",
                        value=", ".join(missing),
                        inline=False)

    embed.set_footer(text="Rates fetched live • ")

    await ctx.send(embed=embed)


#======PREMIUM

# main.py — Paywall: pay once per server

import discord
from discord.ext import commands
from database import (
    guild_mark_grandfathered,
    guild_is_grandfathered,
    guild_is_paid,
    guild_mark_paid,
    guild_mark_bypass,
    guild_access_status,
)
# Import your DB helpers and economy functions
# from database import (guild_is_paid, guild_mark_paid, guild_access_status,
#                       guild_mark_bypass, guild_mark_grandfathered, guild_is_grandfathered)

PAYWALL_COST_QC = 10.0
BOT_OWNER_ID = 806561257556541470  # special ID for !invite_bypass
PAYWALL_WHITELIST = {
    "help", "about", "invite_pay", "invite_status", "invite_bypass", "bal",
    "deposit", "balance", "withdraw", "convert"
}
# allowed without activation


# 1) On startup, mark all already-joined servers as grandfathered (no pay required)
@bot.event
async def on_ready():
    # Your existing on_ready logic...
    # Ensure DB init complete, then grandfather all guilds where the bot is currently present
    try:
        for g in bot.guilds:
            guild_mark_grandfathered(g.id)
    except Exception as e:
        log.warning(f"[PAYWALL] Grandfather pass failed for some guilds: {e}")

    log.info(
        "Premium paywall ready: existing servers are grandfathered free forever."
    )
    # Continue your existing on_ready tasks...


# 2) Global check: gate commands in new servers unless paid or bypassed
@bot.check
async def _premium_paid_gate(ctx: commands.Context) -> bool:
    # Allow non-guild contexts (DMs)
    if ctx.guild is None:
        return True

    gid = ctx.guild.id

    # Old server: grandfathered, always allowed
    if guild_is_grandfathered(gid):
        return True

    # If paid/bypassed: allowed
    if guild_is_paid(gid):
        return True

    # Not paid new server: allow only whitelist
    if ctx.command and ctx.command.name in PAYWALL_WHITELIST:
        return True

    # Block and hint
    try:
        await ctx.send(
            "🚫 This server is not activated for premium features.\n"
            f"Use `!invite_pay` to activate for {PAYWALL_COST_QC:.0f} QC and unlock the bot here."
        )
    except Exception:
        pass
    return False


# 3) Command: !invite_pay — pays for THIS server (new servers only)
@bot.command(name="invite_pay")
async def invite_pay_cmd(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.send("❌ Run this in the server to activate.")

    gid = ctx.guild.id
    # Already grandfathered or paid?
    if guild_is_grandfathered(gid) or guild_is_paid(gid):
        return await ctx.send(
            "✅ This server is already activated. Enjoy premium features!")

    # Optional: require Manage Guild to prevent random users from paying
    # Comment out the next lines if anyone can pay is acceptable
    if not ctx.author.guild_permissions.manage_guild:
        return await ctx.send(
            "🔐 You need 'Manage Server' permission to activate this server.")

    # Check balance and charge
    u = fetch_user(ctx.author.id)
    if u["balance"] < PAYWALL_COST_QC:
        return await ctx.send(
            f"❌ Insufficient QC. Need {PAYWALL_COST_QC:.0f} QC; you have {u['balance']:.3f} QC."
        )

    # Deduct and mark paid
    update_balance(ctx.author.id, -PAYWALL_COST_QC)
    try:
        update_stats(ctx.author.id,
                     total_wagered=0)  # optional; or track in a dedicated stat
    except Exception:
        pass
    guild_mark_paid(gid, ctx.author.id, PAYWALL_COST_QC)

    # Premium styled confirmation
    e = discord.Embed(
        title="🌟 Premium Activated",
        description=(
            f"Server: **{ctx.guild.name}**\n"
            f"Activated by: {ctx.author.mention}\n"
            f"Cost: `{PAYWALL_COST_QC:.0f} QC`\n\n"
            "You now have access to all premium features in this server."),
        color=discord.Color.gold())
    e.set_footer(text="Thank you for supporting the premium experience ✨")
    await ctx.send(embed=e)

    # Try to create a fresh invite and DM the payer (optional, looks premium)
    invite_link = None
    try:
        channel = next(
            (c for c in ctx.guild.text_channels
             if c.permissions_for(ctx.guild.me).create_instant_invite), None)
        if channel:
            inv = await channel.create_invite(max_age=0,
                                              max_uses=0,
                                              unique=True)
            invite_link = str(inv)
    except Exception:
        invite_link = None

    if invite_link:
        try:
            await ctx.author.send(
                f"🔗 Your premium server invite for **{ctx.guild.name}**:\n{invite_link}"
            )
        except Exception:
            await ctx.send(
                "ℹ️ Unable to DM the invite link. Check your DM settings.")
    else:
        await ctx.send(
            "ℹ️ I couldn’t create an invite automatically. Ensure I have 'Create Invite' in a text channel."
        )


# 4) Command: !invite_status — show current activation status
@bot.command(name="invite_status")
async def invite_status_cmd(ctx: commands.Context):
    if ctx.guild is None:
        return await ctx.send("ℹ️ Run this inside a server.")
    gid = ctx.guild.id

    if guild_is_grandfathered(gid):
        e = discord.Embed(
            title="🏛️ Premium Status",
            description=
            "This server is grandfathered and does not require payment.",
            color=discord.Color.green())
        return await ctx.send(embed=e)

    info = guild_access_status(gid)
    if not info:
        e = discord.Embed(
            title="🕒 Premium Status",
            description=(
                "This is a new server and is not activated yet.\n"
                f"Use `!invite_pay` to activate for {PAYWALL_COST_QC:.0f} QC."
            ),
            color=discord.Color.orange())
        return await ctx.send(embed=e)

    status = info.get("status", "unknown")
    paid_by = info.get("paid_by", None)
    amount = float(info.get("amount_qc", 0.0))
    when = int(info.get("created_at", 0))

    desc = [
        f"Status: **{status}**",
        f"Amount: `{amount:.3f} QC`",
    ]
    if paid_by:
        desc.append(f"By: <@{paid_by}>")
    if when:
        desc.append(f"At: <t:{when}:f>")

    e = discord.Embed(title="🌟 Premium Status",
                      description="\n".join(desc),
                      color=discord.Color.gold()
                      if status == "paid" else discord.Color.blurple())
    await ctx.send(embed=e)


# 5) Command: !invite_bypass — owner-only permanent bypass for a server
@bot.command(name="invite_bypass")
async def invite_bypass_cmd(ctx: commands.Context):
    # Owner-only
    if ctx.author.id != BOT_OWNER_ID:
        return await ctx.send("🚫 Only the owner can use this command.")
    if ctx.guild is None:
        return await ctx.send("ℹ️ Run this inside the server to bypass.")

    gid = ctx.guild.id
    guild_mark_bypass(gid, ctx.author.id)
    e = discord.Embed(
        title="🛡️ Premium Bypass Enabled",
        description=(f"Server: **{ctx.guild.name}**\n"
                     "Payment requirement has been bypassed by owner."),
        color=discord.Color.purple())
    await ctx.send(embed=e)


#====ticker
# === !ticker — CoinGecko Pro v3.0.1 (pure-Python sparkline, robust) ==========
# Dependencies: aiohttp, pillow

# === !ticker — Coinlib.io (no charts, robust) =================================
# Dependencies: aiohttp

import aiohttp
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timezone
from typing import Optional, Dict, Any

COINLIB_BASE = "https://coinlib.io/api/v1"
COINLIB_KEY = "3b02ee2f949b0228"  # your key

# Default and selectable quote currencies (Coinlib uses symbols like USD/EUR/INR)
DEFAULT_PREF = "USD"
SUPPORTED_PREFS = ["USD", "EUR", "INR"]

# ---------------- Shared HTTP session ----------------
_coinlib_session: Optional[aiohttp.ClientSession] = None


async def _get_session() -> aiohttp.ClientSession:
    global _coinlib_session
    if _coinlib_session is None or _coinlib_session.closed:
        _coinlib_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20),
            headers={
                "Accept": "application/json",
                "User-Agent": "QueenBot/1.0 (+discord.py)"
            })
    return _coinlib_session


async def _coinlib_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    sess = await _get_session()
    url = f"{COINLIB_BASE}{path}"
    q = {k: str(v) for k, v in params.items() if v is not None}
    async with sess.get(url, params=q) as resp:
        text = await resp.text()
        if resp.status >= 400:
            raise RuntimeError(f"Coinlib {resp.status}: {text[:200]}")
        try:
            return await resp.json()
        except Exception:
            return {}


# ---------------- Formatting helpers ----------------
def _fmt_money(v: str | float | int, pref: str) -> str:
    sym = {"USD": "$", "EUR": "€", "INR": "₹"}.get(pref.upper(), "")
    try:
        f = float(v)
    except Exception:
        return f"{sym}0.00"
    a = abs(f)
    if a >= 100_000: return f"{sym}{f:,.0f}"
    if a >= 1: return f"{sym}{f:,.2f}"
    if a >= 0.01: return f"{sym}{f:,.4f}"
    return f"{sym}{f:,.6f}"


def _pct(v: str | float | int | None) -> str:
    try:
        if v is None:
            return "—"
        f = float(v)
        return f"{f:+.2f}%"
    except Exception:
        return "—"


def _clean_symbol(s: str) -> str:
    return (s or "").strip().upper()


# ---------------- UI Views ----------------
class CLTickerView(discord.ui.View):

    def __init__(self, symbol: str, pref: str):
        super().__init__(timeout=90)
        self.symbol = symbol
        self.pref = pref
        self.add_item(CLPrefSelect(self))
        self.add_item(CLRefreshButton(self))


class CLPrefSelect(discord.ui.Select):

    def __init__(self, parent: CLTickerView):
        opts = [
            discord.SelectOption(label=p, value=p, default=(p == parent.pref))
            for p in SUPPORTED_PREFS
        ]
        super().__init__(placeholder="Currency",
                         min_values=1,
                         max_values=1,
                         options=opts)
        self._parent = parent

    async def callback(self, interaction: discord.Interaction):
        self._parent.pref = self.values[0]
        await _send_coinlib_ticker(interaction,
                                   self._parent.symbol,
                                   self._parent.pref,
                                   edit=True)


class CLRefreshButton(discord.ui.Button):

    def __init__(self, parent: CLTickerView):
        super().__init__(label="Refresh",
                         style=discord.ButtonStyle.primary,
                         emoji="🔄")
        self._parent = parent

    async def callback(self, interaction: discord.Interaction):
        await _send_coinlib_ticker(interaction,
                                   self._parent.symbol,
                                   self._parent.pref,
                                   edit=True)


# ---------------- Core sender ----------------
async def _send_coinlib_ticker(ctx_or_inter: commands.Context
                               | discord.Interaction,
                               symbol: str,
                               pref: str,
                               edit: bool = False):
    is_inter = isinstance(ctx_or_inter, discord.Interaction)
    try:
        sym = _clean_symbol(symbol)
        prf = (pref or DEFAULT_PREF).upper()

        data = await _coinlib_get(
            "/coin",
            {
                "key": COINLIB_KEY,
                "symbol":
                sym,  # single symbol; Coinlib can accept comma list but we use one
                "pref": prf
            })

        if "error" in data:
            msg = f"❌ Coinlib error: {data.get('error')}"
            if is_inter:
                if not ctx_or_inter.response.is_done():
                    return await ctx_or_inter.response.send_message(
                        msg, ephemeral=True)
                return await ctx_or_inter.followup.send(msg, ephemeral=True)
            return await ctx_or_inter.send(msg)

        # Normalize: /coin returns either a single object or {"coins":[...]}
        coin = None
        if isinstance(data, dict) and data.get("symbol"):
            coin = data
        elif isinstance(data, dict) and isinstance(data.get("coins"),
                                                   list) and data["coins"]:
            coin = data["coins"][0]

        if not coin:
            msg = f"❌ Symbol not found on Coinlib: {sym}"
            if is_inter:
                if not ctx_or_inter.response.is_done():
                    return await ctx_or_inter.response.send_message(
                        msg, ephemeral=True)
                return await ctx_or_inter.followup.send(msg, ephemeral=True)
            return await ctx_or_inter.send(msg)

        # Fields (decimals are strings)
        name = coin.get("name") or sym
        show = coin.get("show_symbol") or sym
        rank = coin.get("rank", "—")
        price = coin.get("price", "0")
        mcap = coin.get("market_cap") or coin.get("marketcap") or coin.get(
            "market_capitalization")
        vol = coin.get("total_volume_24h") or coin.get(
            "volume_24h") or coin.get("volume")
        low = coin.get("low_24h")
        high = coin.get("high_24h")
        d1h = coin.get("delta_1h")
        d24h = coin.get("delta_24h")
        d7d = coin.get("delta_7d")
        d30d = coin.get("delta_30d")
        remaining = data.get("remaining") or coin.get("remaining")

        e = discord.Embed(
            title=f"{name} ({show}) • {prf}",
            description=f"Price: {_fmt_money(price, prf)}",
            color=discord.Color.blurple(),
            timestamp=datetime.now(timezone.utc),
        )
        e.add_field(
            name="Change",
            value=
            f"• 1h {_pct(d1h)}  • 24h {_pct(d24h)}  • 7d {_pct(d7d)}  • 30d {_pct(d30d)}",
            inline=False)
        if rank not in (None, "—"):
            e.add_field(name="Rank", value=str(rank), inline=True)
        if mcap is not None:
            e.add_field(name="Market Cap",
                        value=_fmt_money(mcap, prf),
                        inline=True)
        if vol is not None:
            e.add_field(name="24h Volume",
                        value=_fmt_money(vol, prf),
                        inline=True)
        if low is not None and high is not None:
            e.add_field(
                name="24h Low / High",
                value=f"{_fmt_money(low, prf)} / {_fmt_money(high, prf)}",
                inline=False)

        footer = f"Coinlib • Remaining quota: {remaining}" if remaining is not None else "Coinlib"
        e.set_footer(text=footer)

        view = CLTickerView(sym, prf)

        if is_inter:
            if edit:
                if not ctx_or_inter.response.is_done():
                    await ctx_or_inter.response.edit_message(embed=e,
                                                             view=view)
                else:
                    await ctx_or_inter.edit_original_response(embed=e,
                                                              view=view)
            else:
                await ctx_or_inter.response.send_message(embed=e, view=view)
        else:
            await ctx_or_inter.send(embed=e, view=view)

    except asyncio.TimeoutError:
        msg = "⏱️ Coinlib timed out. Please try again."
        if is_inter:
            if not ctx_or_inter.response.is_done():
                await ctx_or_inter.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_inter.followup.send(msg, ephemeral=True)
        else:
            await ctx_or_inter.send(msg)
    except Exception as e:
        msg = f"❌ {e}"
        if is_inter:
            if not ctx_or_inter.response.is_done():
                await ctx_or_inter.response.send_message(msg, ephemeral=True)
            else:
                await ctx_or_inter.followup.send(msg, ephemeral=True)
        else:
            await ctx_or_inter.send(msg)


# ---------------- Public command ----------------
@bot.command(name="ticker")
async def ticker_cmd(ctx: commands.Context, *, symbol: str):
    """
    Live price and stats from Coinlib (no charts).
    Usage:
      !ticker BTC
      !ticker eth
      !ticker pepe
    Default currency: USD. Use the menu to switch.
    """
    await _send_coinlib_ticker(ctx, symbol, DEFAULT_PREF, edit=False)


# ---------------- Optional cleanup ----------------
async def _close_coinlib_session():
    global _coinlib_session
    try:
        if _coinlib_session and not _coinlib_session.closed:
            await _coinlib_session.close()
    except Exception:
        pass


# Optional owner-only shutdown command:
@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown_cmd(ctx):
    await ctx.reply("Shutting down…")
    await _close_coinlib_session()
    await bot.close()


# ===========================end of ticker

import sqlite3
import time
from datetime import datetime, timezone, timedelta
from typing import List
import discord

try:
    import psutil
except Exception:
    psutil = None

if not hasattr(__builtins__, "_bot_start_time"):
    __builtins__._bot_start_time = time.time()


def _humanize_seconds(seconds: int) -> str:
    if seconds < 0:
        seconds = 0
    d, rem = divmod(seconds, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)


def _gini(values: List[float]) -> float:
    n = len(values)
    if n == 0:
        return 0.0
    vals = sorted(v for v in values if v >= 0.0)
    if not vals:
        return 0.0
    total = sum(vals)
    if total <= 0:
        return 0.0
    cum = 0.0
    cum_sum = 0.0
    for i, v in enumerate(vals, 1):
        cum += v
        cum_sum += cum
    return max(0.0, min(1.0, 1.0 + 1.0 / n - 2.0 * (cum_sum / (n * total))))


def _fetch_pragma_scalar(conn: sqlite3.Connection, name: str):
    try:
        row = conn.execute(f"PRAGMA {name}").fetchone()
        if row is None:
            return "?"
        return row[0]
    except Exception:
        return "?"


@bot.command(name="bot_stats")
async def bot_stats_cmd(ctx):
    if ctx.author.id != 806561257556541470:
        return await ctx.send(
            "❌ You do not have permission to use this command.")

    conn = get_conn()

    # Core aggregates
    bot_row = fetch_user(bot.user.id)
    bot_balance = float(bot_row["balance"])

    row = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()
    total_users = int(row["c"] if row and row["c"] is not None else 0)

    row = conn.execute("SELECT SUM(balance) AS s FROM users").fetchone()
    total_qc_circ = float(row["s"] if row and row["s"] is not None else 0.0)

    totals = conn.execute(
        "SELECT SUM(total_depo) AS depo, SUM(total_withdraw) AS withd FROM users"
    ).fetchone()
    total_depo = float(
        totals["depo"] if totals and totals["depo"] is not None else 0.0)
    total_withdraw = float(
        totals["withd"] if totals and totals["withd"] is not None else 0.0)

    # Users (excluding bot)
    row = conn.execute(
        "SELECT AVG(balance) AS avg_bal FROM users WHERE user_id != ?",
        (bot.user.id, )).fetchone()
    avg_user_balance = float(
        row["avg_bal"] if row and row["avg_bal"] is not None else 0.0)

    # Median (excluding bot)
    try:
        rows = conn.execute(
            "SELECT balance FROM users WHERE user_id != ? ORDER BY balance",
            (bot.user.id, )).fetchall()
        balances = [float(r["balance"]) for r in rows]
        n = len(balances)
        if n == 0:
            median_balance = 0.0
        elif n % 2 == 1:
            median_balance = balances[n // 2]
        else:
            median_balance = (balances[n // 2 - 1] + balances[n // 2]) / 2.0
    except Exception:
        balances = []
        median_balance = 0.0

    row = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE user_id != ? AND balance > 0",
        (bot.user.id, )).fetchone()
    nonzero_users = int(row["c"] if row and row["c"] is not None else 0)

    # Gini and concentration metrics (exclude bot)
    if not balances:
        try:
            bal_rows = conn.execute(
                "SELECT balance FROM users WHERE user_id != ?",
                (bot.user.id, )).fetchall()
            balances = [float(r["balance"]) for r in bal_rows]
        except Exception:
            balances = []
    gini = _gini([b for b in balances if b > 0])

    try:
        top_rows = conn.execute(
            "SELECT user_id, balance FROM users WHERE user_id != ? ORDER BY balance DESC LIMIT 10",
            (bot.user.id, )).fetchall()
    except Exception:
        top_rows = []

    top10_conc = 0.0
    largest_share_pct = 0.0
    if total_qc_circ > 0 and top_rows:
        top_sum = sum(float(r["balance"]) for r in top_rows)
        top10_conc = (top_sum / total_qc_circ) * 100.0
        largest_share_pct = (float(top_rows[0]["balance"]) /
                             total_qc_circ) * 100.0

    # Net P/L totals and wagering
    pl_totals = conn.execute(
        "SELECT SUM(net_profit_loss) AS pl_sum, SUM(total_wagered) AS wager_sum FROM users"
    ).fetchone()
    net_pl_sum = float(pl_totals["pl_sum"] if pl_totals
                       and pl_totals["pl_sum"] is not None else 0.0)
    total_wagered = float(pl_totals["wager_sum"] if pl_totals
                          and pl_totals["wager_sum"] is not None else 0.0)

    # SOL tracking — always show section; add robust recent list
    row = conn.execute(
        "SELECT SUM(total_sol_deposited) AS sol_sum FROM users").fetchone()
    try:
        total_sol_deposited = float(
            row["sol_sum"]) if row and row["sol_sum"] is not None else 0.0
    except Exception:
        total_sol_deposited = 0.0

    last_dep = conn.execute("""
        SELECT user_id, last_deposit_at, last_deposit_signature
        FROM users
        WHERE last_deposit_at IS NOT NULL
        ORDER BY last_deposit_at DESC
        LIMIT 1
    """).fetchone()

    # Also fetch a small recent list to prove activity
    recent_rows = conn.execute("""
        SELECT user_id, last_deposit_at
        FROM users
        WHERE last_deposit_at IS NOT NULL
        ORDER BY last_deposit_at DESC
        LIMIT 3
    """).fetchall()

    # Rewards stats
    try:
        today = datetime.utcnow().date().isoformat()
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM user_rewards WHERE last_reward = ?",
            (today, )).fetchone()
        rewards_today = int(row["c"] if row and row["c"] is not None else 0)
    except Exception:
        rewards_today = 0

    # Lottery stats
    try:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM lottery WHERE status='active'"
        ).fetchone()
        lot_active = int(row["c"] if row and row["c"] is not None else 0)
        row = conn.execute("SELECT SUM(pot) AS s FROM lottery").fetchone()
        lot_pot_total = float(
            row["s"] if row and row["s"] is not None else 0.0)
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM lottery_entries").fetchone()
        lot_entries = int(row["c"] if row and row["c"] is not None else 0)
        last_winner_row = conn.execute(
            "SELECT winner_id, pot FROM lottery WHERE winner_id IS NOT NULL ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if last_winner_row:
            last_winner = int(last_winner_row["winner_id"])
            last_winner_pot = float(last_winner_row["pot"] or 0.0)
            last_winner_str = f"<@{last_winner}> won `{last_winner_pot:,.3f} QC`"
        else:
            last_winner_str = "—"
    except Exception:
        lot_active = 0
        lot_pot_total = 0.0
        lot_entries = 0
        last_winner_str = "—"

    # Derived metrics
    user_circ = float(total_qc_circ) - bot_balance
    bot_share_pct = (bot_balance / total_qc_circ *
                     100.0) if total_qc_circ else 0.0
    depo_withdraw_ratio = (total_depo /
                           total_withdraw) if total_withdraw else None
    ratio_str = f"{depo_withdraw_ratio:.2f}x" if depo_withdraw_ratio else "—"

    # Activity from last_deposit_at as proxy
    try:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_ago = now - timedelta(days=7)

        row = conn.execute(
            "SELECT COUNT(*) AS c FROM users WHERE last_deposit_at >= ?",
            (week_ago.isoformat(), )).fetchone()
        new_users_7d = int(row["c"] if row and row["c"] is not None else 0)

        row = conn.execute(
            "SELECT COUNT(*) AS c FROM users WHERE last_deposit_at >= ?",
            (today_start.isoformat(), )).fetchone()
        new_users_today = int(row["c"] if row and row["c"] is not None else 0)

        active_7d = new_users_7d
        active_today = new_users_today
    except Exception:
        new_users_7d = 0
        new_users_today = 0
        active_7d = 0
        active_today = 0

    # Whale/minnow segmentation
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE user_id != ? AND balance >= 1000",
        (bot.user.id, )).fetchone()
    whales = int(row["c"] if row and row["c"] is not None else 0)

    row = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE user_id != ? AND balance > 0 AND balance <= 1",
        (bot.user.id, )).fetchone()
    minnows = int(row["c"] if row and row["c"] is not None else 0)

    # Uptime and process metrics
    uptime_seconds = int(time.time() -
                         getattr(__builtins__, "_bot_start_time", time.time()))
    uptime_human = _humanize_seconds(uptime_seconds)

    mem_used_str = cpu_used_str = "—"
    try:
        if psutil:
            p = psutil.Process()
            mem_info = p.memory_info()
            mem_used_str = f"{mem_info.rss / (1024*1024):.1f} MB"
            p.cpu_percent(interval=None)
            cpu_pct = p.cpu_percent(interval=0.1)
            cpu_used_str = f"{cpu_pct:.1f}%"
    except Exception:
        pass

    # DB PRAGMAs
    journal_mode = _fetch_pragma_scalar(conn, "journal_mode")
    foreign_keys = _fetch_pragma_scalar(conn, "foreign_keys")
    synchronous = _fetch_pragma_scalar(conn, "synchronous")
    cache_size = _fetch_pragma_scalar(conn, "cache_size")
    busy_timeout = _fetch_pragma_scalar(conn, "busy_timeout")

    row = conn.execute(
        "SELECT value FROM meta WHERE key='schema_version'").fetchone()
    schema_ver = (row["value"] if row else "unknown")

    # Build embed
    embed = discord.Embed(title="📊 Bot Global Stats",
                          color=0x00FF99,
                          timestamp=datetime.now(timezone.utc))
    embed.set_author(name="Quanta Bot • System Overview")
    embed.set_thumbnail(url="https://cryptologos.cc/logos/solana-sol-logo.png")

    # Treasury & Supply
    embed.add_field(
        name="🏦 Treasury",
        value=(f"• Bot QC Balance: `{bot_balance:,.3f} QC`\n"
               f"• Treasury Share: `{bot_share_pct:.2f}%`\n"
               f"• Largest Holder Share: `{largest_share_pct:.2f}%`"),
        inline=False)
    embed.add_field(
        name="💱 Circulation",
        value=(f"• Total QC in Circulation: `{total_qc_circ:,.3f} QC`\n"
               f"• User-held QC: `{user_circ:,.3f} QC`\n"
               f"• Top-10 Concentration: `{top10_conc:.2f}%`\n"
               f"• Gini (inequality): `{gini:.3f}`"),
        inline=False)

    # Users & Segments
    embed.add_field(
        name="👥 Users",
        value=(f"• Total Users: `{total_users:,}`\n"
               f"• With Balance > 0: `{nonzero_users:,}`\n"
               f"• Avg Balance (excl. bot): `{avg_user_balance:,.3f} QC`\n"
               f"• Median Balance: `{median_balance:,.3f} QC`"),
        inline=True)
    embed.add_field(name="🧭 Activity",
                    value=(f"• Active Today (deposits): `{active_today:,}`\n"
                           f"• Active 7d (deposits): `{active_7d:,}`\n"
                           f"• New Users Today: `{new_users_today:,}`\n"
                           f"• New Users 7d: `{new_users_7d:,}`"),
                    inline=True)
    embed.add_field(name="🐳 Whales & 🐟 Minnows",
                    value=(f"• Whales (≥1,000 QC): `{whales:,}`\n"
                           f"• Minnows (≤1 QC): `{minnows:,}`"),
                    inline=True)

    # Deposits / Withdrawals / Gameplay
    embed.add_field(name="📥 Deposits / 📤 Withdrawals",
                    value=(f"• Total Deposited: `{total_depo:,.3f} QC`\n"
                           f"• Total Withdrawn: `{total_withdraw:,.3f} QC`\n"
                           f"• Depo/Withd Ratio: `{ratio_str}`"),
                    inline=True)
    embed.add_field(name="🎲 Gameplay",
                    value=(f"• Total Wagered: `{total_wagered:,.3f} QC`\n"
                           f"• Net P/L (all users): `{net_pl_sum:,.3f} QC`"),
                    inline=True)

    # SOL Activity — always visible, plus recent depositors list
    last_dep_str = "—"
    if last_dep:
        try:
            last_dep_str = f"<@{last_dep['user_id']}> at `{last_dep['last_deposit_at']}`\n• Sig: `{last_dep['last_deposit_signature'] or '—'}`"
        except Exception:
            last_dep_str = "—"

    recent_lines = []
    if recent_rows:
        for r in recent_rows:
            try:
                recent_lines.append(
                    f"• <@{r['user_id']}> — `{r['last_deposit_at']}`")
            except Exception:
                continue
    recent_block = "\n".join(
        recent_lines) if recent_lines else "No recent depositors."

    embed.add_field(
        name="🔗 SOL Activity",
        value=(f"• Total SOL Deposited: `{total_sol_deposited:,.6f} SOL`\n"
               f"• Last Deposit: {last_dep_str}\n"
               f"• Recent Depositors:\n{recent_block}"),
        inline=False)

    # Lottery
    embed.add_field(
        name="🎟️ Lottery",
        value=(f"• Active Lotteries: `{lot_active}`\n"
               f"• Total Pot (all time): `{lot_pot_total:,.3f} QC`\n"
               f"• Total Entries (all time): `{lot_entries:,}`\n"
               f"• Last Winner: {last_winner_str}"),
        inline=False)

    # Leaderboard (Top 10)
    if top_rows:
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        lb_lines = []
        for i, r in enumerate(top_rows, 0):
            uid = r["user_id"]
            bal = float(r["balance"])
            m = medals[i] if i < len(medals) else f"{i+1}."
            lb_lines.append(f"{m} <@{uid}> — `{bal:,.3f} QC`")
        embed.add_field(name="🏅 Top Holders",
                        value="\n".join(lb_lines),
                        inline=False)
    else:
        embed.add_field(name="🏅 Top Holders",
                        value="No users found.",
                        inline=False)

    # System / Uptime / Process
    fk_flag = "ON" if str(_fetch_pragma_scalar(
        conn, "foreign_keys")).lower() in ("1", "on", "true") else "OFF"
    embed.add_field(name="🕒 Uptime", value=f"`{uptime_human}`", inline=True)

    mem_cpu = f"• Memory: `{mem_used_str}`\n• CPU: `{cpu_used_str}`"
    embed.add_field(name="🧠 Process", value=mem_cpu, inline=True)

    embed.add_field(name="🧰 Database",
                    value=(f"• Path: `{DB_PATH}`\n"
                           f"• Schema Version: `{schema_ver}`\n"
                           f"• Journal Mode: `{journal_mode}`\n"
                           f"• Foreign Keys: `{fk_flag}`\n"
                           f"• Synchronous: `{synchronous}`\n"
                           f"• Cache Size: `{cache_size}`\n"
                           f"• Busy Timeout: `{busy_timeout} ms`"),
                    inline=False)

    # Risk flags
    risk_msgs = []
    if bot_share_pct := (bot_balance / total_qc_circ *
                         100.0) if total_qc_circ else 0.0:
        if bot_share_pct >= 50:
            risk_msgs.append("High treasury dominance (≥50%).")
    if top10_conc >= 70:
        risk_msgs.append("High top-10 concentration (≥70%).")
    if gini >= 0.9:
        risk_msgs.append("Extreme inequality (Gini ≥0.90).")
    if risk_msgs:
        embed.add_field(name="⚠️ Risk Flags",
                        value="• " + "\n• ".join(risk_msgs),
                        inline=False)

    embed.set_footer(
        text="System snapshot • All values computed from local database")
    await ctx.send(embed=embed)


# ===== PROFILE PRIVACY FEATURE =====
_profile_privacy = set()  # store user IDs who have privacy enabled


@bot.command(name="profile_restrict")
async def profile_restrict_cmd(ctx):
    """Toggle profile view restriction for yourself."""
    uid = ctx.author.id
    if uid in _profile_privacy:
        _profile_privacy.remove(uid)
        await ctx.send(
            "🔓 Your profile is now **public**. Others can view it with `!profile @you`."
        )
    else:
        _profile_privacy.add(uid)
        await ctx.send(
            "🔒 Your profile is now **private**. Others cannot view it with `!profile @you`."
        )


@bot.command(name="profile", aliases=["me"])
async def profile_cmd(ctx, member: discord.Member = None):
    """
    Show a QC user profile (self or mentioned user) with balance, wagers,
    profit/loss, SOL info, ranking, and more. Respects profile privacy settings.
    """
    target = member or ctx.author

    # After you've retrieved the profile target (example variable name "target_user")

    # Privacy check: block viewing others if they've set profile to private
    if target.id != ctx.author.id and target.id in _profile_privacy:
        return await ctx.send(
            f"🔒 {target.display_name} has set their profile to private.")

    try:
        u = fetch_user(target.id)
        if not u:
            return await ctx.send(f"❌ No profile found for {target.mention}.")

        # Main QC stats
        qc_bal = float(u.get("balance", 0.0))
        sol_equiv = qc_bal * 0.001  # 1 QC = 0.001 SOL (adjust if needed)
        total_deposited = float(u.get("total_depo", 0.0))
        total_withdrawn = float(u.get("total_withdraw", 0.0))
        total_wagered = float(u.get("total_wagered", 0.0))
        net_pnl = float(u.get("net_profit_loss", 0.0))
        sol_address = u.get("sol_address")

        # Display server join date if present; fallback to account creation date
        if getattr(target, "joined_at", None):
            join_or_created_label = "📅 This Server Join Date"
            join_or_created_value = discord.utils.format_dt(
                target.joined_at, style="R")  # relative time
        else:
            join_or_created_label = "🆔 Account Created"
            join_or_created_value = discord.utils.format_dt(
                target.created_at, style="R")  # relative time

        # Fetch live SOL balance for deposit address (best-effort)
        live_sol_balance = 0.0
        if sol_address:
            try:
                live_sol_balance = await get_live_sol_balance(sol_address)
            except Exception:
                pass

        # Rank by QC balance
        rank = None
        try:
            conn = get_conn()
            row = conn.execute(
                "SELECT COUNT(*) + 1 AS rank FROM users WHERE balance > ?",
                (qc_bal, )).fetchone()
            if row:
                # sqlite3.Row or dict-like; handle both
                rank = row["rank"] if isinstance(row, dict) or hasattr(
                    row, "keys") else row[0]
        except Exception:
            rank = "—"

        # Live SOL price to fiat conversions (best-effort)
        fiat_lines = []
        try:
            async with aiohttp.ClientSession() as session:
                prices = await fetch_sol_price(session, SUPPORTED_FIATS)
                symbols = {
                    "usd": "$",
                    "eur": "€",
                    "gbp": "£",
                    "aud": "A$",
                    "inr": "₹"
                }
                for fiat, symbol in symbols.items():
                    p = prices.get(fiat)
                    if p:
                        fiat_lines.append(
                            f"{fiat.upper()}: {symbol}{sol_equiv * p:,.2f}")
        except Exception:
            pass

        # Build embed
        embed = discord.Embed(
            title=f"💳 {target.display_name}'s QuantaCoin Profile",
            colour=discord.Colour.gold(),
            description="Your account summary and on-chain stats")
        if target.display_avatar:
            embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="🏦 QC Balance",
                        value=f"{qc_bal:.3f} QC",
                        inline=True)
        embed.add_field(name="💠 SOL Equivalent",
                        value=f"{sol_equiv:.6f} SOL",
                        inline=True)
        embed.add_field(name="🌍 Fiat Value",
                        value=" |  ".join(fiat_lines) if fiat_lines else "—",
                        inline=False)

        embed.add_field(name="📥 Total Deposited",
                        value=f"{total_deposited:.3f} QC",
                        inline=True)
        embed.add_field(name="📤 Total Withdrawn",
                        value=f"{total_withdrawn:.3f} QC",
                        inline=True)
        embed.add_field(name="🎲 Total Wagered",
                        value=f"{total_wagered:.3f} QC",
                        inline=True)

        sign = "+" if net_pnl >= 0 else ""
        embed.add_field(name="📈 Net Profit/Loss",
                        value=f"{sign}{net_pnl:.3f} QC",
                        inline=True)
        embed.add_field(
            name="🏅 Rank",
            value=f"#{rank}" if isinstance(rank, int) else str(rank or "—"),
            inline=True)
        embed.add_field(name=join_or_created_label,
                        value=join_or_created_value,
                        inline=True)

        embed.add_field(name="💳 Deposit Address", value=f"`{sol_address}`")

        embed.set_footer(
            text=
            "Use !profile_restrict to toggle privacy. Or use !help to know more about the commands. "
        )
        await ctx.send(embed=embed)

        # EXTRA MESSAGE for special user
        special_id = 1252301575955812534
        if target.id == special_id and ctx.author.id != special_id:
            await ctx.send(
                f"🌟 **{target.display_name}** is a special person who played a key role in development. 🙌 Thank you for your support certified Queen 👑 !"
            )

        judge_id = 644780286072193045
        if target.id == judge_id and ctx.author.id != special_id:
            await ctx.send(
                f"🌟 **{target.display_name}** is a certified fucker and a Judge."
            )

    except Exception as e:
        await ctx.send(f"❌ Failed to load profile: `{e}`")


#======lottery

# ========= FLEXIBLE LOTTERY (persistent, variable cost/duration, auto-payout with DM) =========
import asyncio
import random
import sqlite3
import time
from datetime import datetime, timezone


# ---------------- Schema ----------------
def _lottery_init_schema():
    conn = get_conn()
    with _transaction() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS lottery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,                  -- 'open', 'settled', 'cancelled'
            entry_cost REAL NOT NULL,              -- QC per entry (e.g., 0.001, 1, etc.)
            pot REAL NOT NULL DEFAULT 0,           -- QC collected
            created_at INTEGER NOT NULL,           -- epoch seconds
            ends_at INTEGER NOT NULL,              -- epoch seconds
            winner_id INTEGER,                     -- after settlement
            channel_id INTEGER                     -- channel used to start/announce
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS lottery_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lottery_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            FOREIGN KEY(lottery_id) REFERENCES lottery(id)
        )
        """)


# Try to initialize immediately (safe if DB not yet ready; will retry later)
try:
    _lottery_init_schema()
except Exception as e:
    log.warning(f"[LOTTERY] Schema init at import deferred: {e}")


def _utc_now() -> int:
    return int(time.time())


# ---------------- Helpers ----------------
def _parse_duration_to_seconds(s: str) -> int:
    """
    Accepts:
      - '30s', '10m', '1h', '2d', '1w' (case-insensitive)
      - plain seconds, e.g., '600'
    Returns seconds (int).
    """
    s = s.strip().lower()
    if not s:
        raise ValueError("Duration is required.")
    if s.isdigit():
        val = int(s)
        if val <= 0:
            raise ValueError("Duration must be positive.")
        return val
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    try:
        num = float(s[:-1])
        suffix = s[-1]
        if suffix not in units or num <= 0:
            raise ValueError
        return int(num * units[suffix])
    except Exception:
        raise ValueError(
            "Invalid duration. Use 30s, 10m, 1h, 2d, 1w, or seconds.")


def _lottery_get_open() -> dict | None:
    row = get_conn().execute(
        "SELECT * FROM lottery WHERE status='open' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else None


def _lottery_get_by_id(lottery_id: int) -> dict | None:
    row = get_conn().execute("SELECT * FROM lottery WHERE id=?",
                             (lottery_id, )).fetchone()
    return dict(row) if row else None


def _lottery_create(entry_cost: float, duration_seconds: int,
                    channel_id: int | None) -> int:
    now = _utc_now()
    ends = now + duration_seconds
    with _transaction() as cur:
        cur.execute(
            "INSERT INTO lottery (status, entry_cost, pot, created_at, ends_at, channel_id) "
            "VALUES (?,?,?,?,?,?)",
            ("open", float(entry_cost), 0.0, now, ends, channel_id))
        return cur.lastrowid


def _lottery_add_entry(lottery_id: int, user_id: int):
    with _transaction() as cur:
        cur.execute(
            "INSERT INTO lottery_entries (lottery_id, user_id, created_at) VALUES (?,?,?)",
            (lottery_id, user_id, _utc_now()))


def _lottery_fetch_entries(lottery_id: int) -> list[int]:
    rows = get_conn().execute(
        "SELECT user_id FROM lottery_entries WHERE lottery_id=?",
        (lottery_id, )).fetchall()
    return [r["user_id"] if hasattr(r, "keys") else r[0] for r in rows]


def _lottery_increment_pot(lottery_id: int, delta_qc: float):
    with _transaction() as cur:
        cur.execute("UPDATE lottery SET pot = pot + ? WHERE id=?",
                    (float(delta_qc), lottery_id))


def _lottery_mark_settled(lottery_id: int, winner_id: int | None):
    with _transaction() as cur:
        cur.execute(
            "UPDATE lottery SET status='settled', winner_id=? WHERE id=?",
            (winner_id, lottery_id))


def _lottery_time_left(ends_at_epoch: int) -> str:
    remaining = max(0, ends_at_epoch - _utc_now())
    units = [("w", 604800), ("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    parts = []
    for label, secs in units:
        if remaining >= secs:
            v = remaining // secs
            remaining -= v * secs
            parts.append(f"{v}{label}")
    return " ".join(parts) if parts else "0s"


# ---------------- Settlement Loop ----------------
async def _lottery_settlement_loop():
    await bot.wait_until_ready()
    # Ensure schema again when bot is fully ready
    try:
        _lottery_init_schema()
    except Exception as e:
        log.error(f"[LOTTERY] Schema init in on_ready failed: {e}")

    while not bot.is_closed():
        try:
            lot = _lottery_get_open()
            if lot and _utc_now() >= int(lot["ends_at"]):
                entries = _lottery_fetch_entries(lot["id"])
                winner_id = None
                pot = float(lot["pot"] or 0.0)

                if entries:
                    winner_id = random.choice(entries)

                    # Pay the pot from bot balance to winner
                    if pot > 0:
                        bot_bal = fetch_user(bot.user.id)["balance"]
                        pay = min(pot, bot_bal)
                        if pay > 0:
                            update_balance(bot.user.id, -pay)
                            update_balance(winner_id, pay)
                            update_stats(winner_id, net_profit_loss=pay)

                    # DM winner best-effort
                    try:
                        if winner_id:
                            user = bot.get_user(winner_id)
                            if user:
                                await user.send(
                                    f"🎉 You won the lottery! Prize: {pot:.6f} QC\n"
                                    f"Congratulations!")
                    except Exception as dm_err:
                        log.warning(f"[LOTTERY] DM to winner failed: {dm_err}")

                _lottery_mark_settled(lot["id"], winner_id)

                # Announce settlement in the channel (best-effort)
                try:
                    ch_id = lot.get("channel_id")
                    if ch_id:
                        ch = bot.get_channel(int(ch_id))
                        if ch:
                            mention = f"<@{winner_id}>" if winner_id else "—"
                            await ch.send(
                                f"🏁 Lottery ended. Pot: {pot:.6f} QC • Winner: {mention}"
                            )
                except Exception as e:
                    log.warning(f"[LOTTERY] Channel announce failed: {e}")

            await asyncio.sleep(5)
        except Exception as e:
            log.error(f"[LOTTERY] Settlement loop error: {e}")
            await asyncio.sleep(5)


# ---------------- Commands ----------------
@bot.command(name="lottery")
async def lottery_cmd(ctx, entry_cost: float = 1.0, duration: str = "10m"):
    """
    Start a lottery with <entry_cost> QC per entry, lasting <duration>.
    Examples:
      !lottery                 -> 1.0 QC each, 10 minutes
      !lottery 0.001 1h        -> 0.001 QC each, 1 hour
      !lottery 5 30s           -> 5 QC each, 30 seconds
      !lottery 2 1d            -> 2 QC each, 1 day
      !lottery 0.5 1w          -> 0.5 QC each, 1 week
      !lottery 3 600           -> 3 QC each, 600 seconds
    """
    _lottery_init_schema()

    if entry_cost <= 0:
        return await ctx.send("❌ Entry cost must be positive.")

    open_lot = _lottery_get_open()
    if open_lot:
        tl = _lottery_time_left(int(open_lot["ends_at"]))
        return await ctx.send(
            f"🎟️ A lottery is already open | Entry: {float(open_lot['entry_cost']):.6f} QC | "
            f"Time left: {tl}\nJoin with `!join`.")

    try:
        secs = _parse_duration_to_seconds(duration)
    except ValueError as ve:
        return await ctx.send(f"❌ {ve}")

    lot_id = _lottery_create(entry_cost=float(entry_cost),
                             duration_seconds=secs,
                             channel_id=ctx.channel.id)
    lot = _lottery_get_by_id(lot_id)
    ends_at = int(lot["ends_at"])
    await ctx.send(f"🎉 Lottery started!\n"
                   f"• Entry: {float(lot['entry_cost']):.6f} QC each\n"
                   f"• Ends: <t:{ends_at}:R> • <t:{ends_at}:f>\n"
                   f"Join with `!join`")


@bot.command(name="join", aliases=["join_lottery"])
async def join_cmd(ctx):
    """Enter the open lottery by paying exactly the configured entry cost."""
    _lottery_init_schema()
    lot = _lottery_get_open()
    if not lot:
        return await ctx.send(
            "❌ No open lottery. Start one with `!lottery <entry_cost> <duration>`."
        )

    cost = float(lot["entry_cost"])
    uid = ctx.author.id
    u = fetch_user(uid)

    if u["balance"] < cost:
        return await ctx.send(f"❌ Insufficient QC. Need {cost:.6f} QC.")

    try:
        update_balance(uid, -cost)
        update_balance(bot.user.id, cost)
        update_stats(uid, total_wagered=cost)
        _lottery_add_entry(lot["id"], uid)
        _lottery_increment_pot(lot["id"], cost)
    except Exception as e:
        return await ctx.send(f"❌ Failed to join lottery: {e}")
    ends_at = int(lot["ends_at"])

    tl = _lottery_time_left(int(lot["ends_at"]))
    await ctx.send(
        f"✅ {ctx.author.mention} entered for {cost:.6f} QC. Result in: <t:{ends_at}:R>"
    )


@bot.command(name="lottery_status", aliases=["lottery_info"])
async def lottery_status_cmd(ctx):
    """Show the current lottery or last settled one."""
    _lottery_init_schema()
    lot = _lottery_get_open()
    if lot:
        entries = _lottery_fetch_entries(lot["id"])
        ends_at = int(lot["ends_at"])
        return await ctx.send(f"🎟️ Lottery is OPEN\n"
                              f"• Entry: {float(lot['entry_cost']):.6f} QC\n"
                              f"• Pot: {float(lot['pot']):.6f} QC\n"
                              f"• Entries: {len(entries)}\n"
                              f"• Ends: <t:{ends_at}:R> • <t:{ends_at}:f>\n"
                              f"Join with `!join`")

    row = get_conn().execute(
        "SELECT * FROM lottery WHERE status='settled' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if not row:
        return await ctx.send(
            "ℹ️ No lottery is open and no history yet. Start one with `!lottery`."
        )
    d = dict(row)
    ended = datetime.fromtimestamp(int(
        d["ends_at"]), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    win_txt = f"<@{d['winner_id']}>" if d.get("winner_id") else "—"
    await ctx.send(
        f"ℹ️ No lottery open.\nLast result: Winner {win_txt} • Pot {float(d['pot']):.6f} QC • Ended: {ended}"
    )


# Ensure the settlement loop is running (safe retry if bot.loop not yet available)
try:
    bot.loop.create_task(_lottery_settlement_loop())
except Exception as e:
    log.warning(f"[LOTTERY] Deferred settlement loop start: {e}")

# === AIRDROP MODULE (Robust, Fixed, Ready-to-Use) ===
import time
import random
import string
import re
import asyncio
import aiohttp
import discord
from discord.ext import commands

# ---------------- Config ----------------
QC_PER_SOL = 1000.0  # 1 SOL = 1000 QC
AIR_MIN_SECONDS = 1
AIR_MAX_SECONDS = 90 * 24 * 3600  # ~3 months
AIR_ID_LEN = 10


# ---------------- Time Helpers ----------------
def _air_ts() -> int:
    return int(time.time())


def _air_fmt_seconds(secs: int) -> str:
    secs = max(0, int(secs))
    units = [("w", 604800), ("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    parts = []
    for label, s in units:
        if secs >= s:
            v = secs // s
            secs -= v * s
            parts.append(f"{v}{label}")
    return " ".join(parts) if parts else "0s"


def _air_human_time(ts: int) -> str:
    return f"<t:{int(ts)}:f> (in {_air_fmt_seconds(max(0, ts - _air_ts()))})"


def _air_unique_id() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(AIR_ID_LEN))


# ---------------- Parsing ----------------
_TIME_UNITS = {
    "s": 1,
    "sec": 1,
    "secs": 1,
    "second": 1,
    "seconds": 1,
    "m": 60,
    "min": 60,
    "mins": 60,
    "minute": 60,
    "minutes": 60,
    "h": 3600,
    "hr": 3600,
    "hrs": 3600,
    "hour": 3600,
    "hours": 3600,
    "d": 86400,
    "day": 86400,
    "days": 86400,
    "w": 604800,
    "week": 604800,
    "weeks": 604800,
    "mon": 2592000,
    "month": 2592000,
    "months": 2592000,
}


def _air_parse_duration(s: str) -> int:
    s = (s or "").strip().lower()
    parts = re.findall(r"(\d+(?:\.\d+)?)\s*([a-z]+)", s)
    if not parts:
        raise ValueError("Invalid duration.")
    total = 0
    for num, unit in parts:
        if unit not in _TIME_UNITS:
            raise ValueError(f"Unknown time unit '{unit}'")
        total += int(float(num) * _TIME_UNITS[unit])
    if total <= 0:
        raise ValueError("Duration must be positive.")
    return total


async def _usd_to_qc(usd_amount: float) -> float:
    async with aiohttp.ClientSession() as session:
        prices = await fetch_sol_price(session, ["usd"])
    usd_per_sol = float(prices.get("usd") or 0.0)
    if usd_per_sol <= 0:
        raise RuntimeError("Live SOL price unavailable.")
    sol = usd_amount / usd_per_sol
    return sol * QC_PER_SOL


async def _air_parse_amount_to_qc(amount_token, unit_token) -> float:
    # Normalize tokens to strings
    if isinstance(amount_token, (list, tuple)):
        amount_token = " ".join(map(str, amount_token))
    else:
        amount_token = str(amount_token)
    if isinstance(unit_token, (list, tuple)):
        unit_token = " ".join(map(str, unit_token))
    elif unit_token is not None:
        unit_token = str(unit_token)

    raw = amount_token.strip().lower()
    has_dollar = "$" in raw
    amt_str = raw.replace("$", "").strip()
    if not amt_str:
        raise ValueError("Invalid amount.")
    amt = float(amt_str)
    unit = (unit_token or "").strip().lower()

    # Explicit units
    if unit in ("qc", "quanta", "quantacoin", "quanta-coin"):
        return amt
    if unit == "sol":
        return amt * QC_PER_SOL
    # USD path if $ present or unit is "$"
    if has_dollar or unit == "$":
        return await _usd_to_qc(amt)
    # Default to QC
    return amt


# ---------------- DB ----------------
def _airdrop_init_schema():
    with _transaction() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS airdrop(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT UNIQUE,
            status TEXT,
            amount_qc REAL,
            created_at INTEGER,
            ends_at INTEGER,
            created_by INTEGER,
            channel_id INTEGER,
            guild_id INTEGER,
            scope TEXT,
            message_id INTEGER
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS airdrop_claims(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airdrop_id INTEGER,
            user_id INTEGER,
            joined_at INTEGER,
            UNIQUE(airdrop_id,user_id)
        )""")


def _airdrop_create(unique_id,
                    amount_qc,
                    duration,
                    created_by,
                    channel_id,
                    guild_id,
                    scope="local"):
    now = _air_ts()
    ends = now + int(duration)
    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO airdrop (unique_id,status,amount_qc,created_at,ends_at,created_by,channel_id,guild_id,scope,message_id)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (unique_id, "open", float(amount_qc), now, ends, int(created_by),
              int(channel_id) if channel_id else None,
              int(guild_id) if guild_id else None, scope, None))
        return cur.lastrowid


def _airdrop_save_message_id(airdrop_pk: int, message_id: int):
    with _transaction() as cur:
        cur.execute("UPDATE airdrop SET message_id=? WHERE id=?",
                    (int(message_id), int(airdrop_pk)))


def _airdrop_get_by_unique(uid: str):
    row = get_conn().execute("SELECT * FROM airdrop WHERE unique_id=?",
                             (uid, )).fetchone()
    return dict(row) if row else None


def _airdrop_list_open():
    rows = get_conn().execute(
        "SELECT * FROM airdrop WHERE status='open' ORDER BY ends_at").fetchall(
        )
    return [dict(r) for r in rows] if rows else []


def _airdrop_recent(limit: int = 5):
    rows = get_conn().execute("SELECT * FROM airdrop ORDER BY id DESC LIMIT ?",
                              (int(limit), )).fetchall()
    return [dict(r) for r in rows] if rows else []


def _airdrop_add_claim(airdrop_pk: int, user_id: int):
    with _transaction() as cur:
        cur.execute(
            "INSERT OR IGNORE INTO airdrop_claims (airdrop_id,user_id,joined_at) VALUES (?,?,?)",
            (int(airdrop_pk), int(user_id), _air_ts()))


def _airdrop_fetch_claimants(airdrop_pk: int):
    rows = get_conn().execute(
        "SELECT user_id FROM airdrop_claims WHERE airdrop_id=?",
        (int(airdrop_pk), )).fetchall()
    out = []
    for r in rows:
        try:
            out.append(int(r["user_id"]))
        except Exception:
            out.append(int(r[0]))
    return out


def _airdrop_set_status(airdrop_pk: int, status: str):
    with _transaction() as cur:
        cur.execute("UPDATE airdrop SET status=? WHERE id=?",
                    (str(status), int(airdrop_pk)))


# ---------------- Join View ----------------
class AirdropJoinView(discord.ui.View):

    def __init__(self, unique_id: str, timeout: float | None = 300):
        super().__init__(timeout=timeout)
        self.unique_id = unique_id

    @discord.ui.button(label="Join Airdrop", style=discord.ButtonStyle.success)
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        uid = (self.unique_id or "").strip().upper()
        d = _airdrop_get_by_unique(uid)
        if not d:
            return await interaction.response.send_message(
                "❌ This airdrop no longer exists.", ephemeral=True)
        if d["status"] != "open":
            return await interaction.response.send_message(
                "ℹ️ This airdrop has ended.", ephemeral=True)
        # Scope enforcement
        if (d.get("scope") or "local") != "public":
            if not interaction.guild or (int(d.get("guild_id") or 0)
                                         != interaction.guild.id):
                return await interaction.response.send_message(
                    "🚫 This airdrop is local to another server.",
                    ephemeral=True)
        try:
            _airdrop_add_claim(d["id"], interaction.user.id)
        except Exception as e:
            return await interaction.response.send_message(
                f"❌ Failed to join: {e}", ephemeral=True)
        tl = _air_fmt_seconds(max(0, int(d["ends_at"]) - _air_ts()))
        await interaction.response.send_message(
            f"✅ {interaction.user.mention} joined `{d['unique_id']}` • Ends in {tl}",
            ephemeral=True)


def make_airdrop_join_view(unique_id: str,
                           live_seconds: int = 300) -> AirdropJoinView:
    return AirdropJoinView(unique_id=unique_id, timeout=live_seconds)


# ---------------- Result embed + edit ----------------
def _air_result_embed(d: dict, claimants: list[int]) -> discord.Embed:
    total_qc = float(d["amount_qc"] or 0.0)
    cc = len(claimants)
    desc = (f"• ID: `{d['unique_id']}`\n"
            f"• Amount: `{total_qc:.3f} QC`\n"
            f"• Created: <t:{int(d['created_at'])}:f>\n"
            f"• Ended: <t:{int(d['ends_at'])}:f>\n"
            f"• Status: Settled ✅\n"
            f"• Claimants: {cc}")
    e = discord.Embed(title="🎁 Airdrop Result",
                      description=desc,
                      color=discord.Color.green())
    if cc:
        names = ", ".join(f"<@{u}>" for u in claimants[:25])
        if cc > 25:
            names += f" … (+{cc-25} more)"
        e.add_field(name="Joined Users", value=names, inline=False)
        e.set_footer(text="Payout split equally among claimants.")
    else:
        e.set_footer(
            text=
            "No claimants. Funds returned to user. Do !airdrop_verify to verify the airdop"
        )
    return e


async def _edit_to_result(d: dict, claimants: list[int]):
    # Construct final embed and remove any components by setting view=None
    embed = _air_result_embed(d, claimants)
    ch_id, msg_id = d.get("channel_id"), d.get("message_id")
    if not ch_id:
        return
    ch = bot.get_channel(int(ch_id))
    if not ch:
        return
    if not msg_id:
        try:
            await ch.send(embed=embed)
        except Exception:
            pass
        return
    try:
        original = await ch.fetch_message(int(msg_id))
        # Critical: remove all buttons by passing view=None during edit[1][2]
        await original.edit(embed=embed, view=None)
    except Exception:
        # If fetch or edit fails, at least post the result
        try:
            await ch.send(embed=embed)
        except Exception:
            pass


# ---------------- Commands ----------------
@bot.command(name="airdrop")
async def airdrop_cmd(ctx, amount: str, *rest):
    """
    Create an airdrop from treasury.
    Examples:
    !airdrop 0.1$ 10s
    !airdrop $1 qc 1m
    !airdrop 1$ sol 10 hr
    !airdrop 1$ 2 mon
    !airdrop 0.1 qc 10s
    Add 'public' at the end for cross-server scope.
    """
    import re

    # 1) Collect tokens
    tokens = [t for t in rest if isinstance(t, str)]

    # 2) Optional trailing scope
    scope = "local"
    if tokens and tokens[-1].lower() == "public":
        scope = "public"
        tokens = tokens[:-1]

    # 3) Optional unit token immediately after amount (letters or $ only)
    unit = None
    if tokens and re.fullmatch(r"[A-Za-z$]+", tokens[0]):
        unit = tokens[0]
        tokens = tokens[1:]

    # 4) Remaining tokens are duration
    dur_str = " ".join(tokens).strip()
    if not dur_str:
        return await ctx.send(
            "❌ Missing duration. Example: `!airdrop 0.1$ 10s` or `!airdrop 0.1 qc 10s`"
        )

    # Convert duration to seconds
    try:
        secs = _air_parse_duration(dur_str)
    except Exception:
        return await ctx.send(
            "❌ Invalid duration. Use 10s, 5m, 1h, 2 mon, etc.")

    # Validate duration bounds
    if not (AIR_MIN_SECONDS <= secs <= AIR_MAX_SECONDS):
        return await ctx.send("❌ Duration must be between 1s and ~3 months.")

    # 5) Convert amount to QC
    try:
        amount_qc = await _air_parse_amount_to_qc(amount, unit)
    except Exception as e:
        return await ctx.send(f"❌ Amount error: {e}")

    if amount_qc <= 0:
        return await ctx.send("❌ Amount must be positive.")

    # 6) Treasury check
    user_qc = fetch_user(ctx.author.id)["balance"]
    if user_qc < amount_qc:
        return await ctx.send(
            f"❌ Insufficient funds. Need {amount_qc:.3f} QC; have {user_qc:.3f} QC."
        )
    update_balance(ctx.author.id, -amount_qc)

    # 8) Create airdrop record
    uid = _air_unique_id()
    try:
        pk = _airdrop_create(
            unique_id=uid,
            amount_qc=amount_qc,
            duration=secs,
            created_by=ctx.author.id,
            channel_id=(ctx.channel.id if ctx.guild else None),
            guild_id=(ctx.guild.id if ctx.guild else None),
            scope=scope)
    except Exception as e:
        update_balance(ctx.author.id, amount_qc)
        return await ctx.send(f"❌ Failed to create: {e}")

    # 9) Announce with button
    d = _airdrop_get_by_unique(uid)
    ends = int(d["ends_at"])
    scope_str = "Public 🌐" if scope == "public" else "Local 🏠"
    embed = discord.Embed(
        title="🎁 Airdrop Created",
        description=(
            f"ID: `{uid}`\n"
            f"Amount: **{amount_qc:.3f} QC** reserved\n"
            f"Ends: {_air_human_time(ends)}\n"
            f"Scope: {scope_str}\n\n"
            f"▶ Click below (or use `!join_airdrop {uid}`) to participate."),
        color=discord.Color.teal())
    live_seconds = min(max(30, ends - _air_ts()), 900)
    msg = await ctx.send(embed=embed,
                         view=make_airdrop_join_view(uid, live_seconds))
    try:
        _airdrop_save_message_id(pk, msg.id)
    except Exception:
        pass


@bot.command(name="join_airdrop", aliases=["airdrop_join"])
async def join_airdrop_cmd(ctx, unique_id: str):
    d = _airdrop_get_by_unique((unique_id or "").strip().upper())
    if not d:
        return await ctx.send("❌ No such airdrop.")
    if d["status"] != "open":
        return await ctx.send("ℹ️ That airdrop has already ended.")
    if (d.get("scope") or "local") != "public":
        if not ctx.guild or (int(d.get("guild_id") or 0) != ctx.guild.id):
            return await ctx.send("🚫 This airdrop is local to another server.")
    try:
        _airdrop_add_claim(d["id"], ctx.author.id)
    except Exception as e:
        return await ctx.send(f"❌ Failed to join: {e}")
    tl = _air_fmt_seconds(max(0, int(d["ends_at"]) - _air_ts()))
    await ctx.send(
        f"✅ {ctx.author.mention} joined `{d['unique_id']}` • Ends in {tl}")


@bot.command(name="airdrop_status", aliases=["a_status", "a_info"])
async def airdrop_status_cmd(ctx):
    opens = _airdrop_list_open()
    if opens:
        lines = []
        for d in opens:
            tl = _air_fmt_seconds(max(0, int(d["ends_at"]) - _air_ts()))
            scope_emoji = "🌐" if (d.get("scope")
                                  or "local") == "public" else "🏠"
            lines.append(
                f"• `{d['unique_id']}` • {float(d['amount_qc']):.3f} QC • Ends in {tl} • {scope_emoji} {d.get('scope')}"
            )
        e = discord.Embed(title="🎁 Airdrops (OPEN)",
                          description="\n".join(lines),
                          color=discord.Color.teal())
        return await ctx.send(embed=e)
    rec = _airdrop_recent(limit=3)
    if rec:
        rows = [
            f"• `{d['unique_id']}` • {d['status']} • {float(d['amount_qc']):.3f} QC • Ended <t:{int(d['ends_at'])}:f>"
            for d in rec
        ]
        e = discord.Embed(title="🎁 Airdrops (No open)",
                          description="\n".join(rows),
                          color=discord.Color.greyple())
        return await ctx.send(embed=e)
    await ctx.send("ℹ️ No airdrop history yet.")


@bot.command(name="airdrop_verify", aliases=["a_verify"])
async def airdrop_verify_cmd(ctx, unique_id: str):
    d = _airdrop_get_by_unique((unique_id or "").strip().upper())
    if not d:
        return await ctx.send("❌ No airdrop found with that ID.")
    claimants = _airdrop_fetch_claimants(d["id"])
    scope = d.get("scope") or "local"
    e = discord.Embed(
        title="🔎 Airdrop Verification",
        description=(
            f"• ID: `{d['unique_id']}`\n"
            f"• Status: `{d['status']}`\n"
            f"• Amount: `{float(d['amount_qc']):.3f} QC`\n"
            f"• Created: <t:{int(d['created_at'])}:f>\n"
            f"• Ends: <t:{int(d['ends_at'])}:f>\n"
            f"• Creator: <@{int(d['created_by'])}>\n"
            f"• Scope: {'Public 🌐' if scope=='public' else 'Local 🏠'}"),
        color=discord.Color.blurple())
    if claimants:
        e.add_field(name="Total Claimants",
                    value=str(len(claimants)),
                    inline=True)
        sample = ", ".join(
            f"<@{u}>"
            for u in claimants[:25]) + (" …" if len(claimants) > 25 else "")
        e.add_field(name="Joined Users (sample)",
                    value=sample or "—",
                    inline=False)
    else:
        e.add_field(name="Claimants", value="None", inline=False)
    await ctx.send(embed=e)


@bot.command(name="airdrop_cancel", aliases=["a_cancel", "cancel_airdrop"])
@commands.guild_only()
async def airdrop_cancel_cmd(ctx, unique_id: str):
    """
    Cancel an open airdrop and refund its reserved QC to the treasury.
    Usage:
      !airdrop_cancel ABC1234
    Permissions:
      - Creator of the airdrop, or
      - Users with Manage Guild permission.
    """
    uid = (unique_id or "").strip().upper()
    if not uid:
        return await ctx.send(
            "❌ Please provide a valid airdrop ID. Example: `!airdrop_cancel ABC1234567`"
        )

    d = _airdrop_get_by_unique(uid)
    if not d:
        return await ctx.send("❌ No airdrop found with that ID.")

    if d["status"] != "open":
        return await ctx.send(
            "ℹ️ This airdrop is not open (already settled or canceled).")

    # Permission check: creator or Manage Guild
    is_creator = int(d.get("created_by") or 0) == ctx.author.id
    has_manage_guild = ctx.author.guild_permissions.manage_guild if ctx.guild else False
    if not (is_creator or has_manage_guild):
        return await ctx.send(
            "🚫 Only the creator or a user with Manage Server can cancel this airdrop."
        )

    # Compute refund: whatever is still reserved in the airdrop
    total_qc = float(d.get("amount_qc") or 0.0)

    # Mark canceled first to stop the settlement loop from touching it
    _airdrop_set_status(d["id"], "canceled")

    # Refund all reserved funds to treasury (bot account)
    if total_qc > 0:
        try:
            update_balance(bot.user.id, total_qc)
        except Exception:
            # If refund fails, we still proceed, but inform the channel
            await ctx.send(
                "⚠️ Airdrop canceled, but refund to treasury may have failed. Please check logs."
            )

    # Try to edit original message to show Canceled and remove components
    async def _edit_to_canceled(dd: dict):
        ch_id, msg_id = dd.get("channel_id"), dd.get("message_id")
        cancel_desc = (f"• ID: `{dd['unique_id']}`\n"
                       f"• Amount: `{float(dd['amount_qc']):.3f} QC`\n"
                       f"• Created: <t:{int(dd['created_at'])}:f>\n"
                       f"• Status: Canceled ⛔")
        embed = discord.Embed(title="🎁 Airdrop Canceled",
                              description=cancel_desc,
                              color=discord.Color.red())
        if not ch_id:
            return
        ch = bot.get_channel(int(ch_id))
        if not ch:
            return
        if not msg_id:
            try:
                await ch.send(embed=embed)
            except Exception:
                pass
            return
        try:
            original = await ch.fetch_message(int(msg_id))
            await original.edit(embed=embed, view=None)
        except Exception:
            try:
                await ch.send(embed=embed)
            except Exception:
                pass

    await _edit_to_canceled(d)
    await ctx.send(f"✅ Airdrop `{uid}` canceled and refunded to treasury.")


# ---------------- Settlement Loop ----------------
async def _airdrop_loop():
    _airdrop_init_schema()
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            now = _air_ts()
            for d in _airdrop_list_open():
                if now >= int(d["ends_at"]):
                    total_qc = float(d["amount_qc"] or 0.0)
                    claimants = _airdrop_fetch_claimants(d["id"])
                    paid = 0.0
                    if claimants and total_qc > 0:
                        share = total_qc / len(claimants)
                        for uid in claimants:
                            try:
                                update_balance(uid, share)
                                update_stats(uid, net_profit_loss=share)
                                paid += share
                            except Exception:
                                # Continue paying others even if one credit fails
                                pass
                        dust = max(0.0, total_qc - paid)
                        if dust > 0:
                            update_balance(int(d["created_by"]), dust)

                    else:
                        if total_qc > 0:
                            update_balance(int(d["created_by"]), total_qc)

                    _airdrop_set_status(d["id"], "settled")
                    await _edit_to_result(d, claimants)
            await asyncio.sleep(3)
        except Exception:
            # Avoid tight failure loops
            await asyncio.sleep(5)


# Recommended startup: create background task in setup_hook to avoid loop issues[10]
if hasattr(bot, "setup_hook"):

    async def _airdrop_setup_hook():
        bot.loop.create_task(_airdrop_loop())

    bot.setup_hook = _airdrop_setup_hook  # type: ignore[attr-defined]
else:
    # Fallback for older discord.py
    @bot.event
    async def on_ready():
        # Create once on first ready
        if not getattr(bot, "_airdrop_loop_started", False):
            bot.loop.create_task(_airdrop_loop())
            bot._airdrop_loop_started = True  # type: ignore[attr-defined]


# === END AIRDROP MODULE ===

#=====END OF AIRDROP

#--------GAMES


# ─GAMESSSS
class TicTacToeView(discord.ui.View):

    def __init__(self, game, wager, ctx, opponent):
        super().__init__(timeout=None)  # No auto-timeout
        self.game = game
        self.wager = wager
        self.ctx = ctx
        self.opponent = opponent
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for i in range(9):
            label = self.game.board[i] if self.game.board[i] != " " else "⬛"
            style = (discord.ButtonStyle.secondary
                     if label == "⬛" else discord.ButtonStyle.success
                     if label == "X" else discord.ButtonStyle.danger)
            button = discord.ui.Button(label=label,
                                       style=style,
                                       row=i // 3,
                                       custom_id=str(i))
            button.callback = self.make_callback(i)
            self.add_item(button)

    def make_callback(self, pos):

        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.game.turn:
                await interaction.response.send_message("❌ Not your turn!",
                                                        ephemeral=True)
                return

            valid, result = self.game.make_move(interaction.user.id, pos)
            if not valid:
                await interaction.response.send_message(f"❌ {result}",
                                                        ephemeral=True)
                return

            self.update_buttons()
            content = f"{self.ctx.author.mention} (X) vs {self.opponent.mention} (O)"

            if self.game.game_over:
                # Disable all buttons after game ends
                for child in self.children:
                    child.disabled = True

                if self.game.winner is None:
                    # Draw → refund wagers
                    if self.wager > 0:
                        update_balance(self.game.player1_id, self.wager)
                        update_balance(self.game.player2_id, self.wager)
                    content += "\n🤝 It's a draw!"
                else:
                    # Someone won
                    winner_id = self.game.winner
                    winner_mention = interaction.guild.get_member(
                        winner_id).mention
                    if self.wager > 0:
                        update_balance(winner_id, self.wager * 2)
                        content += f"\n💰 {winner_mention} won {self.wager:.3f} QuantaCoin and has been credited!"
                    else:
                        content += f"\n🏆 {winner_mention} wins!"

            await interaction.response.edit_message(content=content, view=self)

        return callback


@bot.command(name="tictactoe", aliases=["ttt"])
async def tictactoe_cmd(ctx, opponent: discord.Member, wager: float = 0):
    """
    Start a button-based TicTacToe game with an opponent.
    Optional QC wager (only deducted once at match start).
    """
    # Can't challenge yourself
    if opponent.id == ctx.author.id:
        return await ctx.send("❌ You cannot challenge yourself.")

    # Reject negative wagers
    if wager < 0:
        return await ctx.send("❌ Wager must be a positive number.")

    # QC balance check if wager > 0
    if wager > 0:
        p1 = fetch_user(ctx.author.id)
        p2 = fetch_user(opponent.id)

        if p1["balance"] < wager:
            return await ctx.send(
                f"❌ {ctx.author.mention} doesn't have enough QC.")
        if p2["balance"] < wager:
            return await ctx.send(
                f"❌ {opponent.mention} doesn't have enough QC.")

        # Deduct wager from both players now — single deduction
        update_balance(ctx.author.id, -wager)
        update_balance(opponent.id, -wager)

    # Create game instance
    import random
    game = TicTacToe(ctx.author.id, opponent.id)

    # Randomize first turn
    game.turn = random.choice([ctx.author.id, opponent.id])

    # Create and attach view
    view = TicTacToeView(game, wager, ctx, opponent)
    starter_mention = ctx.guild.get_member(game.turn).mention

    await ctx.send(
        f"🎮 **TicTacToe Started!**\n"
        f"{ctx.author.mention} (X) vs {opponent.mention} (O)\n"
        f"{starter_mention} goes first!",
        view=view)


# === KENO (Provably Fair with 1% House Edge, supports 'auto' picks) ===
import hmac
import hashlib
import secrets
import time
import re
import asyncio
import discord
from discord.ext import commands

_last_keno_play: dict[int, dict] = {}

# === Config ===
KENO_ALLOWED_PICKS = 6
KENO_POOL_MIN = 1
KENO_POOL_MAX = 40
KENO_DRAWS = 8
KENO_MIN_WAGER = 0.005
KENO_MAX_WAGER = 100_000
KENO_TIMEOUT = 60
KENO_HOUSE_EDGE = 0.01  # 1% house edge (applied on wins)

# Multipliers for exactly 6 picks (base multipliers; house edge applied afterwards)
KENO_PAYOUTS_6 = {
    0: 0,
    1: 0,
    2: 1.2,
    3: 2.5,
    4: 10,
    5: 100,
    6: 800,
}

# ===== Provably Fair (PF) state for Keno =====
_keno_pf_state: dict[int, dict] = {
}  # user_id -> {server_seed, server_hash, client_seed, nonce}


def keno_pf_new_commitment(user_id: int) -> dict:
    """
    Create a fresh PF commitment (server_seed, server_hash, client_seed, nonce=0) for this user.
    """
    server_seed = secrets.token_hex(32)
    server_hash = hashlib.sha256(server_seed.encode()).hexdigest()
    client_seed = f"{user_id}-{int(time.time())}-{secrets.token_hex(4)}"
    _keno_pf_state[user_id] = {
        "server_seed": server_seed,
        "server_hash": server_hash,
        "client_seed": client_seed,
        "nonce": 0
    }
    return _keno_pf_state[user_id]


def keno_pf_get_or_create(user_id: int) -> dict:
    return _keno_pf_state.get(user_id) or keno_pf_new_commitment(user_id)


def keno_pf_set_client_seed(user_id: int, client_seed: str):
    st = keno_pf_get_or_create(user_id)
    st["client_seed"] = client_seed
    st["nonce"] = 0  # reset nonce when changing client seed


def _keno_pf_hmac_hex(server_seed: str, message: str) -> str:
    return hmac.new(server_seed.encode(),
                    msg=message.encode(),
                    digestmod=hashlib.sha256).hexdigest()


def keno_generate_draw(user_id: int) -> tuple[set[int], int]:
    """
    Deterministic draw of KENO_DRAWS unique numbers within KENO_POOL_MIN..KENO_POOL_MAX
    using HMAC(server_seed, f"{client_seed}:{nonce}:{chunk_index}") to produce a byte stream.
    Returns (draw_set, nonce_used). Increments nonce after use.
    """
    st = keno_pf_get_or_create(user_id)
    server_seed = st["server_seed"]
    client_seed = st["client_seed"]
    nonce = st["nonce"]

    draw = set()
    chunk_index = 0
    while len(draw) < KENO_DRAWS:
        digest_hex = _keno_pf_hmac_hex(server_seed,
                                       f"{client_seed}:{nonce}:{chunk_index}")
        # Consume digest in 4-hex-byte chunks (2 bytes) to map into pool range
        for i in range(0, len(digest_hex), 8):
            part = digest_hex[i:i + 8]
            if len(part) < 8:
                continue
            val = int(part, 16)
            rng_num = (val %
                       (KENO_POOL_MAX - KENO_POOL_MIN + 1)) + KENO_POOL_MIN
            draw.add(rng_num)
            if len(draw) >= KENO_DRAWS:
                break
        chunk_index += 1

    st["nonce"] += 1
    return draw, nonce


# === Utility funcs ===
def _format_number_list(nums):
    return ", ".join(str(n) for n in sorted(nums)) if nums else "—"


def _render_draw_with_highlight(draw_set, picks_set):
    return " ".join(
        (f"✅{n}" if n in picks_set else f"🔲{n}") for n in sorted(draw_set))


def _parse_amount_str(s: str, user_balance: float) -> float:
    s = s.strip().lower()
    if s == "all":
        return user_balance
    return float(s)


def _parse_picks_str(s: str):
    s = s.strip().rstrip(")")
    raw = re.split(r"[, \s]+", s)
    nums = []
    for token in raw:
        if token:
            nums.append(int(token))
    return nums


def _validate_picks(nums):
    if len(nums) != KENO_ALLOWED_PICKS:
        return False, f"❌ Exactly {KENO_ALLOWED_PICKS} numbers are required."
    if len(set(nums)) != len(nums):
        return False, "❌ Invalid numbers (numbers repeated)."
    for n in nums:
        if not (KENO_POOL_MIN <= n <= KENO_POOL_MAX):
            return False, f"❌ Numbers must be between {KENO_POOL_MIN}-{KENO_POOL_MAX}."
    return True, ""


def _calc_multiplier(matches: int) -> float:
    return float(KENO_PAYOUTS_6.get(matches, 0))


def get_bot_qc_balance() -> float:
    BOT_USER_ID = bot.user.id
    return fetch_user(BOT_USER_ID)["balance"]


# === Commands ===
@bot.command(name="keno_payout")
async def keno_payout_cmd(ctx):
    embed = discord.Embed(title=f"🎯 Keno Payouts ({KENO_ALLOWED_PICKS} picks)",
                          color=discord.Color.gold(),
                          description="Payout = wager × multiplier × (1−1%)")
    lines = []
    for hits in sorted(KENO_PAYOUTS_6.keys()):
        lines.append(f"- {hits} hits → x{KENO_PAYOUTS_6[hits]:g}")
    embed.add_field(name="Table", value="\n".join(lines), inline=False)
    await ctx.send(embed=embed)


@bot.command(name="keno_seed")
async def keno_seed_cmd(ctx, *, client_seed: str):
    """Set your Keno client seed for provable fairness."""
    if not client_seed or len(client_seed) > 64:
        return await ctx.send("❌ Invalid seed. Max length 64.")
    keno_pf_set_client_seed(ctx.author.id, client_seed.strip())
    st = keno_pf_get_or_create(ctx.author.id)
    await ctx.send(f"✅ Keno client seed set.\n"
                   f"PF Server Hash: `{st['server_hash']}`\n"
                   f"Nonce reset to 0.")


@bot.command(name="keno")
async def keno_cmd(ctx):
    """
    Conversational Keno (Provably Fair, 1% house edge):
    1) Ask QC amount
    2) Ask for exactly 6 unique numbers between 1–40 (type 'auto' to let the bot pick)
    3) PF draw using HMAC(server_seed, f"{client_seed}:{nonce}:{chunk}")
    4) Payout from bot balance; refund if bot can't cover
    5) Reveal seeds for verification
    """
    user_id = ctx.author.id
    u = fetch_user(user_id)
    st = keno_pf_get_or_create(user_id)  # ensure PF commitment exists

    # STEP 1 — Ask wager
    await ctx.send(f"{ctx.author.mention} Amount of QC? (number or 'all')")

    def amt_check(m: discord.Message):
        return m.author.id == user_id and m.channel.id == ctx.channel.id

    try:
        amt_msg = await bot.wait_for("message",
                                     check=amt_check,
                                     timeout=KENO_TIMEOUT)
    except asyncio.TimeoutError:
        return await ctx.send("⏰ Timed out waiting for amount.")

    try:
        wager = _parse_amount_str(amt_msg.content, u["balance"])
    except Exception:
        return await ctx.send("❌ Invalid amount. Enter a number or 'all'.")

    if wager < KENO_MIN_WAGER:
        return await ctx.send(f"❌ Minimum wager is {KENO_MIN_WAGER:.3f} QC.")
    if wager > KENO_MAX_WAGER:
        return await ctx.send(f"❌ Maximum wager is {KENO_MAX_WAGER:.3f} QC.")
    if u["balance"] < wager:
        return await ctx.send(
            f"❌ Insufficient QC. Balance: {u['balance']:.3f} QC.")

    # Deduct now (wager goes to bot)
    update_balance(user_id, -wager)
    update_balance(bot.user.id, wager)
    update_stats(user_id, total_wagered=wager)

    # STEP 2 — Ask picks (supports 'auto')
    await ctx.send(
        f"Pick {KENO_ALLOWED_PICKS} numbers between {KENO_POOL_MIN} and {KENO_POOL_MAX} (comma-separated), or type `auto`."
    )

    def picks_check(m: discord.Message):
        return m.author.id == user_id and m.channel.id == ctx.channel.id

    while True:
        try:
            picks_msg = await bot.wait_for("message",
                                           check=picks_check,
                                           timeout=KENO_TIMEOUT)
        except asyncio.TimeoutError:
            # Refund wager if user doesn't finish
            update_balance(user_id, wager)
            update_balance(bot.user.id, -wager)
            return await ctx.send(
                "⏰ Timed out waiting for numbers. Wager refunded.")

        content = picks_msg.content.strip().lower()
        if content == "auto":
            # Bot generates a valid random set of picks
            import random as _r
            auto_nums = sorted(
                _r.sample(range(KENO_POOL_MIN, KENO_POOL_MAX + 1),
                          KENO_ALLOWED_PICKS))
            await ctx.send(
                f"🤖 Auto picks selected: `{_format_number_list(auto_nums)}`")
            nums = auto_nums
        else:
            try:
                nums = _parse_picks_str(picks_msg.content)
            except Exception:
                await ctx.send(
                    "❌ Invalid format. Example: 2, 1, 3, 4, 5, 6 (or type `auto`)"
                )
                continue

        ok, err = _validate_picks(nums)
        if not ok:
            await ctx.send(err)
            await ctx.send("↩️ Choose again or type `auto`:")
            continue

        picks = set(nums)
        break

    # STEP 3 — PF Draw
    draw, nonce_used = keno_generate_draw(user_id)
    matches = len(draw & picks)
    mult = _calc_multiplier(matches)
    # Apply 1% house edge on wins
    payout = wager * mult * (1.0 - KENO_HOUSE_EDGE)

    # STEP 4 — Payout logic
    prize_paid = False
    if payout > 0:
        bot_balance = get_bot_qc_balance()
        if payout > bot_balance:
            await ctx.send(
                "❌ Not enough bot balance to payout, please contact admin.")
            # Refund wager (cancel round)
            update_balance(user_id, wager)
            update_balance(bot.user.id, -wager)
            return
        else:
            update_balance(user_id, payout)
            update_balance(bot.user.id, -payout)
            update_stats(user_id, net_profit_loss=(payout - wager))
            prize_paid = True
    else:
        update_stats(user_id, net_profit_loss=(-wager))

    _last_keno_play[user_id] = {"wager": wager, "picks": picks}

    # STEP 5 — Results (embed + PF reveal)
    draw_display = _render_draw_with_highlight(draw, picks)
    embed = discord.Embed(
        title="🎰 Keno Result (Provably Fair, 1% HE)",
        color=discord.Color.green() if prize_paid else discord.Color.red(),
        description=
        (f"- Wager: `{wager:.3f}` QC\n"
         f"- Your picks: {_format_number_list(picks)}\n"
         f"- Drawn ({KENO_DRAWS}): {draw_display}\n"
         f"- Matches: `{matches}`  •  Multiplier: `x{mult:g}`\n"
         f"- {'🏆 Won: ' + f'`{payout:.3f}` QC' if prize_paid else '❌ Lost'}\n"
         f"• Payout formula: wager × multiplier × (1−1%)"))
    embed.add_field(
        name="🔒 PF Commitment (before roll)",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce_used: `{nonce_used}`",
        inline=False)
    embed.add_field(
        name="🔓 PF Reveal (after roll)",
        value=
        f"server_seed: `{st['server_seed']}`\nUse `!keno_verify` to check.",
        inline=False)
    embed.set_footer(
        text=
        "Fairness: draw = HMAC(server_seed, f'{client_seed}:{nonce}:{chunk}')")
    await ctx.send(embed=embed)


@bot.command(name="keno_reroll")
async def keno_reroll_cmd(ctx):
    """
    Reuse last wager and picks; performs a fresh PF draw using the next nonce (1% house edge).
    """
    user_id = ctx.author.id
    u = fetch_user(user_id)

    if user_id not in _last_keno_play:
        return await ctx.send(
            "❌ No previous Keno game found. Play one with `!keno` first.")

    wager = _last_keno_play[user_id]["wager"]
    picks = _last_keno_play[user_id]["picks"]

    if u["balance"] < wager:
        return await ctx.send(
            f"❌ Insufficient QC. Balance: {u['balance']:.3f} QC.")

    # Deduct again (new round)
    update_balance(user_id, -wager)
    update_balance(bot.user.id, wager)
    update_stats(user_id, total_wagered=wager)

    # PF state exists
    st = keno_pf_get_or_create(user_id)

    # Fresh PF draw
    draw, nonce_used = keno_generate_draw(user_id)
    matches = len(draw & picks)
    mult = _calc_multiplier(matches)
    payout = wager * mult * (1.0 - KENO_HOUSE_EDGE)

    prize_paid = False
    if payout > 0:
        bot_balance = get_bot_qc_balance()
        if payout > bot_balance:
            await ctx.send(
                "❌ Not enough bot balance to payout, please contact admin.")
            # Refund
            update_balance(user_id, wager)
            update_balance(bot.user.id, -wager)
            return
        else:
            update_balance(user_id, payout)
            update_balance(bot.user.id, -payout)
            update_stats(user_id, net_profit_loss=(payout - wager))
            prize_paid = True
    else:
        update_stats(user_id, net_profit_loss=(-wager))

    draw_display = _render_draw_with_highlight(draw, picks)
    embed = discord.Embed(
        title="🎰 Keno Reroll (Provably Fair, 1% HE)",
        color=discord.Color.green() if prize_paid else discord.Color.red(),
        description=
        (f"- Wager: `{wager:.3f}` QC\n"
         f"- Your picks: {_format_number_list(picks)}\n"
         f"- Drawn ({KENO_DRAWS}): {draw_display}\n"
         f"- Matches: `{matches}`  •  Multiplier: `x{mult:g}`\n"
         f"- {'🏆 Won: ' + f'`{payout:.3f}` QC' if prize_paid else '❌ Lost'}\n"
         f"• Payout formula: wager × multiplier × (1−1%)"))
    embed.add_field(
        name="🔒 PF Commitment (before roll)",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce_used: `{nonce_used}`",
        inline=False)
    embed.add_field(
        name="🔓 PF Reveal (after roll)",
        value=
        f"server_seed: `{st['server_seed']}`\nUse `!keno_verify` to check.",
        inline=False)
    embed.set_footer(
        text=
        "Fairness: draw = HMAC(server_seed, f'{client_seed}:{nonce}:{chunk}')")
    await ctx.send(embed=embed)


@bot.command(name="keno_verify")
async def keno_verify_cmd(ctx,
                          server_seed: str = None,
                          client_seed: str = None,
                          nonce: int = None):
    """
    Verify Keno fairness:
    Usage:
      - Without args, uses your last PF state (current nonce-1).
      - Or provide: !keno_verify <server_seed> <client_seed> <nonce>
    Recomputes the deterministic draw for comparison.
    """
    user_id = ctx.author.id
    st = _keno_pf_state.get(user_id)

    if server_seed is not None and client_seed is not None and nonce is not None:
        use_server_seed = server_seed.strip()
        use_client_seed = client_seed.strip()
        try:
            use_nonce = int(nonce)
        except Exception:
            return await ctx.send("❌ Nonce must be an integer.")
    else:
        if not st:
            return await ctx.send(
                "❌ No PF state found. Run `!keno` first or provide seeds and nonce."
            )
        use_server_seed = st["server_seed"]
        use_client_seed = st["client_seed"]
        use_nonce = max(0, st["nonce"] - 1)

    # Recompute draw deterministically
    draw = set()
    chunk_index = 0
    while len(draw) < KENO_DRAWS:
        digest_hex = _keno_pf_hmac_hex(
            use_server_seed, f"{use_client_seed}:{use_nonce}:{chunk_index}")
        for i in range(0, len(digest_hex), 8):
            part = digest_hex[i:i + 8]
            if len(part) < 8:
                continue
            val = int(part, 16)
            rng_num = (val %
                       (KENO_POOL_MAX - KENO_POOL_MIN + 1)) + KENO_POOL_MIN
            draw.add(rng_num)
            if len(draw) >= KENO_DRAWS:
                break
        chunk_index += 1

    embed = discord.Embed(
        title="🔎 Keno Fairness Verification",
        color=discord.Color.blurple(),
        description=
        ("Recomputed draw for the given seeds and nonce.\n"
         "Compare with your result embed: if it matches, the round was provably fair."
         ))
    embed.add_field(name="server_seed",
                    value=f"`{use_server_seed}`",
                    inline=False)
    embed.add_field(name="client_seed",
                    value=f"`{use_client_seed}`",
                    inline=False)
    embed.add_field(name="nonce", value=f"`{use_nonce}`", inline=False)
    embed.add_field(name=f"Drawn ({KENO_DRAWS})",
                    value=" ".join(str(n) for n in sorted(draw)),
                    inline=False)
    embed.set_footer(
        text=
        "Fairness rule: draw = HMAC(server_seed, f'{client_seed}:{nonce}:{chunk}')"
    )
    await ctx.send(embed=embed)


# ===== LIMBO GAME (Corrected, ~50% Win Chance for mid targets) =====
import hmac
import hashlib
import time
import secrets
import discord
from typing import Optional

# ---- Config ----
LIMBO_HOUSE_EDGE = 0.01
LIMBO_VIEW_TIMEOUT = 120
LIMBO_IDLE_GIF = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTZlODVqNmlpZnVvOHR6b2J4cGlpNHl5ZmlyY3A3dXdtNzJiZWt5cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gwZoQmiNyymp12vukB/giphy.gif"
LIMBO_TAKEOFF_GIF = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmFobGx5ZnV1M3h1c204amtpYm9oZXhoOTJkcmY4YzN0N25tenh0aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KxHaSWSpTlEGc/giphy.gif"
LIMBO_BOOM_GIF = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExem80dXg4NDFqZTJ5YTB5N3VybXdtYmtua2R0aDM4bnNlendxYjgxdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Uk0qiMZ1yGkoPABua5/giphy.gif"
LIMBO_DEFAULT_TARGETS = [1.10, 1.50, 2.00, 3.00, 5.00, -1.0]
_limbo_active_sessions: set[int] = set()

# ---- PF State (in-memory for example) ----
_pf_state: dict[int, dict] = {}


def limbo_pf_new_commitment(user_id: int) -> dict:
    server_seed = secrets.token_hex(32)
    server_hash = hashlib.sha256(server_seed.encode()).hexdigest()
    client_seed = f"{user_id}-{int(time.time())}-{secrets.token_hex(4)}"
    _pf_state[user_id] = {
        "server_seed": server_seed,
        "server_hash": server_hash,
        "client_seed": client_seed,
        "nonce": 0
    }
    return _pf_state[user_id]


def limbo_pf_get_or_create(user_id: int) -> dict:
    return _pf_state.get(user_id) or limbo_pf_new_commitment(user_id)


def limbo_pf_set_client_seed(user_id: int, client_seed: str):
    st = limbo_pf_get_or_create(user_id)
    st["client_seed"] = client_seed
    st["nonce"] = 0


def _limbo_pf_hmac_hex(server_seed: str, message: str) -> str:
    return hmac.new(server_seed.encode(),
                    msg=message.encode(),
                    digestmod=hashlib.sha256).hexdigest()


# ---- Game Math ----
def limbo_generate_rng(user_id: int) -> float:
    """Return a PF RNG in [0,1) based on seeds."""
    st = limbo_pf_get_or_create(user_id)
    digest = _limbo_pf_hmac_hex(st["server_seed"],
                                f"{st['client_seed']}:{st['nonce']}")
    n = int(digest[:13], 16)
    return n / float(1 << 52)


def limbo_payout_amount(wager: float, target: float, win: bool) -> float:
    return (wager * target * (1.0 - LIMBO_HOUSE_EDGE)) if win else 0.0


# ---- UI ----
class LimboMultiplierSelect(discord.ui.Select):

    def __init__(self, owner_id: int):
        opts = [
            discord.SelectOption(label=f"{t:.2f}×", value=str(t))
            for t in LIMBO_DEFAULT_TARGETS if t > 0
        ]
        opts.append(discord.SelectOption(label="Custom…", value="custom"))
        super().__init__(placeholder="Pick multiplier", options=opts)
        self.owner_id = owner_id
        self.selected_target: Optional[float] = None

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Not your game.",
                                                           ephemeral=True)
        if self.values[0] == "custom":
            await interaction.response.send_modal(
                LimboCustomMultiplierModal(self))
        else:
            self.selected_target = float(self.values[0])
            await interaction.response.send_message(
                f"🎯 Target set: {self.selected_target:.2f}×", ephemeral=True)


class LimboCustomMultiplierModal(discord.ui.Modal, title="Custom Multiplier"):

    def __init__(self, select_ref: LimboMultiplierSelect):
        super().__init__()
        self.select_ref = select_ref
        self.multiplier_input = discord.ui.TextInput(label="Multiplier",
                                                     placeholder="1.50",
                                                     required=True)
        self.add_item(self.multiplier_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = float(self.multiplier_input.value)
            if not (1.02 <= val <= 100):
                raise ValueError
            self.select_ref.selected_target = round(val, 2)
            await interaction.response.send_message(
                f"🎯 Target set: {self.select_ref.selected_target:.2f}×",
                ephemeral=True)
        except:
            await interaction.response.send_message("❌ Invalid multiplier.",
                                                    ephemeral=True)


class LimboRollButton(discord.ui.Button):

    def __init__(self, owner_id: int, wager: float,
                 select: LimboMultiplierSelect):
        super().__init__(label="Roll", style=discord.ButtonStyle.primary)
        self.owner_id = owner_id
        self.wager = wager
        self.select = select

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Not your game.",
                                                           ephemeral=True)
        if not self.select.selected_target:
            return await interaction.response.send_message(
                "⚠️ Pick a target first.", ephemeral=True)
        if self.owner_id in _limbo_active_sessions:
            return await interaction.response.send_message(
                "⏳ Already playing.", ephemeral=True)
        _limbo_active_sessions.add(self.owner_id)
        try:
            target = self.select.selected_target
            u = fetch_user(self.owner_id)
            if u["balance"] < self.wager:
                return await interaction.response.send_message(
                    "❌ Not enough QC.", ephemeral=True)
            # Deduct wager
            update_balance(self.owner_id, -self.wager)
            update_balance(interaction.client.user.id, self.wager)
            update_stats(self.owner_id, total_wagered=self.wager)
            if (self.wager * target * (1 - LIMBO_HOUSE_EDGE)) > fetch_user(
                    interaction.client.user.id)["balance"]:
                update_balance(self.owner_id, self.wager)
                update_balance(interaction.client.user.id, -self.wager)
                return await interaction.response.send_message(
                    "❌ Bot can't cover payout. Contact admin anus_69 and dont delete this messgae.",
                    ephemeral=True)

            # PF RNG for win/loss
            st = limbo_pf_get_or_create(self.owner_id)
            rng = limbo_generate_rng(self.owner_id)

            # Target p(win) ~ (0.99 / target) for ~50% win near 2×
            p_win = (0.99 / target)
            win = rng <= p_win

            # Visual crash point (for fun only)
            crash = round(target + rng * target * 2, 2) if win else round(
                max(1.00, rng * target), 2)

            payout = limbo_payout_amount(self.wager, target, win)
            if win and payout > 0:
                update_balance(self.owner_id, payout)
                update_balance(interaction.client.user.id, -payout)
                update_stats(self.owner_id,
                             net_profit_loss=payout - self.wager)
            else:
                update_stats(self.owner_id, net_profit_loss=-self.wager)

            # Build result embed
            embed = discord.Embed(
                title="🚀 Limbo Result",
                colour=discord.Colour.green() if win else discord.Colour.red(),
                description=
                f"Wager: `{self.wager:.3f}` QC | Target: `{target:.2f}×` | Crash: `{crash:.2f}×`"
            )
            embed.set_image(url=LIMBO_TAKEOFF_GIF if win else LIMBO_BOOM_GIF)
            embed.add_field(name="Outcome",
                            value=(f"🏆 Won {payout:.3f} QC"
                                   if win else f"💥 Lost {self.wager:.3f} QC"),
                            inline=False)
            embed.add_field(
                name="PF Reveal",
                value=
                f"server_seed: `{st['server_seed']}`\nserver_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{st['nonce']}`",
                inline=False)
            embed.set_footer(
                text=
                f"House edge {LIMBO_HOUSE_EDGE*100:.0f}% | Win chance ≈ {p_win*100:.1f}%"
            )
            st["nonce"] += 1  # increment after use

            for c in self.view.children:
                c.disabled = True
            await interaction.response.edit_message(embed=embed,
                                                    view=self.view)
        finally:
            _limbo_active_sessions.discard(self.owner_id)


class LimboView(discord.ui.View):

    def __init__(self, owner_id: int, wager: float):
        super().__init__(timeout=LIMBO_VIEW_TIMEOUT)
        select = LimboMultiplierSelect(owner_id)
        self.add_item(select)
        self.add_item(LimboRollButton(owner_id, wager, select))

    async def on_timeout(self):
        for c in self.children:
            c.disabled = True


# ---- Commands ----
@bot.command(name="limbo")
async def limbo_cmd(ctx, amount: float):
    if amount <= 0:
        return await ctx.send("❌ Wager must be positive.")
    if fetch_user(ctx.author.id)["balance"] < amount:
        return await ctx.send("❌ Not enough QC.")
    st = limbo_pf_get_or_create(ctx.author.id)
    embed = discord.Embed(
        title="🚀 Limbo",
        colour=discord.Colour.gold(),
        description=
        f"Wager: `{amount:.3f}` QC\nPick multiplier, press Roll.\nPayout: wager × target × (1-{int(LIMBO_HOUSE_EDGE*100)}%)"
    )
    embed.set_image(url=LIMBO_IDLE_GIF)
    embed.add_field(name="PF Server Hash",
                    value=f"`{st['server_hash']}`",
                    inline=False)
    embed.add_field(name="Client Seed",
                    value=f"`{st['client_seed']}` (change with !limbo_seed)",
                    inline=False)
    await ctx.send(embed=embed, view=LimboView(ctx.author.id, amount))


@bot.command(name="limbo_seed")
async def limbo_seed_cmd(ctx, *, client_seed: str):
    if not client_seed or len(client_seed) > 64:
        return await ctx.send("❌ Invalid seed.")
    limbo_pf_set_client_seed(ctx.author.id, client_seed.strip())
    st = limbo_pf_get_or_create(ctx.author.id)
    await ctx.send(f"✅ Seed set. Server hash: `{st['server_hash']}`")


@bot.command(name="limbo_verify")
async def limbo_verify_cmd(ctx):
    """
    Interactive verifier:
    Asks for server_seed, client_seed, and nonce step-by-step.
    """

    def check_author(m):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

    # Step 1 — Ask for server_seed
    await ctx.send("🔍 Please input **server seed** (from PF Reveal):")
    try:
        msg = await bot.wait_for("message", check=check_author, timeout=60)
        server_seed = msg.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏰ Timed out waiting for server seed.")

    # Step 2 — Ask for client_seed
    await ctx.send("📥 Please input **client seed** (from PF Reveal):")
    try:
        msg = await bot.wait_for("message", check=check_author, timeout=60)
        client_seed = msg.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏰ Timed out waiting for client seed.")

    # Step 3 — Ask for nonce
    await ctx.send("🔢 Please input **nonce** (number from PF Reveal):")
    try:
        msg = await bot.wait_for("message", check=check_author, timeout=60)
        nonce = int(msg.content.strip())
    except asyncio.TimeoutError:
        return await ctx.send("⏰ Timed out waiting for nonce.")
    except ValueError:
        return await ctx.send("❌ Nonce must be an integer.")

    # --- Verification ---
    try:
        digest = _limbo_pf_hmac_hex(server_seed, f"{client_seed}:{nonce}")
        n = int(digest[:13], 16)
        rng = n / float(1 << 52)
        await ctx.send(
            f"✅ Verification complete!\n"
            f"**RNG:** `{rng:.10f}`\n"
            f"**Rule:** Win if `RNG <= (0.98 / target)` for that round.\n"
            f"Compare this RNG with your bet's target multiplier to confirm fairness."
        )
    except Exception as e:
        await ctx.send(f"❌ Verification failed: {e}")


#==========================================
# ========= UNIVERSAL PROVABLY-FAIR CASINO GAMES (1% House Edge baseline) =========
# Uses existing helpers from your bot:
# - fetch_user(user_id), update_balance(user_id, delta), update_stats(user_id, **fields)
# - get_bot_qc_balance(), bot (discord.py)
# Wagers are in QC; house edge applied to wins only.
# PF: HMAC-SHA256(server_seed, f"{client_seed}:{nonce}"), first 13 hex → int.

import hmac, hashlib, secrets, time
from typing import Dict, Any, List, Optional
import discord
from discord.ext import commands

HOUSE_EDGE = 0.01


# -------- Shared PF helpers --------
def _pf_new_commitment(state_dict: dict, user_id: int) -> dict:
    server_seed = secrets.token_hex(32)
    server_hash = hashlib.sha256(server_seed.encode()).hexdigest()
    client_seed = f"{user_id}-{int(time.time())}-{secrets.token_hex(4)}"
    state_dict[user_id] = {
        "server_seed": server_seed,
        "server_hash": server_hash,
        "client_seed": client_seed,
        "nonce": 0,
    }
    return state_dict[user_id]


def _pf_get_or_create(state_dict: dict, user_id: int) -> dict:
    return state_dict.get(user_id) or _pf_new_commitment(state_dict, user_id)


def _pf_hmac_int(server_seed: str, msg: str) -> int:
    h = hmac.new(server_seed.encode(), msg.encode(),
                 hashlib.sha256).hexdigest()
    return int(h[:13], 16)


def _ensure_funds_or_refund(ctx, user_id: int, wager: float,
                            needed: float) -> bool:
    if get_bot_qc_balance() < needed:
        # Refund wager
        update_balance(user_id, wager)
        update_balance(bot.user.id, -wager)
        return False
    return True


def _format_win_embed(title: str, win: bool, push: bool, wager: float,
                      payout: float, net: float) -> str:
    if push:
        return f"↔ Outcome: Push — refunded `{wager:.3f} QC` (Net 0.000 QC)"
    if win:
        return f"🏆 Outcome: YOU WON `{payout:.3f} QC` (Net {net:.3f} QC)"
    else:
        return f"💥 Outcome: You lost `{wager:.3f} QC` (Net -{wager:.3f} QC)"


# -------- Game registry for !games --------
_GAME_DESCRIPTIONS: Dict[str, Dict[str, Any]] = {}


def _register_game(key: str,
                   name: str,
                   aliases: List[str],
                   desc: str,
                   usage: str,
                   emoji: str = "🎮",
                   group: str = "Games"):
    _GAME_DESCRIPTIONS[key] = {
        "name": name,
        "aliases": aliases,
        "desc": desc,
        "usage": usage,
        "emoji": emoji,
        "group": group,
    }


# ==============================================================================
# 1) COINFLIP (aliases: cf)
_coin_pf_state: Dict[int, dict] = {}
_last_coinflip: Dict[int, dict] = {}


@bot.command(name="coinflip", aliases=["cf"])
async def coinflip_cmd(ctx, amount: float, choice: str):
    choice = choice.lower().strip()
    if choice not in ("heads", "tails"):
        return await ctx.send("❌ Choice must be heads/tails.")
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_coin_pf_state, ctx.author.id)
    used_nonce = st["nonce"]
    rng = _pf_hmac_int(st["server_seed"], f"{st['client_seed']}:{used_nonce}")
    st["nonce"] += 1

    result = "heads" if (rng % 2 == 0) else "tails"
    win = (choice == result)
    payout = amount * 2 * (1 - HOUSE_EDGE) if win else 0.0
    net = payout - amount

    if win and payout > 0:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_coinflip[ctx.author.id] = {"amount": amount, "choice": choice}

    embed = discord.Embed(
        title="🪙 Coinflip",
        description=f"You chose `{choice}`, result: `{result}`",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Result",
                    value=_format_win_embed("Coinflip", win, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{used_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !coinflip_verify <server_seed> <client_seed> <nonce> | Reroll with !coinflip_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="coinflip_reroll", aliases=["cf_reroll"])
async def coinflip_reroll_cmd(ctx):
    last = _last_coinflip.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous coinflip found for reroll.")
    await coinflip_cmd(ctx, last["amount"], last["choice"])


@bot.command(name="coinflip_verify", aliases=["cf_verify"])
async def coinflip_verify_cmd(ctx, server_seed: str, client_seed: str,
                              nonce: int):
    rng = _pf_hmac_int(server_seed.strip(),
                       f"{client_seed.strip()}:{int(nonce)}")
    result = "heads" if (rng % 2 == 0) else "tails"
    await ctx.send(f"✅ Coinflip verify: nonce {nonce} → `{result}`")


_register_game(
    key="coinflip",
    name="Coinflip",
    aliases=["cf"],
    desc="50/50 coin toss; win pays 2× minus 1%.",
    usage="!coinflip <amount> <heads|tails>",
    emoji="🪙",
    group="Quick bets",
)

# ==============================================================================
# 2) DICE (roll-under; aliases: d)
_dice_pf_state: Dict[int, dict] = {}
_last_dice: Dict[int, dict] = {}


@bot.command(name="dice", aliases=["d"])
async def dice_cmd(ctx, amount: float, target: int):
    if not (2 <= target <= 100):
        return await ctx.send("❌ Target must be 2–100.")
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_dice_pf_state, ctx.author.id)
    used_nonce = st["nonce"]
    rng = _pf_hmac_int(st["server_seed"], f"{st['client_seed']}:{used_nonce}")
    st["nonce"] += 1

    roll = (rng % 100) + 1
    win = (roll <= target)
    odds = target / 100.0
    payout_mult = (1 / odds) * (1 - HOUSE_EDGE)
    payout = amount * payout_mult if win else 0.0
    net = payout - amount

    if win and payout > 0:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_dice[ctx.author.id] = {"amount": amount, "target": target}

    embed = discord.Embed(
        title="🎲 Dice (Roll-under)",
        description=f"Roll: `{roll}` vs Target: `{target}`",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Result",
                    value=_format_win_embed("Dice", win, False, amount, payout,
                                            net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{used_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !dice_verify <server_seed> <client_seed> <nonce> <target> | Reroll with !d_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="d_reroll", aliases=["dice_reroll"])
async def dice_reroll_cmd(ctx):
    last = _last_dice.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous dice roll found for reroll.")
    await dice_cmd(ctx, last["amount"], last["target"])


@bot.command(name="dice_verify", aliases=["d_verify"])
async def dice_verify_cmd(ctx, server_seed: str, client_seed: str, nonce: int,
                          target: int):
    rng = _pf_hmac_int(server_seed.strip(),
                       f"{client_seed.strip()}:{int(nonce)}")
    roll = (rng % 100) + 1
    win = (roll <= target)
    await ctx.send(
        f"✅ Dice verify: nonce {nonce} → roll `{roll}` • Win vs {target}: {win}"
    )


_register_game(
    key="dice",
    name="Dice (Roll-under)",
    aliases=["d"],
    desc=
    "Pick target 2–100; win if roll ≤ target. Payout scales by odds, minus 1%.",
    usage="!dice <amount> <target>",
    emoji="🎲",
    group="Quick bets",
)

# ==============================================================================
# 3) BLACKJACK (auto 17+; aliases: bj)
_blackjack_pf_state: Dict[int, dict] = {}
_last_blackjack: Dict[int, dict] = {}


def _bj_draw_value(server_seed: str, client_seed: str, nonce: int) -> int:
    return (_pf_hmac_int(server_seed, f"{client_seed}:{nonce}") %
            13) + 1  # 1..13


@bot.command(name="blackjack", aliases=["bj"])
async def blackjack_cmd(ctx, amount: float):
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_blackjack_pf_state, ctx.author.id)
    used_start = st["nonce"]

    player_vals: List[int] = []
    n = st["nonce"]
    while sum(min(c, 10) for c in player_vals) < 17:
        player_vals.append(
            _bj_draw_value(st["server_seed"], st["client_seed"], n))
        n += 1

    dealer_vals: List[int] = []
    while sum(min(c, 10) for c in dealer_vals) < 17:
        dealer_vals.append(
            _bj_draw_value(st["server_seed"], st["client_seed"], n))
        n += 1

    st["nonce"] = n
    used_end = n - 1

    player_score = min(sum(min(c, 10) for c in player_vals), 21)
    dealer_score = min(sum(min(c, 10) for c in dealer_vals), 21)
    push = (player_score == dealer_score and player_score <= 21)
    win = (player_score <= 21) and (dealer_score > 21
                                    or player_score > dealer_score)

    if push:
        payout, net = amount, 0.0
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=0.0)
    elif win:
        payout = amount * 2 * (1 - HOUSE_EDGE)
        net = payout - amount
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)
        payout, net = 0.0, -amount

    _last_blackjack[ctx.author.id] = {"amount": amount}

    embed = discord.Embed(
        title="🂡 Blackjack",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(
        name="Your Hand",
        value=f"{[min(c,10) for c in player_vals]} → {player_score}",
        inline=True)
    embed.add_field(
        name="Dealer Hand",
        value=f"{[min(c,10) for c in dealer_vals]} → {dealer_score}",
        inline=True)
    embed.add_field(name="Result",
                    value=_format_win_embed("Blackjack", win, push, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce range: `{used_start}..{used_end}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !blackjack_verify <server_seed> <client_seed> <start_nonce> • Reroll with !bj_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="bj_reroll", aliases=["blackjack_reroll"])
async def blackjack_reroll_cmd(ctx):
    last = _last_blackjack.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous blackjack found for reroll.")
    await blackjack_cmd(ctx, last["amount"])


@bot.command(name="blackjack_verify", aliases=["bj_verify"])
async def blackjack_verify_cmd(ctx, server_seed: str, client_seed: str,
                               start_nonce: int):
    n = int(start_nonce)
    player_vals: List[int] = []
    while sum(min(c, 10) for c in player_vals) < 17:
        player_vals.append(
            (_pf_hmac_int(server_seed.strip(), f"{client_seed.strip()}:{n}") %
             13) + 1)
        n += 1
    dealer_vals: List[int] = []
    while sum(min(c, 10) for c in dealer_vals) < 17:
        dealer_vals.append(
            (_pf_hmac_int(server_seed.strip(), f"{client_seed.strip()}:{n}") %
             13) + 1)
        n += 1
    end_nonce = n - 1
    p = min(sum(min(c, 10) for c in player_vals), 21)
    d = min(sum(min(c, 10) for c in dealer_vals), 21)
    push = (p == d and p <= 21)
    win = (p <= 21) and (d > 21 or p > d)
    await ctx.send("✅ Blackjack verify:\n"
                   f"- Player: {[min(c,10) for c in player_vals]} → {p}\n"
                   f"- Dealer: {[min(c,10) for c in dealer_vals]} → {d}\n"
                   f"- Win: {win} • Push: {push}\n"
                   f"- Nonce range: {start_nonce}..{end_nonce}")


_register_game(
    key="blackjack",
    name="Blackjack",
    aliases=["bj"],
    desc="Auto-draw to 17+ vs dealer. Push refunds. 1% cut on wins.",
    usage="!blackjack <amount>",
    emoji="🂡",
    group="Table",
)

# ==============================================================================
# 4) HI-LO (aliases: hilo, hl)
_hilo_pf_state: Dict[int, dict] = {}
_last_hilo: Dict[int, dict] = {}


@bot.command(name="hilo", aliases=["hl"])
async def hilo_cmd(ctx, amount: float, guess: str):
    guess = guess.lower().strip()
    if guess not in ("higher", "lower"):
        return await ctx.send("❌ Guess must be 'higher' or 'lower'.")
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_hilo_pf_state, ctx.author.id)
    used_nonce = st["nonce"]
    draw = (_pf_hmac_int(st["server_seed"],
                         f"{st['client_seed']}:{used_nonce}") % 13) + 1
    st["nonce"] += 1

    win = False if draw == 7 else ((guess == "higher" and draw > 7) or
                                   (guess == "lower" and draw < 7))
    payout = amount * 2 * (1 - HOUSE_EDGE) if win else 0.0
    net = payout - amount

    if win and payout > 0:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_hilo[ctx.author.id] = {"amount": amount, "guess": guess}

    embed = discord.Embed(
        title="⬆⬇ Hi-Lo",
        description=f"Card: `{min(draw,10)}` (raw {draw}) vs guess `{guess}`",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Result",
                    value=_format_win_embed("Hi-Lo", win, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{used_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !hilo_verify <server_seed> <client_seed> <nonce> | Reroll with !hl_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="hl_reroll", aliases=["hilo_reroll"])
async def hilo_reroll_cmd(ctx):
    last = _last_hilo.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous Hi-Lo found for reroll.")
    await hilo_cmd(ctx, last["amount"], last["guess"])


@bot.command(name="hilo_verify", aliases=["hl_verify"])
async def hilo_verify_cmd(ctx, server_seed: str, client_seed: str, nonce: int):
    draw = (_pf_hmac_int(server_seed.strip(),
                         f"{client_seed.strip()}:{int(nonce)}") % 13) + 1
    await ctx.send(
        f"✅ Hi-Lo verify: nonce {nonce} → raw card {draw} (score {min(draw,10)})"
    )


_register_game(
    key="hilo",
    name="Hi‑Lo",
    aliases=["hl"],
    desc="Guess higher/lower than 7 (7 loses). Win pays 2× minus 1%.",
    usage="!hilo <amount> <higher|lower>",
    emoji="🔼",
    group="Quick bets",
)

# ==============================================================================
# 5) ROULETTE (aliases: roulette, r)
_roulette_pf_state: Dict[int, dict] = {}
_last_roulette: Dict[int, dict] = {}

_ROUGE = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


@bot.command(name="roulette", aliases=["r"])
async def roulette_cmd(ctx, amount: float, bet: str):
    bet = bet.lower().strip()
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    valid_simple = {"red", "black", "even", "odd"}
    num_bet: Optional[int] = None
    if bet not in valid_simple:
        try:
            nb = int(bet)
            if 0 <= nb <= 36:
                num_bet = nb
            else:
                return await ctx.send("❌ Number bet must be 0–36.")
        except:
            return await ctx.send(
                "❌ Bet must be red/black/even/odd or a number 0–36.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_roulette_pf_state, ctx.author.id)
    used_nonce = st["nonce"]
    raw = _pf_hmac_int(st["server_seed"], f"{st['client_seed']}:{used_nonce}")
    st["nonce"] += 1

    result_num = raw % 37
    color = "red" if result_num in _ROUGE else (
        "black" if result_num != 0 else "green")
    evenodd = ("even" if result_num != 0 and result_num % 2 == 0 else
               ("odd" if result_num % 2 == 1 else "zero"))

    if num_bet is not None:
        win = (result_num == num_bet)
        payout = amount * 36 * (1 - HOUSE_EDGE) if win else 0.0
    else:
        win = (bet == color) if bet in ("red", "black") else (bet == evenodd)
        payout = amount * 2 * (1 - HOUSE_EDGE) if win else 0.0

    net = payout - amount

    if win and payout > 0:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_roulette[ctx.author.id] = {"amount": amount, "bet": bet}

    embed = discord.Embed(
        title="🎡 Roulette",
        description=
        f"Result: `{result_num}` ({color}, {evenodd}) • Your bet: `{bet}`",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Result",
                    value=_format_win_embed("Roulette", win, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{used_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !roulette_verify <server_seed> <client_seed> <nonce> <bet> | Reroll with !r_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="r_reroll", aliases=["roulette_reroll"])
async def roulette_reroll_cmd(ctx):
    last = _last_roulette.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous roulette found for reroll.")
    await roulette_cmd(ctx, last["amount"], last["bet"])


@bot.command(name="roulette_verify", aliases=["r_verify"])
async def roulette_verify_cmd(ctx, server_seed: str, client_seed: str,
                              nonce: int, bet: str):
    raw = _pf_hmac_int(server_seed.strip(),
                       f"{client_seed.strip()}:{int(nonce)}")
    result_num = raw % 37
    color = "red" if result_num in _ROUGE else (
        "black" if result_num != 0 else "green")
    evenodd = ("even" if result_num != 0 and result_num % 2 == 0 else
               ("odd" if result_num % 2 == 1 else "zero"))
    await ctx.send(
        f"✅ Roulette verify: nonce {nonce} → `{result_num}` ({color}, {evenodd})"
    )


_register_game(
    key="roulette",
    name="Roulette",
    aliases=["r"],
    desc=
    "Bet red/black/even/odd or a single number. Wins pay standard odds minus 1%.",
    usage="!roulette <amount> <red|black|even|odd|0-36>",
    emoji="🎡",
    group="Table",
)

# ==============================================================================
# 6) SLOTS (aliases: slots, sl) — 3-reel, house-favored
_slots_pf_state: Dict[int, dict] = {}
_last_slots: Dict[int, dict] = {}

_SLOTS_SYMBOLS = ["🍒", "🍋", "🔔", "💎", "⭐", "7️⃣"]


def _slots_payout_multiplier(symbols: List[str]) -> float:
    """
    House-favored with uniform reels:
    - 3x: 7️⃣=36x, 💎=16x, ⭐=9x, 🔔=5x, 🍋=4x, 🍒=4x
    - Any 2-of-a-kind: 1.5x
    Net EV ≈ 0.975 after 1% win cut (house edge ≈2.5%).
    If you prefer ~1% edge: use 7️⃣=40, 💎=18, ⭐=10, 🔔=5, 🍋=4, 🍒=4 (EV≈0.99).
    """
    if len(set(symbols)) == 1:
        s = symbols[0]
        return {
            "7️⃣": 36.0,
            "💎": 16.0,
            "⭐": 9.0,
            "🔔": 5.0,
            "🍋": 4.0,
            "🍒": 4.0,
        }.get(s, 0.0)

    # exact 2-of-a-kind
    for sym in _SLOTS_SYMBOLS:
        if symbols.count(sym) == 2:
            return 1.5
    return 0.0


@bot.command(name="slots", aliases=["sl"])
async def slots_cmd(ctx, amount: float):
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_slots_pf_state, ctx.author.id)
    used_nonce = st["nonce"]

    reels = []
    n = used_nonce
    for _ in range(3):
        idx = _pf_hmac_int(st["server_seed"],
                           f"{st['client_seed']}:{n}") % len(_SLOTS_SYMBOLS)
        reels.append(_SLOTS_SYMBOLS[idx])
        n += 1
    st["nonce"] = n
    end_nonce = n - 1

    mult = _slots_payout_multiplier(reels)
    payout = amount * mult * (1 - HOUSE_EDGE) if mult > 0 else 0.0
    net = payout - amount
    win = payout > 0

    if win:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_slots[ctx.author.id] = {"amount": amount}

    embed = discord.Embed(
        title="🎰 Slots",
        description=f"Result: {' | '.join(reels)}",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Result",
                    value=_format_win_embed("Slots", win, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce range: `{used_nonce}..{end_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !slots_verify <server_seed> <client_seed> <start_nonce> | Reroll with !sl_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="sl_reroll", aliases=["slots_reroll"])
async def slots_reroll_cmd(ctx):
    last = _last_slots.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous slots found for reroll.")
    await slots_cmd(ctx, last["amount"])


@bot.command(name="slots_verify", aliases=["sl_verify"])
async def slots_verify_cmd(ctx, server_seed: str, client_seed: str,
                           start_nonce: int):
    reels = []
    n = int(start_nonce)
    for _ in range(3):
        idx = _pf_hmac_int(server_seed.strip(),
                           f"{client_seed.strip()}:{n}") % len(_SLOTS_SYMBOLS)
        reels.append(_SLOTS_SYMBOLS[idx])
        n += 1
    end_nonce = n - 1
    await ctx.send(
        f"✅ Slots verify: reels {' | '.join(reels)} • nonce range {start_nonce}..{end_nonce}"
    )


_register_game(
    key="slots",
    name="Slots",
    aliases=["sl"],
    desc="3-reel Slots. 3× and 2× matches pay; 1% cut on wins.",
    usage="!slots <amount>",
    emoji="🎰",
    group="Machines",
)

# ==============================================================================
# 7) WHEEL (aliases: wheel, wh) — tuned for ~1% edge
_wheel_pf_state: Dict[int, dict] = {}
_last_wheel: Dict[int, dict] = {}

# Uniform segments sum to 6.0 → mean=1.0 → net EV≈0.99 after 1% cut
_WHEEL_SEGMENTS = [0.2, 0.4, 0.7, 1.0, 1.6, 2.1]


@bot.command(name="wheel", aliases=["wh"])
async def wheel_cmd(ctx, amount: float):
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_wheel_pf_state, ctx.author.id)
    used_nonce = st["nonce"]
    idx = _pf_hmac_int(
        st["server_seed"],
        f"{st['client_seed']}:{used_nonce}") % len(_WHEEL_SEGMENTS)
    st["nonce"] += 1

    seg = _WHEEL_SEGMENTS[idx]
    payout = amount * seg * (1 - HOUSE_EDGE)
    net = payout - amount
    win = payout > 0

    if win:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_wheel[ctx.author.id] = {"amount": amount}

    embed = discord.Embed(title="🛞 Wheel",
                          description=f"Multiplier landed: `{seg:.2f}×`",
                          color=discord.Color.green())
    embed.add_field(name="Result",
                    value=_format_win_embed("Wheel", True, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce: `{used_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !wheel_verify <server_seed> <client_seed> <nonce> | Reroll with !wh_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="wh_reroll", aliases=["wheel_reroll"])
async def wheel_reroll_cmd(ctx):
    last = _last_wheel.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous wheel found for reroll.")
    await wheel_cmd(ctx, last["amount"])


@bot.command(name="wheel_verify", aliases=["wh_verify"])
async def wheel_verify_cmd(ctx, server_seed: str, client_seed: str,
                           nonce: int):
    idx = _pf_hmac_int(
        server_seed.strip(),
        f"{client_seed.strip()}:{int(nonce)}") % len(_WHEEL_SEGMENTS)
    seg = _WHEEL_SEGMENTS[idx]
    await ctx.send(f"✅ Wheel verify: nonce {nonce} → `{seg:.2f}×`")


_register_game(
    key="wheel",
    name="Wheel",
    aliases=["wh"],
    desc="Spin and land a multiplier. Uniform segments tuned for ~1% edge.",
    usage="!wheel <amount>",
    emoji="🛞",
    group="Machines",
)

# ==============================================================================
# 8) MINES (aliases: mines, mn) — 5x5 grid, 5 mines
_mines_pf_state: Dict[int, dict] = {}
_last_mines: Dict[int, dict] = {}


@bot.command(name="mines", aliases=["mn"])
async def mines_cmd(ctx, amount: float, picks: int = 3):
    if not (1 <= picks <= 10):
        return await ctx.send("❌ Picks must be 1–10.")
    u = fetch_user(ctx.author.id)
    if u["balance"] < amount or amount <= 0:
        return await ctx.send("❌ Insufficient QC or invalid amount.")

    update_balance(ctx.author.id, -amount)
    update_balance(bot.user.id, amount)
    update_stats(ctx.author.id, total_wagered=amount)

    st = _pf_get_or_create(_mines_pf_state, ctx.author.id)
    used_nonce = st["nonce"]

    total_cells = 25
    mine_count = 5

    # Determine mine positions (5 unique)
    mines_set = set()
    n = used_nonce
    while len(mines_set) < mine_count:
        idx = _pf_hmac_int(st["server_seed"],
                           f"{st['client_seed']}:{n}") % total_cells
        mines_set.add(idx)
        n += 1

    # Deterministic picks (auto mode demo)
    chosen = []
    safe_count = 0
    for _ in range(picks):
        idx = _pf_hmac_int(st["server_seed"],
                           f"{st['client_seed']}:{n}") % total_cells
        n += 1
        while idx in chosen:
            idx = _pf_hmac_int(st["server_seed"],
                               f"{st['client_seed']}:{n}") % total_cells
            n += 1
        chosen.append(idx)
        if idx not in mines_set:
            safe_count += 1

    st["nonce"] = n
    end_nonce = n - 1

    win = (safe_count == picks)

    # Multiply by inverse of odds of drawing safe picks without hitting a mine (approx step product)
    odds = 1.0
    safe = total_cells - mine_count
    total = total_cells
    for i in range(picks):
        odds *= (safe - i) / (total - i)
    mult = (1 / odds) if odds > 0 else 0.0

    payout = amount * mult * (1 - HOUSE_EDGE) if win else 0.0
    net = payout - amount

    if win and payout > 0:
        if not _ensure_funds_or_refund(ctx, ctx.author.id, amount, payout):
            return await ctx.send("❌ Bot can't cover payout. Wager refunded.")
        update_balance(ctx.author.id, payout)
        update_balance(bot.user.id, -payout)
        update_stats(ctx.author.id, net_profit_loss=net)
    else:
        update_stats(ctx.author.id, net_profit_loss=-amount)

    _last_mines[ctx.author.id] = {"amount": amount, "picks": picks}

    grid_display = "".join("💣" if i in mines_set else "🟩"
                           for i in range(total_cells))
    grid_lines = "\n".join(
        [grid_display[i:i + 5] for i in range(0, total_cells, 5)])

    embed = discord.Embed(
        title="💣 Mines",
        description=
        f"Picked {picks} cells • {'SAFE' if win else 'BOOM'}\nGrid (5x5):\n{grid_lines}",
        color=discord.Color.green() if win else discord.Color.red())
    embed.add_field(name="Chosen cells",
                    value=", ".join(str(i) for i in chosen),
                    inline=False)
    embed.add_field(name="Result",
                    value=_format_win_embed("Mines", win, False, amount,
                                            payout, net),
                    inline=False)
    embed.add_field(
        name="PF Proof",
        value=
        f"server_hash: `{st['server_hash']}`\nclient_seed: `{st['client_seed']}`\nnonce range: `{used_nonce}..{end_nonce}`",
        inline=False)
    embed.set_footer(
        text=
        "Verify with !mines_verify <server_seed> <client_seed> <start_nonce> <picks> | Reroll with !mn_reroll"
    )
    await ctx.send(embed=embed)


@bot.command(name="mn_reroll", aliases=["mines_reroll"])
async def mines_reroll_cmd(ctx):
    last = _last_mines.get(ctx.author.id)
    if not last:
        return await ctx.send("❌ No previous mines found for reroll.")
    await mines_cmd(ctx, last["amount"], last["picks"])


@bot.command(name="mines_verify", aliases=["mn_verify"])
async def mines_verify_cmd(ctx, server_seed: str, client_seed: str,
                           start_nonce: int, picks: int):
    total_cells = 25
    mine_count = 5
    mines_set = set()
    n = int(start_nonce)
    while len(mines_set) < mine_count:
        idx = _pf_hmac_int(server_seed.strip(),
                           f"{client_seed.strip()}:{n}") % total_cells
        mines_set.add(idx)
        n += 1
    chosen = []
    for _ in range(int(picks)):
        idx = _pf_hmac_int(server_seed.strip(),
                           f"{client_seed.strip()}:{n}") % total_cells
        n += 1
        while idx in chosen:
            idx = _pf_hmac_int(server_seed.strip(),
                               f"{client_seed.strip()}:{n}") % total_cells
            n += 1
        chosen.append(idx)
    end_nonce = n - 1
    await ctx.send("✅ Mines verify:\n"
                   f"- Mines: {sorted(list(mines_set))}\n"
                   f"- Chosen: {chosen}\n"
                   f"- Nonce range: {start_nonce}..{end_nonce}")


_register_game(
    key="mines",
    name="Mines",
    aliases=["mn"],
    desc=
    "Pick safe cells on 5×5 grid with 5 mines. Win pays inverse odds minus 1%.",
    usage="!mines <amount> [picks=3]",
    emoji="💣",
    group="Machines",
)


# ==============================================================================
# GAMES CATALOG (Compact, Pretty, Includes KENO and LIMBO)
@bot.command(name="games")
async def games_cmd(ctx):
    # Group by category for readability
    groups = {}
    for key, info in _GAME_DESCRIPTIONS.items():
        groups.setdefault(info["group"], []).append(
            (info["emoji"], info["name"], info["aliases"], info["desc"],
             info["usage"]))

    embed = discord.Embed(
        title="🎮 Quanta Casino — Games Catalog",
        description=
        "Provably Fair • 1% baseline edge (some games slightly house-favored)",
        color=discord.Color.gold())

    # Order groups
    order = ["Quick bets", "Table", "Machines", "Special"]
    # Add Keno and Limbo callouts at top
    embed.add_field(
        name="🎯 Keno (1% edge)",
        value=
        "Command: `!keno` — Pick 6 numbers (1–40), 8 drawn, payouts up to 800× minus 1%.",
        inline=False)
    embed.add_field(
        name="🚀 Limbo (1% edge)",
        value=
        "Command: `!limbo <amount>` — Set target (e.g., 2.00×). Win chance scales, wins pay target× minus 1%.",
        inline=False)

    for grp in order:
        if grp not in groups:
            continue
        lines = []
        for emoji, name, aliases, desc, usage in groups[grp]:
            alias_str = ", ".join(aliases) if aliases else "—"
            lines.append(
                f"{emoji} {name} ({alias_str}) — {desc}\nUsage: `{usage}`")
        if lines:
            embed.add_field(name=f"{grp}",
                            value="\n\n".join(lines),
                            inline=False)

    embed.set_footer(
        text=
        "Use !help for wallet & on-chain commands • Set client seeds where supported for PF."
    )
    await ctx.send(embed=embed)


#====USER CORRECTIONS

import difflib
import discord
from discord.ext import commands


# ─────────── HANDLER: Casual & Rude Chat ───────────
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return  # Ignore other bots completely

    # Check if user mentioned the bot OR replied directly to bot
    is_mention = bot.user.mentioned_in(message)
    is_reply_to_bot = (message.reference
                       and message.reference.resolved and isinstance(
                           message.reference.resolved, discord.Message)
                       and message.reference.resolved.author.id == bot.user.id)

    if not (is_mention or is_reply_to_bot):
        # Not directed at the bot → skip, only process commands
        await bot.process_commands(message)
        return

    # Convert to lowercase for easy matching
    content = message.content.lower().strip()

    # Greetings / Normal interactions
    greetings = [
        "hi", "hello", "hey", "yo", "sup", "gm", "good morning", "good night",
        "bye"
    ]
    if any(content == g or content.startswith(g + " ") for g in greetings):
        await message.channel.send(
            f"✨ {message.author.mention} {content.capitalize()}!")
        return

    # Thanks
    if content in ["thanks", "thank you", "ty", "thx"]:
        await message.channel.send(
            f"🙏 Anytime {message.author.mention}, you’re welcome!")
        return

    # Rude triggers
    rude_triggers = {
        "stfu":
        " Shut your worthless mouth before I staple it closed, you pathetic worm.",
        "fuck": " How about i fuck you?",
        "fuck you":
        " Fuck me? Nah, I'd rather watch you choke on your own bile, you disgusting reject.",
        "loser":
        " Loser? You're the human equivalent of a participation trophy that even the trash bin rejects, {mention}.",
        "idiot":
        " Idiot? You're a black hole of stupidity sucking in everyone around you, {mention}.",
        "lmao":
        " LMAO? Your life's a joke so bad even the punchline wants to die of embarrassment.",
        "cry": " Cry me a river, then drown in it, you sniveling failure.",
        "bruh": " Bruh, your existence is the biggest bruh moment in history.",
        "noob":
        " Noob? You're still in diapers while the world laps you, you incompetent fetus.",
        "shut up":
        " Shut up? Or I'll expose every embarrassing secret you've buried, you spineless fraud.",
        "dumbass":
        " Dumbass? Your brain's so fried it's a wonder you remember to breathe, you drooling moron.",
        "moron":
        " Moron? You're the reason evolution's considering a recall, you genetic dead-end.",
        "fuck off":
        " Fuck off? Stay and watch me dismantle your fragile ego piece by humiliating piece.",
        "you're wrong":
        " Wrong? You're always wrong, like a compass that points straight to failure.",
        "asshole":
        " Asshole? You're the gaping void where decency goes to die, {mention}.",
        "stupid":
        " Stupid? If ignorance was bliss, you'd be in eternal orgasm, you brainless husk.",
        "hater":
        " Hater? Jealousy looks ugly on you, but then again, so does everything else.",
        "bitch":
        " Bitch? You're the stray dog nobody wants, scavenging for scraps of attention.",
        "dork":
        " Dork? At least I'm not a walking embarrassment like your sorry ass.",
        "go away":
        " Go away? Nah, stick around so I can keep reminding you of your irrelevance.",
        "ugly":
        " Ugly? Your face could curdle milk from across the room, you grotesque troll.",
        "fat":
        " Fat? You're a bloated sack of regrets and bad decisions, waddling through life.",
        "skinny":
        " Skinny? Starve yourself more, maybe you'll disappear like your personality already has.",
        "old":
        " Old? You're a fossilized relic of failure, crumbling under your own irrelevance.",
        "young":
        " Young? Go back to kindergarten where your opinions might matter, you immature brat.",
        "poor":
        " Poor? Broke in wallet and spirit, begging for scraps while the world laughs.",
        "rich":
        " Rich? Money can't hide the void where your soul should be, you empty shell.",
        "weak":
        " Weak? You couldn't lift your own shattered self-esteem, you fragile snowflake.",
        "strong":
        " Strong? All brawn, no brain—your muscles compensate for your microscopic intellect.",
        "slow":
        " Slow? Your mind's a glacier melting into oblivion, you sluggish idiot.",
        "fast":
        " Fast? Rushing headfirst into stupidity, setting world records in failure.",
        "boring":
        " Boring? Your existence is a coma-inducing nightmare, {mention}. Wake up and end it.",
        "funny":
        " Funny? Your 'humor' is a cry for help disguised as bad jokes.",
        "smart":
        " Smart? Overrated delusions from a certified fool playing pretend.",
        "dumb": " Dumb? Your IQ's so low it's a limbo contest winner.",
        "crazy":
        " Crazy? You're the asylum's star patient, escaped and infecting the world.",
        "sane":
        " Sane? Boringly predictable, like a robot programmed for mediocrity.",
        "lazy":
        " Lazy? You're a parasite leeching off society, too slothful to even decay properly.",
        "hardworking":
        " Hardworking? Grinding away at nothing, like a hamster powering your own cage.",
        "tall":
        " Tall? Compensation for that short fuse and even shorter worth.",
        "short":
        " Short? Napoleon had more height in his ego than you do in reality.",
        "hot":
        " Hot? Delusional fever dream—your 'heat' is just swamp gas from the bog you crawled out of.",
        "cold":
        " Cold? Ice-hearted bitch with the warmth of a serial killer's smile.",
        "loud": " Loud? Yelling to mask the echo in your empty skull.",
        "quiet":
        " Quiet? Silent because even your thoughts are ashamed to be voiced.",
        "weird": " Weird? You're the freak show exhibit nobody pays to see.",
        "normal":
        " Normal? Bland as unsalted oatmeal in a world starving for flavor.",
        "happy":
        " Happy? Fake joy plastered over a pit of despair—keep smiling, clown.",
        "sad":
        " Sad? Wallow in it, you deserve every tear in your pathetic puddle.",
        "angry":
        " Angry? Rage all you want, it's the only fire you'll ever spark.",
        "calm":
        " Calm? Repressed volcano ready to erupt into a mess of failure.",
        "brave": " Brave? Reckless idiot mistaking stupidity for courage.",
        "coward": " Coward? Hiding behind screens while life kicks your ass.",
        "hero":
        " Hero? In your dreams—reality calls you the sidekick nobody remembers.",
        "villain":
        " Villain? Amateur hour—real evil laughs at your weak attempts.",
        "genius":
        " Genius? At failing spectacularly, yes. Otherwise, a drooling fool.",
        "fool":
        " Fool? Court jester in the kingdom of idiots, crowned by your own stupidity.",
        "king": " King? Of a crumbling empire built on delusions and denial.",
        "queen":
        " Queen? Drama diva ruling over a court of clowns and rejects.",
        "boss":
        " Boss? Tyrant of tiny minds, lording over your imaginary domain.",
        "slave": " Slave? To your own vices—break free or rot in chains.",
        "free": " Free? Trapped in the prison of your worthless existence.",
        "trapped":
        " Trapped? Good, the world doesn't need more of your kind loose.",
        "win": " Win? Your 'victories' are pity prizes from a rigged game.",
        "lose": " Lose? It's your default setting, failure factory.",
        "fight":
        " Fight? I'll eviscerate you verbally until you're begging for mercy.",
        "peace": " Peace? Hypocrite preaching calm while seething inside.",
        "love": " Love? Twisted obsession from a heartless void.",
        "hate": " Hate? Fuel for your empty life—keep it coming, fanboy.",
        "friend": " Friend? Backstabber in waiting, loyalty sold cheap.",
        "enemy": " Enemy? Worthless foe not even worth the swing.",
        "family": " Family? Dysfunctional mess you dragged down with you.",
        "alone": " Alone? Deserved isolation for a toxic plague like you.",
        "crowd": " Crowd? Blending in as the forgettable nobody you are.",
        "light": " Light? Dim flicker about to be snuffed out forever.",
        "dark": " Dark? Edgy wannabe hiding in shadows from your own shame.",
        "day": " Day? Exposes every flaw in your rotten core.",
        "night": " Night? When your demons come out to play—and win.",
        "sun": " Sun? Burn away your illusions, leave the ashes.",
        "moon": " Moon? Lunatic howling at irrelevance.",
        "star": " Star? Burned-out has-been falling into oblivion.",
        "planet": " Planet? You're the asteroid headed for extinction.",
        "space": " Space? Vast emptiness matching your soul.",
        "earth": " Earth? Polluted by your presence—time to leave.",
        "fire": " Fire? I'll incinerate your ego to cinders.",
        "water": " Water? Drown in the flood of your own tears.",
        "air": " Air? Hot wind from a bloviating fool.",
        "ground": " Ground? Rock bottom's your permanent address.",
        "sky": " Sky? Limits you can't reach with your clipped wings.",
        "dream": " Dream? Nightmares are more your speed, loser.",
        "reality": " Reality? Slaps you harder than your absent parents.",
        "hope": " Hope? Delusional crutch for the hopelessly inept.",
        "despair": " Despair? Your natural state—embrace it.",
        "success": " Success? Foreign concept to a chronic failure like you.",
        "failure": " Failure? Your autobiography in one word.",
        "power": " Power? Illusion for the powerless pawn you are.",
        "weakness": " Weakness? Your defining trait, etched in stone.",
        "beautiful": " Beautiful? Surface-level lie hiding inner rot.",
        "hideous": " Hideous? Mirror-cracking monstrosity inside and out.",
        "kind": " Kind? Fake niceties from a venomous snake.",
        "mean": " Mean? Petty cruelty from a small-minded thug.",
        "generous":
        " Generous? Giving away what little dignity you have left.",
        "selfish": " Selfish? Hoarding misery like it's treasure.",
        "honest": " Honest? Brutal truths from a liar's mouth.",
        "liar": " Liar? Pathological deceiver weaving webs of bullshit.",
        "trust": " Trust? Shattered by your betrayals, fool.",
        "betray": " Betray? Your specialty—knife in the back expert.",
        "loyal": " Loyal? Dog-like obedience to your own destruction.",
        "traitor": " Traitor? Selling out for scraps, worthless scum.",
        "alive": " Alive? Barely—zombie shuffling through existence.",
        "dead":
        " Dead? Inside already, just waiting for the body to catch up.",
        "birth": " Birth? The world's biggest mistake.",
        "death": " Death? Mercy for someone as wretched as you.",
        "god": " God? Imaginary friend for the godless void you are.",
        "devil": " Devil? Amateur—Satan takes notes from you.",
        "heaven": " Heaven? Barred entry for scum like you.",
        "hell": " Hell? Your future home—pack light.",
        "angel": " Angel? Fallen so low you're underground.",
        "demon": " Demon? Possessed by your own idiocy.",
        "magic": " Magic? Illusion for the gullible fool you are.",
        "science": " Science? Facts that debunk your delusions.",
        "art": " Art? Your life's a scribble on toilet paper.",
        "trash": " Trash? Self-description nailed it."
    }

    for word, reply in rude_triggers.items():
        if word in content:
            await message.channel.send(
                reply.format(mention=message.author.mention))
            return

    # Else, process as normal command or ignore
    await bot.process_commands(message)


# ─────────── HANDLER: Global Command Errors ───────────
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Fuzzy correction
        available = [cmd.name for cmd in bot.commands]
        suggestion = difflib.get_close_matches(
            ctx.message.content.split()[0].lstrip("!"),
            available,
            n=1,
            cutoff=0.6)
        suggested = f" Did you mean `!{suggestion}`?" if suggestion else " Use `!help` to see commands."

        embed = discord.Embed(
            title="❓ Unknown Command",
            description=
            f"`{ctx.message.content}` is not recognized.{suggested}",
            color=discord.Color.red())
        embed.set_footer(text="Tip: Commands start with ! (example: !balance)")
        await ctx.send(embed=embed, delete_after=20)

    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="⚠️ Missing Argument",
            description=f"You missed **{error.param.name}**.\n"
            f"✅ Try: `{ctx.command.usage or '!'+ctx.command.name}`",
            color=discord.Color.orange())
        await ctx.send(embed=embed, delete_after=20)

    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="⚠️ Invalid Argument",
            description=f"That doesn’t look right.\n"
            f"💡 Example: `{ctx.command.usage or '!'+ctx.command.name}`",
            color=discord.Color.orange())
        await ctx.send(embed=embed, delete_after=20)

    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏳ Chill out!",
            description=
            f"Cooldown active. Try again in **{error.retry_after:.1f}s**.",
            color=discord.Color.blue())
        await ctx.send(embed=embed, delete_after=10)

    else:
        # Unexpected errors
        embed = discord.Embed(
            title="⚠️ Unexpected Error",
            description="Something broke. Don’t cry, blame the devs 🛠️",
            color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=20)
        raise error  # Still raise for logs


#====meme

# === MEME COMMAND (D3vd/Meme_API) ===
import asyncio
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime, timezone

_MEME_LAST_BY_USER: dict[int, dict] = {}  # cache last meme per user

MEME_API_BASE = "https://meme-api.com/gimme"


def build_meme_embed(data: dict, requester: discord.Member) -> discord.Embed:
    title = str(data.get("title") or "Meme")
    post_link = str(data.get("postLink") or "")
    subreddit = str(data.get("subreddit") or "memes")
    author = str(data.get("author") or "unknown")
    ups = int(data.get("ups") or 0)
    url = str(data.get("url") or "")
    nsfw = bool(data.get("nsfw") or False)
    is_gif = url.lower().endswith((".gif", ".gifv"))

    color = discord.Color.purple() if is_gif else discord.Color.blurple()
    e = discord.Embed(
        title=title,
        description=f"r/{subreddit} • by u/{author}\n[Post link]({post_link})",
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_author(name="Meme Time 🤡")
    e.set_image(url=url)
    footer_left = "NSFW • " if nsfw else ""
    e.set_footer(
        text=f"{footer_left}Requested by {requester.display_name} • 👍 {ups}")
    return e


async def fetch_meme(subreddit: str | None = None) -> dict:
    url = MEME_API_BASE + (f"/{subreddit}" if subreddit else "")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as resp:
            if resp.status != 200:
                # Meme_API returns JSON error sometimes; try to read it for clarity
                try:
                    err = await resp.json()
                except Exception:
                    err = {"message": f"HTTP {resp.status}"}
                raise RuntimeError(
                    f"Meme API error: {err.get('message','HTTP error')} (status {resp.status})"
                )
            data = await resp.json()
            # Expected keys from Meme_API:
            # postLink, subreddit, title, url, nsfw, spoiler, author, ups, preview[]
            # Optional: num (when hitting /gimme/<n>) — not used here
            return data


class MemeView(discord.ui.View):

    def __init__(self,
                 requester_id: int,
                 initial_payload: dict,
                 *,
                 subreddit: str | None,
                 timeout: float = 90):
        super().__init__(timeout=timeout)
        self.requester_id = requester_id
        self.payload = initial_payload
        self.subreddit = subreddit

    def _is_owner(self, interaction: discord.Interaction) -> bool:
        return interaction.user and interaction.user.id == self.requester_id

    async def _fetch_safe_meme(self, interaction: discord.Interaction) -> dict:
        # try up to 3 times to get a SFW meme if channel is SFW and API gives NSFW
        attempts = 0
        while attempts < 3:
            data = await fetch_meme(self.subreddit)
            if not data.get("nsfw"):
                return data
            if hasattr(interaction.channel,
                       "is_nsfw") and interaction.channel.is_nsfw():
                return data
            attempts += 1
        return data  # fallback with last attempt

    @discord.ui.button(label="Next Meme",
                       style=discord.ButtonStyle.primary,
                       emoji="🔁")
    async def next_meme(self, interaction: discord.Interaction,
                        button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        try:
            await interaction.response.defer()  # acknowledge quickly
            data = await self._fetch_safe_meme(interaction)
            self.payload = data
            _MEME_LAST_BY_USER[self.requester_id] = data
            embed = build_meme_embed(data, interaction.user)
            await interaction.edit_original_response(embed=embed, view=self)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to fetch a meme: {e}",
                                            ephemeral=True)

    @discord.ui.button(label="Save (DM)",
                       style=discord.ButtonStyle.success,
                       emoji="💾")
    async def save_dm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        try:
            embed = build_meme_embed(self.payload, interaction.user)
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("✅ Sent to your DMs!",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Can't DM you. Enable DMs or DM me first.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to save: {e}",
                                                    ephemeral=True)

    @discord.ui.button(label="Share Again",
                       style=discord.ButtonStyle.secondary,
                       emoji="📤")
    async def share_again(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        try:
            embed = build_meme_embed(self.payload, interaction.user)
            await interaction.response.send_message("✅ Shared!",
                                                    ephemeral=True)
            await interaction.channel.send(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to share: {e}",
                                                    ephemeral=True)

    async def on_timeout(self):
        for c in self.children:
            c.disabled = True


@bot.command(name="meme")
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme_cmd(ctx: commands.Context, subreddit: str | None = None):
    """
    Fetch a meme from D3vd/Meme_API.
    Usage:
      !meme
      !meme <subreddit>
    """
    # typing indicator for compatibility across discord.py versions
    async with ctx.typing():
        try:
            data = await fetch_meme(subreddit)
        except asyncio.TimeoutError:
            return await ctx.send("⏱️ Meme API timed out. Try again.")
        except Exception as e:
            return await ctx.send(f"❌ {e}")

    # NSFW gate: block if channel is SFW and meme is NSFW
    if bool(data.get("nsfw")) and hasattr(
            ctx.channel, "is_nsfw") and not ctx.channel.is_nsfw():
        return await ctx.send(
            "🔞 That meme is NSFW and this channel is not marked NSFW. Try again in an NSFW channel or use a different subreddit."
        )

    embed = build_meme_embed(data, ctx.author)
    view = MemeView(requester_id=ctx.author.id,
                    initial_payload=data,
                    subreddit=subreddit)
    _MEME_LAST_BY_USER[ctx.author.id] = data

    await ctx.send(embed=embed, view=view)


# === END MEME COMMAND ===

# === CAT COMMAND (The Cat API) — REWRITE ===
import asyncio
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union

CAT_API_KEY = "live_Z3sPO1Sms6sFq6FCEVJTknHzzSIFOWi9enkwevhnZHObPvKtFJu0Z6PKHgLO7wzH"
CAT_API_BASE = "https://api.thecatapi.com/v1/images/search"


# ---------- Helpers ----------
def _first_breed(breeds: Any) -> Optional[dict]:
    """
    Safely return the first breed dict if present.
    Handles cases:
      - []                         -> None
      - [{...}]                    -> dict
      - [[{...}], {...}] (rare)    -> dict inside first list
      - non-dict entries are ignored
    """
    if not breeds:
        return None
    first = breeds[0]
    if isinstance(first, list):
        if first and isinstance(first, dict):
            return first
        return None
    if isinstance(first, dict):
        return first
    return None


def _cat_title(item: dict) -> str:
    b = _first_breed(item.get("breeds"))
    if b and isinstance(b, dict):
        name = b.get("name")
        if name:
            return str(name)
    return "Random Cat"


def _cat_desc(item: dict) -> str:
    b = _first_breed(item.get("breeds"))
    if not (b and isinstance(b, dict)):
        return "A random kitty for your day."
    temperament = b.get("temperament")
    origin = b.get("origin")
    desc = b.get("description")
    lines = []
    if temperament:
        lines.append(f"Temperament: {temperament}")
    if origin:
        lines.append(f"Origin: {origin}")
    if desc:
        s = str(desc)
        lines.append(s[:220] + ("…" if len(s) > 220 else ""))
    return "\n".join(lines) if lines else "A random kitty for your day."


def build_cat_embed(item: dict, requester: discord.Member, index: int,
                    total: int) -> discord.Embed:
    url = str(item.get("url") or "")
    post_id = str(item.get("id") or "")
    is_gif = url.lower().endswith((".gif", ".gifv"))
    color = discord.Color.purple() if is_gif else discord.Color.teal()
    e = discord.Embed(
        title=_cat_title(item),
        description=_cat_desc(item),
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_author(name="The Cat API 🐾")
    if url:
        e.set_image(url=url)
    suffix = f" • ID: {post_id}" if post_id else ""
    e.set_footer(
        text=
        f"Requested by {requester.display_name} • {index+1}/{total}{suffix}")
    return e


async def fetch_cats(
    *,
    breed_id: Optional[str] = None,
    mime_types: Optional[str] = None,  # "jpg,png,gif" or single like "jpg"
    limit: int = 1,
) -> List[dict]:
    params = {
        "limit": max(1, min(int(limit or 1), 5)),
        "order": "RANDOM",
        "size": "med",
    }
    if breed_id:
        params["breed_ids"] = breed_id
    if mime_types:
        params["mime_types"] = mime_types

    headers = {"x-api-key": CAT_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(CAT_API_BASE,
                               params=params,
                               headers=headers,
                               timeout=15) as resp:
            if resp.status != 200:
                try:
                    err = await resp.json()
                except Exception:
                    err = {"message": f"HTTP {resp.status}"}
                raise RuntimeError(
                    f"The Cat API error: {err.get('message','HTTP error')} (status {resp.status})"
                )
            data = await resp.json()
            if not isinstance(data, list):
                raise RuntimeError("Unexpected response from The Cat API.")
            items = [d for d in data if isinstance(d, dict)]
            if not items:
                raise RuntimeError("No cats found (empty response).")
            return items


# ---------- Interactive View ----------
class CatView(discord.ui.View):

    def __init__(
        self,
        requester_id: int,
        items: List[dict],
        *,
        breed_id: Optional[str],
        mime_types: Optional[str],
        timeout: float = 120,
    ):
        super().__init__(timeout=timeout)
        self.requester_id = requester_id
        self.items = items
        self.index = 0
        self.breed_id = breed_id
        self.mime_types = mime_types

    def _is_owner(self, i: discord.Interaction) -> bool:
        return i.user and i.user.id == self.requester_id

    def _current(self) -> dict:
        return self.items[self.index]

    def _total(self) -> int:
        return len(self.items)

    async def _edit_embed(self, interaction: discord.Interaction):
        embed = build_cat_embed(self._current(), interaction.user, self.index,
                                self._total())
        await interaction.edit_original_response(embed=embed, view=self)

    @discord.ui.button(label="New Cats 🔄", style=discord.ButtonStyle.success)
    async def new_btn(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        await interaction.response.defer()
        try:
            new_items = await fetch_cats(breed_id=self.breed_id,
                                         mime_types=self.mime_types,
                                         limit=self._total())
            self.items = new_items
            self.index = 0
            await self._edit_embed(interaction)
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Failed to fetch new cats: {e}", ephemeral=True)

    @discord.ui.button(label="Save (DM) 💾",
                       style=discord.ButtonStyle.secondary)
    async def save_btn(self, interaction: discord.Interaction,
                       button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        try:
            embed = build_cat_embed(self._current(), interaction.user,
                                    self.index, self._total())
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("✅ Sent to your DMs!",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Can't DM you. Enable DMs or DM me first.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to save: {e}",
                                                    ephemeral=True)

    async def on_timeout(self):
        for c in self.children:
            c.disabled = True


# ---------- Command ----------
@bot.command(name="cat", aliases=["cats", "pussy", "pussies"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def cat_cmd(
    ctx: commands.Context,
    breed: Optional[str] = commands.parameter(
        default=None, description="Breed ID (e.g., abys)"),
    imgtype: Optional[str] = commands.parameter(
        default=None, description="One of: jpg, png, gif"),
    count: Optional[int] = commands.parameter(default=1,
                                              description="How many (1-5)"),
):
    """
    Show a random cat image from The Cat API.
    Usage:
      !cat
      !cat abys
      !cat abys gif 3
      !cat None jpg 2
    Notes:
      - breed is the Cat API breed_id (e.g., 'abys' for Abyssinian).
      - imgtype limits mime types: jpg, png, or gif.
      - count is 1–5 and shows navigation buttons.
    """
    # Normalize params
    mime = None
    if imgtype:
        t = imgtype.strip().lower()
        if t not in {"jpg", "png", "gif"}:
            return await ctx.send("❌ imgtype must be one of: jpg, png, gif.")
        # Cat API expects "gif" or "jpg,png" formats; we pass single type directly
        mime = t

    limit = max(1, min(int(count or 1), 5))

    async with ctx.typing():
        try:
            items = await fetch_cats(
                breed_id=breed,
                mime_types=mime,
                limit=limit,
            )
        except asyncio.TimeoutError:
            return await ctx.send("⏱️ The Cat API timed out. Try again.")
        except Exception as e:
            return await ctx.send(f"❌ {e}")

    embed = build_cat_embed(items[0], ctx.author, 0, len(items))
    view = CatView(
        requester_id=ctx.author.id,
        items=items,
        breed_id=breed,
        mime_types=mime,
    )
    await ctx.send(embed=embed, view=view)


# === END CAT COMMAND (REWRITE) ===

# === DOG COMMAND (Dog CEO API) ===
import asyncio
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DOG_API_BASE = "https://dog.ceo/api"


def _parse_breed_from_url(url: str) -> str:
    # Example URL: https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg
    # or https://images.dog.ceo/breeds/hound/afghan.jpg
    try:
        parts = url.split("/breeds/")[1].split("/")
        breed_part = parts  # e.g., "hound-afghan" or "hound"
        # Replace dashes with spaces; title-case for nice display
        return breed_part.replace("-", " ").title()
    except Exception:
        return "Doggo"


def _dog_title(url: str) -> str:
    return _parse_breed_from_url(url)


def _dog_desc(url: str) -> str:
    return f"Source: {url}"


def build_dog_embed(img_url: str, requester: discord.Member, index: int,
                    total: int) -> discord.Embed:
    is_gif = img_url.lower().endswith((".gif", ".gifv"))
    color = discord.Color.purple() if is_gif else discord.Color.green()
    title = _dog_title(img_url)
    desc = _dog_desc(img_url)

    e = discord.Embed(
        title=title,
        description=desc,
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    e.set_author(name="Dog CEO API 🐶")
    e.set_image(url=img_url)
    e.set_footer(
        text=f"Requested by {requester.display_name} • {index+1}/{total}")
    return e


async def fetch_random_dogs(
        *,
        breed: Optional[str] = None,  # e.g. "hound" or "hound afghan"
        count: int = 1) -> List[str]:
    # Normalize breed/sub-breed
    # Dog CEO supports:
    # - /breeds/image/random
    # - /breeds/image/random/{n}
    # - /breed/{breed}/images/random
    # - /breed/{breed}/{sub}/images/random
    count = max(1, min(int(count or 1), 50))

    # Build endpoint
    endpoint: str
    if breed:
        tokens = [t for t in breed.lower().split() if t]
        if len(tokens) == 1:
            b = tokens[0]
            endpoint = f"/breed/{b}/images/random"
        else:
            b, sub = tokens, tokens[1]
            endpoint = f"/breed/{b}/{sub}/images/random"
        # Dog CEO returns one image per request at breed endpoints; for multiple, call loop
        urls: List[str] = []
        async with aiohttp.ClientSession() as session:
            for _ in range(count):
                async with session.get(DOG_API_BASE + endpoint,
                                       timeout=15) as resp:
                    data = await resp.json()
                    if data.get("status") != "success":
                        raise RuntimeError(
                            f"Dog API error: {data.get('message','unknown error')}"
                        )
                    urls.append(str(data.get("message")))
        return urls
    else:
        endpoint = f"/breeds/image/random/{count}" if count > 1 else "/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(DOG_API_BASE + endpoint,
                                   timeout=15) as resp:
                data = await resp.json()
                if data.get("status") != "success":
                    raise RuntimeError(
                        f"Dog API error: {data.get('message','unknown error')}"
                    )
                # message is either a string (single) or list (multiple)
                msg = data.get("message")
                if isinstance(msg, list):
                    return [str(u) for u in msg]
                else:
                    return [str(msg)]


class DogView(discord.ui.View):

    def __init__(self,
                 requester_id: int,
                 items: List[str],
                 *,
                 breed: Optional[str],
                 timeout: float = 120):
        super().__init__(timeout=timeout)
        self.requester_id = requester_id
        self.items = items
        self.index = 0
        self.breed = breed

    def _is_owner(self, i: discord.Interaction) -> bool:
        return i.user and i.user.id == self.requester_id

    def _current(self) -> str:
        return self.items[self.index]

    def _total(self) -> int:
        return len(self.items)

    async def _send_or_edit(self, interaction: discord.Interaction):
        embed = build_dog_embed(self._current(), interaction.user, self.index,
                                self._total())
        await interaction.edit_original_response(embed=embed, view=self)

    @discord.ui.button(label="New Batch 🔄", style=discord.ButtonStyle.success)
    async def new_btn(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        await interaction.response.defer()
        try:
            items = await fetch_random_dogs(breed=self.breed,
                                            count=self._total())
            self.items = items
            self.index = 0
            await self._send_or_edit(interaction)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to fetch: {e}",
                                            ephemeral=True)

    @discord.ui.button(label="Save (DM) 💾",
                       style=discord.ButtonStyle.secondary)
    async def save_btn(self, interaction: discord.Interaction,
                       button: discord.ui.Button):
        if not self._is_owner(interaction):
            return await interaction.response.send_message(
                "❌ Only the requester can use these controls.", ephemeral=True)
        try:
            embed = build_dog_embed(self._current(), interaction.user,
                                    self.index, self._total())
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("✅ Sent to your DMs!",
                                                    ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Can't DM you. Enable DMs or DM me first.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to save: {e}",
                                                    ephemeral=True)

    async def on_timeout(self):
        for c in self.children:
            c.disabled = True


@bot.command(name="dog", aliases=["dogs"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def dog_cmd(
    ctx: commands.Context,
    breed: Optional[str] = commands.parameter(
        default=None,
        description="Breed or 'breed subbreed' (e.g., hound or 'hound afghan')"
    ),
    count: Optional[int] = commands.parameter(default=1,
                                              description="How many (1-50)")):
    """
    Show random dog image(s) from Dog CEO API.
    Usage:
      !dog
      !dog 3
      !dog husky
      !dog "hound afghan" 5
    Notes:
      - Max images per request: 50
      - Breed format for sub-breeds: "breed subbreed" (e.g., "hound afghan")
    """
    # If the first arg is numeric, treat it as count when breed omitted
    if breed and isinstance(
            breed, str) and breed.isdigit() and (count is None or count == 1):
        count = int(breed)
        breed = None

    async with ctx.typing():
        try:
            cnt = max(1, min(int(count or 1), 50))
            items = await fetch_random_dogs(breed=breed, count=cnt)
        except asyncio.TimeoutError:
            return await ctx.send("⏱️ Dog API timed out. Try again.")
        except Exception as e:
            return await ctx.send(f"❌ {e}")

    embed = build_dog_embed(items[0], ctx.author, 0, len(items))
    view = DogView(requester_id=ctx.author.id, items=items, breed=breed)
    await ctx.send(embed=embed, view=view)


# === END DOG COMMAND ===

# ==== BATTLE ROYALE (with schema init, button join, status, verify, embed feed) ====
import asyncio, time, random
import discord
from discord.ext import commands
from typing import List

from database import (
    get_conn,
    update_balance,
    record_transaction,
    fetch_user,
    db_create_battle,
    db_add_participant,
    db_update_battle_status,
    db_get_battle,
    db_list_participants,
    db_list_open,
    db_list_recent,
)

BATTLE_MIN_PLAYERS = 2
BATTLE_MAX_PLAYERS = 100
BATTLE_EVENT_DELAY = (1.1, 2.0)
QC_PER_SOL = 1000.0


def _mention(uid: int):
    return f"<@{uid}>"


def _pick_event_template():
    pools = [
        # Killer-victim events: dark, twisted, corny as hell
        "{killer} burst from the bushes and force-fed {victim} a cyanide smoothie—bottoms up!",
        "{killer} lured {victim} with a 'free hugs' sign, then hugged them with a bear trap.",
        "{killer} nailed a 360 no-scope headshot on {victim}, turning their skull into abstract art.",
        "{killer} yeeted {victim} into the lava, yelling 'Hot potato!' as they sizzled like bacon.",
        "{killer} and {victim} clashed in a bloodbath—{killer} walked away, munching on {victim}'s entrails.",
        "{victim} stumbled into {killer}'s trap: a pit of spikes greased with orphan tears.",
        "{killer} out-meme’d {victim} so brutally, they rage-quit life and self-deleted.",
        "{killer} whispered 'ez' while shoving {victim} into a woodchipper—easy mulch.",
        "{killer} booby-trapped {victim}'s loot crate with a clown bomb: honk honk, you're dead.",
        "{killer} and {victim} dueled at dawn—{killer} won by cheating with a poisoned fidget spinner.",
        "{killer} skinned {victim} alive and wore them as a cape—fashionably fatal.",
        "{killer} tricked {victim} into a fake therapy session, then therapized them with an axe.",
        "{killer} turned {victim} into a human piñata and beat the candy out—sweet victory.",
        "{killer} force-choked {victim} like Darth Vader on bath salts—feel the unhinged force.",
        "{killer} baked {victim} into a pie and served it to their squad—cannibalism for the win.",
        # Hazards (killer='The Zone'): even darker, unhinged absurdity
        "The Zone swallowed {victim} whole, burping out their soul as toxic gas.",
        "An airdrop pancaked {victim} flatter than a depressed tortilla—splat goes the weasel.",
        "A rogue slot machine exploded, showering {victim} in coins and their own intestines.",
        "A wild goose chased {victim} off a cliff—honk if you're suicidal!",
        "The Zone's fog whispered dark secrets, driving {victim} to chew their own face off.",
        "A cursed vending machine dispensed {victim}'s doom: exploding soda and existential dread.",
        "Radioactive squirrels gnawed {victim}'s legs off—nature's furry apocalypse.",
        "A glitchy portal sucked {victim} in, spitting them out as minced meat confetti.",
        "Killer clowns from the Zone circus juggled {victim}'s organs—final act: death by laughter.",
        "The Zone's wind howled lullabies, rocking {victim} to sleep... eternal, bloody sleep."
    ]

    return random.choice(pools)


# --------- Ensure schema exists (idempotent) ----------
def _ensure_battle_schema():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS battles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        host_id INTEGER,
        pot_qc REAL,
        ratio TEXT,
        max_players INTEGER,
        created_at INTEGER,
        ends_at INTEGER,
        status TEXT,
        winner_id INTEGER
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS battle_participants(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        battle_id INTEGER,
        user_id INTEGER,
        joined_at INTEGER,
        UNIQUE(battle_id,user_id)
    )
    """)


# Call at startup
if hasattr(bot, "setup_hook"):

    async def _battle_setup_hook():
        _ensure_battle_schema()

    bot.setup_hook = _battle_setup_hook  # type: ignore[attr-defined]
else:

    @bot.event
    async def on_ready():
        _ensure_battle_schema()


# ================== JOIN BUTTON VIEW ==================
class BattleJoinView(discord.ui.View):

    def __init__(self, battle_id: int, ends_at: int):
        super().__init__(timeout=None)
        self.battle_id = battle_id
        self.ends_at = ends_at

    @discord.ui.button(label="Join Battle",
                       style=discord.ButtonStyle.success,
                       emoji="⚔️")
    async def join_btn(self, interaction: discord.Interaction,
                       button: discord.ui.Button):
        _ensure_battle_schema()
        b = db_get_battle(self.battle_id)
        if not b or b["status"] != "open":
            return await interaction.response.send_message(
                "❌ This battle is closed.", ephemeral=True)

        uid = interaction.user.id
        players = db_list_participants(self.battle_id)
        if uid in players:
            return await interaction.response.send_message(
                "ℹ️ You already joined this battle.", ephemeral=True)
        if len(players) >= int(b["max_players"] or 0):
            return await interaction.response.send_message("❌ Lobby is full.",
                                                           ephemeral=True)

        db_add_participant(self.battle_id, uid)
        # Soft-update the lobby message if present (best effort)
        try:
            await interaction.response.send_message(
                f"✅ {interaction.user.mention} joined battle #{self.battle_id}!",
                ephemeral=True)
        except Exception:
            pass


# ================== COMMANDS ==================
@bot.group(name="battle", invoke_without_command=True)
async def battle_group(ctx):
    await ctx.send(
        "Use `!battle create <pot> <QC|SOL> <time> <ratio>` • `!battle_status` • `!battle_verify <id>`"
    )


@battle_group.command(name="create")
async def battle_create(ctx,
                        amount: float,
                        cur: str,
                        duration: str = "45s",
                        ratio: str = "100",
                        max_players: int = 20):
    _ensure_battle_schema()

    # parse time
    try:
        dur = duration.strip().lower()
        if dur.endswith("s"): secs = int(float(dur[:-1]))
        elif dur.endswith("m"): secs = int(float(dur[:-1]) * 60)
        elif dur.endswith("h"): secs = int(float(dur[:-1]) * 3600)
        else: secs = int(dur)
        secs = max(1, min(secs, 24 * 3600))
    except Exception:
        return await ctx.send(
            "❌ Invalid duration. Use 30s, 2m, 1h, or seconds.")

    # ratio parse
    try:
        ratio_vals = [float(x) for x in ratio.split("-") if x]
        if not ratio_vals or sum(ratio_vals) <= 0:
            return await ctx.send(
                "❌ Ratio must be like 70-30 or 50-30-20 and sum > 0.")
    except Exception:
        return await ctx.send(
            "❌ Invalid ratio format. Example: 70-30 or 50-30-20.")

    # convert QC
    pot_qc = float(amount) if cur.upper() == "QC" else amount * QC_PER_SOL
    if pot_qc <= 0:
        return await ctx.send("❌ Pot must be positive.")

    # escrow properly
    host = fetch_user(ctx.author.id)
    bal = float(host.get("balance", 0))
    if bal < pot_qc:
        return await ctx.send(
            f"❌ Need {pot_qc:.3f} QC but you have {bal:.3f} QC.")
    update_balance(ctx.author.id, -pot_qc)
    try:
        record_transaction(ctx.author.id, "debit", "battle_escrow", pot_qc,
                           "Battle pot funded")
    except Exception:
        pass

    # create battle in DB
    bid = db_create_battle(ctx.channel.id, ctx.author.id, pot_qc, ratio,
                           max_players, secs)
    db_add_participant(bid, ctx.author.id)

    ends_at = int(time.time()) + secs
    lobby_embed = discord.Embed(
        title=f"🛡️ Battle #{bid} Created",
        description=(f"Host: {_mention(ctx.author.id)}\n"
                     f"Pot: {pot_qc:.3f} QC\n"
                     f"Ratio: {ratio}\n"
                     f"Max players: {max_players}\n"
                     f"Ends: <t:{ends_at}:R>\n"
                     f"Click below to join!"),
        color=discord.Color.blurple())
    view = BattleJoinView(bid, ends_at)
    lobby_msg = await ctx.send(embed=lobby_embed, view=view)

    # finalize after timeout
    async def finalize_after_timeout():
        await asyncio.sleep(secs)
        await finalize_battle(ctx.channel, bid, lobby_msg)

    bot.loop.create_task(finalize_after_timeout())


@battle_group.command(name="start")
async def battle_start(ctx):
    _ensure_battle_schema()
    # Start the most recent open battle in this channel (simple policy)
    opens = [b for b in db_list_open() if b["channel_id"] == ctx.channel.id]
    if not opens:
        return await ctx.send("ℹ️ No open battle here.")
    b = opens[0]
    if ctx.author.id != b["host_id"]:
        return await ctx.send("🚫 Only the host can start early.")
    # Try to find the lobby message? We may not have its ID; finalize without edit
    await finalize_battle(ctx.channel, b["id"], None)


@bot.command(name="battle_status")
async def battle_status(ctx):
    _ensure_battle_schema()
    opens = db_list_open()
    if opens:
        lines = [
            f"#{b['id']} • Pot {b['pot_qc']:.3f} QC • Ends <t:{b['ends_at']}:R>"
            for b in opens if b["channel_id"] == ctx.channel.id
        ]
        if lines:
            emb = discord.Embed(title="⚔️ Open Battles",
                                description="\n".join(lines),
                                color=discord.Color.blue())
            return await ctx.send(embed=emb)
    rec = db_list_recent(5)
    if rec:
        lines = [
            f"#{b['id']} • {b['status']} • Pot {b['pot_qc']:.3f} QC"
            for b in rec if b["channel_id"] == ctx.channel.id
        ]
        if lines:
            emb = discord.Embed(title="Recent Battles",
                                description="\n".join(lines),
                                color=discord.Color.greyple())
            return await ctx.send(embed=emb)
    await ctx.send("No battles found in this channel.")


@bot.command(name="battle_verify")
async def battle_verify(ctx, battle_id: int):
    _ensure_battle_schema()
    b = db_get_battle(battle_id)
    if not b:
        return await ctx.send("❌ Battle not found.")
    parts = db_list_participants(battle_id)
    emb = discord.Embed(
        title=f"🔎 Battle #{battle_id}",
        description=(f"Host: {_mention(b['host_id'])}\n"
                     f"Pot: {b['pot_qc']:.3f} QC\n"
                     f"Ratio: {b['ratio']}\n"
                     f"Status: {b['status']}\n"
                     f"Players: {len(parts)}\n" +
                     (", ".join(_mention(u)
                                for u in parts) if parts else "—")),
        color=discord.Color.orange())
    await ctx.send(embed=emb)


# ================== FINALIZE & RUN ==================
async def finalize_battle(channel: discord.TextChannel, battle_id: int,
                          lobby_msg: discord.Message | None):
    _ensure_battle_schema()
    row = db_get_battle(battle_id)
    if not row or row["status"] != "open":
        return
    players = db_list_participants(battle_id)

    # Lock lobby: edit message to show final participant list and remove button
    if lobby_msg:
        locked = discord.Embed(
            title=f"🔒 Battle #{battle_id} Locked",
            description=(f"Participants ({len(players)}):\n" +
                         (", ".join(_mention(u)
                                    for u in players) if players else "—")),
            color=discord.Color.dark_gold())
        try:
            await lobby_msg.edit(embed=locked, view=None)
        except Exception:
            pass

    if len(players) < BATTLE_MIN_PLAYERS:
        db_update_battle_status(battle_id, "cancelled")
        # Refund pot to host
        try:
            update_balance(row["host_id"], row["pot_qc"])
            record_transaction(row["host_id"], "credit", "battle_refund",
                               row["pot_qc"],
                               "Battle cancelled (not enough players)")
        except Exception:
            pass
        await channel.send(
            f"❌ Battle #{battle_id} cancelled. Not enough players.")
        return

    db_update_battle_status(battle_id, "started")
    # Run simulation
    ratio_vals = [float(x) for x in str(row["ratio"]).split("-") if x]
    await run_battle(channel, battle_id, float(row["pot_qc"]), ratio_vals,
                     players)


async def run_battle(channel, bid: int, pot_qc: float, ratios: List[float],
                     players: List[int]):
    alive = players.copy()
    random.shuffle(alive)
    eliminated = []
    intro = discord.Embed(
        title="⚔️ Battle Royale Begins!",
        description=f"{len(players)} enter, one leaves alive…",
        color=discord.Color.orange())
    await channel.send(embed=intro)

    while len(alive) > 1:
        await asyncio.sleep(random.uniform(*BATTLE_EVENT_DELAY))
        a, b = random.sample(alive, 2)
        killer, victim = (a, b) if random.random() >= 0.3 else (b, a)
        alive.remove(victim)
        eliminated.append(victim)
        desc = _pick_event_template().format(killer=_mention(killer),
                                             victim=_mention(victim))
        embed = discord.Embed(title="💥 Elimination",
                              description=desc,
                              color=discord.Color.red())
        embed.set_footer(
            text=f"Alive: {len(alive)} | Eliminated: {len(eliminated)}")
        await channel.send(embed=embed)

    winner = alive[0]
    placements = [winner] + list(reversed(eliminated))
    podium = [
        f"{i+1}. {_mention(placements[i])} — {int(ratios[i])}%"
        for i in range(min(len(ratios), len(placements)))
    ]
    result = discord.Embed(title="🏁 Battle Finished",
                           description=f"Winner: {_mention(winner)}\n\n" +
                           "\n".join(podium),
                           color=discord.Color.green())
    await channel.send(embed=result)

    # payouts
    top_n = min(len(ratios), len(placements))
    for i in range(top_n):
        uid = placements[i]
        share = round(pot_qc * (ratios[i] / 100.0), 6)
        if share > 0:
            try:
                update_balance(uid, share)
                record_transaction(uid, "credit", "battle_prize", share,
                                   f"Battle placement #{i+1}")
            except Exception:
                pass
    db_update_battle_status(bid, "finished", winner)
