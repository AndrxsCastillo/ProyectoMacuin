from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, send_file
import requests
from datetime import datetime
import io

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        api_url = current_app.config['API_URL']
        
        login_data = {'username': email, 'password': password}
        
        try:
            response = requests.post(f"{api_url}/token", data=login_data)
            if response.status_code == 200:
                token_info = response.json()
                # ¡Magia! Guardamos el token en la sesión del navegador
                session['token'] = token_info.get('access_token')
                flash("¡Inicio de sesión exitoso!", "success")
                return redirect(url_for('main.inventario'))
            else:
                flash("Correo o contraseña incorrectos", "danger")
        except Exception as e:
            flash(f"Error de conexión con la API: {str(e)}", "danger")

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('token', None) # Borramos el token al salir
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('main.login'))

# === CAMBIO: De /dashboard a /inventario ===
@main.route('/inventario')
def inventario():
    # Protegemos la ruta: si no hay token, lo regresamos al login
    if 'token' not in session:
        flash("Por favor, inicia sesión para acceder al panel.", "warning")
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']
    
    try:
        # Hacemos una petición GET a FastAPI para traer el catálogo
        response = requests.get(f"{api_url}/autopartes/")
        if response.status_code == 200:
            autopartes = response.json()
        else:
            autopartes = []
            flash("No se pudo cargar el inventario.", "danger")
    except Exception as e:
        autopartes = []
        flash(f"Error conectando con la API Central: {str(e)}", "danger")

    # === CAMBIO: Ahora carga inventario.html en lugar de dashboard.html ===
    return render_template('inventario.html', autopartes=autopartes, now=datetime.now())

@main.route('/autopartes/nueva', methods=['GET', 'POST'])
def nueva_autoparte():
    if 'token' not in session:
        flash("Por favor, inicia sesión.", "warning")
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']

    if request.method == 'POST':
        # La lógica de guardar se queda exactamente igual
        nueva_pieza = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion'),
            "categoria_id": int(request.form.get('categoria_id')), # Ahora vendrá del select
            "marca": request.form.get('marca'),
            "precio": float(request.form.get('precio')),
            "stock_inicial": int(request.form.get('stock_inicial')),
            "stock_minimo": int(request.form.get('stock_minimo')),
            "activo": True
        }
        try:
            response = requests.post(f"{api_url}/autopartes/", json=nueva_pieza)
            if response.status_code == 200:
                flash("¡Autoparte registrada con éxito!", "success")
                return redirect(url_for('main.inventario'))
            else:
                flash(f"Error de la API: {response.text}", "danger")
        except Exception as e:
            flash(f"Error de conexión: {str(e)}", "danger")

    # === NUEVO CÓDIGO PARA EL GET ===
    # Si apenas va a abrir el formulario, pedimos las categorías
    try:
        cat_response = requests.get(f"{api_url}/categorias/")
        if cat_response.status_code == 200:
            lista_categorias = cat_response.json()
        else:
            lista_categorias = []
    except Exception:
        lista_categorias = []

    # Le pasamos la lista de categorías al HTML
    return render_template('nueva_autoparte.html', categorias=lista_categorias)

