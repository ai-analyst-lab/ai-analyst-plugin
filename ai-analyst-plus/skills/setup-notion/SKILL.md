---
name: setup-notion
description: >-
  Guided Notion connection setup wizard. Verifies the Notion connector is enabled, walks the user
  through enabling and authorizing it, and checks for an Analysis Gallery database. Use when the
  user says "/setup-notion", "connect to notion", "set up notion", "I want to export to Notion",
  or when a Notion export or ingest fails because Notion tools are not available.
---

# Skill: Setup Notion

Requires the Notion connector enabled in Cowork.

## Purpose
Guided Notion connection setup wizard. Verifies the Notion connector,
walks the user through enabling it, and confirms the connection by
searching their workspace.

## When to Use
- User says `/setup-notion`, "connect to notion", "set up notion",
  "I want to export to Notion"
- Routed here from `/connect-data` or `/export notion` when Notion tools
  are not available

## Invocation
`/setup-notion` — start the setup wizard

Tool names vary by connector version: discover the exact tool names from the connector's available tools in-session and read each schema before calling.

## Instructions

### Step 1: Check Whether Notion Tools Are Available

Try to call the Notion connector's search tool with a test query.

**Decision matrix:**
- Notion tools available → skip to Step 4 (verify)
- Notion tools NOT available → continue to Step 2

### Step 2: Enable the Notion Connector

Tell the user to enable the Notion connector in Cowork:
- "Open Cowork's connector settings and enable the **Notion** connector."
- "A browser window will open — sign in to Notion and authorize access."
- "Select which pages/databases to share (or share the whole workspace)."
- "This uses Notion's official OAuth flow — no API key needed."

**Important:** During authorization, the user chooses which pages Claude can
access. Remind them: "Share at least the page or database where you want
analysis exports to go."

### Step 3: Re-check

Once the user says the connector is enabled, try the Notion search tool again.
If tools are still not available, ask the user to start a fresh session so the
newly enabled connector is loaded, then run `/setup-notion` again. Stop here —
do not proceed to Step 4 in this session if the tools are not yet available.

### Step 4: Verify Connection

Use the Notion MCP search tool to verify access:
```
the Notion connector's search tool(query="", filter={"value": "page"})
```

**If it works:**
- Show the user how many pages/databases are accessible
- List 3-5 example pages by title so they can confirm scope is right
- Continue to Step 5

**If it fails:**
- "Notion connection failed. Try running `/mcp` to re-authenticate."
- Common issues: OAuth expired, pages not shared with the integration,
  workspace permissions

### Step 5: Check for Analysis Gallery

Search for an "Analysis Gallery" database:
```
the Notion connector's search tool(query="Analysis Gallery", filter={"value": "database"})
```

**If found:**
- "Found your Analysis Gallery database. Exports will create new entries there."
- Store the database ID for future exports.

**If not found:**
- Offer to create one: "No Analysis Gallery found. Want me to help you set
  one up? It's a Notion database that organizes all your analysis exports
  with properties like Title, Date, Dataset, and Confidence Grade."
- If yes: create a new database page with properties:
  - Title (title type)
  - Date (date type)
  - Dataset (text type)
  - Confidence (select type: A, B, C, D, F)
  - Status (select type: Draft, Final)
- If no: "No problem. Exports will create standalone pages instead."

### Step 6: Summary

```
Notion is connected:
  Server: Notion hosted MCP (OAuth)
  Workspace: {workspace_name}
  Accessible pages: {count}
  Analysis Gallery: {Found / Not found / Created}

You can now:
  - `/export notion` — export any analysis to Notion
  - Analysis Gallery entries include charts, data stamps, and provenance
```

## Rules
1. Never ask for an API key — the Notion connector uses OAuth exclusively
2. Always test the connection before declaring success
3. If tools are unavailable right after enabling, a fresh session picks up the
   connector; never claim the connection works without a successful search
4. Remind users to share relevant pages with the integration during OAuth
