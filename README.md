# BGG Extractor

Python extractor for BoardGameGeek that collects board game data including rankings, categories, and mechanics. The output is saved into CSV files.

## Features
- Fetches board game information (name, description, year published, player count, playtime, age, ratings, etc.)
- Collects board game categories and mechanics
- Handles large lists of game IDs in batches
- Outputs data to CSV files: `output.csv`, `categories.csv`, `mechanics.csv`

> ⚠️ The `boardgames_ranks.csv` file is not included. You can download it [here](https://boardgamegeek.com/data_dumps/bg_ranks).

## Configuration
Create a `.env` file in the project root with your BoardGameGeek Bearer token.
This token is required to authenticate requests to the BGG API. Without it, the extractor will not be able to fetch data.

Example `.env` file:

```
BEARER_TOKEN=your_bgg_api_token_here
```

Replace `your_bgg_api_token_here` with your actual token.  
