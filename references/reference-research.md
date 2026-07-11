# Reference research

## Research objective

Find three **real A-roll** creator setups that can seed three room-specific visual directions. A reference earns its place because its camera-to-subject-to-background relationship can work in the supplied room; the raw reference is not the final product.

## Required research protocol

1. Use `agent-reach` for discovery and run its doctor first. If it is not on `PATH`, try `$HOME/.agent-reach-venv/bin/agent-reach`. For live page reading, screenshots, or logged-in platforms, follow `web-access` first. If both are unavailable, use an official built-in web/search capability and label it as fallback mode.
2. Search creator-native sources first: YouTube, Bilibili, Instagram, Xiaohongshu, creator portfolios, or a creator's own site.
3. Verify the featured frame is A-roll. The source should show the creator talking to lens in the actual set, ideally in the relevant video—not only a studio reveal.
4. Record the direct source URL, platform, creator identity, and what the frame proves.
5. Prefer exactly one usable image/frame per candidate; do not pad output with generic inspiration images.
6. Translate the three candidates into the user's room before asking for a preference, unless the user explicitly requested a reference-only checkpoint.

## Selection score (100)

| Dimension | Weight | Test |
| --- | ---: | --- |
| Room geometry | 35 | camera angle, usable background depth, curtain/wall/shelf relationship can be recreated |
| Lighting transfer | 25 | direction and contrast can be made with common fixtures in this room |
| Lane identity | 20 | the setup supports the creator's intended content and audience |
| Cost/complexity | 10 | additions are proportionate to likely budget and rental constraints |
| Composition durability | 10 | looks good in actual A-roll, not only in a single staged photo |

Reject candidates with a total below 70 unless the user explicitly wants a far-reaching style reference.

## Candidate card

```markdown
### A. [Creator] — [lane] — [score]/100
Source: [platform/profile or source video](URL)
Frame: [embedded/captured A-roll image, or precise timestamp]
Why it matches: [two concrete room relationships]
Lighting read: key [direction/softness]; background [practical]; separation [method].
Borrow: [two reproducible moves].
Do not borrow: [one incompatible move].
```

## Quality checks

- Use three different creators, not three clips of the same person.
- Attribute every reference clearly; never present a web image as an original render.
- Do not label a talking-over-screen, product B-roll, teaching slide, or course recording as A-roll.
- Do not over-index on large monitors, RGB strips, or expensive studio furniture. They rarely solve the user's framing problem.
- Do not let a new reference erase elements from a prior render that the user explicitly approved. Treat reference style and approved set dressing as separate inputs.
