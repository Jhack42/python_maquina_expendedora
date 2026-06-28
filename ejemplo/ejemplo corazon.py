print("====================")
print("Maquinita de comidas")
print("====================")

saldo = 0
opcion = "SI"

productos = {
    1: {"nombre": "Chocolate", "precio": 200},
    2: {"nombre": "Caramandunga", "precio": 300},
    3: {"nombre": "Galleta", "precio": 100}
}

casilleros = {
    "1": {"producto_id": 1, "stock": 4},
    "2": {"producto_id": 2, "stock": 5},
    "3": {"producto_id": 3, "stock": 5}
}

dinero_categoria = {
    1: {"id_dinero_categoria": 1, "nombre": "billete"},
    2: {"id_dinero_categoria": 2, "nombre": "moneda"}
}

dinero = {
    1: {"id_dinero": 1, "valor": 0.10, "dinero_categoria_id": 2, "cantidad": 10},
    2: {"id_dinero": 2, "valor": 0.20, "dinero_categoria_id": 2, "cantidad": 10},
    3: {"id_dinero": 3, "valor": 0.50, "dinero_categoria_id": 2, "cantidad": 10},
    4: {"id_dinero": 4, "valor": 1.00, "dinero_categoria_id": 2, "cantidad": 10},
    5: {"id_dinero": 5, "valor": 2.00, "dinero_categoria_id": 2, "cantidad": 10},
    6: {"id_dinero": 6, "valor": 5.00, "dinero_categoria_id": 2, "cantidad": 10},
    7: {"id_dinero": 7, "valor": 10.00, "dinero_categoria_id": 1, "cantidad": 10},
    8: {"id_dinero": 8, "valor": 20.00, "dinero_categoria_id":  1, "cantidad": 10},
    9: {"id_dinero": 9, "valor": 50.00, "dinero_categoria_id": 1, "cantidad": 10},
    10: {"id_dinero": 10, "valor": 100.00, "dinero_categoria_id": 1, "cantidad": 10},
    11: {"id_dinero": 11, "valor": 200.00, "dinero_categoria_id": 1, "cantidad": 10}
}


def mostrar_soles(cantidad_centimos):
    return "S/. {:.2f}".format(cantidad_centimos / 100)


def convertir_a_centimos(monto):
    return int(round(monto * 100))


def obtener_nombre_dinero(datos_dinero):
    categoria_id = datos_dinero["dinero_categoria_id"]
    categoria = dinero_categoria[categoria_id]["nombre"]
    return categoria + " de " + mostrar_soles(convertir_a_centimos(datos_dinero["valor"]))


def buscar_dinero_por_valor(valor_centimos):
    for id_dinero, datos_dinero in dinero.items():
        if convertir_a_centimos(datos_dinero["valor"]) == valor_centimos:
            return id_dinero

    return None


def calcular_vuelto(vuelto):
    vuelto_entregado = {}
    dinero_ordenado = sorted(
        dinero.items(),
        key=lambda item: item[1]["valor"],
        reverse=True
    )

    for id_dinero, datos_dinero in dinero_ordenado:
        valor_centimos = convertir_a_centimos(datos_dinero["valor"])
        cantidad_necesaria = vuelto // valor_centimos
        cantidad_disponible = datos_dinero["cantidad"]
        cantidad_a_usar = min(cantidad_necesaria, cantidad_disponible)

        if cantidad_a_usar > 0:
            vuelto_entregado[id_dinero] = cantidad_a_usar
            vuelto -= valor_centimos * cantidad_a_usar

    if vuelto == 0:
        return vuelto_entregado
    else:
        return None


print("===========================")
print("Dinero disponible en maquina")
print("===========================")

for id_dinero, datos_dinero in dinero.items():
    print(obtener_nombre_dinero(datos_dinero), ":", datos_dinero["cantidad"])

while opcion == "SI":
    print("==============================")
    print("Valores aceptados")
    print("==============================")

    for datos_dinero in dinero.values():
        print("-", obtener_nombre_dinero(datos_dinero))

    monto = float(input("Ingrese moneda o billete en soles: "))
    monto_centimos = convertir_a_centimos(monto)
    id_dinero_ingresado = buscar_dinero_por_valor(monto_centimos)

    if id_dinero_ingresado is not None:
        saldo += monto_centimos
        dinero[id_dinero_ingresado]["cantidad"] += 1
        print("Su saldo es de:", mostrar_soles(saldo))
    else:
        print("Valor no aceptado por la maquina")

    opcion = input("Desea seguir ingresando dinero? (SI/NO): ").upper()

print("Saldo total:", mostrar_soles(saldo))

print("======================")
print("Productos disponibles")
print("======================")

for codigo, datos in casilleros.items():

    producto_id = datos["producto_id"]

    nombre = productos[producto_id]["nombre"]

    precio = productos[producto_id]["precio"]

    stock = datos["stock"]

    print(codigo, "=", nombre,
          "| precio:", mostrar_soles(precio),
          "| stock:", stock)

seleccion = input("Escriba el numero: ")

if seleccion in casilleros:

    producto_id = casilleros[seleccion]["producto_id"]

    nombre = productos[producto_id]["nombre"]

    precio = productos[producto_id]["precio"]

    stock = casilleros[seleccion]["stock"]

    if stock > 0:

        if saldo >= precio:

            vuelto = saldo - precio
            vuelto_entregado = calcular_vuelto(vuelto)

            if vuelto_entregado is not None:
                casilleros[seleccion]["stock"] -= 1

                for id_dinero, cantidad in vuelto_entregado.items():
                    dinero[id_dinero]["cantidad"] -= cantidad

                print("===========================")
                print("Inicia despacho de producto")
                print("===========================")

                print("Producto:", nombre)

                if vuelto > 0:
                    print("===========================")
                    print("Vuelto entregado")
                    print("===========================")

                    for id_dinero, cantidad in vuelto_entregado.items():
                        print(cantidad, "x", obtener_nombre_dinero(dinero[id_dinero]))

                print("Saldo restante:", mostrar_soles(0))
            else:
                print("La maquina no tiene dinero suficiente para dar vuelto")
                print("Operacion cancelada")

        else:
            print("Saldo insuficiente")

    else:
        print("Producto agotado")

else:
    print("Numero no valido")

print("===========================")
print("Actualizacion de productos")
print("===========================")

for codigo, datos in casilleros.items():

    producto_id = datos["producto_id"]

    nombre = productos[producto_id]["nombre"]

    stock = datos["stock"]

    print(codigo, "=", nombre,
          "| stock:", stock)

print("===========================")
print("Dinero actualizado en maquina")
print("===========================")

for id_dinero, datos_dinero in dinero.items():
    print(obtener_nombre_dinero(datos_dinero), ":", datos_dinero["cantidad"])