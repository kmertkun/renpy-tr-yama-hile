## Türkçe yama: oyunun içindeki hazır Türkçe çeviriyi ilk açılışta bir kez etkinleştirir.
## Sonrasında dili Ayarlar menüsünden istediğin gibi değiştirebilirsin, yama tekrar zorlamaz.

define config.default_language = "turkish"

init 999 python:
    if not persistent.tr_yama_uygulandi:
        persistent.tr_yama_uygulandi = True
        _preferences.language = "turkish"
        # Oyunun "yapay zeka çevirisi" uyarısını da bir kez gösterilmiş say
        persistent.seen_ai_warning = True
