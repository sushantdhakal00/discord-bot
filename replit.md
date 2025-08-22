# Overview

Queen Bot is a Discord bot that integrates Quanta Coin (QC) with the Solana blockchain. The bot provides a comprehensive gaming and economy system where users can deposit SOL, receive QC tokens at a 1:1000 rate, play provably fair casino games, and participate in airdrops. The system features on-chain deposits and withdrawals, ensuring real cryptocurrency backing for the in-game economy.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Discord Bot Interface**: Uses discord.py library for user interactions through Discord commands
- **Web Dashboard**: Flask-based web server providing real-time statistics and monitoring
- **Command System**: Prefix-based commands (!command) with premium gating and whitelisting
- **Rich Embeds**: Formatted Discord embeds for success/error messages and game interfaces

## Backend Architecture
- **Modular Design**: Separated concerns across multiple modules (commands, games, database, solana_integration)
- **Asynchronous Processing**: Built on asyncio for handling concurrent Discord events and Solana transactions
- **Premium Gate System**: Tiered access control with grandfathered servers and premium subscriptions
- **Provably Fair Gaming**: Cryptographic seed-based randomization for game integrity

## Data Storage
- **SQLite Database**: Local database for user balances, game history, and bot statistics
- **WAL Mode**: Write-Ahead Logging for improved concurrency and crash recovery
- **Thread-Safe Access**: Connection pooling and locking mechanisms for database operations
- **Wallet Management**: Secure storage of Solana keypairs with multiple format support (base58, JSON, base64)

## Gaming System
- **Casino Games**: Multiple games including dice, coinflip, blackjack, roulette, limbo, and keno
- **Tic-Tac-Toe**: Interactive multiplayer game with Discord button interface
- **House Edge**: Configurable 1% house edge across all games
- **Bet Limits**: Configurable minimum and maximum betting amounts for risk management

## Economy Features
- **QC Token System**: Internal economy token backed by real SOL deposits
- **Exchange Rate**: Fixed 1 QC = 0.001 SOL conversion rate
- **Tipping System**: Peer-to-peer QC transfers between users
- **Currency Conversion**: Real-time conversion to 20+ fiat currencies
- **Airdrop System**: Timed airdrops with public/private modes

# External Dependencies

## Blockchain Integration
- **Solana RPC**: Connection to Solana mainnet for on-chain operations
- **solana-py & solders**: Python libraries for Solana transaction handling
- **Wallet Management**: House wallet for managing deposits and withdrawals

## Discord Platform
- **Discord API**: Bot interactions through discord.py library
- **WebSocket Connections**: Real-time event handling for messages and interactions

## Web Services
- **Flask Web Server**: Dashboard and statistics API endpoints
- **Bootstrap & Font Awesome**: Frontend styling and icons
- **Real-time Updates**: Live statistics and monitoring capabilities

## External APIs
- **Forex-Python**: Currency conversion rates for fiat currencies
- **SOL Price Feeds**: Real-time SOL price data for conversions

## Development Dependencies
- **Python Environment**: Dotenv for configuration management
- **Logging System**: Comprehensive logging across all modules
- **Threading**: Thread-safe database operations and web server