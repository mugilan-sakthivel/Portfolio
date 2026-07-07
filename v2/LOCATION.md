# Live location — how it works & phone setup

The site footer ("11:39pm in Bengaluru, India") reads from a GitHub gist at page load:

- Gist: https://gist.github.com/mugilan-sakthivel/7430d2ac7a323ef732c8d31d08e0e68b
- Raw URL the site fetches: https://gist.githubusercontent.com/mugilan-sakthivel/7430d2ac7a323ef732c8d31d08e0e68b/raw/location.json
- Format: `{"city": "Bengaluru, India", "tz": "Asia/Kolkata"}`

Updating the gist updates the site instantly (next page load, ~5 min raw cache) —
**no redeploy needed**. The clock timezone follows `tz` too.

## Update manually (anywhere)

```bash
printf '{"city": "Bengaluru, India", "tz": "Asia/Kolkata"}' > /tmp/location.json
gh gist edit 7430d2ac7a323ef732c8d31d08e0e68b /tmp/location.json
```

## Auto-update daily from iPhone

1. Create a fine-grained token at github.com/settings/tokens — only scope needed: **Gists (read/write)**.
2. iPhone **Shortcuts** app → Automation → New → Time of Day (e.g. 9:00 AM, daily, "Run Immediately":
   - **Get current location** (needs Location Services on)
   - **Get details of location** → City / Country
   - **Text**: `{"city": "[City], [Country]", "tz": "[Current timezone via Date format zzzz or hardcode per trip]"}`
   - **Get contents of URL**:
     - URL: `https://api.github.com/gists/7430d2ac7a323ef732c8d31d08e0e68b`
     - Method: PATCH
     - Headers: `Authorization: Bearer <token>`, `Accept: application/vnd.github+json`
     - Request body (JSON): `{"files": {"location.json": {"content": "<the Text above>"}}}`
3. When your phone's location is off, the shortcut just fails silently and the site keeps the last city.

Timezone tip: for trips, easiest is to update `tz` manually per country (IANA names:
`Asia/Kolkata`, `Asia/Singapore`, `Europe/London`, …). City alone is enough for the label.
