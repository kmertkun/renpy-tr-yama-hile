## Path of Desire - Hile Menusu
## Oyun icinde F8 tusu veya sag kenardaki "HİLE" butonu ile acilir.
## Kaldirmak icin bu dosyayi (ve olusan zz_cheatmenu.rpyc dosyasini) silmen yeterli.

default cheat_money_input = ""

init 999 python:
    import copy as _cheat_copy

    def cheat_ready():
        return (not main_menu) and (not _in_replay) and getattr(store, "myGame", None) is not None

    # ---------- Para ----------
    def cheat_money_add(amount):
        p = store.myGame.player
        p.money = max(0, int(p.money) + int(amount))
        renpy.notify("Para: " + p.getFormattedMoney)

    def cheat_money_set(value):
        try:
            value = int(str(value).replace(".", "").replace(",", "").strip())
        except Exception:
            renpy.notify("Gecersiz sayi")
            return
        store.myGame.player.money = max(0, value)
        renpy.notify("Para: " + store.myGame.player.getFormattedMoney)

    def cheat_money_set_from_input():
        cheat_money_set(store.cheat_money_input or "0")

    def cheat_set_var(name, value):
        setattr(store, name, value)

    # ---------- Oyuncu statlari ----------
    # (attr, etiket, ust sinir) - None = sinirsiz
    cheat_player_stats = [
        ("horny", "Lust (Şehvet)", 100),
        ("corruption", "Corruption (Yozlaşma)", 100),
        ("dominance", "Dominance (Baskınlık)", None),
        ("submissive", "Submissiveness (İtaat)", None),
        ("restraint", "Restraint (Kontrol)", None),
    ]

    def cheat_player_stat(attr, amount, cap):
        p = store.myGame.player
        v = getattr(p, attr, 0) + amount
        if cap is not None:
            v = min(cap, v)
        setattr(p, attr, max(0, v))

    def cheat_player_stat_set(attr, value):
        setattr(store.myGame.player, attr, value)

    # ---------- NPC ----------
    def cheat_npc_list():
        mgr = getattr(store, "myNpcs", None)
        if mgr is None:
            return []
        return list(mgr.npcs.values())

    def _cheat_npc_bounds(attr):
        return (-100 if attr == "affection" else 0), 100

    def cheat_npc_change(npc, attr, amount):
        lo, hi = _cheat_npc_bounds(attr)
        setattr(npc, attr, max(lo, min(hi, getattr(npc, attr, 0) + amount)))

    def cheat_npc_set(npc, attr, value):
        lo, hi = _cheat_npc_bounds(attr)
        setattr(npc, attr, max(lo, min(hi, value)))

    def cheat_all_npcs_max():
        for npc in cheat_npc_list():
            npc.affection = 100
            npc.desire = 100
        renpy.notify("Tüm NPC'ler: Affection & Desire = 100")

    # ---------- Muttefikler (Memory Nexus) ----------
    def cheat_ally_list():
        mgr = getattr(store, "myAllies", None)
        if mgr is None:
            return []
        return mgr.getAllAllies()

    def cheat_ally_level(ally, levels=1):
        for _i in range(levels):
            if ally.level >= ally.level_cap:
                ally.level_cap = ally.level + 1
            ally.gainExp(max(1, ally.exp_to_next - ally.exp))
        ally.exp = 0
        ally.recalculateAllStats(full_heal=True)

    def cheat_ally_points(ally, amount):
        ally.level_up_points = max(0, ally.level_up_points + amount)

    def cheat_ally_jutsu(ally, amount):
        ally.jutsu_points = max(0, getattr(ally, "jutsu_points", 0) + amount)

    def cheat_ally_cap(ally, amount):
        ally.level_cap = max(ally.level, ally.level_cap + amount)

    def cheat_ally_heal(ally):
        ally.fullHealAndRevive()

    def cheat_ally_unlock(ally):
        ally.unlocked = True
        dungeon = getattr(store, "myDungeon", None)
        if dungeon is not None:
            dungeon.available_allies[ally.name] = ally

    # ---------- Esyalar ----------
    def cheat_item_list():
        result = []
        for name in sorted(dir(store)):
            if name.startswith("item_"):
                obj = getattr(store, name, None)
                if isinstance(obj, Item):
                    result.append(obj)
        return result

    def cheat_item_add(item, count):
        store.myGame.player.inventory.addItem(_cheat_copy.deepcopy(item), count)
        renpy.notify(str(item.name) + " x" + str(count) + " eklendi")

    def cheat_item_remove(item, count):
        store.myGame.player.inventory.removeItem(item.name, count)

    def cheat_all_items(count):
        for item in cheat_item_list():
            if not item.questitem:
                store.myGame.player.inventory.addItem(_cheat_copy.deepcopy(item), count)
        renpy.notify("Tüm eşyalar x" + str(count) + " eklendi (görev eşyaları hariç)")

    config.overlay_screens.append("cheat_overlay")


