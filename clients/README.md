# Clients

Each client has its own folder. Never mix files between clients.

```
clients/
├── food-palace/                     # Food Palace, Haripur (restaurant)
│   ├── INFO.md                      # research and contact details
│   └── site/                        # their website (created when work starts)
└── haripur-international-hospital/  # Haripur International Hospital
    ├── INFO.md
    └── site/
```

- A client's website, images and fonts stay inside that client's own `site/` folder.
- Shared design style skills live in `.claude/skills/` and contain no client data.
- When a site goes live, it gets its own deployment (and its own repo if needed), so clients never affect each other.
