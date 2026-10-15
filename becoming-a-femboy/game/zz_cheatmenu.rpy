## Becoming a Femboy - Hile Menüsü
## Oyun içinde F8 tuşu veya sağ kenardaki "HİLE" butonu ile açılır.
## Kaldırmak için bu dosyayı (ve oluşan zz_cheatmenu.rpyc dosyasını) silmen yeterli.

default cheat_money_input = ""

init 999 python:

    def cheat_ready():
        return (not main_menu) and (not _in_replay) and getattr(store, "pc", None) is not None

    # ---------- Para ----------
    def cheat_money_add(amount):
        store.pc.money = max(0, int(store.pc.money) + int(amount))
        renpy.notify("Para: " + str(store.pc.money))

    def cheat_money_set(value):
        try:
            value = int(str(value).replace(".", "").replace(",", "").strip() or "0")
        except Exception:
            renpy.notify("Geçersiz sayı")
            return
        store.pc.money = max(0, value)
        renpy.notify("Para: " + str(store.pc.money))

    def cheat_money_set_from_input():
        cheat_money_set(store.cheat_money_input)

    # ---------- Statlar ----------
    cheat_stat_labels = [
        ("perversion", "Perversion (Sapkınlık)"),
        ("submission", "Submission (İtaat)"),
        ("domination", "Domination (Baskınlık)"),
        ("adaptation", "Adaptation (Uyum)"),
        ("oral", "Oral"),
        ("anal", "Anal"),
        ("handjob", "Handjob (El işi)"),
        ("intellegence", "Intelligence (Zeka)"),
        ("dexterity", "Dexterity (Beceri)"),
        ("yoga", "Yoga"),
        ("service", "Service (Hizmet)"),
        ("sports", "Sports (Spor)"),
    ]

    def cheat_stat_change(key, amount):
        st = store.pc.stats.stats
        st[key] = max(0, st.get(key, 0) + amount)

    def cheat_stat_set(key, value):
        store.pc.stats.stats[key] = value

    def cheat_all_stats(value):
        for key, _label in cheat_stat_labels:
            store.pc.stats.stats[key] = value
        renpy.notify("Tüm statlar = " + str(value))

    # ---------- Anal seviyeleri ----------
    def cheat_set_stretching(level):
        store.pc.anal.stretching_level = level

    def cheat_set_enjoiment(level):
        store.pc.anal.enjoiment_level = level

    def cheat_anal_value(attr, amount):
        setattr(store.pc.anal, attr, max(0, getattr(store.pc.anal, attr, 0) + amount))

    # ---------- Mağaza / galeri / not defteri ----------
    def cheat_buy_all_shop():
        n = 0
        for shop_item in getattr(store, "shop_items", []):
            if not shop_item.bought:
                store.inventory.append(shop_item.item)
                shop_item.set_bought()
                n += 1
        renpy.notify("Mağazadan " + str(n) + " ürün bedavaya alındı")

    def cheat_unlock_gallery():
        persistent.gallery_unlocked = True
        store.gallery_images = list(getattr(store, "all_gallery_images", []))
        renpy.notify("Galeri tamamen açıldı")

    def cheat_reveal_notebook():
        n = 0
        for name, value in list(store.__dict__.items()):
            if name.startswith("cd_") and isinstance(value, CharacterData):
                value.unlocked = True
                for fact in value._facts:
                    fact.reveal()
                    n += 1
        renpy.notify("Not defteri: " + str(n) + " bilgi açıldı")

    # (değişken, etiket)
    cheat_ui_flags = [
        ("map_available", "Harita"),
        ("smartphone_available", "Telefon"),
        ("inventory_available", "Envanter"),
        ("notebook_available", "Not defteri"),
        ("money_available", "Para göstergesi"),
        ("reflections_available", "Düşünceler"),
    ]

    def cheat_toggle_var(name):
        setattr(store, name, not getattr(store, name, False))

    config.overlay_screens.append("cheat_overlay")


style cheat_text is default:
    font "DejaVuSans.ttf"
    size 20
    color "#ffffff"
    outlines [(1, "#000000", 0, 0)]

style cheat_title is cheat_text:
    size 28
    bold True
    color "#ff9ad5"

style cheat_head is cheat_text:
    size 22
    bold True
    color "#ffc6e8"

style cheat_button is default:
    background "#2e2e3acc"
    hover_background "#d6449acc"
    selected_background "#8f2d67cc"
    insensitive_background "#2e2e3a66"
    padding (10, 4)
    xminimum 50
    margin (2, 2)

style cheat_button_text is cheat_text:
    size 18
    xalign 0.5
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#777777"


screen cheat_overlay():
    zorder 190
    if cheat_ready() and not renpy.get_screen("cheat_menu"):
        key "K_F8" action Show("cheat_menu")
        textbutton "HİLE":
            style "cheat_button"
            text_style "cheat_button_text"
            xalign 1.0 yalign 0.55
            action Show("cheat_menu")