@main.route('/autopartes/editar/<int:id>', methods=['GET', 'POST'])
def editar_autoparte(id):
    if 'token' not in session:
        flash("Por favor, inicia sesión.", "warning")
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']

    if request.method == 'POST':
        # Recolectamos los datos actualizados del formulario, incluyendo el stock
        pieza_actualizada = {
            "nombre": request.form.get('nombre'),
            "descripcion": request.form.get('descripcion'),
            "categoria_id": int(request.form.get('categoria_id')),
            "marca": request.form.get('marca'),
            "precio": float(request.form.get('precio')),
            "stock_actual": int(request.form.get('stock_actual') or 0), # NUEVO
            "stock_minimo": int(request.form.get('stock_minimo') or 0), # NUEVO
            "activo": True
        }
        
        try:
            # Hacemos una petición PUT (Actualizar) a FastAPI
            response = requests.put(f"{api_url}/autopartes/{id}", json=pieza_actualizada)
            
            if response.status_code == 200:
                flash("¡Autoparte e inventario actualizados con éxito!", "success")
                return redirect(url_for('main.inventario'))
            else:
                flash(f"Error al actualizar: {response.text}", "danger")
        except Exception as e:
            flash(f"Error de conexión: {str(e)}", "danger")

    # === LÓGICA GET (Mostrar el formulario pre-llenado) ===
    try:
        # 1. Pedimos los datos actuales de la pieza (y su inventario)
        pieza_response = requests.get(f"{api_url}/autopartes/{id}")
        if pieza_response.status_code == 200:
            pieza_actual = pieza_response.json()
        else:
            flash("No se encontró la autoparte.", "danger")
            return redirect(url_for('main.inventario'))

        # 2. Pedimos las categorías para llenar el <select>
        cat_response = requests.get(f"{api_url}/categorias/")
        categorias = cat_response.json() if cat_response.status_code == 200 else []
        
    except Exception as e:
        flash(f"Error de conexión: {str(e)}", "danger")
        return redirect(url_for('main.inventario'))

    # Le pasamos la pieza y las categorías al HTML
    return render_template('editar_autoparte.html', pieza=pieza_actual, categorias=categorias)

@main.route('/autopartes/borrar/<int:id>', methods=['POST'])
def borrar_autoparte(id):
    if 'token' not in session:
        flash("Por favor, inicia sesión.", "warning")
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']
    
    try:
        # Hacemos la petición DELETE a FastAPI
        response = requests.delete(f"{api_url}/autopartes/{id}")
        
        if response.status_code == 200:
            flash("¡Autoparte eliminada permanentemente del catálogo!", "success")
        else:
            flash(f"No se pudo eliminar: {response.text}", "danger")
    except Exception as e:
        flash(f"Error de conexión con la API: {str(e)}", "danger")

    # Sea cual sea el resultado, regresamos al usuario al dashboard
    return redirect(url_for('main.inventario'))

@main.route('/pedidos')
def pedidos():
    if 'token' not in session:
        return redirect(url_for('main.login'))
        
    api_url = current_app.config['API_URL']
    try:
        # Pedimos la lista global de pedidos a FastAPI
        response = requests.get(f"{api_url}/pedidos/")
        lista_pedidos = response.json() if response.status_code == 200 else []
    except Exception as e:
        lista_pedidos = []
        flash(f"Error conectando con la API: {str(e)}", "danger")
        
    return render_template('pedidos.html', pedidos=lista_pedidos)

@main.route('/pedidos/estatus/<int:id>', methods=['POST'])
def cambiar_estatus_pedido(id):
    if 'token' not in session:
        return redirect(url_for('main.login'))
        
    nuevo_estatus = request.form.get('estatus')
    api_url = current_app.config['API_URL']
    
    try:
        response = requests.put(f"{api_url}/pedidos/{id}/estatus", json={"estatus": nuevo_estatus})
        
        if response.status_code == 200:
            flash(f"El pedido #{id} ahora está marcado como {nuevo_estatus}.", "success")
        else:
            # Extraemos el mensaje de error específico que manda FastAPI
            error_data = response.json()
            mensaje_error = error_data.get("detail", "Error desconocido al actualizar la base de datos.")
            flash(f"No se pudo actualizar: {mensaje_error}", "danger")
            
    except Exception as e:
        flash("Error de conexión con el servidor central.", "danger")
        
    return redirect(url_for('main.pedidos'))

# ==========================================
# RUTAS DE GESTIÓN DE USUARIOS
# ==========================================
@main.route('/usuarios')
def usuarios():
    if 'token' not in session:
        return redirect(url_for('main.login'))
        
    api_url = current_app.config['API_URL']
    try:
        response = requests.get(f"{api_url}/usuarios/")
        lista_usuarios = response.json() if response.status_code == 200 else []
    except Exception as e:
        lista_usuarios = []
        flash("Error de conexión con la API.", "danger")
        
    return render_template('usuarios.html', usuarios=lista_usuarios)

