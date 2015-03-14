from tsoliasgame import load_image


class Images:

    wall_image = load_image("pngs/walls.png")
    blue_blink_image = load_image("pngs/blue_blink.png")
    blue_shrink_image = load_image("pngs/blue_shrink.png")
    blue_blink_original = blue_blink_image.copy()
    blue_shrink_original = blue_shrink_image.copy()
    purple_image = load_image("pngs/purple.png")
    red_image = load_image("pngs/red.png")
    death_image = load_image("pngs/death.png")
    exit_image = load_image("pngs/exit.png")
    splatters_image = load_image("pngs/splatters.png")
    moverU_image = load_image("pngs/moverU.png")
    moverD_image = load_image("pngs/moverD.png")
    moverL_image = load_image("pngs/moverL.png")
    moverR_image = load_image("pngs/moverR.png")
    rock_image = load_image("pngs/rock.png")
    rock_shrink_image = load_image("pngs/rock_shrink.png")
    switch_en_image = load_image("pngs/switch_en.png")
    switch_dis_image = load_image("pngs/switch_dis.png")
    teleporter_image = load_image("pngs/teleporter_en.png")
    teleporter_active_image = load_image("pngs/teleporter_active.png")
    teleporter_dis_image = load_image("pngs/teleporter_dis.png")
    water_image = load_image("pngs/water.png")
    ice_image = load_image("pngs/ice.png")
    wood_image = load_image("pngs/wood.png")
    hud_image = load_image("pngs/hud.png")
    padlock_closed_image = load_image("pngs/padlock_closed.png")
    padlock_open_image = load_image("pngs/padlock_open.png")
    start_image = load_image("pngs/start.png")
    arrowu_image = load_image("pngs/arrowU.png")
    arrowd_image = load_image("pngs/arrowD.png")
    lock_image = load_image("pngs/lock.png")
    tick_image = load_image("pngs/tick.png")
    switch_image = load_image("pngs/switch.png")
    paused_image = load_image("pngs/paused.png")
    play_menu_image = load_image("pngs/play_menu.png")
    restart_menu_image = load_image("pngs/restart_menu.png")
    back_menu_image = load_image("pngs/back_menu.png")
    help_menu_image = load_image("pngs/help_menu.png")
    options_menu_image = load_image("pngs/options_menu.png")
    exit_menu_image = load_image("pngs/exit_menu.png")
    arrows_image = load_image("pngs/arrows.png")
    message_image = load_image("pngs/message.png")
    question_image = load_image("pngs/question.png")
    town_image = load_image("pngs/town.png")

    def __init__(self):
        pass  # this class is supposed to be a singleton!