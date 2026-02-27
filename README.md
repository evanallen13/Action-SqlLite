# QuasiDB

A demonstration project showing how to use GitHub Actions workflow caching to persist SQLite database data between workflow runs.

## Overview

This project demonstrates how GitHub Actions cache can be used to maintain persistent data across workflow executions. Instead of losing data when a workflow completes, we use the `actions/cache` action to save and restore a SQLite database file, effectively creating a simple persistent storage solution within GitHub Actions.

## How It Works

1. **Database Creation**: The Python script (`main.py`) creates a SQLite database at `data/example.db`
2. **Cache Restoration**: On each workflow run, we attempt to restore the cached database from previous runs
3. **Data Operations**: The script adds new users to the database (Alice and Bob)
4. **Cache Update**: After running the script, we delete the old cache and save the updated database
5. **Persistence**: On subsequent runs, the database already contains data from previous executions

## Key Components

### Python Script (`main.py`)
- Creates a SQLite database if it doesn't exist
- Inserts sample user data
- Displays all users and database statistics

### GitHub Actions Workflow (`.github/workflows/run.yml`)
- Triggered manually via `workflow_dispatch`
- Uses `actions/cache/restore@v5` to retrieve the cached database
- Runs the Python script to modify the database
- Uses `actions/cache/save@v5` to persist the updated database
- Implements concurrency control to prevent parallel runs

## Usage

1. Go to the Actions tab in your GitHub repository
2. Select the "Generate and Push Database" workflow
3. Click "Run workflow"
4. The database will be created/updated and cached for the next run

## Benefits

- **Persistent Storage**: Data survives between workflow runs
- **Cost Effective**: Uses GitHub's free cache storage (up to 10GB per repository)
- **Simple Setup**: No external database or storage service required

## Limitations

- Cache entries expire after 7 days of no access
- Maximum cache size is 10GB per repository
- Not suitable for production applications requiring guaranteed persistence
- Concurrent workflow runs are prevented to avoid cache conflicts

## Requirements

See `requirements.txt` for Python dependencies.
