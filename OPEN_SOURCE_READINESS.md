# Open-source readiness

## Scope

This repository is a portfolio-safe demo of a conversational laptop and desktop recommendation assistant. It is intended to run with synthetic/demo data and user-provided API credentials.

## Before publishing

- Confirm written permission to publish the code, prompts, UI assets, and any competition materials.
- Keep `.env`, `data/`, `*.db`, logs, screenshots, exports, and real product/customer data out of Git.
- Replace all real endpoints, account identifiers, cookies, and server information with placeholders.
- Review dependencies and frontend assets for license compatibility.
- Do not claim live pricing accuracy: results depend on the configured search provider and may become stale.
- Run the health check and a no-key demo-data smoke test from a clean environment.

## Portfolio positioning

The project demonstrates a complete Agent workflow rather than a single prompt: intent analysis, follow-up/fallback handling, search abstraction, caching, product scoring, structured response generation, WebSocket conversation state, and browser visualization.

## Known limitations

- No-key mode is suitable for demonstration, not production recommendation quality.
- Search results and prices are external and time-sensitive.
- The application is designed for local development; production deployment needs authentication, rate limiting, observability, and stricter outbound-network controls.

