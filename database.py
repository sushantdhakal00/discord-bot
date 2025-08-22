import logging
import os
import sqlite3
import threading
import json
import base64
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple

import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DB_PATH: str = os.getenv("QUANTA_DB_PATH", "quanta.db")
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
HOUSE_SECRET = os.getenv("SOLANA_SECRET_KEY")  # can be base58, base64, or JSON

_log = logging.getLogger("quanta.database")

# SQLite PRAGMAs for performance & safety
_PRAGMAS: Tuple[Tuple[str, Any], ...] = (
    ("journal_mode", "wal"),
    ("foreign_keys", 1),
    ("synchronous", 1),
    ("cache_size", 8192),
    ("busy_timeout", 5000),
)

# -----------------------------------------------------------------------------
# Load house wallet key (supports base58, JSON, base64 seed)
# -----------------------------------------------------------------------------
if not HOUSE_SECRET:
    raise SystemExit("❌ Missing SOLANA_SECRET_KEY in env")

_house: Optional[Keypair] = None

# Try base58 full 64-byte keypair
try:
    _house = Keypair.from_base58_string(HOUSE_SECRET)
    _log.info("Loaded house wallet from base58 string")
except Exception:
    pass

# Try JSON array (Solana CLI id.json)
if _house is None:
    try:
        raw_64 = bytes(json.loads(HOUSE_SECRET))
        if len(raw_64) == 64:
            _house = Keypair.from_bytes(raw_64)
            _log.info("Loaded house wallet from JSON array")
    except Exception:
        pass

# Try base64 32-byte seed
if _house is None:
    try:
        seed32 = base64.b64decode(HOUSE_SECRET)
        if len(seed32) == 32:
            _house = Keypair.from_seed(seed32)
            _log.info("Loaded house wallet from base64 32-byte seed")
    except Exception:
        pass

if _house is None:
    raise SystemExit(
        "❌ Failed to parse SOLANA_SECRET_KEY in any supported format")

_log.info("House wallet public key: %s", _house.pubkey())

# -----------------------------------------------------------------------------
# SQLite globals
# -----------------------------------------------------------------------------
_lock = threading.Lock()
_conn: Optional[sqlite3.Connection] = None


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    """Check if a column exists in a table."""
    row = conn.execute(
        f"SELECT 1 FROM pragma_table_info('{table}') WHERE name=?",
        (column, ),
    ).fetchone()
    return row is not None


