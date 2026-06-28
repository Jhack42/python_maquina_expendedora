maquina_saldo = 0
saldo_cliente_10_centimos_sol = 10
saldo_cliente_20_centimos_sol = 10
saldo_cliente_50_centimos_sol = 10
saldo_cliente_1_sol = 10
saldo_cliente_2_sol = 10
saldo_cliente_5_sol = 10
saldo_cliente_10_sol = 10
saldo_cliente_20_sol = 10
saldo_cliente_50_sol = 10
saldo_cliente_100_sol = 10
saldo_cliente_200_sol = 10
opcion = "SI"

vuelto = 0
cliente_productos = []
productos = {
    1: {"nombre": "Agua Cielo", "precio": 2, "img": "img/productos/agua_cielo.png"},
    2: {"nombre": "Coca cola", "precio": 3, "img": "img/productos/coca_cola.png"},
    3: {"nombre": "Sublime", "precio": 2, "img": "img/productos/chocolate_sublime.png"},
    4: {"nombre": "Cuates", "precio": 3.5, "img": "img/productos/cuates.png"},
    5: {"nombre": "Galleta Soda", "precio": 2.2, "img": "img/productos/galleta_soda.png"},
    6: {"nombre": "Inca Cola", "precio": 4.5, "img": "img/productos/inca_cola.png"},
    7: {"nombre": "Papitas Lays", "precio": 4, "img": "img/productos/papitas_lays.png"},
    8: {"nombre": "karamanduka", "precio": 3, "img": "img/productos/karamanduka.png"}
}

casilleros = {
    "1": {"producto_id": 1, "stock": 4},
    "2": {"producto_id": 2, "stock": 5},
    "3": {"producto_id": 3, "stock": 5},
    "4": {"producto_id": 4, "stock": 7},
    "5": {"producto_id": 5, "stock": 6},
    "6": {"producto_id": 6, "stock": 5},
    "7": {"producto_id": 7, "stock": 7},
    "9": {"producto_id": 8, "stock": 5}
}

dinero_categoria = {
    1: {"id_dinero_categoria": 1, "nombre": "billete"},
    2: {"id_dinero_categoria": 2, "nombre": "moneda"}
}

dinero = {
    1: {"id_dinero": 1, "valor": 0.10, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/10_centimos.png"},
    2: {"id_dinero": 2, "valor": 0.20, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/20_centimos.png"},
    3: {"id_dinero": 3, "valor": 0.50, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/50_centimos.png"},
    4: {"id_dinero": 4, "valor": 1.00, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/1_sol.png"},
    5: {"id_dinero": 5, "valor": 2.00, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/2_soles.png"},
    6: {"id_dinero": 6, "valor": 5.00, "dinero_categoria_id": 2, "cantidad": 10, "img": "img/monedas/5_soles.png"},
    7: {"id_dinero": 7, "valor": 10.00, "dinero_categoria_id": 1, "cantidad": 10, "img": "img/billetes/10_soles.jpg"},
    8: {"id_dinero": 8, "valor": 20.00, "dinero_categoria_id": 1, "cantidad": 10, "img": "img/billetes/20_soles.jpg"},
    9: {"id_dinero": 9, "valor": 50.00, "dinero_categoria_id": 1, "cantidad": 10, "img": "img/billetes/50_soles.jpg"},
    10: {"id_dinero": 10, "valor": 100.00, "dinero_categoria_id": 1, "cantidad": 10, "img": "img/billetes/100_soles.jpg"},
    11: {"id_dinero": 11, "valor": 200.00, "dinero_categoria_id": 1, "cantidad": 10, "img": "img/billetes/200_soles.jpg"}
}