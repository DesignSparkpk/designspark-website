# Clients

Each client has its own folder. Never mix files between clients.

```
clients/
├── food-palace/                     # Food Palace, Haripur (restaurant)
│   ├── INFO.md                      # research and contact details
│   └── site/                        # their website (created when work starts)
├── haripur-international-hospital/  # Haripur International Hospital (already has a website: low priority)
│   └── INFO.md
└── beacon-public-school/            # Beacon Public School & College, Haripur
    ├── INFO.md
    └── site/
```

- A client's website, images and fonts stay inside that client's own `site/` folder.
- Shared design style skills live in `.claude/skills/` and contain no client data.
- When a site goes live, it gets its own deployment (and its own repo if needed), so clients never affect each other.

## Status (24 Nov 2026)
| Client | Status |
|---|---|
| Food Palace | Cold message sent, waiting for reply |
| Haripur International Hospital | Skipped: already has a website |
| Beacon Public School & College | Paused by owner. Finished 6-page Glassmorphism site kept as a portfolio sample and school template |
