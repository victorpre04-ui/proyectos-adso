from flask import Flask, render_template_string, request, redirect, send_file
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)
ARCHIVO_DATOS = "inventario_datos.json"

# 👥 AQUI VAN LOS NOMBRES DE LOS TÉCNICOS 
LISTA_TECNICOS = [
    "Edinson Zuñiga",
    "Luis Carlos Saavedra",
    "Hely Fuquene contratista",
    "Otro"
]

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r') as f:
            return json.load(f)
    return {"productos": {}, "historial": []}

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(datos, f, indent=4)

# Diseño Premium con Alertas de Stock y Ajuste Manual Directo
HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Gestión ADSO - Inventario</title>
    <style>
        :root {
            --primary: #2b579a;
            --primary-dark: #1e3d6b;
            --success: #107c41;
            --danger: #ef4444;
            --bg: #f3f4f6;
            --card-bg: #ffffff;
            --text-main: #333333;
            --text-muted: #666666;
            --border: #e5e7eb;
        }

        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            background-color: var(--bg); 
            color: var(--text-main);
        }

        .navbar {
            background-color: var(--primary); color: white; padding: 15px 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex;
            justify-content: space-between; align-items: center;
        }

        .navbar h1 { margin: 0; font-size: 1.4rem; font-weight: 600; }

        /* Alertas de error del sistema */
        .alert {
            background-color: #fee2e2; border: 1px solid #fca5a5; color: #991b1b;
            padding: 12px 20px; border-radius: 8px; margin: 20px auto 0 auto;
            max-width: 1060px; font-weight: 600;
        }

        /* Sistema de Ventanas */
        .tabs-container {
            max-width: 1100px; margin: 20px auto 0 auto; padding: 0 20px; display: flex; gap: 10px;
        }

        .tab-button {
            background-color: #e5e7eb; color: var(--text-muted); padding: 12px 24px;
            border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: 600; font-size: 0.95rem;
        }

        .tab-button.active {
            background-color: var(--card-bg); color: var(--primary);
            border-top: 4px solid var(--primary); box-shadow: 0 -2px 6px rgba(0,0,0,0.05);
        }

        .container { max-width: 1100px; margin: 0 auto 30px auto; padding: 20px; }

        .window-content {
            display: none; background: var(--card-bg); padding: 25px;
            border-radius: 0 12px 12px 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid var(--border);
        }

        .window-content.active { display: block; }

        h2, h3 { margin-top: 0; color: var(--primary-dark); }
        h2 { border-bottom: 2px solid #f3f4f6; padding-bottom: 10px; margin-bottom: 20px; }

        label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }
        input[type="text"], input[type="number"], select, input[type="file"] { 
            padding: 10px 12px; width: 100%; box-sizing: border-box;
            margin-bottom: 15px; border: 1px solid var(--border); border-radius: 6px; 
            font-size: 0.95rem; background-color: #fafafa;
        }
        input:focus, select:focus { outline: none; border-color: var(--primary); background-color: #fff; box-shadow: 0 0 0 3px rgba(43,87,154,0.1); }

        .btn { 
            display: inline-flex; align-items: center; justify-content: center;
            background-color: var(--primary); color: white; padding: 10px 20px; 
            border: none; border-radius: 6px; cursor: pointer; font-weight: 600; text-decoration: none; 
        }
        .btn:hover { background-color: var(--primary-dark); }
        .btn-success { background-color: var(--success); }
        .btn-success:hover { background-color: #0b592e; }
        .btn-danger { background-color: var(--danger); padding: 6px 12px; }

        .fila-material { 
            background: #f9fafb; padding: 15px; border-radius: 8px; margin-bottom: 12px; 
            border: 1px dashed var(--border); display: grid; grid-template-columns: 3fr 1fr auto; align-items: end; gap: 15px;
        }

        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 12px 15px; border-bottom: 1px solid var(--border); }
        th { background-color: #f8fafc; color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; }
        
        .badge-cantidad { background-color: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 12px; font-weight: 700; }
        .badge-entrada { background-color: #dcfce7; color: #15803d; padding: 4px 8px; border-radius: 12px; font-weight: 600; }
        .badge-salida { background-color: #fee2e2; color: #b91c1c; padding: 4px 8px; border-radius: 12px; font-weight: 600; }
    </style>
    
    <script>
        function abrirVentana(evt, nombreVentana) {
    const contenidos = document.querySelectorAll(".window-content");
    contenidos.forEach(function(contenido) {
        contenido.classList.remove("active");
    });

    const botones = document.querySelectorAll(".tab-button");
    botones.forEach(function(boton) {
        boton.classList.remove("active");
    });

    document.getElementById(nombreVentana).classList.add("active");
    evt.currentTarget.classList.add("active");
}

        function agregarFilaSalida() {
            const contenedor = document.getElementById('contenedor-salidas');
            const nuevaFila = document.createElement('div');
            nuevaFila.className = 'fila-material';
            nuevaFila.innerHTML = `
                <div><input type="text" name="material[]" list="lista-articulos" placeholder="Escribe material..." required autocomplete="off"></div>
                <div><input type="number" name="cantidad[]" min="1" placeholder="Cant." required></div>
                <div><button type="button" class="btn btn-danger" onclick="this.parentElement.parentElement.remove()">✕</button></div>
            `;
            contenedor.appendChild(nuevaFila);
        }

        function agregarFilaEntrada() {
            const contenedor = document.getElementById('contenedor-entradas');
            const nuevaFila = document.createElement('div');
            nuevaFila.className = 'fila-material';
            nuevaFila.innerHTML = `
                <div><input type="text" name="material_in[]" list="lista-articulos" placeholder="Escribe material..." required autocomplete="off"></div>
                <div><input type="number" name="cantidad_in[]" min="1" placeholder="Cant." required></div>
                <div><button type="button" class="btn btn-danger" onclick="this.parentElement.parentElement.remove()">✕</button></div>
            `;
            contenedor.appendChild(nuevaFila);
        }
        function alternarTabla() {
            const cajaTabla = document.getElementById('contenedor-tabla-stock');
            if (cajaTabla.style.display === "none") {
                cajaTabla.style.display = "block";
            } else {
                cajaTabla.style.display = "none";
            }
        }
    </script>
</head>
<body>

    <div class="navbar">
        <h1>📦 Sistema Integral de Inventarios ADSO</h1>
        <span>Módulo Almacén</span>
    </div>

    <!-- NOTIFICACIONES DE ERROR POR STOCK INSUFICIENTE -->
    {% if error %}
    <div class="alert">
        ⚠️ {{ error }}
    </div>
    {% endif %}

    <div class="tabs-container">
        <button class="tab-button active" onclick="abrirVentana(event, 'ventana-stock')">📋 STOCK Y REPORTES</button>
        <button class="tab-button" onclick="abrirVentana(event, 'ventana-salidas')">📤 SALIDAS Y ENTREGAS</button>
        <button class="tab-button" onclick="abrirVentana(event, 'ventana-entradas')">📥 ENTRADAS Y DEVOLUCIONES</button>
    </div>

    <div class="container">
        
        <!-- 🖥️ VENTANA STOCK, REPORTES Y AJUSTE MANUAL -->
        <div id="ventana-stock" class="window-content active">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2>Existencias de Almacén en Tiempo Real</h2>
                <a href="/exportar-excel" class="btn" style="background-color: #107c41;">🟢 Exportar Cierre (.xlsx)</a>
            </div>
            
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 25px;">
                <!-- Carga de Excel Inicial -->
                <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                    <h4 style="margin: 0 0 10px 0;">📊 Importar desde Excel</h4>
                    <form action="/cargar-excel" method="post" enctype="multipart/form-data" style="display: flex; gap: 10px;">
                        <input type="file" name="archivo_excel" accept=".xlsx, .xls" required style="margin-bottom: 0;">
                        <button type="submit" class="btn btn-success">Cargar Archivo</button>
                    </form>
                </div>

                <!-- 🛠️ NUEVO: FORMULARIO DE AJUSTE MANUAL DIRECTO -->
                <div style="background: #fffbeb; padding: 15px; border-radius: 8px; border: 1px solid #fef3c7;">
                    <h4 style="margin: 0 0 10px 0; color: #b45309;">⚙️ Ajuste Manual Rápido</h4>
                    <form action="/ajuste-manual" method="post" style="display: flex; flex-direction: column; gap: 5px;">
                        <input type="text" name="material_ajuste" list="lista-articulos" placeholder="Selecciona material..." required autocomplete="off" style="margin-bottom: 5px; padding: 6px;">
                        <input type="number" name="nueva_cantidad" min="0" placeholder="Nueva Cantidad Física" required style="margin-bottom: 5px; padding: 6px;">
                        <button type="submit" class="btn" style="background-color: #d97706; padding: 6px; font-size: 0.85rem;">Corregir Stock</button>
                    </form>
                </div>
            </div>

            <button type="button" class="btn" style="background-color: #4b5563; margin-bottom: 15px;" onclick="alternarTabla()">
                👁️ Mostrar / Ocultar Tabla de Existencias
            </button>

            <div id="contenedor-tabla-stock">
                <table>
                    <thead>
                        <tr><th>Descripción de Artículo</th><th>Cantidad Actual</th></tr>
                    </thead>
                    <tbody>
                        {% for prod, cant in datos.productos.items() %}
                        <tr>
                            <td style="font-weight: 500;">{{ prod }}</td>
                            <td><span class="badge-cantidad">{{ cant }} unidades</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            </div>
            

        <!-- 🖥️ VENTANA 1: SALIDAS Y ENTREGAS -->
        <div id="ventana-salidas" class="window-content">
            <h2>📤 Registro de Entregas a Técnicos</h2>
            <form action="/movimiento" method="post">
                <input type="hidden" name="tipo_flujo" value="SALIDA">
                
                <label>Seleccione el Técnico Destinatario</label>
                <select name="responsable" required>
                    <option value="" disabled selected>-- Elegir Técnico --</option>
                    {% for tecnico in tecnicos %}
                        <option value="{{ tecnico }}">{{ tecnico }}</option>
                    {% endfor %}
                </select>
                
                <label>Proyecto / Destino / Obra</label>
                <input type="text" name="para_quien" placeholder="Ej. Instalación Casa Matriz" required>
                
                <label>Materiales a Retirar</label>
                <div id="contenedor-salidas">
                    <div class="fila-material">
                        <div><input type="text" name="material[]" list="lista-articulos" placeholder="Buscar material..." required autocomplete="off"></div>
                        <div><input type="number" name="cantidad[]" min="1" placeholder="Cant." required></div>
                        <div></div>
                    </div>
                </div>
                
                <button type="button" class="btn" style="background-color: #6b7280; font-size: 0.85rem;" onclick="agregarFilaSalida()">+ Agregar Ítem</button>
                <br><br>
                <button type="submit" class="btn" style="width: 100%; background-color: var(--primary-dark);">💾 Confirmar Salida de Almacén</button>
            </form>
        </div>

        <!-- 🖥️ VENTANA 2: ENTRADAS Y DEVOLUCIONES (INFLOW) -->
        <div id="ventana-entradas" class="window-content">
            <h2>📥 Cargue de Materiales y Devoluciones de Obra</h2>
            <form action="/movimiento" method="post">
                <input type="hidden" name="tipo_flujo" value="ENTRADA">
                
                <label>Motivo de Entrada al Almacén</label>
                <select name="para_quien" required>
                    <option value="ABASTECIMIENTO / COMPRAS">Abastecimiento General (Nueva Compra / Proveedor)</option>
                    <option value="DEVOLUCION DE OBRA">Devolución de Material Sobrante de Técnico</option>
                </select>

                <label>Técnico que entrega (Solo si aplica para devolución)</label>
                <select name="responsable">
                    <option value="PROVEEDOR / CENTRAL">N/A - Viene de Proveedor</option>
                    {% for tecnico in tecnicos %}
                        <option value="{{ tecnico }}">{{ tecnico }}</option>
                    {% endfor %}
                </select>
                
                <label>Materiales a Reingresar</label>
                <div id="contenedor-entradas">
                    <div class="fila-material">
                        <div><input type="text" name="material_in[]" list="lista-articulos" placeholder="Buscar material..." required autocomplete="off"></div>
                        <div><input type="number" name="cantidad_in[]" min="1" placeholder="Cant." required></div>
                        <div></div>
                    </div>
                </div>
                
                <button type="button" class="btn" style="background-color: #6b7280; font-size: 0.85rem;" onclick="agregarFilaEntrada()">+ Agregar Ítem</button>
                <br><br>
                <button type="submit" class="btn btn-success" style="width: 100%;">📥 Procesar Entrada e Incrementar Inventario</button>
            </form>
        </div>

        <!-- 📜 BITÁCORA GLOBAL -->
        <div class="window-content active" style="margin-top: 25px; padding-top: 15px;">
            <h3>📜 Historial Consolidado de Movimientos (Kárdex)</h3>
            <table>
                <thead>
                    <tr><th>Tipo</th><th>Material</th><th>Cant.</th><th>Responsable</th><th>Concepto / Destino</th></tr>
                </thead>
                <tbody>
                    {% for h in datos.historial %}
                    <tr>
                        <td>{% if h.tipo == 'SALIDA' %}<span class="badge-salida">OUTFLOW</span>{% else %}<span class="badge-entrada">INFLOW</span>{% endif %}</td>
                        <td style="font-weight: 500;">{{ h.material }}</td>
                        <td><strong>{{ h.cantidad }}</strong></td>
                        <td>{{ h.responsable }}</td>
                        <td><span style="color: var(--text-muted); font-size: 0.9rem;">{{ h.concepto }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

    </div>

    <datalist id="lista-articulos">
        {% for prod in datos.productos.keys() %}
            <option value="{{ prod }}"></option>
        {% endfor %}
    </datalist>

</body>
</html>
"""

@app.route('/')
def index():
    datos = cargar_datos()
    error = request.args.get('error')
    return render_template_string(HTML_BASE, datos=datos, tecnicos=LISTA_TECNICOS, error=error)

@app.route('/movimiento', methods=['POST'])
def movimiento():
    datos = cargar_datos()
    tipo_flujo = request.form.get('tipo_flujo')
    responsable = request.form.get('responsable', 'DESCONOCIDO')
    concepto = request.form.get('para_quien')
    
    if tipo_flujo == 'SALIDA':
        materiales = request.form.getlist('material[]')
        cantidades = request.form.getlist('cantidad[]')
    else:
        materiales = request.form.getlist('material_in[]')
        cantidades = request.form.getlist('cantidad_in[]')

    # 🛡️ VALIDACIÓN PREVIA (Evita que el stock quede en negativo si piden más de lo que hay)
    if tipo_flujo == 'SALIDA':
        for mat_raw, cant_str in zip(materiales, cantidades):
            if not mat_raw: continue
            material = mat_raw.strip().upper()
            try: cantidad = int(cant_str)
            except: continue
            
            stock_actual = datos["productos"].get(material, 0)
            if stock_actual < cantidad:
                return redirect(f"/?error=Stock insuficiente para '{material}'. Solicitado: {cantidad}, Disponible: {stock_actual}")

    # Procesamos los movimientos de forma segura
    for mat_raw, cant_str in zip(materiales, cantidades):
        if not mat_raw: continue
        try: cantidad = int(cant_str)
        except: continue
            
        material = mat_raw.strip().upper()
        
        if tipo_flujo == 'SALIDA':
            datos["productos"][material] -= cantidad
            datos["historial"].append({
                "tipo": "SALIDA", "material": material, "cantidad": cantidad,
                "responsable": responsable, "concepto": concepto
            })
        elif tipo_flujo == 'ENTRADA':
            if material in datos["productos"]:
                datos["productos"][material] += cantidad
            else:
                datos["productos"][material] = cantidad
                
            datos["historial"].append({
                "tipo": "ENTRADA", "material": material, "cantidad": cantidad,
                "responsable": responsable, "concepto": concepto
            })
            
    guardar_datos(datos)
    return redirect('/')

# 🛠️ RUTA NUEVA: PERMITE EDITAR EL STOCK A MANO DE FORMA DIRECTA
@app.route('/ajuste-manual', methods=['POST'])
def ajuste_manual():
    datos = cargar_datos()
    material = request.form.get('material_ajuste', '').strip().upper()
    try:
        nueva_cantidad = int(request.form.get('nueva_cantidad', 0))
    except:
        return redirect('/')

    if material in datos["productos"]:
        cantidad_anterior = datos["productos"][material]
        datos["productos"][material] = nueva_cantidad
        # Dejamos evidencia en el Kárdex de que se hizo una corrección de inventario
        datos["historial"].append({
            "tipo": "ENTRADA" if nueva_cantidad >= cantidad_anterior else "SALIDA",
            "material": material,
            "cantidad": abs(nueva_cantidad - cantidad_anterior),
            "responsable": "ADMINISTRADOR (AJUSTE)",
            "concepto": f"Corrección manual de existencias (Antes: {cantidad_anterior} -> Ahora: {nueva_cantidad})"
        })
        guardar_datos(datos)
    else:
        return redirect(f"/?error=El material '{material}' no existe en el catálogo.")
        
    return redirect('/')

@app.route('/cargar-excel', methods=['POST'])
def cargar_excel():
    datos = cargar_datos()
    file = request.files['archivo_excel']
    if file:
        try:
            excel_completo = pd.ExcelFile(file)
            for nombre_pestana in excel_completo.sheet_names:
                df = excel_completo.parse(nombre_pestana, header=2)
                df.columns = df.columns.str.strip()
                
                columnas_desc = [i for i, col in enumerate(df.columns) if "Descripcion" in str(col) or "Descripción" in str(col)]
                columnas_cant = [i for i, col in enumerate(df.columns) if "Cantidad" in str(col)]
                
                for idx_desc, idx_cant in zip(columnas_desc, columnas_cant):
                    for _, fila in df.iterrows():
                        val_material = fila.iloc[idx_desc]
                        val_cantidad = fila.iloc[idx_cant]
                        
                        if pd.isna(val_material) or pd.isna(val_cantidad) or str(val_material).strip() in ["Descripcion", "Descripción"]:
                            continue
                            
                        material = str(val_material).strip().upper()
                        try: cantidad = int(val_cantidad)
                        except: cantidad = 0
                            
                        if material in datos["productos"]:
                            datos["productos"][material] += cantidad
                        else:
                            datos["productos"][material] = cantidad
                            
            guardar_datos(datos)
        except Exception as e:
            print(f"Error: {e}")
    return redirect('/')

@app.route('/exportar-excel')
def exportar_excel():
    datos = cargar_datos()
    lista_productos = [{"Material o Artículo": prod, "Existencia Final (Saldo)": cant} for prod, cant in datos["productos"].items()]
    df = pd.DataFrame(lista_productos)
    if df.empty:
        df = pd.DataFrame(columns=["Material o Artículo", "Existencia Final (Saldo)"])
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"Cierre_Inventario_{fecha_hoy}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    return send_file(nombre_archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)