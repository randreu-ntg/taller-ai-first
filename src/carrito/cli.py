"""Línea de comandos del carrito."""

import argparse

from carrito.datos import pedido
from carrito.descuentos import PROMOCIONES
from carrito.precios import precio_linea
from carrito.resumen import resumen


def main():
    parser = argparse.ArgumentParser(prog="carrito")
    parser.add_argument("comando", choices=["total"])
    parser.add_argument("--pedido", type=int, required=True)
    parser.add_argument("--sin", action="append", choices=sorted(PROMOCIONES), default=[])
    parser.add_argument("--detalle", action="store_true")
    args = parser.parse_args()

    elegido = pedido(args.pedido)
    elegido.promociones = [p for p in elegido.promociones if p not in args.sin]
    if args.detalle:
        detalle = [
            (f"{linea.producto.nombre} x {linea.cantidad}", precio_linea(linea))
            for linea in elegido.lineas
        ]
        _imprimir_alineado(detalle)
        print("-")
    _imprimir_alineado(list(resumen(elegido).items()))


def _imprimir_alineado(lineas: list[tuple[str, int]]):
    """Imprime pares etiqueta/monto con el monto alineado a la derecha."""
    ancho_etiqueta = max(len(etiqueta) for etiqueta, _ in lineas)
    ancho_monto = max(len(str(monto)) for _, monto in lineas)
    for etiqueta, monto in lineas:
        print(f"{etiqueta:<{ancho_etiqueta}} {monto:>{ancho_monto}}")


if __name__ == "__main__":
    main()
