"""Entry point for cli, enables execution with `python -m health-util`"""

from .cli import cli
import signal
import sys

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    cli()