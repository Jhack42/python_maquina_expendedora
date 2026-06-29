"""
Módulo de administración para la máquina expendedora.
Contiene funciones relacionadas con reportes, estado del admin y generación de boletas.
"""

from datetime import datetime
from pathlib import Path

# Importar datos y funciones base
from negocio import datos as datos_base
from negocio.funciones import (
    _normalizar_productos,
    _normalizar_dinero,
    mostrar_soles,
    dinero_maquina,
    productos,
    cliente_productos,
)

BASE_DIR = Path(__file__).resolve().parents[2]
REPORTES_DIR = BASE_DIR / "reportes"


def _crear_directorio_reportes():
    """Crea el directorio de reportes si no existe"""
    REPORTES_DIR.mkdir(parents=True, exist_ok=True)


def _formatear_fecha():
    """Formatea la fecha actual en formato legible"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def obtener_estado_admin():
    total_dinero_centimos = 0
    monedas_resumen = []
    billetes_resumen = []
    
    for item in sorted(dinero_maquina.values(), key=lambda x: x["valor_centimos"]):
        valor_total_centimos = item["cantidad"] * item["valor_centimos"]
        total_dinero_centimos += valor_total_centimos
        
        dato = {
            "nombre": item["nombre"],
            "valor": item["valor_centimos"] / 100,
            "cantidad": item["cantidad"],
            "total": valor_total_centimos / 100,
            "imagen": item.get("imagen", "")
        }
        
        if item["tipo"] == "billete":
            billetes_resumen.append(dato)
        else:
            monedas_resumen.append(dato)
    
    # Calcular total de productos
    total_productos = sum(p["stock"] for p in productos)
    
    return {
        "dinero_total": total_dinero_centimos / 100,
        "dinero_total_texto": mostrar_soles(total_dinero_centimos),
        "monedas": monedas_resumen,
        "billetes": billetes_resumen,
        "productos": [
            {
                "codigo": p["codigo"],
                "nombre": p["nombre"],
                "stock": p["stock"],
                "precio": p["precio_centimos"] / 100,
                "imagen": p.get("imagen", "")
            }
            for p in productos
        ],
        "total_productos": total_productos,
        "saldo_maquina_centimos": 0
    }


def generar_reporte_inventario(nombre_archivo="inventario.txt"):

    _crear_directorio_reportes()
    ruta = REPORTES_DIR / nombre_archivo
    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write("=" * 70 + "\n")
        archivo.write("REPORTE DE INVENTARIO DE PRODUCTOS\n")
        archivo.write("=" * 70 + "\n")
        archivo.write(f"Fecha: {_formatear_fecha()}\n\n")
        archivo.write(f"{'CÓDIGO':<8} {'PRODUCTO':<30} {'STOCK':<8} {'ORDEN':<6}\n")
        archivo.write("-" * 70 + "\n")
        
        for codigo_casillero, casillero in sorted(
            datos_base.casilleros.items(),
            key=lambda item: item[1].get("orden", 0),
        ):
            producto = datos_base.productos.get(casillero.get("producto_id"))
            if producto is None:
                continue
            archivo.write(
                f"{int(codigo_casillero):02d}       {producto['nombre']:<30} "
                f"{casillero.get('stock', 0):<8} {casillero.get('orden', 0):<6}\n"
            )
        
        archivo.write("-" * 70 + "\n")
        archivo.write("=" * 70 + "\n")
    
    return f"/reportes/{ruta.name}"


def generar_reporte_monedas(nombre_archivo="monedas.txt"):
    _crear_directorio_reportes()
    ruta = REPORTES_DIR / nombre_archivo
    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write("=" * 70 + "\n")
        archivo.write("REPORTE DE MONEDAS Y BILLETES EN LA MÁQUINA\n")
        archivo.write("=" * 70 + "\n")
        archivo.write(f"Fecha: {_formatear_fecha()}\n\n")
        
        # Separar monedas y billetes
        monedas_list = [item for item in sorted(dinero_maquina.values(), key=lambda x: x["valor_centimos"]) if item["tipo"] == "moneda"]
        billetes_list = [item for item in sorted(dinero_maquina.values(), key=lambda x: x["valor_centimos"]) if item["tipo"] == "billete"]
        
        # Reportar monedas
        archivo.write("\n--- MONEDAS ---\n")
        archivo.write(f"{'DENOMINACIÓN':<20} {'CANTIDAD':<12} {'TOTAL':<12}\n")
        archivo.write("-" * 70 + "\n")
        total_monedas = 0
        total_valor_monedas = 0
        for item in monedas_list:
            archivo.write(
                f"{item['nombre']:<20} {item['cantidad']:<12} S/ {(item['cantidad'] * item['valor_centimos'] / 100):>9.2f}\n"
            )
            total_monedas += item['cantidad']
            total_valor_monedas += item['cantidad'] * item['valor_centimos'] / 100
        
        archivo.write("-" * 70 + "\n")
        archivo.write(f"{'TOTAL MONEDAS':<20} {total_monedas:<12} S/ {total_valor_monedas:>9.2f}\n\n")
        
        # Reportar billetes
        archivo.write("--- BILLETES ---\n")
        archivo.write(f"{'DENOMINACIÓN':<20} {'CANTIDAD':<12} {'TOTAL':<12}\n")
        archivo.write("-" * 70 + "\n")
        total_billetes = 0
        total_valor_billetes = 0
        for item in billetes_list:
            archivo.write(
                f"{item['nombre']:<20} {item['cantidad']:<12} S/ {(item['cantidad'] * item['valor_centimos'] / 100):>9.2f}\n"
            )
            total_billetes += item['cantidad']
            total_valor_billetes += item['cantidad'] * item['valor_centimos'] / 100
        
        archivo.write("-" * 70 + "\n")
        archivo.write(f"{'TOTAL BILLETES':<20} {total_billetes:<12} S/ {total_valor_billetes:>9.2f}\n\n")
        
        # Resumen general
        archivo.write("=" * 70 + "\n")
        archivo.write("RESUMEN GENERAL\n")
        archivo.write("=" * 70 + "\n")
        archivo.write(f"Total de Monedas: {total_monedas} unidades - S/ {total_valor_monedas:.2f}\n")
        archivo.write(f"Total de Billetes: {total_billetes} unidades - S/ {total_valor_billetes:.2f}\n")
        archivo.write(f"TOTAL GENERAL: {total_monedas + total_billetes} unidades - S/ {total_valor_monedas + total_valor_billetes:.2f}\n")
        archivo.write("=" * 70 + "\n")
    
    return f"/reportes/{ruta.name}"


def generar_boleta_con_productos(items=None, pago_centimos=None, vuelto_centimos=None):
    if items is None:
        items = cliente_productos

    if pago_centimos is None:
        pago_centimos = 0
    if vuelto_centimos is None:
        vuelto_centimos = 0

    _crear_directorio_reportes()
    nombre_archivo = f"boleta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    ruta = REPORTES_DIR / nombre_archivo

    total_productos_centimos = 0

    with ruta.open("w", encoding="utf-8") as archivo:
        # Encabezado
        archivo.write("=" * 60 + "\n")
        archivo.write("BOLETA DE VENTA ELECTRÓNICA".center(60) + "\n")
        archivo.write("=" * 60 + "\n\n")

        archivo.write("RUC: 12345678901\n")
        archivo.write("Razón Social: MÁQUINA EXPENDEDORA DE PRODUCTOS S.A.C.\n")
        archivo.write("Dirección: Centro Operativo\n")
        archivo.write("Teléfono: (01) 1234567\n")
        archivo.write(f"Fecha: {_formatear_fecha()}\n")
        archivo.write(f"Boleta Nº: {datetime.now().strftime('%Y%m%d%H%M%S')}\n\n")

        archivo.write("-" * 60 + "\n")
        archivo.write(f"CLIENTE: {'NO IDENTIFICADO':<42} DNI/RUC: NO IDENTIFICADO\n")
        archivo.write("-" * 60 + "\n\n")

        archivo.write(f"{'ITEM':<6}{'DESCRIPCIÓN':<28}{'CANT':<6}{'PRECIO':>12}\n")
        archivo.write("-" * 60 + "\n")

        if not items:
            archivo.write("SIN PRODUCTOS\n")
        else:
            item_num = 1
            for producto in items:
                precio_unitario = producto.get("precio_centimos")
                if precio_unitario is None:
                    for prod in productos:
                        if prod["nombre"] == producto["nombre"]:
                            precio_unitario = prod["precio_centimos"]
                            break
                if precio_unitario is None:
                    continue

                cantidad = int(producto.get("cantidad", 1))
                total_centimos = precio_unitario * cantidad
                total_productos_centimos += total_centimos

                archivo.write(
                    f"{item_num:<6}{producto['nombre']:<28}{cantidad:<6}S/ {precio_unitario/100:>7.2f}\n"
                )
                item_num += 1

        archivo.write("-" * 60 + "\n")
        archivo.write(f"{'SUBTOTAL:':<50} S/ {total_productos_centimos/100:>8.2f}\n")
        archivo.write(f"{'IGV (18%):':<50} S/ {(total_productos_centimos * 0.18)/100:>8.2f}\n")
        archivo.write("=" * 60 + "\n")
        archivo.write(f"{'TOTAL A PAGAR:':<50} S/ {(total_productos_centimos * 1.18)/100:>8.2f}\n")
        archivo.write(f"{'PAGÓ:':<50} S/ {pago_centimos/100:>8.2f}\n")
        archivo.write(f"{'VUELTO:':<50} S/ {vuelto_centimos/100:>8.2f}\n")
        archivo.write("=" * 60 + "\n\n")

        archivo.write("GRACIAS POR SU COMPRA\n")
        archivo.write("Por favor, guarde su boleta para futuras consultas\n")
        archivo.write("Vuelva pronto - ¡Que disfrute sus productos!\n\n")
        archivo.write("=" * 60 + "\n")

    return f"/reportes/{ruta.name}"