@main.route('/usuarios/borrar/<int:id>', methods=['POST'])
def borrar_usuario(id):
    if 'token' not in session:
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']
    try:
        response = requests.delete(f"{api_url}/usuarios/{id}")
        if response.status_code == 200:
            flash("Usuario eliminado del sistema.", "success")
        else:
            flash("No se pudo eliminar el usuario.", "danger")
    except Exception as e:
        flash("Error de conexión.", "danger")

    return redirect(url_for('main.usuarios'))

@main.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if 'token' not in session:
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']

    if request.method == 'POST':
        try:
            # Recolectamos los datos del formulario
            nuevo_usuario = {
                "nombre": request.form.get('nombre'),
                "email": request.form.get('email'),
                "password": request.form.get('password'),
                "rol_id": int(request.form.get('rol_id')), # Puede que aquí esté fallando si no se selecciona nada
                "activo": True
            }
            
            # Enviamos el POST a FastAPI
            response = requests.post(f"{api_url}/usuarios/", json=nuevo_usuario)
            
            # Aceptamos 200 (OK) o 201 (Created)
            if response.status_code in [200, 201]:
                flash("Usuario creado exitosamente.", "success")
                return redirect(url_for('main.usuarios'))
            else:
                try:
                    # Intentamos leer el error como JSON
                    error_data = response.json()
                    if isinstance(error_data, list):
                        mensaje = error_data[0].get("msg", "Error de validación")
                    else:
                        mensaje = error_data.get("detail", "Error desconocido")
                    flash(f"Aviso de la API: {mensaje}", "warning")
                except Exception:
                    # SI NO ES JSON, IMPRIMIMOS EL TEXTO CRUDO Y EL CÓDIGO DE ESTADO
                    flash(f"Fallo en la Base de Datos (Status {response.status_code}): {response.text}", "danger")
                    
        except Exception as e:
            flash(f"Fallo interno en Flask: {str(e)}", "danger")

    # Si es GET, consultamos los roles para llenar el select del formulario
    try:
        response_roles = requests.get(f"{api_url}/roles/")
        roles = response_roles.json() if response_roles.status_code == 200 else []
    except:
        roles = []
        flash("No se pudieron cargar los roles.", "warning")

    return render_template('crear_usuario.html', roles=roles)

@main.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'token' not in session:
        return redirect(url_for('main.login'))

    api_url = current_app.config['API_URL']

    if request.method == 'POST':
        # 1. Recolectamos los datos básicos
        datos_actualizados = {
            "nombre": request.form.get('nombre'),
            "email": request.form.get('email'),
            "rol_id": int(request.form.get('rol_id')),
            "activo": request.form.get('activo') == 'on'  # Checkbox de estado
        }
        
        # 2. Solo enviamos la contraseña si el admin escribió una nueva
        nueva_password = request.form.get('password')
        if nueva_password and nueva_password.strip() != "":
            datos_actualizados["password"] = nueva_password

        try:
            # 3. Enviamos el PUT a FastAPI
            response = requests.put(f"{api_url}/usuarios/{id}", json=datos_actualizados)
            if response.status_code == 200:
                flash("Datos del usuario actualizados correctamente.", "success")
                return redirect(url_for('main.usuarios'))
            else:
                flash(f"Error al actualizar: {response.text}", "danger")
        except Exception as e:
            flash("Error de conexión con la API.", "danger")

    # Si es GET (cargar la pantalla), buscamos al usuario específico
    try:
        # Obtenemos todos los usuarios y filtramos por ID
        res_usuarios = requests.get(f"{api_url}/usuarios/")
        usuario_actual = next((u for u in res_usuarios.json() if u['id'] == id), None)
        
        # Obtenemos los roles para el select
        res_roles = requests.get(f"{api_url}/roles/")
        roles = res_roles.json() if res_roles.status_code == 200 else []
    except Exception:
        usuario_actual = None
        roles = []

    if not usuario_actual:
        flash("No se encontró la información del usuario.", "warning")
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', usuario=usuario_actual, roles=roles)

