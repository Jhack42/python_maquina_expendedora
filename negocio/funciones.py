from datetime import datetime
from pathlib import Path

from negocio import datos as datos_base

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTES_DIR = BASE_DIR / "reportes"


def _normalizar_productos():
    productos = []
    casilleros_ordenados = sorted(
        datos_base.casilleros.items(),
        key=lambda item: item[1].get("orden", 0),
    )

    for codigo_casillero, casillero in casilleros_ordenados:
        producto_id = casillero.get("producto_id")
        producto = datos_base.productos.get(producto_id)
        if producto is None:
            continue

        productos.append(
            {
                "codigo": f"{int(codigo_casillero):02d}",
                "nombre": producto["nombre"],
                "precio_centimos": int(float(producto["precio"]) * 100),
                "stock": casillero.get("stock", 0),
                "imagen": producto.get("img", producto.get("imagen", "")),
            }
        )
    return productos


def _normalizar_dinero():
    items = []
    for id_dinero, item in datos_base.dinero.items():
        valor = float(item["valor"])
        valor_centimos = int(valor * 100)
        categoria = "billete" if item["dinero_categoria_id"] == 1 else "moneda"
        nombre = item.get("nombre")
        if not nombre:
            if categoria == "moneda":
                if valor < 1:
                    nombre = f"{int(valor * 100)} centimos"
                else:
                    nombre = f"{int(valor)} sol"
            else:
                nombre = f"{int(valor)} soles"

        items.append(
            {
                "id": str(id_dinero),
                "tipo": categoria,
                "nombre": nombre,
                "valor_centimos": valor_centimos,
                "imagen": item.get("img", item.get("imagen", "")),
                "cantidad_maquina": item.get("cantidad", 0),
                "cantidad_bolsillo": item.get("cantidad", 0),
            }
        )
    return items


def _crear_directorio_reportes():
    REPORTES_DIR.mkdir(parents=True, exist_ok=True)


def _formatear_fecha():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


productos = _normalizar_productos()
dinero_base = _normalizar_dinero()
COMPATIBLE_IDS = {
    "m10": "1",
    "m20": "2",
    "m50": "3",
    "m1": "4",
    "m2": "5",
    "m5": "6",
    "b10": "7",
    "b20": "8",
    "b50": "9",
    "b100": "10",
    "b200": "11",
}

def _normalize_dinero_id(id_dinero):
    if id_dinero is None:
        return None
    if isinstance(id_dinero, int):
        return str(id_dinero)
    if isinstance(id_dinero, str):
        if id_dinero in dinero_maquina or id_dinero in bolsillo:
            return id_dinero
        if id_dinero.isdigit():
            return str(int(id_dinero))
        return COMPATIBLE_IDS.get(id_dinero.lower().strip())
    return None


dinero_maquina = {
    item["id"]: {
        "id": item["id"],
        "tipo": item["tipo"],
        "nombre": item["nombre"],
        "valor_centimos": item["valor_centimos"],
        "imagen": item["imagen"],
        "cantidad": item["cantidad_maquina"],
    }
    for item in dinero_base
}
bolsillo = {
    item["id"]: {
        "id": item["id"],
        "tipo": item["tipo"],
        "nombre": item["nombre"],
        "valor_centimos": item["valor_centimos"],
        "imagen": item["imagen"],
        "cantidad": item["cantidad_bolsillo"],
    }
    for item in dinero_base
}
saldo_maquina_centimos = 0
ultima_entrega = {"monedas": [], "billetes": [], "productos": []}
cliente_productos = []
ultimo_mensaje = "Bienvenido."


def mostrar_soles(cantidad_centimos):
    return f"S/ {cantidad_centimos / 100:.2f}"


def _buscar_producto(codigo):
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    return None


def _item_bolsillo(id_dinero):
    normalized_id = _normalize_dinero_id(id_dinero)
    if normalized_id is None:
        return None
    return bolsillo.get(normalized_id)


def _limpiar_entregas():
    global ultima_entrega
    ultima_entrega = {"monedas": [], "billetes": [], "productos": []}


