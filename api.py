from http.server import SimpleHTTPRequestHandler
from json import dumps, loads

from negocio.funciones import (
    cambiar_cantidad_bolsillo,
    comprar_producto,
    insertar_desde_bolsillo,
    obtener_estado,
    recoger_entrega,
)


class ApiHandler(SimpleHTTPRequestHandler):
    def obtener_json(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        cuerpo = self.rfile.read(content_length) if content_length > 0 else b"{}"
        return loads(cuerpo.decode("utf-8"))

    def responder(self, datos, estado=200):
        contenido = dumps(datos).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def do_GET(self):
        if self.path == "/api/estado":
            self.api_estado()
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/bolsillo/cambiar":
            self.api_cambiar_bolsillo()
            return
        if self.path == "/api/insertar":
            self.api_insertar()
            return
        if self.path == "/api/comprar":
            self.api_comprar()
            return
        if self.path == "/api/recoger":
            self.api_recoger()
            return
        self.send_error(404)

    def api_estado(self):
        self.responder({"estado": obtener_estado()})

    def api_cambiar_bolsillo(self):
        datos = self.obtener_json()
        respuesta = cambiar_cantidad_bolsillo(datos["id"], int(datos["delta"]))
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_insertar(self):
        datos = self.obtener_json()
        respuesta = insertar_desde_bolsillo(datos["id"], datos["tipo_ranura"])
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_comprar(self):
        datos = self.obtener_json()
        respuesta = comprar_producto(datos["codigo"])
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_recoger(self):
        respuesta = recoger_entrega()
        self.responder(respuesta, 200 if respuesta["ok"] else 400)