@main.route('/reportes')
def reportes():
    if 'token' not in session:
        return redirect(url_for('main.login'))
        
    api_url = current_app.config['API_URL']
    
    # Variables iniciales para las métricas superiores
    ingresos_totales = 0.0
    total_pedidos = 0
    alertas_stock = 0
    
    # NUEVO: Variable para guardar las categorías
    lista_categorias = []
    
    try:
        # 1. Calcular Ingresos y Pedidos
        req_pedidos = requests.get(f"{api_url}/pedidos/")
        if req_pedidos.status_code == 200:
            pedidos = req_pedidos.json()
            total_pedidos = len(pedidos)
            for pedido in pedidos:
                if pedido.get('estatus') in ['Recibido', 'Surtido', 'Enviado']:
                    ingresos_totales += float(pedido.get('total', 0))

        # 2. Alertas de Stock
        req_autopartes = requests.get(f"{api_url}/autopartes/")
        if req_autopartes.status_code == 200:
            autopartes = req_autopartes.json()
            for pieza in autopartes:
                stock_actual = int(pieza.get('stock_inicial', 0)) 
                stock_minimo = int(pieza.get('stock_minimo', 0))
                if stock_actual <= stock_minimo:
                    alertas_stock += 1
                    
        # 3. NUEVO: Traer las categorías reales para la lista desplegable
        req_categorias = requests.get(f"{api_url}/categorias/")
        if req_categorias.status_code == 200:
            lista_categorias = req_categorias.json()

    except Exception as e:
        flash(f"Error al calcular métricas en tiempo real: {str(e)}", "danger")

    metricas = {
        'ingresos': f"{ingresos_totales:,.2f}",
        'pedidos': total_pedidos,
        'alertas': alertas_stock
    }

    # Pasamos las métricas y AHORA TAMBIÉN las categorías a la vista
    return render_template('reportes.html', metricas=metricas, categorias=lista_categorias)

@main.route('/reportes/generar/<tipo>', methods=['GET'])
def generar_reporte(tipo):
    if 'token' not in session:
        return redirect(url_for('main.login'))

    # 1. Atrapamos los filtros que vienen del formulario HTML
    formato = request.args.get('formato', 'pdf')
    filtros = {'formato': formato}
    
    if tipo == 'ventas':
        filtros['fecha_inicio'] = request.args.get('fecha_inicio')
        filtros['fecha_fin'] = request.args.get('fecha_fin')
    elif tipo == 'inventario':
        filtros['categoria'] = request.args.get('categoria')
    elif tipo == 'usuarios':
        filtros['rol'] = request.args.get('rol')

    api_url = current_app.config['API_URL']
    
    try:
        # 2. Hacemos la petición a tu FastAPI Central para que construya el archivo
        response = requests.get(f"{api_url}/reportes/generar/{tipo}", params=filtros)
        
        if response.status_code == 200:
            # 3. Determinamos el tipo de archivo para que el navegador sepa qué descargar
            mimetypes = {
                'pdf': 'application/pdf',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            
            # 4. ¡La magia! Tomamos los bytes crudos de la API y forzamos la descarga
            return send_file(
                io.BytesIO(response.content),
                mimetype=mimetypes.get(formato, 'application/octet-stream'),
                as_attachment=True,
                download_name=f"macuin_reporte_{tipo}.{formato}"
            )
        else:
            # Si FastAPI marca un error (ej. 404), lo mostramos
            flash(f"Error de la API: {response.text}", "danger")
            
    except Exception as e:
        flash(f"Error de conexión con el motor de reportes: {str(e)}", "danger")

    # Si algo falla, lo regresamos a la pantalla de reportes
    return redirect(url_for('main.reportes'))