def _ensure_columns(conn: sqlite3.Connection) -> None:
    if not _column_exists(conn, "users", "sol_address"):
        conn.execute("ALTER TABLE users ADD COLUMN sol_address TEXT")
        _log.info("Added missing column: sol_address")
    if not _column_exists(conn, "users", "sol_balance"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN sol_balance REAL NOT NULL DEFAULT 0")
        _log.info("Added missing column: sol_balance")
    if not _column_exists(conn, "users", "last_deposit_signature"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN last_deposit_signature TEXT")
        _log.info("Added missing column: last_deposit_signature")
    if not _column_exists(conn, "users", "last_deposit_at"):
        conn.execute("ALTER TABLE users ADD COLUMN last_deposit_at TEXT")
        _log.info("Added missing column: last_deposit_at")
    if not _column_exists(conn, "users", "total_sol_deposited"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN total_sol_deposited REAL NOT NULL DEFAULT 0"
        )
        _log.info("Added missing column: total_sol_deposited")


def _init_schema(conn: sqlite3.Connection) -> None:
    """Create base schema for a new DB."""
    conn.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS users (
        user_id         INTEGER PRIMARY KEY,
        balance         REAL    NOT NULL DEFAULT 0,
        total_wagered   REAL    NOT NULL DEFAULT 0,
        net_profit_loss REAL    NOT NULL DEFAULT 0,
        total_depo      REAL    NOT NULL DEFAULT 0,
        total_withdraw  REAL    NOT NULL DEFAULT 0,
        sol_address     TEXT,
        sol_balance     REAL    NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS meta (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', 1);
    COMMIT;
    """)


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        first = not Path(DB_PATH).exists()
        _conn = sqlite3.connect(DB_PATH,
                                isolation_level=None,
                                check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        for pragma, val in _PRAGMAS:
            _conn.execute(f"PRAGMA {pragma} = {val}")
        if first:
            _init_schema(_conn)
        try:
            _ensure_columns(_conn)
            _init_rewards_table(_conn)
            _init_loans_table(_conn)
            _ensure_battle_schema(_conn)
            airdrop_init_schema()
            _ensure_guild_access_schema()
            _withdraw_init_schema()
            ensure_lottery_tables()
        except Exception as e:
            _log.error(f"Schema initialization failed: {e}")
            raise
        _log.info("SQLite ready: %s", DB_PATH)
    return _conn


@contextmanager
def _transaction() -> Generator[sqlite3.Cursor, None, None]:
    """Thread-safe transaction block."""
    conn = get_conn()
    with _lock:
        conn.execute("BEGIN IMMEDIATE")
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        _log.exception("Transaction rolled back!")
        raise


# =============================================================================
# USER API
# =============================================================================


def create_user(user_id: int) -> None:
    with _transaction() as cur:
        cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                    (user_id, ))


def fetch_user(user_id: int) -> Dict[str, Any]:
    create_user(user_id)
    row = get_conn().execute("SELECT * FROM users WHERE user_id=?",
                             (user_id, )).fetchone()
    data = dict(row) if row else {}

    # Ensure defaults so old DBs without migration don't cause KeyError
    data.setdefault("sol_address", None)
    data.setdefault("sol_balance", 0.0)

    # 🆕 Deposit tracking defaults
    data.setdefault("last_deposit_signature", None)
    data.setdefault("last_deposit_at", None)
    data.setdefault("total_sol_deposited", 0.0)

    return data


def update_balance(user_id: int, delta: float) -> None:
    if delta == 0:
        return
    with _transaction() as cur:
        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",
                    (delta, user_id))


def update_stats(user_id: int, **fields: float) -> None:
    if not fields:
        return
    assigns = ", ".join(f"{k} = {k} + ?" for k in fields)
    params = list(fields.values()) + [user_id]
    with _transaction() as cur:
        cur.execute(f"UPDATE users SET {assigns} WHERE user_id = ?", params)

    def tip_coins(sender: int, recipient: int, amount: float) -> bool:
        if amount <= 0 or sender == recipient:
            return False
        with _transaction() as cur:
            # ensure both users exist
            cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                        (sender, ))
            cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                        (recipient, ))

            # check sender balance
            cur.execute("SELECT balance FROM users WHERE user_id=?",
                        (sender, ))
            bal = cur.fetchone()["balance"]
            if bal < amount:
                return False

            # move funds
            cur.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (amount, sender))
            cur.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, recipient))

    # Log the transactions
    log_transaction(
        user_id=sender,
        transaction_type="tip_sent",
        amount_qc=-amount,  # Negative for outgoing
        recipient_id=recipient)
    log_transaction(
        user_id=recipient,
        transaction_type="tip_received",
        amount_qc=amount,  # Positive for incoming
        sender_id=sender)
    return True


def deposit(user_id: int, amount: float) -> bool:
    if amount <= 0:
        return False
    with _transaction() as cur:
        cur.execute(
            """
            UPDATE users
            SET balance = balance + ?,
                total_depo = total_depo + ?
            WHERE user_id = ?
        """, (amount, amount, user_id))

    # Log the transaction
    log_transaction(
        user_id=user_id,
        transaction_type="deposit",
        amount_qc=amount,
        amount_sol=amount * 0.001  # 1 QC = 0.001 SOL
    )
    return True


def withdraw(user_id: int, amount: float) -> bool:
    if amount <= 0:
        return False
    with _transaction() as cur:
        cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id, ))
        bal = cur.fetchone()["balance"]
        if bal < amount:
            return False
        cur.execute(
            """
            UPDATE users
            SET balance = balance - ?,
                total_withdraw = total_withdraw + ?
            WHERE user_id = ?
        """, (amount, amount, user_id))

    # Log the transaction
    log_transaction(
        user_id=user_id,
        transaction_type="withdraw",
        amount_qc=amount,
        amount_sol=amount * 0.001  # 1 QC = 0.001 SOL
    )
    return True


def record_user_deposit(user_id: int, lamports: int, signature: str,
                        iso_time: str) -> None:
    sol_amount = lamports / 1_000_000_000
    with _transaction() as cur:
        cur.execute(
            """
            UPDATE users
            SET total_sol_deposited = total_sol_deposited + ?,
                last_deposit_signature = ?,
                last_deposit_at = ?
            WHERE user_id = ?
            """, (sol_amount, signature, iso_time, user_id))


# -----------------------------------------------------------------------------
# DEBUG CLI
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, pprint

    parser = argparse.ArgumentParser(
        description="Simple DB CLI for Quanta Coin")
    parser.add_argument("command",
                        choices=["get", "deposit", "withdraw", "tip"])
    parser.add_argument("args", nargs="+", help="Arguments for the command")
    ns = parser.parse_args()

    if ns.command == "get":
        uid = int(ns.args[0])
        pprint.pprint(fetch_user(uid))
    elif ns.command == "deposit":
        uid, amt = map(float, ns.args)
        deposit(int(uid), amt)
        print("Deposited.")
    elif ns.command == "withdraw":
        uid, amt = map(float, ns.args)
        withdraw(int(uid), amt)
        print("Withdrew.")
    elif ns.command == "tip":
        sender, dest, amt = map(float, ns.args)
        ok = tip_coins(int(sender), int(dest), amt)
        print("OK" if ok else "Failed")

from datetime import datetime


# --- Rewards schema/init ---
def _init_rewards_table(conn: sqlite3.Connection) -> None:
    """Create the user_rewards table if not exists."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_rewards (
            user_id INTEGER PRIMARY KEY,
            last_reward TEXT
        )
    """)


# Modify get_conn to also init rewards table
def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        first = not Path(DB_PATH).exists()
        _conn = sqlite3.connect(DB_PATH,
                                isolation_level=None,
                                check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        for pragma, val in _PRAGMAS:
            _conn.execute(f"PRAGMA {pragma} = {val}")
        if first:
            _init_schema(_conn)
        _ensure_columns(_conn)
        _init_rewards_table(_conn)  # <-- ensure rewards table exists
        _log.info("SQLite ready: %s", DB_PATH)
    return _conn


# --- Rewards helpers ---
def can_claim_reward(user_id: int) -> bool:
    """Return True if the user can claim today's reward."""
    _init_rewards_table(get_conn())
    today = datetime.utcnow().date().isoformat()
    row = get_conn().execute(
        "SELECT last_reward FROM user_rewards WHERE user_id=?",
        (user_id, )).fetchone()
    if row is None:
        return True
    return row["last_reward"] != today


def record_reward_claim(user_id: int) -> None:
    """Record that the user claimed today's reward."""
    _init_rewards_table(get_conn())
    today = datetime.utcnow().date().isoformat()
    with _transaction() as cur:
        cur.execute(
            "INSERT OR REPLACE INTO user_rewards (user_id, last_reward) VALUES (?, ?)",
            (user_id, today))


# --- Optional: expose a helper to ensure lottery tables from DB module ---
def ensure_lottery_tables():
    conn = get_conn()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lottery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                entry_cost REAL NOT NULL,
                pot REAL NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL,
                ends_at INTEGER NOT NULL,
                winner_id INTEGER,
                channel_id INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lottery_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lottery_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(lottery_id) REFERENCES lottery(id)
            )
        """)


def record_transaction(user_id: int,
                       type_: str,
                       category: str,
                       amount: float,
                       description: str = "") -> None:
    # Stub: no-op so cogs can import and call this without requiring a transactions table.
    # Later you can implement real logging without changing your cogs.
    return


# ===== Airdrop DB schema and helpers =====
# Requirements:
# - get_conn() -> sqlite3.Connection
# - _transaction() context manager
# These should already exist in your database layer.

import time
from typing import Optional, List, Dict, Any


def airdrop_init_schema():
    """
    Initialize or upgrade the airdrop schema.
    Adds guild_id and scope if missing (migration-safe).
    """
    conn = get_conn()
    with _transaction() as cur:
        # Core tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS airdrop (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT NOT NULL UNIQUE,       -- human-friendly ID
            status TEXT NOT NULL,                 -- 'open','settled','cancelled'
            amount_qc REAL NOT NULL,              -- total QC reserved
            created_at INTEGER NOT NULL,          -- epoch seconds
            ends_at INTEGER NOT NULL,             -- epoch seconds
            created_by INTEGER NOT NULL,          -- user_id
            channel_id INTEGER,                   -- origin channel
            guild_id INTEGER,                     -- origin guild (for local scope)
            scope TEXT NOT NULL DEFAULT 'local',  -- 'local' or 'public'
            note TEXT                             -- optional metadata
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS airdrop_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airdrop_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at INTEGER NOT NULL,
            UNIQUE(airdrop_id, user_id),
            FOREIGN KEY(airdrop_id) REFERENCES airdrop(id) ON DELETE CASCADE
        )
        """)

        # Migration: ensure guild_id and scope exist
        try:
            cols = {
                r[1]
                for r in conn.execute("PRAGMA table_info(airdrop)").fetchall()
            }
            if "guild_id" not in cols:
                cur.execute("ALTER TABLE airdrop ADD COLUMN guild_id INTEGER")
            if "scope" not in cols:
                cur.execute(
                    "ALTER TABLE airdrop ADD COLUMN scope TEXT NOT NULL DEFAULT 'local'"
                )
        except Exception:
            # If PRAGMA fails for any reason, we skip; table definition above covers new installs.
            pass


def airdrop_create(
    unique_id: str,
    amount_qc: float,
    duration_seconds: int,
    created_by: int,
    channel_id: Optional[int],
    guild_id: Optional[int],
    scope: str = "local",
    note: str = "",
) -> int:
    """
    Create a new airdrop record (status='open').
    Returns the inserted row id (PK).
    """
    now = int(time.time())
    ends = now + int(duration_seconds)
    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO airdrop (unique_id, status, amount_qc, created_at, ends_at, created_by, channel_id, guild_id, scope, note)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
                unique_id,
                "open",
                float(amount_qc),
                now,
                ends,
                int(created_by),
                channel_id,
                guild_id,
                scope,
                note,
            ))
        return cur.lastrowid


