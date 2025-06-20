import pytest
from datetime import datetime, timedelta
from app.cupones import Cupon, CuponInvalidoError

def get_fecha_futura():
    """Helper para obtener una fecha futura válida"""
    return (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

def get_fecha_pasada():
    """Helper para obtener una fecha pasada"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def test_cupon_valido():
    cupon = Cupon("TEST10", 10, get_fecha_futura())
    es_valido, mensaje = cupon.validar(100)
    assert es_valido
    assert mensaje == "Cupón válido"

def test_cupon_expirado():
    cupon = Cupon("TEST10", 10, get_fecha_pasada())
    es_valido, mensaje = cupon.validar(100)
    assert not es_valido
    assert "expirado" in mensaje.lower()

def test_monto_minimo_no_alcanzado():
    cupon = Cupon("TEST10", 10, get_fecha_futura(), min_compra=100)
    es_valido, mensaje = cupon.validar(50)
    assert not es_valido
    assert "mínimo" in mensaje.lower()

def test_aplicar_descuento_exitoso():
    cupon = Cupon("TEST10", 10, get_fecha_futura())
    monto_final = cupon.aplicar_descuento(100)
    assert monto_final == 90

def test_aplicar_descuento_con_maximo():
    cupon = Cupon("TEST20", 20, get_fecha_futura(), max_descuento=15)
    monto_final = cupon.aplicar_descuento(100)
    assert monto_final == 85  # Descuento máximo de 15

def test_aplicar_descuento_cupon_invalido():
    cupon = Cupon("TEST10", 10, get_fecha_pasada())
    with pytest.raises(CuponInvalidoError):
        cupon.aplicar_descuento(100)

# Test de regresión
def test_regresion_descuento_maximo():
    """
    Este test demuestra una regresión donde el descuento máximo no se aplica correctamente
    cuando el monto es muy alto
    """
    cupon = Cupon("TEST20", 20, get_fecha_futura(), max_descuento=100)
    monto_final = cupon.aplicar_descuento(1000)
    # El descuento debería ser máximo 100, por lo que el monto final debería ser 900
    assert monto_final == 900, "Regresión detectada: el descuento máximo no se está aplicando correctamente" 