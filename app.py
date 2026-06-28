from http.server import ThreadingHTTPServer
from pathlib import Path
import os
import sys

from api import ApiHandler


HOST = "127.0.0.1"
PORT = 5500
BASE_DIR = Path(__file__).resolve().parent


class StaticHandler(ApiHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)


def main() -> None:
    os.chdir(BASE_DIR)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = None

    for candidate_port in range(port, port + 20):
        try:
            server = ThreadingHTTPServer((HOST, candidate_port), StaticHandler)
            port = candidate_port
            break
        except PermissionError:
            continue
        except OSError:
            continue

    if server is None:
        raise RuntimeError("No se pudo abrir un puerto entre 5500 y 5519.")

    print(f"Servidor activo en http://{HOST}:{port}")
    print(f"Sirviendo archivos desde: {BASE_DIR}")
    print("Presiona Ctrl+C para detenerlo.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