def airdrop_get_by_unique(unique_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch an airdrop by its human-friendly unique ID.
    """
    row = get_conn().execute("SELECT * FROM airdrop WHERE unique_id=?",
                             (unique_id, )).fetchone()
    return dict(row) if row else None


def airdrop_get_by_id(airdrop_pk: int) -> Optional[Dict[str, Any]]:
    """
    Fetch an airdrop by primary key (internal ID).
    """
    row = get_conn().execute("SELECT * FROM airdrop WHERE id=?",
                             (airdrop_pk, )).fetchone()
    return dict(row) if row else None


def airdrop_list_open(limit: int = 100) -> List[Dict[str, Any]]:
    """
    List up to 'limit' open airdrops ordered by soonest ending.
    """
    rows = get_conn().execute(
        "SELECT * FROM airdrop WHERE status='open' ORDER BY ends_at ASC LIMIT ?",
        (int(limit), ),
    ).fetchall()
    return [dict(r) for r in rows] if rows else []


def airdrop_recent(limit: int = 10) -> List[Dict[str, Any]]:
    """
    List recent airdrops (any status), newest first.
    """
    rows = get_conn().execute(
        "SELECT * FROM airdrop ORDER BY id DESC LIMIT ?",
        (int(limit), ),
    ).fetchall()
    return [dict(r) for r in rows] if rows else []


def airdrop_add_claim(airdrop_pk: int, user_id: int) -> None:
    """
    Register a user for an airdrop (idempotent).
    """
    now = int(time.time())
    with _transaction() as cur:
        cur.execute(
            """
            INSERT OR IGNORE INTO airdrop_claims (airdrop_id, user_id, joined_at)
            VALUES (?,?,?)
        """, (airdrop_pk, int(user_id), now))


def airdrop_fetch_claimants(airdrop_pk: int) -> List[int]:
    """
    Get a list of user IDs who joined an airdrop.
    """
    rows = get_conn().execute(
        "SELECT user_id FROM airdrop_claims WHERE airdrop_id=?",
        (airdrop_pk, ),
    ).fetchall()
    return [int(r["user_id"] if hasattr(r, "keys") else r[0]) for r in rows]


def airdrop_mark_settled(airdrop_pk: int) -> None:
    """
    Mark an airdrop as settled (distribution completed).
    """
    with _transaction() as cur:
        cur.execute(
            "UPDATE airdrop SET status='settled' WHERE id=?",
            (airdrop_pk, ),
        )


def airdrop_cancel(airdrop_pk: int) -> None:
    """
    Mark an airdrop as cancelled (funds should be refunded by caller).
    """
    with _transaction() as cur:
        cur.execute(
            "UPDATE airdrop SET status='cancelled' WHERE id=?",
            (airdrop_pk, ),
        )


# database.py
import sqlite3, threading, time
from pathlib import Path
from contextlib import contextmanager

DB_PATH = "quanta.db"
_lock = threading.Lock()
_conn = None


def get_conn():
    global _conn
    if _conn is None:
        first = not Path(DB_PATH).exists()
        _conn = sqlite3.connect(DB_PATH,
                                isolation_level=None,
                                check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        if first: _init_schema(_conn)
    return _conn


def _init_schema(conn):
    with conn:
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
            status TEXT,             -- open, started, finished, cancelled
            winner_id INTEGER
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS battle_participants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            battle_id INTEGER,
            user_id INTEGER,
            joined_at INTEGER,
            UNIQUE(battle_id,user_id)
        )""")


