from typing import Dict, Optional, Tuple
from datetime import datetime

class CuponInvalidoError(Exception):
    pass

class Cupon:
    def __init__(self, codigo: str, descuento: float, fecha_expiracion: str, 
                 min_compra: float = 0, max_descuento: Optional[float] = None):
        self.codigo = codigo
        self.descuento = descuento  # Porcentaje de descuento (0-100)
        self.fecha_expiracion = datetime.strptime(fecha_expiracion, "%Y-%m-%d")
        self.min_compra = min_compra
        self.max_descuento = max_descuento

    def validar(self, monto: float) -> Tuple[bool, str]:
        """
        Valida si el cupón puede ser aplicado al monto dado.
        Retorna una tupla (es_valido, mensaje)
        """
        # Corregimos la validación de fecha para considerar todo el día de expiración
        fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_exp = self.fecha_expiracion.replace(hour=23, minute=59, second=59)
        
        if fecha_actual > fecha_exp:
            return False, "Cupón expirado"
        
        if monto < self.min_compra:
            return False, f"Monto mínimo de compra no alcanzado (${self.min_compra})"
        
        return True, "Cupón válido"

    def aplicar_descuento(self, monto: float) -> float:
        """
        Aplica el descuento al monto dado.
        Retorna el monto con descuento aplicado.
        """
        es_valido, mensaje = self.validar(monto)
        if not es_valido:
            raise CuponInvalidoError(mensaje)
        
        descuento = (self.descuento / 100) * monto
        
        if self.max_descuento is not None:
            descuento = min(descuento, self.max_descuento)
            
        return monto - descuento

# Base de datos simulada de cupones
CUPONES: Dict[str, Cupon] = {
    "BIENVENIDA": Cupon("BIENVENIDA", 10, "2024-12-31", min_compra=100),
    "PREMIUM": Cupon("PREMIUM", 20, "2024-12-31", min_compra=500, max_descuento=200),
} 