# Project0001 Bot Completion Plan

## Goal

Build one personal assistant bot that you can talk to through Telegram and Discord. The bot should hold a natural conversation, remember useful context, and answer questions about everyday topics, trading, sports, and fitness with clear, accurate, practical responses.

The most important first milestone is communication: you should be able to message the bot reliably from Telegram and Discord and get a useful answer back.

## Current Capabilities

### Main Chat Bot

- `mainbot/main.py` runs a Telegram bot.
- It supports `/start`, `/reset`, `/remember`, and `/memory`.
- It receives text messages and passes them to `Brain`.
- `mainbot/brain.py` uses OpenAI to generate replies.
- It keeps short-term memory per Telegram chat.
- It detects likely personal preferences or user facts and asks "Should I remember this?" before saving.
- If `OPENAI_API_KEY` is missing, it tells you the key is not configured.

### Local Domain Helpers

- `mainbot/domain_tools.py` can answer a few structured questions before using OpenAI:
  - Fitness macro estimates.
  - Kelly bankroll sizing.
  - Simple sports win simulation.

### Fitness Code

- `fitnessbot/coach.py` can estimate calories and macros from bodyweight and goal.
- `fitnessbot/analytics.py` has basic weight trend and workout volume calculations.
- `fitnessbot/models.py` defines simple database tables for users, weight logs, workout logs, and nutrition logs.
- `fitnessbot/main.py` is now a harmless macro demo instead of a hard-coded database writer.

### Sports Code

- `sportsbot/agents/simulation_agent.py` can run a simple random simulation using two strength numbers.
- `sportsbot/ai/bankroll.py` can calculate Kelly stake sizing for decimal odds.
- `sportsbot/ai/predictor.py` contains a basic scikit-learn random forest wrapper.
- `sportsbot/agents/news_agent.py`, `odds_agent.py`, and `data/sports_api.py` now fail gracefully when keys or dependencies are missing.
- Sports API wrappers now use environment keys, timeouts, and error responses instead of hard-coded fake keys.

### Trading Code

- `tradebot/main.py` is now a safe placeholder that explains the trading capability is not built yet.
- It no longer imports missing modules or pretends live trading infrastructure exists.

### Obsidian

- This project folder contains `.obsidian/`, so it appears to be an Obsidian vault root.
- Markdown files created here should show up in Obsidian if this folder is opened as the vault.
- There is no active Obsidian API/plugin connector in the current Codex session.
- `Bot Memory.md` is now the first file-based long-term memory note for the bot.
- Telegram now has `/remember <thing>` and `/memory` commands.
- `Bot Memory.md` is organized into Core Profile, Preferences, Goals, Fitness, Trading, Sports, and Important Context.
- The bot only saves suggested memories after a yes/no confirmation.

## Current Project Layout

```text
Project0001/
  .env.example
  Bot Memory.md
  BOT_COMPLETION_PLAN.md
  README.md
  mainbot/
    main.py
    brain.py
    config.py
    domain_tools.py
    memory.py
    personality.py
    requirements.txt
    fitnessbot/
      main.py
      coach.py
      analytics.py
      database.py
      models.py
      requirements.txt
    sportsbot/
      main.py
      config.py
      requirements.txt
      agents/
        news_agent.py
        odds_agent.py
        simulation_agent.py
      ai/
        bankroll.py
        predictor.py
      data/
        sports_api.py
      database/
        db.py
        models.py
    tradebot/
      main.py
      layout.txt
```

## What Is Not Accurate, Incomplete, or Placeholder

### Discord

- Discord is not implemented yet.
- `DISCORD_BOT_TOKEN` is listed in `.env.example` and loaded by config.
- There is no Discord message handler.
- There is no shared app entry point that can run Telegram and Discord together.

### Telegram

- Telegram exists, but it is still MVP-level.
- It only handles text messages.
- There is no command for checking health/status.
- There is no graceful shutdown or admin-only controls.
- Short-term conversation memory is stored only in process memory, so it disappears when the bot restarts.
- Long-term personal memory is file-based in `Bot Memory.md`, but it does not yet support editing/deleting individual saved memories through chat.

### OpenAI Usage

- `Brain` currently uses chat completions directly.
- It does not use tool calling yet.
- It reads `Bot Memory.md` as personal context.
- It does not yet search all Obsidian/Markdown notes.
- It does not verify current facts with live APIs.
- It does not separate high-risk answers, such as financial, betting, medical, or fitness advice, into stricter response modes.

### Sports

- News, odds, and sports data wrappers are safer now, but they still need real API keys and provider choices.
- The active main virtualenv does not currently have `requests` installed, so sports API wrappers return a clear dependency error until sports dependencies are installed.
- Sports API calls still need provider-specific schemas and rate-limit handling.
- The simulation agent is a toy model and should not be treated as a real prediction engine.
- The predictor has no training data pipeline, feature schema, model persistence, evaluation, or backtesting.

