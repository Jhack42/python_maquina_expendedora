from http.server import SimpleHTTPRequestHandler
from json import dumps, loads

from negocio.funciones import (
    cambiar_cantidad_bolsillo,
    comprar_producto,
    insertar_desde_bolsillo,
    obtener_estado,
    recoger_entrega,
    recoger_producto,
)
from negocio.funcinones.admin import (
    obtener_estado_admin,
    generar_reporte_inventario,
    generar_reporte_monedas,
    generar_boleta_con_productos,
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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(contenido)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        elif self.path == "/admin":
            self.path = "/admin.html"
        
        if self.path == "/api/estado":
            self.api_estado()
            return
        if self.path == "/api/admin/estado":
            self.api_admin_estado()
            return
        if self.path == "/api/admin/descargar/inventario":
            self.api_descargar_inventario()
            return
        if self.path == "/api/admin/descargar/monedas":
            self.api_descargar_monedas()
            return
        
        # Servir archivos estáticos con headers CORS
        response = super().do_GET()
        self.send_header("Access-Control-Allow-Origin", "*")
        return response

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
        if self.path == "/api/recoger-producto":
            self.api_recoger_producto()
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
        if respuesta["ok"] and respuesta.get("producto_entregado"):
            boleta_path = generar_boleta_con_productos([
                {
                    "nombre": respuesta["producto_entregado"]["nombre"],
                    "cantidad": 1,
                    "precio_centimos": respuesta["producto_entregado"]["precio_centimos"],
                }
            ], pago_centimos=respuesta.get("pago_centimos", 0), vuelto_centimos=respuesta.get("vuelto_centimos", 0))
            respuesta["boleta"] = boleta_path
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_recoger(self):
        respuesta = recoger_entrega()
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_recoger_producto(self):
        respuesta = recoger_producto()
        # Generar boleta cuando se recoge el producto
        if respuesta["ok"] and respuesta["estado"]["cliente_productos"]:
            boleta_path = generar_boleta_con_productos()
            respuesta["boleta"] = boleta_path
        self.responder(respuesta, 200 if respuesta["ok"] else 400)

    def api_admin_estado(self):
        self.responder({"estado": obtener_estado_admin()})

    def api_descargar_inventario(self):
        path = generar_reporte_inventario()
        self.responder({"path": path})

    def api_descargar_monedas(self):
        path = generar_reporte_monedas()
        self.responder({"path": path})