style cheat_text is default:
    font "DejaVuSans.ttf"
    size 22
    color "#ffffff"
    outlines [(1, "#000000", 0, 0)]

style cheat_title is cheat_text:
    size 30
    bold True
    color "#ffb347"

style cheat_head is cheat_text:
    size 24
    bold True
    color "#ffd27f"

style cheat_button is default:
    background "#2e2e3acc"
    hover_background "#ff623bcc"
    selected_background "#b8452acc"
    insensitive_background "#2e2e3a66"
    padding (10, 4)
    xminimum 52
    margin (2, 2)

style cheat_button_text is cheat_text:
    size 20
    xalign 0.5
    hover_color "#ffffff"
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
        xsize 1500 ysize 940
        background "#15151dee"
        padding (24, 18)

        vbox:
            spacing 10

            hbox:
                xfill True
                text "HİLE MENÜSÜ" style "cheat_title"
                textbutton "Kapat [[F8]" style "cheat_button" text_style "cheat_button_text" xalign 1.0 action Hide("cheat_menu")

            hbox:
                spacing 6
                textbutton "Para & Oyuncu" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "money")
                textbutton "Karakterler (NPC)" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "npc")
                textbutton "Müttefikler (Nexus)" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "ally")
                textbutton "Eşyalar" style "cheat_button" text_style "cheat_button_text" action SetScreenVariable("tab", "items")

            null height 4

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 790

                vbox:
                    spacing 8
                    xsize 1420

                    if tab == "money":
                        use cheat_tab_money
                    elif tab == "npc":
                        use cheat_tab_npc
                    elif tab == "ally":
                        use cheat_tab_ally
                    elif tab == "items":
                        use cheat_tab_items


screen cheat_tab_money():
    $ p = myGame.player

    text "Para: [p.getFormattedMoney] ryō" style "cheat_head"
    hbox:
        spacing 4
        for amt in (100, 1000, 10000, 100000, 1000000):
            textbutton "+{:,}".format(amt).replace(",", ".") style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_add, amt)
        textbutton "-1.000" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_add, -1000)
        textbutton "Sıfırla" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_set, 0)

    hbox:
        spacing 8
        text "Tam miktar yaz:" style "cheat_text" yalign 0.5
        frame:
            background "#00000088"
            xsize 260
            padding (8, 4)
            input value VariableInputValue("cheat_money_input", returnable=False) allow "0123456789" length 12 style "cheat_text"
        textbutton "Ayarla" style "cheat_button" text_style "cheat_button_text" action Function(cheat_money_set_from_input)

    null height 6
    text "Karui borcu: [karui_debt] ryō" style "cheat_head"
    hbox:
        spacing 4
        textbutton "Borcu sıfırla" style "cheat_button" text_style "cheat_button_text" action Function(cheat_set_var, "karui_debt", 0)

    null height 6
    text "Oyuncu statları" style "cheat_head"
    for attr, label, cap in cheat_player_stats:
        $ val = getattr(p, attr, 0)
        hbox:
            spacing 4
            text "[label]" style "cheat_text" xsize 380 yalign 0.5
            text "[val]" style "cheat_text" xsize 80 yalign 0.5
            textbutton "-10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat, attr, -10, cap)
            textbutton "-1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat, attr, -1, cap)
            textbutton "+1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat, attr, 1, cap)
            textbutton "+10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat, attr, 10, cap)
            textbutton "0" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat_set, attr, 0)
            textbutton "100" style "cheat_button" text_style "cheat_button_text" action Function(cheat_player_stat_set, attr, 100)


