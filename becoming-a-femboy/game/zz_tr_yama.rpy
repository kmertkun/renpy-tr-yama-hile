## Türkçe yama: game/tl/turkish klasöründeki çeviriyi etkinleştirir.
## İlk açılışta bir kez Türkçe'ye geçer; sonra Ayarlar ekranındaki "Türkçe" / "English"
## butonlarıyla istediğin zaman değiştirebilirsin.

init 999 python:
    if not persistent.tr_yama_uygulandi:
        persistent.tr_yama_uygulandi = True
        _preferences.language = "turkish"

    # Oyun bazı not görsellerini persistent.lang ile seçiyor (sadece "en"/"ru" var).
    # Türkçe'de İngilizce görseller kullanılsın.
    if persistent.lang not in ("en", "ru", "pt", "es"):
        persistent.lang = "en"

    config.overlay_screens.append("tr_yama_dil_butonu")


screen tr_yama_dil_butonu():
    zorder 150
    if renpy.get_screen("preferences"):
        hbox:
            xalign 0.98 yalign 0.97
            spacing 8
            textbutton "Türkçe":
                text_font "DejaVuSans.ttf"
                text_size 20
                action [Language("turkish"), SetField(persistent, "lang", "en")]
            textbutton "English":
                text_font "DejaVuSans.ttf"
                text_size 20
                action [Language(None), SetField(persistent, "lang", "en")]
