# Ren'Py Turkish Patches & Cheat Menus

**[English](#english) | [Türkçe](#türkçe)**

---

## English

Unofficial Turkish translation patches and in-game cheat menus for Ren'Py games.
**This repo contains no game files.** You need your own copy of each game.

| Game | Version | Turkish patch | Cheat menu |
|---|---|---|---|
| Path of Desire: Cursed Chakra | 0.8.0 | Turns on the game's built-in Turkish translation (already 100% complete) | ✅ |
| Becoming a Femboy | 3.10.0a | Full translation: 10,586 lines (dialogue + UI) | ✅ |

### Installation
1. Download this repo (**Code → Download ZIP**) and extract it.
2. Open the folder for your game (`path-of-desire/` or `becoming-a-femboy/`).
3. Copy its `game` folder into the game's main folder (the one with the `.exe`). Choose **merge / replace** if asked.
4. Start the game. It switches to Turkish on first launch.

### Cheat menu
Press **F8** in game, or click the **HİLE** button on the right edge of the screen.

**Path of Desire**
- Money: add or set an exact amount. Reset Karui's debt.
- Player stats: Lust, Corruption, Dominance, Submissiveness, Restraint.
- Every character's Affection, Desire and Dominance, plus a "max all" button.
- Memory Nexus allies: level up, raise the level cap, add stat and jutsu points, full heal, unlock.
- Items: add or remove any item, or add all items at once.

**Becoming a Femboy**
- Money: add or set an exact amount.
- All 12 stats (Perversion, Submission, Domination, Oral, Anal, Yoga, …).
- Anal stretching and enjoyment levels.
- Buy everything in the shop for free.
- Unlock the full gallery and every notebook fact.
- Toggle the UI locks (map, phone, inventory, notebook, …).

### Language switch
- **Becoming a Femboy:** use the **Türkçe / English** buttons at the bottom right of the Preferences screen.
- **Path of Desire:** use the game's own language menu.

### Uninstall
Delete the `zz_*.rpy` / `zz_*.rpyc` files from the game's `game` folder.
For Becoming a Femboy, also delete `game/tl/turkish`.

### Tools (`tools/`)
These are the scripts used to build the patches. Each one is a standalone Python 3 script with no dependencies.

| Script | Purpose |
|---|---|
| `unrpa.py` | Extract an RPA-3.0 archive: `python unrpa.py scripts.rpa out_dir` |
| `tl_extract.py` | Split a Ren'Py `tl/<lang>` template into JSON chunks for translation |
| `tl_inject.py` | Put translated chunks back, checking `[vars]`, `{tags}` and `%s` |
| `tlscan.py`, `gapcheck.py` | Measure translation coverage and find missing lines |
| `fontcheck.py` | Check whether a font contains the Turkish glyphs (ı ş ğ İ …) |
| `translation_rules.md` | The style guide and glossary used for the translation |

To make a fresh template, run the game's Ren'Py with the sources on disk:
`<game>/lib/py3-windows-x86_64/python.exe <game>.py <project_dir> translate turkish`

### Notes
- The Becoming a Femboy translation was machine translated with AI and checked automatically. Some wording may sound unnatural, so corrections via issues or PRs are welcome.
- The patches are for the versions listed above. On newer versions they still work, but newly added lines stay in English.
- Back up your saves before using cheats. Raising some values early can skip story events.

### License
The code in this repo (cheat menus, patch loaders, tools) is released under the [MIT License](LICENSE).
The games, and all their characters, art and story, belong to their respective developers. This is an unofficial fan project and is not affiliated with them. Please support the developers.

---

## Türkçe

Ren'Py oyunları için resmi olmayan Türkçe yamalar ve oyun içi hile menüleri.
**Bu repoda oyun dosyası yoktur.** Oyunun kendisine sahip olman gerekir.

| Oyun | Sürüm | Türkçe yama | Hile menüsü |
|---|---|---|---|
| Path of Desire: Cursed Chakra | 0.8.0 | Oyunun kendi Türkçe çevirisini açar (zaten %100 tam) | ✅ |
| Becoming a Femboy | 3.10.0a | Tam çeviri: 10.586 satır (diyalog + arayüz) | ✅ |

### Kurulum
1. Bu repoyu indir (**Code → Download ZIP**) ve zipten çıkar.
2. Oyununun klasörünü aç (`path-of-desire/` veya `becoming-a-femboy/`).
3. İçindeki `game` klasörünü oyunun ana klasörüne kopyala (`.exe` dosyasının olduğu yer). Sorarsa **birleştir / değiştir** de.
4. Oyunu aç. İlk açılışta kendiliğinden Türkçe'ye geçer.

### Hile menüsü
Oyun içinde **F8** tuşuna bas ya da ekranın sağ kenarındaki **HİLE** butonuna tıkla.

**Path of Desire**
- Para: ekleme veya tam miktar ayarlama. Karui borcunu sıfırlama.
- Oyuncu statları: Lust, Corruption, Dominance, Submissiveness, Restraint.
- Her karakterin Affection, Desire ve Dominance değeri, ayrıca "hepsini MAX yap" butonu.
- Memory Nexus müttefikleri: level atlatma, level sınırını yükseltme, stat ve jutsu puanı ekleme, tam iyileştirme, kilit açma.
- Eşyalar: istediğin eşyayı ekleme/çıkarma veya hepsini birden ekleme.

**Becoming a Femboy**
- Para: ekleme veya tam miktar ayarlama.
- 12 statın hepsi (Perversion, Submission, Domination, Oral, Anal, Yoga, …).
- Anal esneme ve zevk seviyeleri.
- Mağazadaki her şeyi bedava alma.
- Galeriyi ve not defterindeki tüm bilgileri açma.
- Arayüz kilitlerini açma/kapama (harita, telefon, envanter, not defteri, …).

### Dil değiştirme
- **Becoming a Femboy:** Ayarlar ekranının sağ altındaki **Türkçe / English** butonlarını kullan.
- **Path of Desire:** Oyunun kendi dil menüsünü kullan.

### Kaldırma
Oyunun `game` klasöründen `zz_*.rpy` / `zz_*.rpyc` dosyalarını sil.
Becoming a Femboy için `game/tl/turkish` klasörünü de sil.

### Araçlar (`tools/`)
Yamaları hazırlamak için kullanılan scriptler. Hepsi tek başına çalışan, ek kütüphane gerektirmeyen Python 3 scriptleridir.

| Script | Ne işe yarar |
|---|---|
| `unrpa.py` | RPA-3.0 arşivini açar: `python unrpa.py scripts.rpa cikti_klasoru` |
| `tl_extract.py` | Ren'Py `tl/<dil>` şablonunu çeviri için JSON parçalarına böler |
| `tl_inject.py` | Çevrilen parçaları geri yerleştirir; `[değişken]`, `{etiket}` ve `%s` kontrolü yapar |
| `tlscan.py`, `gapcheck.py` | Çevirinin ne kadarının tamam olduğunu ölçer, eksik satırları bulur |
| `fontcheck.py` | Bir yazı tipinde Türkçe karakterlerin (ı ş ğ İ …) olup olmadığını kontrol eder |
| `translation_rules.md` | Çeviride kullanılan üslup kuralları ve terim sözlüğü |

Yeni bir şablon üretmek için oyunun Ren'Py'sini, kaynaklar diskteyken çalıştır:
`<oyun>/lib/py3-windows-x86_64/python.exe <oyun>.py <proje_klasoru> translate turkish`

### Notlar
- Becoming a Femboy çevirisi yapay zeka ile yapıldı ve otomatik olarak kontrol edildi. Bazı ifadeler doğal durmayabilir; düzeltmeler için issue veya PR açabilirsin.
- Yamalar yukarıdaki sürümler için hazırlandı. Daha yeni sürümlerde de çalışır, ama yeni eklenen satırlar İngilizce kalır.
- Hile kullanmadan önce kayıtlarını yedekle. Bazı değerleri erken yükseltmek hikâye olaylarını atlatabilir.

### Lisans
Bu repodaki kod (hile menüleri, yama yükleyicileri, araçlar) [MIT Lisansı](LICENSE) ile yayınlanmıştır.
Oyunlar ve oyunlardaki tüm karakterler, görseller ve hikâye kendi geliştiricilerine aittir. Bu, onlarla bağlantısı olmayan, resmi olmayan bir hayran projesidir. Lütfen geliştiricileri destekle.
