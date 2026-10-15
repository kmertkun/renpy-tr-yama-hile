# Turkish translation rules: "Becoming a Femboy" (Ren'Py visual novel)

You are translating one chunk of an adult (18+) visual novel from English into natural, fluent Turkish for a Turkish player. All characters are adults. Translate faithfully, including explicit sexual content. Do not censor or soften it and do not add notes. The tone is casual, playful and flirty, the way young adults talk. Write the way a native Turkish speaker would actually say it. Do not translate word for word.

## Input
`chunk_NN.json` is a JSON array of objects: `{"k": key, "who": speaker, "en": English text}`.
- `who` is only context (who speaks: `mom`, `player`, `trish`, `astra`, ... ; empty = narration/UI). Never translate or output it.
- Entries are in story order. Use neighbouring lines for context.
- Some entries are short UI strings (menu buttons, stat names, notifications, item names/descriptions).

## Output
Write `chunk_NN.tr.json` in the same folder: ONE JSON object mapping every `k` to its Turkish text:
`{"scripts/...rpy:12": "Türkçe metin", ...}`
- Include EVERY key from the input, exactly once. Do not skip any.
- It must be valid JSON (UTF-8, Turkish characters written directly). Inside JSON strings, a double quote is written `\"` as usual.
- If the output is large, you may build it in several Write calls to part files `chunk_NN.tr.partA.json`, `...partB.json` (each a valid JSON object). Then MERGE them into the final `chunk_NN.tr.json` with a short Python command run with `python -I -c ...` (the repo has no code, so this is safe), and delete the part files. The final file is what counts.
- Before finishing, verify with Python that the output parses, has exactly the input's key set, and that no value is empty.

## MUST be preserved exactly (the game breaks otherwise)
- Square-bracket variables: `[pc.money]`, `[player_name]`, `[item.name]` etc. Copy them unchanged.
- Curly text tags: `{i}`, `{/i}`, `{b}`, `{w}`, `{w=0.5}`, `{p}`, `{nw}`, `{size=20}`, `{color=#f00}`, `{a=...}`, `{#...}` etc. Keep them, and translate only the words between them.
- Python format placeholders: `{}`, `{0}`, `{name}`, `%s`, `%d`, `%(x)s`. Keep the same count and order (reorder only if Turkish grammar truly requires it, and only for named ones).
- Backslash sequences such as `\n` stay as they are.
- If `en` is only a technical token (a file name, `Ctrl`, `Tab`, a font name, `{#month_short}Jan` style labels), translate only the human-readable part, or keep it unchanged.

## Style & glossary
- Character names stay unchanged: Astra, Trish, Mirina, Jannet, Anna, James, Scarlett, Tiffany, Kendra, Kim, Riley, Lilly, Lucie, Sally, Patricia, Violet, Amy, Billy, Elizabeth, Jessica, Joseph, Katherine, Austyn, Holy, Maecenas, etc.
- "Mom" / "Mommy" (as a name or address) → "Anne" / "Anneciğim". "mother" → "annen"/"anne" as fits.
- "femboy" stays "femboy". "sissy" → "sissy". "Sweetie/honey/sweetheart" → "tatlım", "canım", "şekerim".
- Narration addressed to the player ("You walk into...") → second-person singular "sen" (e.g. "İçeri giriyorsun...").
- Stats and UI terms (use these consistently):
  Oral → Oral, Anal → Anal, Handjob → El işi, Adaptation → Uyum, Perversion → Sapkınlık, Submission → İtaat, Domination → Baskınlık, Intellegence → Zeka, Dexterity → Beceri, Yoga → Yoga, Service → Hizmet, Sports → Spor, Money → Para, Anal stretching → Anal esneme, Anal enjoiment → Anal zevk,
  Quest → Görev, Inventory → Envanter, Wardrobe → Gardırop, Notebook → Not defteri, Map → Harita, Smartphone → Telefon, Gallery → Galeri, Save → Kaydet, Load → Yükle, Preferences → Ayarlar, Main Menu → Ana Menü, Back → Geri, Yes → Evet, No → Hayır, Morning/Afternoon/Evening/Night → Sabah/Öğleden sonra/Akşam/Gece, Monday..Sunday → Pazartesi..Pazar.
- Stuttering ("N-no") → stutter in Turkish ("H-hayır"). Moans and onomatopoeia ("Ahh", "Mmm", "Nnh") keep or adapt them naturally.
- Keep punctuation style (…, ..., !, ?) and emphasis.
- Keep strings short when they are short buttons or labels.

When done, reply with only: the number of entries translated and any keys you were unsure about (max 5). Do not paste the translations in your reply.