def _serializar_producto(producto):
    return {
        "codigo": producto["codigo"],
        "nombre": producto["nombre"],
        "precio": producto["precio_centimos"] / 100,
        "stock": producto["stock"],
        "imagen": producto["imagen"],
    }


def _serializar_bolsillo(item):
    return {
        "id": item["id"],
        "tipo": item["tipo"],
        "nombre": item["nombre"],
        "valor": item["valor_centimos"] / 100,
        "imagen": item["imagen"],
        "cantidad": item["cantidad"],
    }


def _serializar_entrega_item(item):
    return {
        "nombre": item["nombre"],
        "imagen": item["imagen"],
        "cantidad": item["cantidad"],
    }


def _agregar_a_cliente_productos(item):
    for producto_en_canasta in cliente_productos:
        if producto_en_canasta["nombre"] == item["nombre"] and producto_en_canasta["imagen"] == item["imagen"]:
            producto_en_canasta["cantidad"] += item.get("cantidad", 1)
            return

    cliente_productos.append(
        {
            "nombre": item["nombre"],
            "imagen": item["imagen"],
            "cantidad": item.get("cantidad", 1),
        }
    )


def obtener_estado():
    return {
        "mensaje": ultimo_mensaje,
        "saldo_maquina": saldo_maquina_centimos / 100,
        "saldo_maquina_texto": mostrar_soles(saldo_maquina_centimos),
        "saldo_personal": sum(
            item["valor_centimos"] * item["cantidad"] for item in bolsillo.values()
        ) / 100,
        "productos": [_serializar_producto(producto) for producto in productos],
        "bolsillo": [_serializar_bolsillo(item) for item in bolsillo.values()],
        "dinero_maquina": [_serializar_bolsillo(item) for item in dinero_maquina.values()],
        "ultima_entrega": {
            "monedas": [_serializar_entrega_item(item) for item in ultima_entrega["monedas"]],
            "billetes": [_serializar_entrega_item(item) for item in ultima_entrega["billetes"]],
            "productos": [_serializar_entrega_item(item) for item in ultima_entrega["productos"]],
        },
        "cliente_productos": [_serializar_entrega_item(item) for item in cliente_productos],
    }


def cambiar_cantidad_bolsillo(id_dinero, delta):
    global ultimo_mensaje
    item = _item_bolsillo(id_dinero)
    if item is None:
        ultimo_mensaje = "Dinero no valido."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    item["cantidad"] = max(0, item["cantidad"] + delta)
    ultimo_mensaje = f"Tu bolsillo ahora tiene {item['cantidad']} de {item['nombre']}."
    return {"ok": True, "estado": obtener_estado()}


def insertar_desde_bolsillo(id_dinero, tipo_ranura):
    global saldo_maquina_centimos, ultimo_mensaje
    item = _item_bolsillo(id_dinero)
    if item is None:
        ultimo_mensaje = "Dinero no valido."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    if item["cantidad"] <= 0:
        ultimo_mensaje = f"No tienes {item['nombre']} disponible."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    if item["tipo"] != tipo_ranura:
        ultimo_mensaje = f"Ese {item['tipo']} no entra por la ranura de {tipo_ranura}."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    normalized_id = _normalize_dinero_id(id_dinero)
    if normalized_id is None or normalized_id not in dinero_maquina:
        ultimo_mensaje = "Dinero no valido."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    item["cantidad"] -= 1
    dinero_maquina[normalized_id]["cantidad"] += 1
    saldo_maquina_centimos += item["valor_centimos"]
    _limpiar_entregas()
    ultimo_mensaje = f"Se recibio {item['nombre']}."
    return {"ok": True, "estado": obtener_estado()}


def calcular_vuelto(vuelto_centimos):
    restante = vuelto_centimos
    vuelto_entregado = {}
    dinero_ordenado = sorted(
        dinero_maquina.values(),
        key=lambda item: item["valor_centimos"],
        reverse=True,
    )

    for item in dinero_ordenado:
        if restante <= 0:
            break
        cantidad_necesaria = restante // item["valor_centimos"]
        cantidad_disponible = item["cantidad"]
        cantidad_a_usar = min(cantidad_necesaria, cantidad_disponible)
        if cantidad_a_usar > 0:
            vuelto_entregado[item["id"]] = cantidad_a_usar
            restante -= item["valor_centimos"] * cantidad_a_usar

    if restante == 0:
        return vuelto_entregado
    return None


