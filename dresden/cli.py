import sys
import webbrowser

import click
import tornado.ioloop

__author__ = "Rohan B. Dalton"


@click.command()
@click.option("--host", "-h", default="127.0.0.1", help="Hostname to bind to")
@click.option("--port", "-p", default=8080, help="Port to listen on")
def server(host: str, port: int) -> None:
    try:
        from snakeviz.main import app
    except ImportError:
        click.echo("Snakeviz is not installed.")
    else:
        # https://github.com/tornadoweb/tornado/issues/2608
        if sys.platform == "win32" and sys.version_info[:2] == (3, 8):
            import asyncio

            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        url = f"http://{host}:{port}/snakeviz/"
        try:
            browser = webbrowser.get()
        except webbrowser.Error:
            click.echo("Unable to find browser")
        else:
            browser.open(url, new=2)

        app.listen(port=port, address=host)

        try:
            click.echo(f"Starting Snakeviz server at {url}.\nEnter Ctrl-C to exit")
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            click.echo("Stopping Snakeviz server")
            tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    server()