@contextmanager
def _tx():
    conn = get_conn()
    with _lock:
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except:
            conn.rollback()
            raise


def db_create_battle(channel_id, host_id, pot_qc, ratio, max_players,
                     duration):
    now = int(time.time())
    ends = now + duration
    with _tx() as cur:
        cur.execute(
            """INSERT INTO battles(channel_id,host_id,pot_qc,ratio,max_players,created_at,ends_at,status)
                      VALUES(?,?,?,?,?,?,?,?)""",
            (channel_id, host_id, pot_qc, ratio, max_players, now, ends,
             "open"))
        return cur.lastrowid


def db_add_participant(battle_id, user_id):
    with _tx() as cur:
        cur.execute(
            """INSERT OR IGNORE INTO battle_participants(battle_id,user_id,joined_at)
                      VALUES(?,?,?)""", (battle_id, user_id, int(time.time())))


def db_update_battle_status(bid, status, winner_id=None):
    with _tx() as cur:
        cur.execute("UPDATE battles SET status=?, winner_id=? WHERE id=?",
                    (status, winner_id, bid))


def db_get_battle(bid):
    return get_conn().execute("SELECT * FROM battles WHERE id=?",
                              (bid, )).fetchone()


def db_list_participants(bid):
    return [
        r["user_id"] for r in get_conn().execute(
            "SELECT user_id FROM battle_participants WHERE battle_id=?", (
                bid, ))
    ]


def db_list_open():
    return get_conn().execute(
        "SELECT * FROM battles WHERE status='open' ORDER BY id DESC").fetchall(
        )


def db_list_recent(limit=5):
    return get_conn().execute("SELECT * FROM battles ORDER BY id DESC LIMIT ?",
                              (limit, )).fetchall()


# database.py — Guild paywall utilities for "pay once per server"

import time
import sqlite3
from typing import Optional

# These should already exist in your project:
# from your_db_module import get_conn, _transaction