def _descomponer_entrega(vuelto_entregado):
    monedas = []
    billetes = []

    for id_dinero, cantidad in vuelto_entregado.items():
        item = dinero_maquina[id_dinero]
        dato = {
            "nombre": item["nombre"],
            "imagen": item["imagen"],
            "cantidad": cantidad,
        }
        if item["tipo"] == "billete":
            billetes.append(dato)
        else:
            monedas.append(dato)

    return {"monedas": monedas, "billetes": billetes}


def comprar_producto(codigo):
    global saldo_maquina_centimos, ultimo_mensaje, ultima_entrega
    _limpiar_entregas()

    if len(codigo) != 2:
        ultimo_mensaje = "El producto se selecciona con dos digitos."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    producto = _buscar_producto(codigo)
    if producto is None:
        ultimo_mensaje = "Codigo no valido."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    if producto["stock"] <= 0:
        ultimo_mensaje = f"{producto['nombre']} agotado."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    if saldo_maquina_centimos < producto["precio_centimos"]:
        falta = producto["precio_centimos"] - saldo_maquina_centimos
        ultimo_mensaje = f"Saldo insuficiente. Faltan {mostrar_soles(falta)}."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    pago_centimos = saldo_maquina_centimos
    vuelto_centimos = pago_centimos - producto["precio_centimos"]
    vuelto_entregado = calcular_vuelto(vuelto_centimos)
    if vuelto_entregado is None:
        ultimo_mensaje = "La maquina no tiene dinero suficiente para dar vuelto."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    producto["stock"] -= 1
    for id_dinero, cantidad in vuelto_entregado.items():
        dinero_maquina[id_dinero]["cantidad"] -= cantidad

    saldo_maquina_centimos = 0
    entrega_vuelto = _descomponer_entrega(vuelto_entregado)
    ultima_entrega = {
        "monedas": entrega_vuelto["monedas"],
        "billetes": entrega_vuelto["billetes"],
        "productos": [
            {
                "nombre": producto["nombre"],
                "imagen": producto["imagen"],
                "cantidad": 1,
            }
        ],
    }
    ultimo_mensaje = (
        f"Compra exitosa: {producto['nombre']}. "
        f"Vuelto {mostrar_soles(vuelto_centimos)}."
    )
    response = {
        "ok": True,
        "producto_entregado": {
            "codigo": producto["codigo"],
            "imagen": producto["imagen"],
            "nombre": producto["nombre"],
            "precio_centimos": producto["precio_centimos"],
        },
        "pago_centimos": pago_centimos,
        "vuelto_centimos": vuelto_centimos,
        "estado": obtener_estado(),
    }
    return response


def recoger_entrega():
    global ultima_entrega, ultimo_mensaje

    if not ultima_entrega["monedas"] and not ultima_entrega["billetes"]:
        ultimo_mensaje = "No hay cambio para recoger."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    for entrega in ultima_entrega["monedas"] + ultima_entrega["billetes"]:
        for item in bolsillo.values():
            if item["imagen"] == entrega["imagen"] or item["nombre"] == entrega["nombre"]:
                item["cantidad"] += entrega["cantidad"]
                break

    ultima_entrega["monedas"] = []
    ultima_entrega["billetes"] = []
    ultimo_mensaje = "Cambio recogido en tu bolsillo."
    return {"ok": True, "estado": obtener_estado()}


def recoger_producto():
    global ultimo_mensaje

    if not ultima_entrega["productos"]:
        ultimo_mensaje = "No hay producto para guardar en la canasta."
        return {"ok": False, "error": ultimo_mensaje, "estado": obtener_estado()}

    for entrega in ultima_entrega["productos"]:
        _agregar_a_cliente_productos(entrega)

    ultima_entrega["productos"] = []
    ultimo_mensaje = "Producto guardado en tu canasta."
    return {"ok": True, "estado": obtener_estado()}