### Trading

- `tradebot/main.py` is runnable as a placeholder only.
- There is no trading data provider connected.
- There is no broker integration.
- There is no paper-trading mode.
- There is no risk policy.
- There is no audit log for decisions.
- There is no protection against accidental live trading.

### Fitness

- Macro estimates are basic rules of thumb.
- There is no user profile connection to Telegram/Discord users.
- There is no real food logging flow.
- There is no workout logging command or chat parser.
- There is no persistence layer connected to the main bot.
- There is no medical disclaimer or safety handling for injury, eating disorder, or extreme diet questions.

### Database and Storage

- Fitness and sports each have separate SQLite ideas.
- The main chat bot has no persistent storage.
- There is no migration system.
- There is no unified user identity system across Telegram and Discord.
- There is no durable memory for preferences, goals, or prior conversations.

### Requirements

- There are multiple `requirements.txt` files.
- The sports requirements are very broad and include heavy packages that are not currently used.
- The main requirements do not include Discord support.
- `.env.example` now exists with the expected keys.
- There is no single reliable installation path yet.

## API Keys Needed

### Required for Chat MVP

- `OPENAI_API_KEY`
  - Needed for natural language responses.
- `TELEGRAM_BOT_TOKEN`
  - Needed to run the Telegram bot.
- `DISCORD_BOT_TOKEN`
  - Needed once Discord support is added.

### Likely Needed Later

- `NEWS_API_KEY`
  - For sports or market news if using NewsAPI.
- `ODDS_API_KEY`
  - For sports odds if using The Odds API.
- Sports data provider key
  - Possible providers: API-Sports, Sportradar, SportsDataIO, or another paid/free source.
- Market data API key
  - Possible providers: Alpha Vantage, Polygon, Twelve Data, Finnhub, IEX Cloud, Alpaca, or Yahoo Finance through `yfinance` for limited non-key usage.
- Broker API key
  - Only if live or paper trading is added.
  - Possible providers: Alpaca, Interactive Brokers, Tradier, or another broker.
- Obsidian integration key
  - Only if using a plugin such as Local REST API.
  - Not needed if the bot simply reads Markdown files from the vault folder.

## Recommended Environment Variables

Create one `.env` file for the main bot:

```text
OPENAI_API_KEY=
OPENAI_MODEL=
TELEGRAM_BOT_TOKEN=
DISCORD_BOT_TOKEN=
NEWS_API_KEY=
ODDS_API_KEY=
SPORTS_API_KEY=
MARKET_DATA_API_KEY=
BROKER_API_KEY=
BROKER_API_SECRET=
OBSIDIAN_VAULT_PATH=
```

Only `OPENAI_API_KEY` and one platform token are required for the first working chat milestone.

## Completion Roadmap

## Phase 1: Make Chat Work Reliably

Priority: highest.

- Keep `Brain` as the shared assistant brain.
- Keep Telegram as one adapter.
- Add Discord as a second adapter.
- Both Telegram and Discord should call the same `Brain.respond()` method.
- Use the existing `DISCORD_BOT_TOKEN` config setting.
- Add basic Discord message handling.
- Prevent the bot from responding to its own messages.
- Add clear startup logs.
- Add `/status` or equivalent command.
- Make `/reset` work for both platforms.

Expected result:

- You can talk to the same bot on Telegram and Discord.
- The bot can answer normal everyday questions.
- The bot remembers short-term conversation context.

## Phase 2: Clean Up Project Structure

Priority: high.

- Convert `mainbot` into the main application package.
- Treat Telegram and Discord as platform adapters.
- Treat fitness, sports, and trading as capability modules.
- Create a single top-level requirements file or dependency group strategy.
- Remove or quarantine code that is only a future blueprint.
- Keep `.env.example` updated as new keys are added.
- Add a real README with setup and run instructions.

Suggested structure:

```text
mainbot/
  app.py
  brain.py
  config.py
  personality.py
  platforms/
    telegram_bot.py
    discord_bot.py
  capabilities/
    fitness.py
    sports.py
    trading.py
    notes.py
  storage/
    db.py
    models.py
```

## Phase 3: Add Persistent Memory

Priority: started, still high.

- Keep `Bot Memory.md` as the first file-based long-term memory store.
- Keep memory permission-based: the bot should ask before saving.
- Keep memories organized by section.
- Store user profiles by platform and user ID.
- Store durable preferences, such as:
  - Name.
  - Fitness goals.
  - Favorite teams.
  - Trading watchlist.
  - Risk tolerance.
  - Preferred response style.