def _ensure_guild_access_schema():
    """
    Create tables to track guild activation and grandfathered servers (joined before paywall).
    - guild_access: records paid/bypassed status
    - guild_grandfathered: one-time list of servers that were already in before feature launch
    """
    conn = get_conn()
    with _transaction() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS guild_access (
            guild_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL,         -- 'paid', 'bypass'
            paid_by INTEGER,              -- user id who paid or set bypass (for audit)
            amount_qc REAL NOT NULL DEFAULT 0,
            created_at INTEGER NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS guild_grandfathered (
            guild_id INTEGER PRIMARY KEY,
            noted_at INTEGER NOT NULL
        )
        """)


def guild_mark_grandfathered(guild_id: int):
    """
    Mark guild as grandfathered (free forever, no paywall), used exactly once
    at feature-activation time when the bot starts, to capture already-joined servers.
    """
    _ensure_guild_access_schema()
    with _transaction() as cur:
        cur.execute(
            "INSERT OR IGNORE INTO guild_grandfathered (guild_id, noted_at) VALUES (?, ?)",
            (int(guild_id), int(time.time())))


def guild_is_grandfathered(guild_id: int) -> bool:
    _ensure_guild_access_schema()
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM guild_grandfathered WHERE guild_id=?",
                       (int(guild_id), )).fetchone()
    return bool(row)


def guild_is_paid(guild_id: int) -> bool:
    """
    True if guild has status 'paid' or 'bypass'.
    """
    _ensure_guild_access_schema()
    conn = get_conn()
    row = conn.execute("SELECT status FROM guild_access WHERE guild_id=?",
                       (int(guild_id), )).fetchone()
    if not row:
        return False
    status = str(row["status"]) if hasattr(row, "keys") else str(row[0])
    return status in ("paid", "bypass")


def guild_mark_paid(guild_id: int, user_id: int, amount_qc: float):
    _ensure_guild_access_schema()
    with _transaction() as cur:
        cur.execute(
            "INSERT OR REPLACE INTO guild_access (guild_id, status, paid_by, amount_qc, created_at) VALUES (?, 'paid', ?, ?, ?)",
            (int(guild_id), int(user_id), float(amount_qc), int(time.time())))


def guild_mark_bypass(guild_id: int, by_user_id: int):
    _ensure_guild_access_schema()
    with _transaction() as cur:
        cur.execute(
            "INSERT OR REPLACE INTO guild_access (guild_id, status, paid_by, amount_qc, created_at) VALUES (?, 'bypass', ?, 0, ?)",
            (int(guild_id), int(by_user_id), int(time.time())))


def guild_access_status(guild_id: int) -> Optional[dict]:
    """
    Return status dict or None.
    """
    _ensure_guild_access_schema()
    conn = get_conn()
    row = conn.execute(
        "SELECT guild_id, status, paid_by, amount_qc, created_at FROM guild_access WHERE guild_id=?",
        (int(guild_id), )).fetchone()
    if not row:
        return None
    d = dict(row) if hasattr(row, "keys") else {
        "guild_id": row[0],
        "status": row[1],
        "paid_by": row[2],
        "amount_qc": row[3],
        "created_at": row[4],
    }
    return d


# ===== Withdraw Book + Withdraw Logs (Schema + Helpers) =====


def _withdraw_init_schema():
    conn = get_conn()
    with _transaction() as cur:
        # Address book (nickname -> SOL address per user)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS withdraw_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nickname TEXT NOT NULL,
            sol_address TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            UNIQUE(user_id, nickname)
        )
        """)
        # Withdraw logs
        cur.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount_qc REAL NOT NULL,
            amount_sol REAL NOT NULL,
            amount_usd REAL,
            dest_nickname TEXT,
            dest_address TEXT,
            status TEXT NOT NULL,       -- pending, confirmed, sent, failed, cancelled
            signature TEXT,
            error TEXT,
            fee_lamports INTEGER,
            net_lamports INTEGER,
            created_at INTEGER NOT NULL,
            confirmed_at INTEGER,
            sent_at INTEGER
        )
        """)
        # Transaction history table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,  -- deposit, withdraw, tip_sent, tip_received, game_wager, game_win, game_loss, airdrop, lottery, loan
            amount_qc REAL NOT NULL,
            amount_sol REAL,
            amount_usd REAL,
            game_name TEXT,              -- for game transactions
            game_details TEXT,           -- JSON details like bet type, result, etc.
            recipient_id INTEGER,        -- for tips, transfers
            sender_id INTEGER,           -- for tips, transfers
            reference_id INTEGER,        -- withdrawal ID, game session ID, etc.
            created_at INTEGER NOT NULL,
            balance_after REAL NOT NULL
        )
        """)
        # Create index for faster queries
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_user_time 
        ON transactions(user_id, created_at DESC)
        """)
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_type 
        ON transactions(transaction_type)
        """)


# Call once at startup
try:
    _withdraw_init_schema()
except Exception as e:
    log.warning(f"[WITHDRAW] Schema init deferred: {e}")

# =============================================================================
# TRANSACTION HISTORY API
# =============================================================================


def log_transaction(user_id: int,
                    transaction_type: str,
                    amount_qc: float,
                    amount_sol: float = None,
                    amount_usd: float = None,
                    game_name: str = None,
                    game_details: dict = None,
                    recipient_id: int = None,
                    sender_id: int = None,
                    reference_id: int = None) -> int:
    """
    Log a transaction to the transaction history table.
    Returns the transaction ID.
    """
    import time
    import json

    # Get current balance after the transaction
    user = fetch_user(user_id)
    balance_after = user.get("balance", 0.0)

    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO transactions (
                user_id, transaction_type, amount_qc, amount_sol, amount_usd,
                game_name, game_details, recipient_id, sender_id, reference_id,
                created_at, balance_after
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, transaction_type,
              float(amount_qc), amount_sol, amount_usd, game_name,
              json.dumps(game_details) if game_details else None, recipient_id,
              sender_id, reference_id, int(time.time()), balance_after))
        return cur.lastrowid