screen cheat_menu():
    modal True
    zorder 200
    default tab = "money"

    key "K_F8" action Hide("cheat_menu")
    key "game_menu" action Hide("cheat_menu")

    add Solid("#000000aa")

    frame:
        xalign 0.5 yalign 0.5
        xsize 1400 ysize 900
        background "#17121bee"
        padding (24, 18)

        vbox:
            spacing 10

            hbox:
                xfill True
                text "HİLE MENÜSÜ" style "cheat_title"
                textbutton "Kapat [[F8]" style "cheat_button" text_style "cheat_button_text" xalign 1.0 action Hide("cheat_menu")

            hbox:
                spacing 6
                textbutton "Para & Statlar" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "money")
                textbutton "Anal seviyeleri" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "anal")
                textbutton "Kilit açma" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "unlock")

            null height 4

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 760

                vbox:
                    spacing 8
                    xsize 1320

                    if tab == "money":
                        use cheat_tab_money
                    elif tab == "anal":
                        use cheat_tab_anal
                    elif tab == "unlock":
                        use cheat_tab_unlock


screen cheat_tab_money():
    $ money = int(pc.money)
    text "Para: [money]" style "cheat_head"
    hbox:
        spacing 4
        for amt in (100, 1000, 10000, 100000):
            textbutton "+[amt]" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_add, amt)
        textbutton "-100" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_add, -100)
        textbutton "Sıfırla" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_set, 0)

    hbox:
        spacing 8
        text "Tam miktar yaz:" style "cheat_text" yalign 0.5
        frame:
            background "#00000088"
            xsize 260
            padding (8, 4)
            input value VariableInputValue("cheat_money_input", returnable=False) allow "0123456789" length 10 style "cheat_text"
        textbutton "Ayarla" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_set_from_input)

    null height 6
    hbox:
        spacing 8
        text "Statlar" style "cheat_head" yalign 0.5
        textbutton "Hepsi 50" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_stats, 50)
        textbutton "Hepsi 100" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_stats, 100)
        textbutton "Hepsi 0" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_stats, 0)

    for key, label in cheat_stat_labels:
        $ val = pc.stats.stats.get(key, 0)
        hbox:
            spacing 4
            text "[label]" style "cheat_text" xsize 360 yalign 0.5
            text "[val]" style "cheat_text" xsize 80 yalign 0.5
            textbutton "-10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_change, key, -10)
            textbutton "-1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_change, key, -1)
            textbutton "+1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_change, key, 1)
            textbutton "+10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_change, key, 10)
            textbutton "0" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_set, key, 0)
            textbutton "100" style "cheat_button" text_style "cheat_button_text" action Function(cheat_stat_set, key, 100)


screen cheat_tab_anal():
    $ anal = pc.anal
    $ sv = anal.stretching_value
    $ ev = anal.enjoiment_value

    text "Anal esneme seviyesi (Stretching)" style "cheat_head"
    hbox:
        spacing 4
        for lvl in StretchingLevel:
            textbutton lvl.value style "cheat_button" text_style "cheat_button_text" selected anal.stretching_level == lvl action Function(cheat_set_stretching, lvl)
    hbox:
        spacing 4
        text "Değer: [sv]" style "cheat_text" xsize 200 yalign 0.5
        textbutton "-5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "stretching_value", -5)
        textbutton "+5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "stretching_value", 5)
        textbutton "+25" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "stretching_value", 25)

    null height 10
    text "Anal zevk seviyesi (Enjoyment)" style "cheat_head"
    hbox:
        spacing 4
        for lvl in EnjoimentLevel:
            textbutton lvl.value style "cheat_button" text_style "cheat_button_text" selected anal.enjoiment_level == lvl action Function(cheat_set_enjoiment, lvl)
    hbox:
        spacing 4
        text "Değer: [ev]" style "cheat_text" xsize 200 yalign 0.5
        textbutton "-5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "enjoiment_value", -5)
        textbutton "+5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "enjoiment_value", 5)
        textbutton "+25" style "cheat_button" text_style "cheat_button_text" action Function(cheat_anal_value, "enjoiment_value", 25)

    null height 10
    text "{size=17}{color=#ffb0b0}Seviyeyi çok erken yükseltmek bazı sahneleri atlatabilir.{/color}{/size}" style "cheat_text"


screen cheat_tab_unlock():
    text "Mağaza, galeri, not defteri" style "cheat_head"
    hbox:
        spacing 6
        textbutton "Mağazadaki her şeyi bedava al" style "cheat_button" text_style "cheat_button_text" action Function(cheat_buy_all_shop)
        textbutton "Galeriyi tamamen aç" style "cheat_button" text_style "cheat_button_text" action Function(cheat_unlock_gallery)
        textbutton "Not defterindeki tüm bilgileri aç" style "cheat_button" text_style "cheat_button_text" action Function(cheat_reveal_notebook)

    null height 10
    text "Arayüz butonları" style "cheat_head"
    text "{size=17}{color=#ffb0b0}Hikâye bunları sırayla açar; erken açmak bazı olayları bozabilir.{/color}{/size}" style "cheat_text"
    hbox:
        spacing 4
        for var, label in cheat_ui_flags:
            $ on = getattr(store, var, False)
            textbutton ("[label]: AÇIK" if on else "[label]: kapalı") style "cheat_button" text_style "cheat_button_text" selected on action Function(cheat_toggle_var, var)
