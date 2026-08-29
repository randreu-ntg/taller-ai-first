"""Tests de la política de orden de descuentos: porcentaje antes de monto fijo."""

from carrito.descuentos import total_con_descuentos
from carrito.dinero import porcentaje
from carrito.modelo import Cupon, Linea, Pedido, Producto


def _pedido_con_dos_cupones() -> Pedido:
    producto = Producto(sku="SKU-1", nombre="Producto de prueba", precio=10_000)
    return Pedido(
        numero=999,
        lineas=[Linea(producto=producto, cantidad=1)],
        cupones=[
            Cupon(codigo="PORC10", tipo="porcentaje", valor=10),
            Cupon(codigo="VALE2000", tipo="monto", valor=2_000),
        ],
    )


def test_cupon_porcentual_se_aplica_antes_que_el_vale_de_monto_fijo():
    """Según el README: primero el cupón porcentual, luego el vale de monto fijo."""
    pedido = _pedido_con_dos_cupones()

    subtotal = 10_000
    esperado_tras_porcentaje = subtotal - porcentaje(subtotal, 10)  # 9_000
    esperado_final = esperado_tras_porcentaje - 2_000  # 7_000

    assert total_con_descuentos(pedido) == esperado_final