def get_user_transactions(user_id: int,
                          transaction_type: str = None,
                          limit: int = 50,
                          offset: int = 0) -> list:
    """
    Get transaction history for a user with optional filtering.
    Returns list of transaction records.
    """
    query = """
        SELECT * FROM transactions 
        WHERE user_id = ?
    """
    params = [user_id]

    if transaction_type:
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = get_conn().execute(query, params).fetchall()
    return [dict(row) for row in rows] if rows else []


def get_user_transaction_count(user_id: int,
                               transaction_type: str = None) -> int:
    """
    Get total count of transactions for a user with optional filtering.
    """
    query = "SELECT COUNT(*) as count FROM transactions WHERE user_id = ?"
    params = [user_id]

    if transaction_type:
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    row = get_conn().execute(query, params).fetchone()
    return row["count"] if row else 0


def get_transaction_summary(user_id: int) -> dict:
    """
    Get a summary of all transaction types for a user.
    """
    query = """
        SELECT 
            transaction_type,
            COUNT(*) as count,
            SUM(amount_qc) as total_qc,
            SUM(amount_sol) as total_sol,
            SUM(amount_usd) as total_usd
        FROM transactions 
        WHERE user_id = ?
        GROUP BY transaction_type
        ORDER BY transaction_type
    """

    rows = get_conn().execute(query, [user_id]).fetchall()
    summary = {}

    for row in rows:
        summary[row["transaction_type"]] = {
            "count": row["count"],
            "total_qc": row["total_qc"] or 0.0,
            "total_sol": row["total_sol"] or 0.0,
            "total_usd": row["total_usd"] or 0.0
        }

    return summary


# -------- Address book helpers --------
def wb_upsert(user_id: int, nickname: str, sol_address: str):
    import time
    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO withdraw_book(user_id, nickname, sol_address, created_at)
            VALUES(?,?,?,?)
            ON CONFLICT(user_id, nickname) DO UPDATE SET sol_address=excluded.sol_address
        """, (user_id, nickname.strip().lower(), sol_address.strip(),
              int(time.time())))


def wb_get(user_id: int, nickname: str) -> str | None:
    row = get_conn().execute(
        """
        SELECT sol_address FROM withdraw_book
        WHERE user_id=? AND nickname=?
    """, (user_id, nickname.strip().lower())).fetchone()
    return row["sol_address"] if row else None


def wb_list(user_id: int):
    rows = get_conn().execute(
        """
        SELECT nickname, sol_address FROM withdraw_book
        WHERE user_id=? ORDER BY nickname
    """, (user_id, )).fetchall()
    return [(r["nickname"], r["sol_address"]) for r in rows] if rows else []


def wb_delete(user_id: int, nickname: str) -> bool:
    with _transaction() as cur:
        cur.execute("DELETE FROM withdraw_book WHERE user_id=? AND nickname=?",
                    (user_id, nickname.strip().lower()))
        return cur.rowcount > 0


# -------- Withdraw log helpers --------
def wlog_create(user_id: int,
                amount_qc: float,
                amount_sol: float,
                amount_usd: float | None,
                dest_nickname: str | None,
                dest_address: str | None,
                status: str = "pending") -> int:
    import time
    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO withdrawals(user_id, amount_qc, amount_sol, amount_usd, dest_nickname, dest_address,
                                    status, created_at)
            VALUES(?,?,?,?,?,?,?,?)
        """, (user_id, float(amount_qc), float(amount_sol), amount_usd,
              (dest_nickname.strip().lower() if dest_nickname else None),
              (dest_address.strip() if dest_address else None), status,
              int(time.time())))
        return cur.lastrowid


def wlog_update_status(wid: int, status: str, **fields):
    sets = ["status=?"]
    vals = [status]
    if "signature" in fields:
        sets.append("signature=?")
        vals.append(fields["signature"])
    if "error" in fields:
        sets.append("error=?")
        vals.append(fields["error"])
    if "fee_lamports" in fields:
        sets.append("fee_lamports=?")
        vals.append(int(fields["fee_lamports"]))
    if "net_lamports" in fields:
        sets.append("net_lamports=?")
        vals.append(int(fields["net_lamports"]))
    if "confirmed" in fields:
        sets.append("confirmed_at=?")
        vals.append(int(fields["confirmed"]))
    if "sent" in fields:
        sets.append("sent_at=?")
        vals.append(int(fields["sent"]))
    with _transaction() as cur:
        cur.execute(f"UPDATE withdrawals SET {', '.join(sets)} WHERE id=?",
                    (*vals, wid))


import logging
import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple
import random
import time

# Configuration
DB_PATH: str = os.getenv("QUANTA_DB_PATH", "quanta.db")
_log = logging.getLogger("quanta.database")

# SQLite PRAGMAs for performance & safety
_PRAGMAS: Tuple[Tuple[str, Any], ...] = (
    ("journal_mode", "wal"),
    ("foreign_keys", 1),
    ("synchronous", 1),
    ("cache_size", 8192),
    ("busy_timeout", 5000),
)