screen cheat_tab_npc():
    hbox:
        spacing 8
        text "Affection: -100..100   Desire / Dominance: 0..100" style "cheat_text" yalign 0.5
        textbutton "Hepsini MAX yap" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_npcs_max)

    for npc in cheat_npc_list():
        frame:
            background "#ffffff10"
            xfill True
            padding (10, 6)
            vbox:
                spacing 2
                $ route = getattr(npc, "current_route", "default")
                $ step = getattr(npc, "route_step", 0)
                text "[npc.name]  {size=16}{color=#aaaaaa}(rota: [route], adım: [step]){/color}{/size}" style "cheat_head"
                for attr, label in (("affection", "Affection (Sevgi)"), ("desire", "Desire (Arzu)"), ("dominance", "Dominance")):
                    $ val = getattr(npc, attr, 0)
                    hbox:
                        spacing 4
                        text "[label]" style "cheat_text" xsize 300 yalign 0.5
                        text "[val]" style "cheat_text" xsize 70 yalign 0.5
                        textbutton "-10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_change, npc, attr, -10)
                        textbutton "-1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_change, npc, attr, -1)
                        textbutton "+1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_change, npc, attr, 1)
                        textbutton "+10" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_change, npc, attr, 10)
                        textbutton "MIN" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_set, npc, attr, -100)
                        textbutton "MAX" style "cheat_button" text_style "cheat_button_text" action Function(cheat_npc_set, npc, attr, 100)


screen cheat_tab_ally():
    text "Memory Nexus müttefikleri. Stat puanlarını oyunun kendi ekranından dağıtabilirsin." style "cheat_text"

    for ally in cheat_ally_list():
        frame:
            background "#ffffff10"
            xfill True
            padding (10, 6)
            vbox:
                spacing 4
                $ jp = getattr(ally, "jutsu_points", 0)
                $ lock = "" if ally.unlocked else "  {color=#ff6666}(KİLİTLİ){/color}"
                text "[ally.name]  {size=18}Lv [ally.level]/[ally.level_cap]  HP [ally.hp]/[ally.max_hp]  Chakra [ally.chakra]/[ally.max_chakra]{/size}[lock!i]" style "cheat_head"
                text "Might [ally.might]  Agility [ally.agility]  Focus [ally.focus]  Technique [ally.technique]   |   Stat puanı: [ally.level_up_points]   Jutsu puanı: [jp]" style "cheat_text"
                hbox:
                    spacing 4
                    textbutton "+1 Level" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_level, ally, 1)
                    textbutton "+5 Level" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_level, ally, 5)
                    textbutton "+10 Level Cap" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_cap, ally, 10)
                    textbutton "+5 Stat puanı" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_points, ally, 5)
                    textbutton "+1 Jutsu puanı" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_jutsu, ally, 1)
                    textbutton "Tam iyileştir" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_heal, ally)
                    if not ally.unlocked:
                        textbutton "Kilidi aç" style "cheat_button" text_style "cheat_button_text" action Function(cheat_ally_unlock, ally)


screen cheat_tab_items():
    $ inv = myGame.player.inventory
    hbox:
        spacing 6
        textbutton "Tüm eşyalardan +5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_items, 5)
        textbutton "Tüm eşyalardan +20" style "cheat_button" text_style "cheat_button_text" action Function(cheat_all_items, 20)
    text "{size=18}{color=#ffb0b0}[[GÖREV] işaretli eşyaları tek tek eklemek görev akışını bozabilir, dikkatli kullan.{/color}{/size}" style "cheat_text"

    for item in cheat_item_list():
        $ have = inv.countItem(item.name)
        $ tag = "  {color=#ff8080}[[GÖREV]{/color}" if item.questitem else ""
        hbox:
            spacing 4
            text "[item.name!t][tag!i]" style "cheat_text" xsize 520 yalign 0.5
            text "Sahip: [have]" style "cheat_text" xsize 140 yalign 0.5
            textbutton "+1" style "cheat_button" text_style "cheat_button_text" action Function(cheat_item_add, item, 1)
            textbutton "+5" style "cheat_button" text_style "cheat_button_text" action Function(cheat_item_add, item, 5)
            textbutton "+20" style "cheat_button" text_style "cheat_button_text" action Function(cheat_item_add, item, 20)
            textbutton "-1" style "cheat_button" text_style "cheat_button_text" sensitive have > 0 action Function(cheat_item_remove, item, 1)
