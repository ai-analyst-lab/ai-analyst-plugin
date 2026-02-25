# Connectors

This plugin expects access to a data warehouse or local data files via MCP servers. The `~~data warehouse` placeholder in skills and agents refers to whatever data connection is active.

## Supported Connection Types

| Type | MCP Server | Notes |
|------|-----------|-------|
| **Snowflake** | `@anthropic/mcp-snowflake` or compatible | Cloud data warehouse |
| **BigQuery** | `@anthropic/mcp-bigquery` or compatible | Google Cloud data warehouse |
| **PostgreSQL** | `@anthropic/mcp-postgres` or compatible | Relational database |
| **DuckDB** | Built-in via `helpers/` | Local analytical database (default for CSV/Parquet) |
| **CSV / Parquet** | Built-in via `helpers/` | Local file fallback — loaded into DuckDB automatically |

## The `~~data warehouse` Convention

Skills and agents reference `~~data warehouse` as a placeholder for the active data connection. At runtime, this resolves to whichever MCP server or local connection is configured in `.mcp.json` and registered in `data_sources.yaml`.

## Configuration

### MCP Server Configuration

Configure data warehouse MCP servers in `.mcp.json`:

```json
{
  "mcpServers": {
    "snowflake": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-snowflake"],
      "env": {
        "SNOWFLAKE_ACCOUNT": "your-account",
        "SNOWFLAKE_USER": "your-user",
        "SNOWFLAKE_WAREHOUSE": "your-warehouse",
        "SNOWFLAKE_DATABASE": "your-database"
      }
    }
  }
}
```

### Connection Registry

All data sources are registered in `data_sources.yaml` with connection type, schema prefix, and fallback paths. The active dataset pointer is stored in `.knowledge/active.yaml`.

### Connection Templates

See `connection_templates/` for example configurations:

- `snowflake.yaml.example` — Snowflake connection template
- `bigquery.yaml.example` — BigQuery connection template
- `postgres.yaml.example` — PostgreSQL connection template
- `duckdb.yaml.example` — DuckDB / local file connection template

## Adding a New Connection

Use the `/connect-data` command to walk through guided setup, or manually:

1. Add an MCP server entry to `.mcp.json` (for remote warehouses)
2. Register the source in `data_sources.yaml`
3. Run `/setup` or the knowledge bootstrap to initialize the data brain