# SQLite globals
_lock = threading.Lock()
_conn: Optional[sqlite3.Connection] = None


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    row = conn.execute(
        f"SELECT 1 FROM pragma_table_info('{table}') WHERE name=?",
        (column, ),
    ).fetchone()
    return row is not None


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance REAL NOT NULL DEFAULT 0,
        total_wagered REAL NOT NULL DEFAULT 0,
        net_profit_loss REAL NOT NULL DEFAULT 0,
        total_depo REAL NOT NULL DEFAULT 0,
        total_withdraw REAL NOT NULL DEFAULT 0,
        sol_address TEXT,
        sol_balance REAL NOT NULL DEFAULT 0,
        loan_banned INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', 1);
    COMMIT;
    """)


def _ensure_columns(conn: sqlite3.Connection) -> None:
    if not _column_exists(conn, "users", "total_depo"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN total_depo REAL NOT NULL DEFAULT 0")
    if not _column_exists(conn, "users", "total_withdraw"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN total_withdraw REAL NOT NULL DEFAULT 0"
        )
    if not _column_exists(conn, "users", "sol_address"):
        conn.execute("ALTER TABLE users ADD COLUMN sol_address TEXT")
    if not _column_exists(conn, "users", "sol_balance"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN sol_balance REAL NOT NULL DEFAULT 0")
    if not _column_exists(conn, "users", "loan_banned"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN loan_banned INTEGER NOT NULL DEFAULT 0"
        )


def _init_rewards_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_rewards (
            user_id INTEGER PRIMARY KEY,
            last_reward TEXT
        )
    """)


def _init_loans_table(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unique_id TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        principal_qc REAL NOT NULL,
        duration_sec INTEGER NOT NULL,
        due_date INTEGER NOT NULL,
        status TEXT NOT NOT NULL DEFAULT 'pending',
        created_at INTEGER NOT NULL,
        approved_by INTEGER,
        withdraw_during_loan INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    if not _column_exists(conn, "users", "loan_banned"):
        conn.execute(
            "ALTER TABLE users ADD COLUMN loan_banned INTEGER NOT NULL DEFAULT 0"
        )


def _ensure_battle_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS battles (
        battle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at INTEGER NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users(user_id)
    );
    CREATE TABLE IF NOT EXISTS battle_participants (
        battle_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        joined_at INTEGER NOT NULL,
        PRIMARY KEY (battle_id, user_id),
        FOREIGN KEY (battle_id) REFERENCES battles(battle_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)


def airdrop_init_schema() -> None:
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS airdrop (
        airdrop_id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        max_users INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at INTEGER NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users(user_id)
    );
    CREATE TABLE IF NOT EXISTS airdrop_claims (
        airdrop_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        claimed_at INTEGER NOT NULL,
        PRIMARY KEY (airdrop_id, user_id),
        FOREIGN KEY (airdrop_id) REFERENCES airdrop(airdrop_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)


def _ensure_guild_access_schema() -> None:
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS guild_access (
        guild_id INTEGER PRIMARY KEY,
        access_type TEXT NOT NULL DEFAULT 'all'
    );
    CREATE TABLE IF NOT EXISTS guild_grandfathered (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (guild_id, user_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)


def _withdraw_init_schema() -> None:
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS withdraw_book (
        user_id INTEGER PRIMARY KEY,
        sol_address TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    CREATE TABLE IF NOT EXISTS withdrawals (
        withdrawal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        sol_address TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at INTEGER NOT NULL,
        tx_signature TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)


def ensure_lottery_tables() -> None:
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS lottery (
        lottery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        max_tickets INTEGER NOT NULL,
        ticket_price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at INTEGER NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users(user_id)
    );
    CREATE TABLE IF NOT EXISTS lottery_entries (
        lottery_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        ticket_count INTEGER NOT NULL,
        entered_at INTEGER NOT NULL,
        PRIMARY KEY (lottery_id, user_id),
        FOREIGN KEY (lottery_id) REFERENCES lottery(lottery_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)


@contextmanager
def _transaction() -> Generator[sqlite3.Cursor, None, None]:
    conn = get_conn()
    with _lock:
        conn.execute("BEGIN IMMEDIATE")
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        _log.exception("Transaction rolled back!")
        raise


def fetch_user(user_id: int) -> Dict[str, Any]:
    with _transaction() as cur:
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, balance, total_wagered, net_profit_loss, total_depo, total_withdraw, sol_balance, loan_banned) VALUES (?, 0, 0, 0, 0, 0, 0, 0)",
            (user_id, ))
        row = cur.execute("SELECT * FROM users WHERE user_id = ?",
                          (user_id, )).fetchone()
    return dict(row) if row else {}


def update_balance(user_id: int, delta: float) -> None:
    with _transaction() as cur:
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, balance, total_wagered, net_profit_loss, total_depo, total_withdraw, sol_balance, loan_banned) VALUES (?, 0, 0, 0, 0, 0, 0, 0)",
            (user_id, ))
        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",
                    (delta, user_id))


# --- LOANS: schema + helpers (database.py) ---
import sqlite3
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager

# Assumes your module already exposes:
# get_conn() -> sqlite3.Connection
# _transaction() -> @contextmanager yielding cursor


def loans_init_schema() -> None:
    """
    Create/migrate loan tables and supporting meta/flags. Idempotent.
    """
    conn = get_conn()
    with _transaction() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS loans(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            principal_qc REAL NOT NULL,
            duration_sec INTEGER NOT NULL,
            due_date INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',  -- pending|active|repaid|denied|defaulted
            created_at INTEGER NOT NULL,
            approved_by INTEGER,
            withdraw_during_loan INTEGER NOT NULL DEFAULT 0
        )
        """)
        # user flag
        try:
            conn.execute(
                "ALTER TABLE users ADD COLUMN loan_banned INTEGER NOT NULL DEFAULT 0"
            )
        except Exception:
            pass
        # meta store for loan-wide flags (pause, caps, thresholds, etc.)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """)
        # default meta keys if missing
        defaults = {
            "loans_paused": "0",
            "loans_total_outstanding_cap_qc": "100000",  # global cap
        }
        for k, v in defaults.items():
            cur.execute("INSERT OR IGNORE INTO meta(key,value) VALUES(?,?)",
                        (k, v))


