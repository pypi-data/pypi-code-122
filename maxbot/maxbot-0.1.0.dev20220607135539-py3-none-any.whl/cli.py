import logging
import pathlib

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

import click
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

from maxbot.bot import MaxBot
from maxbot.channels import TelegramShim
from maxbot.schemas import Definitions


def _validate_project_dir(ctx, param, project_dir):
    if project_dir.exists():
        raise click.BadParameter(f'directory "{project_dir}" already exists')
    return project_dir


@click.command()
@click.argument(
    "project_dir", type=click.Path(path_type=pathlib.Path), callback=_validate_project_dir
)
@click.option(
    "--telegram-token",
    help="Go to https://t.me/botfather ask him to create a bot and generate a token",
    prompt=True,
)
def new(project_dir, telegram_token):
    """
    Create new project from template.

    PROJECT_DIR     Directory where the project will be created.

    Example:

        maxbot new hello-world

        maxbot new mybot --telegram-token XXX
    """
    project_dir.mkdir()
    bot_file = project_dir / "bot.yaml"
    bot_file.write_text(HELLO_WORLD.format(telegram_token=telegram_token))
    click.echo(f"Generate file {bot_file}")
    click.echo("Project succseed")


HELLO_WORLD = """
channels:
  telegram:
    api_key: {telegram_token}
intents:
  - name: greetings
    examples:
      - Good morning
      - Hello
      - Hi
  - name: ending
    examples:
      - Goodbye
      - Bye
      - See you
dialog:
  - condition: intents.greetings
    response: Good day to you!
  - condition: intents.ending
    response: OK. See you later.
""".strip()


@click.command()
def develop():
    """
        Run a bot in interactive mode.
    """
    definitions = Definitions().from_yaml("./bot.yaml", dotenv_values())
    shim = TelegramShim(MaxBot(definitions))

    def callback(update: Update, context: CallbackContext):
        shim(update, context.bot)

    updater = Updater(definitions.channels.telegram.api_key)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, callback))
    updater.start_polling()
    updater.idle()


@click.group()
def main():
    pass


main.add_command(new)
main.add_command(develop)
