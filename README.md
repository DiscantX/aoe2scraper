
<img width="1226" height="344" alt="AgeKeeperBanner_Cropped" src="https://github.com/user-attachments/assets/706c6b69-c43f-4a95-8605-07df03d7b007" />

# AgeKeeper

A Python wrapper for querying the Age of Empires II (AOE2) public stats API and downloading match replays, with a replay scraper included.

## What it does

- Download a match replay ZIP by `match_id` and optionally unzip it.
- Fetch match details, full player stats, a player's recent match list, campaign stats, and leaderboard data.
- Can be used as a Python package you can use in your own scripts, or as a CLI tool (in progess).
- Scrape replays from a range of match ids (see `replay_scraper.py`).

## Requirements

- Python 3 (tested with standard CPython)

## Quick start

Download a replay ZIP:

```bash
python aoe2api.py replay --match-id 453704442 --profile-id 199325 --output replays --unzip --remove-zip
```

Fetch match details:

```bash
python aoe2api.py match-details --match-id 453704442 --profile-id 199325
```

Scrape a short range in ascending order:

```bash
python replay_scraper.py --start_id 450000000 --end_id 450000050 --request-interval 5
```

Scrape a range in descending order with exponential backoff:

```bash
python replay_scraper.py --start_id 453704499 --end_id 453700000 --count-backwards --back-off-delay 20 --back-off-multiplier 2 --max-back-off-delay 300
```

Resume a previous run (uses `scrape_state.txt`):

```bash
python replay_scraper.py --resume --start_id 450000000 --end_id 450010000 --request-interval 5
```

## Configuration

Edit the `defaults` dict in `fetch_replay.py` to change:

- `destination_folder`: where replay ZIPs are saved (default: `replays`)
- `game`: game key (default: `age2`)
- `profile_id`: used for sample calls (default: Hera's profile ID)
- `match_id`: used for sample calls (default: a match from Hera's profile)
- `unzip`: whether to unzip downloaded replay ZIPs (default: `True`)
- `remove_zip`: whether to delete the ZIP after extraction (default: `True`)
- `headers`: default headers sent with API requests

Edit the `defaults` dict in `replay_scraper.py` to change:

- `request_interval`: delay between requests in seconds
- `back_off_delay`: base backoff delay when rate limited (seconds)
- `back_off_multiplier`: exponential backoff multiplier
- `max_back_off_delay`: maximum backoff delay (seconds)
- `start_id`: starting match ID
- `end_id`: ending match ID
- `count_backwards`: scrape from `start_id` down to `end_id` when `True`
- `unzip_replays`: whether to unzip downloaded replays
- `remove_zip`: whether to delete ZIPs after extraction
- `scrape_state_file`: scrape state file path

## Core functions

- `save_replay(response, destination_folder=..., unzip=..., remove_zip=...)`
- `fetch_player_match_list(profile_id, game=..., sortColumn='dateTime', sort_direction='DESC', match_type='3')`
- `fetch_leaderboard(region='7', match_type='3', console_match_type=15, search_player='', page=1, count=100, sort_column='rank', sort_direction='ASC')`
- `fetch_endpoint(endpoint_name, profile_id=..., match_id=..., headers=..., data=None)`
- `run_endpoint_tests()`

## Endpoints

The script currently supports these endpoint keys (see `endpoints` in `aoe2api.py`):

- `replay`
- `match_details`
- `player_stats`
- `player_match_list`
- `player_campaign_stats`
- `leaderboard`

## Notes and caveats

- The headers/payloads are based on requests captured from the official Age of Empires website and may change.
- `fetch_player_match_list` only returns the most recent matches; paging behavior appears limited to page 1.
- `match_type` values are partially documented in the comments in `fetch_replay.py` and may require further verification.
- The replay download endpoint requires both `matchId` and `profileId` query parameters, even though the `profileId` value does not appear to matter.

## AOE2 API CLI

- `replay`: download a match replay ZIP.
- `match-details`: fetch match details for a match ID.
- `player-stats`: fetch full player stats for a match.
- `player-match-list`: fetch a player's recent matches.
- `player-campaign-stats`: fetch campaign stats for a player.
- `leaderboard`: fetch leaderboard data with filters.
- `endpoint`: fetch a raw endpoint by name.

Command summary:

| Command | Purpose | Common flags |
| --- | --- | --- |
| `replay` | Download a replay ZIP | `--match-id`, `--profile-id`, `--output`, `--unzip`, `--remove-zip` |
| `match-details` | Fetch match details | `--match-id`, `--profile-id` |
| `player-stats` | Fetch player stats for a match | `--match-id`, `--profile-id` |
| `player-match-list` | Fetch recent matches | `--profile-id`, `--match-type`, `--sort-column`, `--sort-direction` |
| `player-campaign-stats` | Fetch campaign stats | `--profile-id` |
| `leaderboard` | Fetch leaderboard data | `--region`, `--match-type`, `--page`, `--count`, `--sort-column`, `--sort-direction` |
| `endpoint` | Fetch a raw endpoint | `--endpoint-name`, `--data`, `--match-id`, `--profile-id` |

Download a replay ZIP:

```bash
python aoe2api.py replay --match-id 453704442 --profile-id 199325 --output replays --unzip --remove-zip
```

Fetch match details:

```bash
python aoe2api.py match-details --match-id 453704442 --profile-id 199325
```

Fetch player stats for a match:

```bash
python aoe2api.py player-stats --match-id 453704442 --profile-id 199325
```

Fetch a player's recent matches:

```bash
python aoe2api.py player-match-list --profile-id 199325 --match-type 3
```

Fetch player campaign stats:

```bash
python aoe2api.py player-campaign-stats --profile-id 199325
```

Fetch the leaderboard:

```bash
python aoe2api.py leaderboard --region 7 --match-type 3 --page 1 --count 100
```

Fetch a raw endpoint by name:

```bash
python aoe2api.py endpoint --endpoint-name replay --match-id 453704442 --profile-id 199325
```

Run built-in endpoint tests:

```bash
python aoe2api.py --run-tests
```

## Replay scraper CLI

Scrape a range of match IDs in ascending order:

```bash
python replay_scraper.py --start_id 450000000 --end_id 450010000 --request-interval 5
```

Scrape in descending order (from end to start), with exponential backoff:

```bash
python replay_scraper.py --start_id 453704499 --end_id 453700000 --count-backwards --back-off-delay 20 --back-off-multiplier 2 --max-back-off-delay 300
```

## Legal and usage

This is an unofficial script and is not affiliated with or endorsed by Microsoft or the Age of Empires team. Use responsibly and respect the terms of service of any API you call. It is unclear to what extent Microsoft will allow scraping of their API. Use at your own risk.

## AI Disclosure

This readme was auto-generated by AI. Some code was auto-filled using either Copilot or Codex, though all was reviewed by the author.
