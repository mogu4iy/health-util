from genericpath import exists
import os
import sys

from .config import VERSION
from .healthcheck import get_config, parse_config, validate_schema

try:
    import click
except ImportError:
    sys.stderr.write('It seems health-util is not installed with cli option. \n'
                     'Run pip install "health-util[cli]" to fix this.')
    sys.exit(1)

@click.group(chain=True)
@click.option('-e', '--env', default=None,
              type=click.Path(file_okay=True),
              help="Path to env file, defaults to .env.healthcheck file in current working directory.")
@click.option('-c', '--config', default='healthcheck.json',
              type=click.Path(exists=True),
              help="Path to config file, defaults to healthcheck.json file in current working directory.")
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx: click.Context, env, config) -> None:
    ctx.ensure_object(dict)
    ctx.obj["ENV_PATH"] = os.path.join(os.getcwd(), env) if env else None
    ctx.obj["ENV_FILE"] = env
    ctx.obj["CONFIG_PATH"] = os.path.join(os.getcwd(), config) if config else None
    ctx.obj["CONFIG_FILE"] = config

@cli.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    config = parse_config(config_path=ctx.obj["CONFIG_PATH"])
    validate_schema(config)
    click.echo(f"Config file '{ctx.obj['CONFIG_FILE']}' is valid.")

@cli.command()
@click.pass_context
def check(ctx: click.Context) -> None:
    print('check')
    config = get_config(config_path=ctx.obj["CONFIG_PATH"], env_path=ctx.obj["ENV_PATH"])
    pass    