from flask import Flask, request, jsonify
from .cupones import CUPONES, CuponInvalidoError

app = Flask(__name__)

@app.route("/api/cupones/validar", methods=["POST"])
def validar_cupon():
    data = request.get_json()
    
    if not data or "codigo" not in data or "monto" not in data:
        return jsonify({
            "error": "Se requiere código de cupón y monto"
        }), 400
    
    codigo = data["codigo"]
    monto = float(data["monto"])
    
    if codigo not in CUPONES:
        return jsonify({
            "error": "Cupón no encontrado"
        }), 404
    
    cupon = CUPONES[codigo]
    es_valido, mensaje = cupon.validar(monto)
    
    return jsonify({
        "codigo": codigo,
        "es_valido": es_valido,
        "mensaje": mensaje
    })

@app.route("/api/cupones/aplicar", methods=["POST"])
def aplicar_cupon():
    data = request.get_json()
    
    if not data or "codigo" not in data or "monto" not in data:
        return jsonify({
            "error": "Se requiere código de cupón y monto"
        }), 400
    
    codigo = data["codigo"]
    monto = float(data["monto"])
    
    if codigo not in CUPONES:
        return jsonify({
            "error": "Cupón no encontrado"
        }), 404
    
    cupon = CUPONES[codigo]
    
    try:
        monto_final = cupon.aplicar_descuento(monto)
        return jsonify({
            "codigo": codigo,
            "monto_original": monto,
            "monto_final": monto_final,
            "descuento": monto - monto_final
        })
    except CuponInvalidoError as e:
        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(debug=True) 