- Store conversation summaries instead of raw endless message history.
- Keep private and sensitive info separated.
- Add commands to list, edit, move, and delete saved memories.
- Add commands to view, update, and clear memory.

Expected result:

- The bot can remember useful facts across restarts.
- The bot can personalize answers without needing you to repeat everything.

## Phase 4: Connect Obsidian/Markdown Notes

Priority: medium-high.

- Current approach is file-based.
- File-based approach:
  - Read Markdown files from the vault folder.
  - Index notes locally.
  - Retrieve relevant note snippets when answering.
- Plugin/API approach:
  - Install/configure an Obsidian REST plugin.
  - Connect with an API key.
  - Query and update notes through the plugin.
- Add a notes capability:
  - Search notes.
  - Summarize notes.
  - Create new notes.
  - Append conversation takeaways.

Expected result:

- The bot can answer using your own notes, not only the model's general knowledge.

## Phase 5: Improve Accuracy

Priority: high after chat works.

- Add tool calling or a router layer so the bot knows when to use:
  - OpenAI.
  - Local calculations.
  - Notes.
  - Sports APIs.
  - Market APIs.
  - Web/news APIs.
- Require citations or source names for current events, sports odds, prices, and news.
- Add current-date awareness.
- Add safety language for:
  - Trading and investing.
  - Sports betting.
  - Fitness and nutrition.
  - Medical/injury questions.
- Add "I do not know" behavior when data is missing.
- Add tests for tool routing.

Expected result:

- The bot becomes less likely to hallucinate.
- The bot can distinguish general advice from live data.

## Phase 6: Sports Capability

Priority: medium.

- Pick a real sports data provider.
- Replace placeholder endpoints.
- Add API key handling.
- Add timeouts and error handling.
- Add supported sports/leagues.
- Add odds lookup.
- Add injury/news lookup.
- Add team/player stats.
- Add simple explainable predictions.
- Add backtesting before trusting prediction outputs.

Important:

- Do not treat the current simulation as a real betting model.
- Do not recommend bets without showing assumptions, data source, confidence, and risk.

## Phase 7: Fitness Capability

Priority: medium.

- Connect fitness profiles to chat users.
- Add commands or natural language parsing for:
  - Bodyweight logs.
  - Workout logs.
  - Nutrition logs.
  - Goal updates.
- Improve macro logic with age, height, sex, activity level, and rate-of-change targets.
- Add progress summaries.
- Add habit tracking.
- Add safety checks for extreme goals, injury, or medical topics.

Expected result:

- The bot becomes a useful personal fitness coach instead of a calculator.

## Phase 8: Trading Capability

Priority: later, because it is higher risk.

- Decide whether the bot is only educational or can place trades.
- Start with education and watchlists only.
- Add market data provider.
- Add quote lookup.
- Add news lookup.
- Add watchlist summaries.
- Add paper trading before any real broker connection.
- Add risk rules:
  - Max position size.
  - Max daily loss.
  - No live execution unless explicitly enabled.
  - Confirm every trade before sending.
- Add audit logs for every trading-related answer or action.

Important:

- Trading should not be connected to live execution until the assistant is stable, logged, and has strict safety controls.

## Phase 9: Testing and Reliability

Priority: ongoing.

- Add unit tests for:
  - Config loading.
  - Brain memory.
  - Domain tools.
  - Bankroll math.
  - Fitness macro calculations.
  - Platform message handlers.
- Add smoke tests for Telegram and Discord startup.
- Add logging around errors.
- Add retry behavior only where safe.
- Add API timeout handling.
- Add rate-limit handling.
- Add dependency cleanup.

## Ways To Improve What Exists Right Now

- Add Discord support next.
- Keep `.env.example` updated.
- Add a unified `requirements.txt`.
- Move Telegram code into a `platforms/telegram_bot.py` adapter.
- Create a `platforms/discord_bot.py` adapter.
- Keep `Brain` platform-neutral.
- Add a `/status` command.
- Improve Obsidian memory with list/edit/delete commands.
- Add broader note search across Markdown files.
- Install or consolidate dependencies, especially `requests` for sports APIs and Discord support.
- Choose real sports and market data providers.
- Add tests for the local domain tools.
- Write setup instructions in README.

## Best Near-Term Plan

The next practical build order should be:

1. Stabilize the Telegram bot.
2. Add Discord support.
3. Create one shared bot runner.
4. Add status/help commands and better startup checks.
5. Improve Obsidian memory controls.
6. Add Obsidian Markdown note search.
7. Add accuracy tools for live/current information.
8. Expand sports, fitness, and trading after communication is reliable.

This keeps the project focused on the real first win: being able to message the bot naturally and trust that it responds consistently.