def _meta_get(key: str, default: str = "") -> str:
    row = get_conn().execute("SELECT value FROM meta WHERE key=?",
                             (key, )).fetchone()
    return (row["value"]
            if row and "value" in row.keys() else row[0]) if row else default


def _meta_set(key: str, value: str) -> None:
    with _transaction() as cur:
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)",
                    (key, value))


def loans_paused() -> bool:
    return _meta_get("loans_paused", "0") == "1"


def loans_set_paused(flag: bool) -> None:
    _meta_set("loans_paused", "1" if flag else "0")


def loans_outstanding_cap_qc() -> float:
    try:
        return float(_meta_get("loans_total_outstanding_cap_qc", "100000"))
    except Exception:
        return 100000.0


def loans_set_outstanding_cap_qc(v: float) -> None:
    _meta_set("loans_total_outstanding_cap_qc", f"{float(v):.6f}")


def loans_total_outstanding_qc() -> float:
    """
    Sum principal of active loans; a simple measure of risk.
    """
    row = get_conn().execute(
        "SELECT COALESCE(SUM(principal_qc),0) AS s FROM loans WHERE status='active'"
    ).fetchone()
    if not row:
        return 0.0
    try:
        return float(row["s"] if hasattr(row, "keys") else row[0])
    except Exception:
        return 0.0


def loans_has_status(user_id: int, status: str) -> bool:
    row = get_conn().execute(
        "SELECT 1 FROM loans WHERE user_id=? AND status=? LIMIT 1",
        (int(user_id), status),
    ).fetchone()
    return bool(row)


def loans_get_by_unique(unique_id: str) -> Optional[Dict[str, Any]]:
    row = get_conn().execute("SELECT * FROM loans WHERE unique_id=?",
                             (unique_id, )).fetchone()
    return dict(row) if row else None


def loans_get_active(user_id: int) -> Optional[Dict[str, Any]]:
    row = get_conn().execute(
        "SELECT * FROM loans WHERE user_id=? AND status='active' LIMIT 1",
        (int(user_id), ),
    ).fetchone()
    return dict(row) if row else None


def loans_get_pending(user_id: int) -> Optional[Dict[str, Any]]:
    row = get_conn().execute(
        "SELECT * FROM loans WHERE user_id=? AND status='pending' LIMIT 1",
        (int(user_id), ),
    ).fetchone()
    return dict(row) if row else None


def loans_list(status: Optional[str] = None,
               limit: int = 50) -> list[Dict[str, Any]]:
    if status:
        rows = get_conn().execute(
            "SELECT * FROM loans WHERE status=? ORDER BY id DESC LIMIT ?",
            (status, int(limit)),
        ).fetchall()
    else:
        rows = get_conn().execute(
            "SELECT * FROM loans ORDER BY id DESC LIMIT ?",
            (int(limit), ),
        ).fetchall()
    return [dict(r) for r in rows]


def loans_create_pending(user_id: int, principal_qc: float,
                         duration_sec: int) -> str:
    """
    Insert a pending loan; returns unique loan id.
    """
    unique_id = f"LOAN-{int(time.time()*1000)%100000000}"
    now = int(time.time())
    due = now + int(duration_sec)
    with _transaction() as cur:
        cur.execute(
            """
            INSERT INTO loans(unique_id, user_id, principal_qc, duration_sec, due_date, created_at, status)
            VALUES(?,?,?,?,?,?,'pending')
        """, (unique_id, int(user_id), float(principal_qc), int(duration_sec),
              int(due), now))
    return unique_id


def loans_update_status(loan_id: int,
                        status: str,
                        approved_by: int | None = None):
    with _transaction() as cur:
        if approved_by is None:
            cur.execute("UPDATE loans SET status=? WHERE id=?",
                        (status, int(loan_id)))
        else:
            cur.execute("UPDATE loans SET status=?, approved_by=? WHERE id=?",
                        (status, int(approved_by), int(loan_id)))


def loans_mark_withdraw_flag(user_id: int):
    """
    If user withdraws while an active loan exists, mark withdraw_during_loan=1 for that loan.
    """
    with _transaction() as cur:
        cur.execute(
            """
            UPDATE loans
            SET withdraw_during_loan=1
            WHERE user_id=? AND status='active'
        """, (int(user_id), ))
