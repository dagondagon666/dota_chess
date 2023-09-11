import logging

def handle_left_click():
    if GAME_STATE.get()["show_winner_overlay"]:
                logging.info("RESET Game")
                GAME_STATE.init_game_state()
            else:
                # Get tile coordinates of the clicked position
                x, y = event.pos
                tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
                logging.info(
                    f"Player {GAME_STATE.get()['current_player']}: clicked ({tile_x}, {tile_y})"
                )

                ## Buttons
                ### End button
                if end_turn_button.collidepoint(x, y):
                    logging.info(
                        f"Player {GAME_STATE.get()['current_player']}: end turn"
                    )
                    GAME_STATE.get()["current_player"] = (
                        3 - GAME_STATE.get()["current_player"]
                    )  # Switch between player 1 and 2
                    GAME_STATE.get()[
                        "hero_moved"
                    ] = []  # Reset the list of moved heroes for the new turn
                    continue
                ### attack button
                elif (
                    attack_button.collidepoint(x, y)
                    and GAME_STATE.get()["selected_hero"]
                ):
                    logging.info(
                        f"Player {GAME_STATE.get()['current_player']}: selected action ATTACK"
                    )
                    GAME_STATE.get()["selected_action"] = "attack"
                    continue
                ### Ability button
                elif (
                    ability_button.collidepoint(x, y)
                    and GAME_STATE.get()["selected_hero"]
                ):
                    logging.info(
                        f"Player {GAME_STATE.get()['current_player']}: selected action ABILITY"
                    )
                    GAME_STATE.get()["selected_action"] = "ability"
                    continue

                # Inside the main loop, within the MOUSEBUTTONDOWN event handling
                if GAME_STATE.get()["selected_hero"]:
                    if (
                        tile_x == GAME_STATE.get()["selected_hero"].x
                        and tile_y == GAME_STATE.get()["selected_hero"].y
                    ):
                        logging.info(
                            f"Player {GAME_STATE.get()['current_player']}: deselect hero {GAME_STATE.get()['selected_hero'].name}"
                        )
                        GAME_STATE.get()["selected_hero"] = None
                        continue
                    if GAME_STATE.get()["selected_action"] == "attack":
                        target_hero = get_hero_at_tile(
                            tile_x,
                            tile_y,
                            GAME_STATE.get()["heroes"][1]
                            if GAME_STATE.get()["current_player"] == 1
                            else GAME_STATE.get()["heroes"][0],
                        )
                        if target_hero:
                            target_hero_old_hp = target_hero.hp
                            target_hero.hp -= 1
                            GAME_STATE.get()[
                                "selected_action"
                            ] = "move"  # Reset action to move after performing attack
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: hero {GAME_STATE.get()['selected_hero'].name} ATTACKED enemy hero {target_hero.name}: {target_hero_old_hp} -> {target_hero.hp}"
                            )
                            GAME_STATE.get()[
                                "selected_hero"
                            ] = None  # Reset selected hero after performing action
                        elif not is_base_tile(
                            tile_x, tile_y
                        ):  # If it's not a base tile, move the hero
                            GAME_STATE.get()["selected_hero"].x = tile_x
                            GAME_STATE.get()["selected_hero"].y = tile_y
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: Attack Moved hero {GAME_STATE.get()['selected_hero'].name} -> {tile_x}, {tile_y}"
                            )
                            GAME_STATE.get()["selected_hero"] = None
                        elif is_base_tile(tile_x, tile_y):
                            target_base = GAME_STATE.get()["bases"][0]
                            if GAME_STATE.get()["current_player"] == 1:
                                target_base = GAME_STATE.get()["bases"][1]
                            old_hp = target_base.hp
                            target_base.hp -= 1
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: hero {GAME_STATE.get()['selected_hero'].name} ATTACKED enemy base: {old_hp} -> {target_base.hp}"
                            )
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            GAME_STATE.get()[
                                "selected_action"
                            ] = "move"  # Reset action to move after performing attack
                            GAME_STATE.get()[
                                "selected_hero"
                            ] = None  # Reset selected hero after performing action
                    elif GAME_STATE.get()["selected_action"] == "ability":
                        target_hero = get_hero_at_tile(
                            tile_x,
                            tile_y,
                            GAME_STATE.get()["heroes"][1]
                            if GAME_STATE.get()["current_player"] == 1
                            else GAME_STATE.get()["heroes"][0],
                        )
                        if target_hero and not is_base_tile(tile_x, tile_y):
                            target_hero_old_hp = target_hero.hp
                            target_hero.hp = round(target_hero.hp / 2)
                            GAME_STATE.get()[
                                "selected_action"
                            ] = "move"  # Reset action to move after using ability
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: hero {GAME_STATE.get()['selected_hero'].name} used ABILITY on enemy hero {target_hero.name}: {target_hero_old_hp} -> {target_hero.hp}"
                            )
                            GAME_STATE.get()[
                                "selected_hero"
                            ] = None  # Reset selected hero after performing action
                        elif not is_base_tile(
                            tile_x, tile_y
                        ):  # If it's not a base tile, move the hero
                            GAME_STATE.get()["selected_hero"].x = tile_x
                            GAME_STATE.get()["selected_hero"].y = tile_y
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: Ability Moved hero {GAME_STATE.get()['selected_hero'].name} -> {tile_x}, {tile_y}"
                            )
                            GAME_STATE.get()["selected_hero"] = None
                    elif (
                        GAME_STATE.get()["selected_action"] == "move"
                    ):  # Move the selected hero to the clicked tile if it is within the map
                        if 0 <= tile_x < 19 and 0 <= tile_y < 19:
                            GAME_STATE.get()["selected_hero"].x = tile_x
                            GAME_STATE.get()["selected_hero"].y = tile_y
                            GAME_STATE.get()["hero_moved"].append(
                                GAME_STATE.get()["selected_hero"]
                            )
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: Moved hero {GAME_STATE.get()['selected_hero'].name} -> {tile_x}, {tile_y}"
                            )
                            GAME_STATE.get()[
                                "selected_hero"
                            ] = None  # Deselect the hero after moving
                else:
                    for hero in (
                        GAME_STATE.get()["heroes"][0]
                        if GAME_STATE.get()["current_player"] == 1
                        else GAME_STATE.get()["heroes"][1]
                    ):
                        if (
                            hero.x == tile_x
                            and hero.y == tile_y
                            and hero not in GAME_STATE.get()["hero_moved"]
                        ):
                            GAME_STATE.get()["selected_hero"] = hero
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: selected hero {GAME_STATE.get()['selected_hero'].name}"
                            )
                            break