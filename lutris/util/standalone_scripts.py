import os

from lutris.game import Game


def generate_script(logger, launch_ui_delegate, db_game, script_path, extra_args):
    """Output a script to a file.
    The script is capable of launching a game without the client
    """

    logger.info(f"Try creating script for '{db_game['name']}'")

    def on_error(error: BaseException) -> None:
        logger.exception("Unable to generate script: %s", error)

    game = Game(db_game["id"])
    game.game_error.register(on_error)
    game.reload_config()

    if extra_args:
        args = merge_args(game, extra_args)
        game.config.game_config["args"] = args

    game.write_script(script_path, launch_ui_delegate)
    absolutePath = os.path.abspath(script_path)
    logger.info(f"Wrote script to: '{absolutePath}'")

def merge_args(game, extra_args):
    args = game.config.game_config["args"] + " " + extra_args.get_string()
    return args
