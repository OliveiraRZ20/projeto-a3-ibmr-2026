from . import create_app


def run_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    app = create_app()
    app.run(host=host, port=port, debug=debug)
