import customtkinter as ctk
import calendar
from datetime import datetime
from database import cargar_eventos
from tkinter import Toplevel
from tkcalendar import Calendar
from PIL import Image
from database import verificar_credenciales
from database import agregar_usuario 
from database import cambiar_tema_usuario
from database import obtener_tema_usuario


# Al inicio de tu archivo
modo_oscuro = True  # Variable global para recordar el modo
usuario_logueado = None


from PIL import Image
import customtkinter as ctk

def ventana_login():
    login = ctk.CTk()
    login.title("¡Bienvenido Ingeniero!")
    login.geometry("600x300")
    login.resizable(False, False)

    # Crear frame contenedor principal con dos columnas
    contenedor = ctk.CTkFrame(login)
    contenedor.pack(expand=True, fill="both", padx=10, pady=10)

    # === Columna izquierda: Imagen ===
    try:
        img = Image.open("logocuadrado.jpg")  # Cambia por tu imagen real
        img = img.resize((250, 250))  # Ajusta según el tamaño de tu logo
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 265))
        img_label = ctk.CTkLabel(contenedor, image=img_ctk, text="")
        img_label.grid(row=0, column=0, padx=10, pady=10)
    except Exception as e:
        print("Error cargando imagen:", e)

    # === Columna derecha: Formulario ===
    formulario = ctk.CTkFrame(contenedor)
    formulario.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    contenedor.grid_columnconfigure(1, weight=1)  # Para que el formulario se centre verticalmente

    # Contenido del formulario
    ctk.CTkLabel(formulario, text="Usuario").pack(pady=(20, 5))
    usuario_entry = ctk.CTkEntry(formulario)
    usuario_entry.pack()

    ctk.CTkLabel(formulario, text="Contraseña").pack(pady=(10, 5))
    contraseña_entry = ctk.CTkEntry(formulario, show="*")
    contraseña_entry.pack()

    mensaje_error = ctk.CTkLabel(formulario, text="", text_color="red")
    mensaje_error.pack()

    def verificar_credenciales_usuario():
        
        global usuario_logueado

        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()

        # Llamar a la función verificar_credenciales de la base de datos
        if verificar_credenciales(usuario, contraseña):
            usuario_logueado = usuario
            login.quit()
            login.destroy()  # Cerrar la ventana de login
            app = crear_interfaz()  # Crear la interfaz principal (tu aplicación)
            app.mainloop()  # Iniciar la aplicación
        else:
            mensaje_error.configure(text="Credenciales incorrectas")

    # Botón para iniciar sesión
    ctk.CTkButton(formulario, text="Iniciar sesión", command=verificar_credenciales_usuario).pack(pady=20)

    login.mainloop()




def crear_interfaz():
    global modo_oscuro
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  

    app = ctk.CTk()
    app.title("Calendario para DIB Hospital Angeles")
    app.geometry("1280x720")

    tema_guardado = obtener_tema_usuario(usuario_logueado)
    ctk.set_appearance_mode(tema_guardado)
    modo_oscuro = (tema_guardado == "dark")
    
    ctk.set_default_color_theme("blue")





    eventos = cargar_eventos() 



    horas= ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']

    def configventana():
        ventana = ctk.CTkToplevel()
        ventana.title("Configuración")
        ventana.geometry("400x400")
        ventana.grab_set()
        ventana.focus()

        titulo = ctk.CTkLabel(ventana, text="Agregar usuario", font=ctk.CTkFont(size=17))
        titulo.pack(padx=10, pady=5)

        entradau = ctk.CTkEntry(ventana, placeholder_text="Usuario")
        entradau.pack(padx=10, pady=5)

        entradac = ctk.CTkEntry(ventana, placeholder_text="Contraseña", show="*")
        entradac.pack(padx=10, pady=5)

        mensaje = ctk.CTkLabel(ventana, text="")
        mensaje.pack(pady=(5, 10))

        def guardar_nuevo_usuario():
            usuario = entradau.get().strip()
            contrasena = entradac.get().strip()

            if not usuario or not contrasena:
                mensaje.configure(text="Por favor ingrese usuario y contraseña", text_color="orange")
                return

            exito = agregar_usuario(usuario, contrasena)

            if exito:
                mensaje.configure(text="Usuario agregado correctamente", text_color="green")
                entradau.delete(0, "end")
                entradac.delete(0, "end")
            else:
                mensaje.configure(text="El usuario ya existe", text_color="red")

        guardu = ctk.CTkButton(ventana, text="Guardar usuario", width=40, command=guardar_nuevo_usuario)
        guardu.pack(padx=10, pady=5)

        def cambiar_tema():
            global modo_oscuro
            modo_oscuro = not modo_oscuro

            nuevo_tema = "dark" if modo_oscuro else "light"
            ctk.set_appearance_mode(nuevo_tema)
            theme_switch.configure(text="Modo Oscuro" if modo_oscuro else "Modo Claro")

            # Guardar el nuevo tema en la base de datos
            if usuario_logueado:
                cambiar_tema_usuario(usuario_logueado, nuevo_tema)

            app.after(100, app.update)

        theme_switch = ctk.CTkSwitch(
            master=ventana,
            text="Modo Oscuro" if modo_oscuro else "Modo Claro",
            command=cambiar_tema
        )
        theme_switch.pack(pady=10)

        if modo_oscuro:
            theme_switch.select()
        else:
            theme_switch.deselect()

    # === BARRA LATERAL ===
    sidebar = ctk.CTkFrame(app, width=200, corner_radius=10)
    sidebar.pack(side="left", fill="y", padx=5, pady=5)

    titulo = ctk.CTkLabel(sidebar, text="Filtrar eventos", font=ctk.CTkFont(size=17))
    titulo.pack(pady=20)

    prioridades = ["Alta", "Media", "Baja", "Todas"]

    mprioridad= ctk.CTkOptionMenu(master=sidebar, values=prioridades, command=lambda valor: print(f"Filtrar por: {valor}"))
    mprioridad.set("Por prioridad:")
    mprioridad.pack(pady=5, padx=10)

    categoria = ["Mantenimiento de equipo", "Capacitación", "Reunión", "Reporte de fallas", "Actividades administrativas", "Supervisión de servicio"]

    mcategoria = ctk.CTkOptionMenu(master=sidebar, values=categoria, command=lambda valor: print(f"Filtrar por: {valor}"))
    mcategoria.set("Por tipo de evento:")
    mcategoria.pack(pady=5, padx=10)

    ubicacion = ["Urgencias", "Unidad de cuidados intensivos","Quirófanos","Postoperatorio","Imagenología","Laboratorio clínico","Hemodiálisis","Hospitalización","Neonatología","Pediatría","Medicina familiar","Farmacia","Centro de esterilizacion","Rehabilitación y Fisioterapia","Banco de sangre","Patología","Gases medicinales","DIB"]

    mubicacion = ctk.CTkOptionMenu(master=sidebar, values=ubicacion, command=lambda valor: print(f"Filtrar por: {valor}"))
    mubicacion.set("Por ubicacion:")
    mubicacion.pack(pady=5, padx=10)

    responsable = ["Ingeniero Juan Hernandez", "Ingeniera Lorena Gilardi", "Ingeniero Sergio Velázquez", "Ingeniero Edgar Quilantán", "Ingeniero Gabriel Armadillo"]

    mresponsable = ctk.CTkOptionMenu(master=sidebar, values=responsable, command=lambda valor: print(f"Filtrar por: {valor}"))
    mresponsable.set("Por responsable:")
    mresponsable.pack(pady=5, padx=10)

    estado = ["Pendiente", "En curso", "Completado", "Cancelado"]

    mestado = ctk.CTkOptionMenu(master=sidebar, values=estado, command=lambda valor: print(f"Filtrar por: {valor}"))
    mestado.set("Por estado:")
    mestado.pack(pady=5, padx=10) 

    def abrir_calendario(variable):
        top = Toplevel()
        top.title("Seleccionar fecha")

        def seleccionar_fecha():
            fecha = cal.get_date()
            variable.set(fecha)
            print("Fecha seleccionada:", fecha)
            top.destroy()

        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd', locale='es_ES')
        cal.pack(pady=10)

        btn = ctk.CTkButton(top, text="Seleccionar", command=seleccionar_fecha)
        btn.pack(pady=10)

           # === FECHAS (BOTONES CON CALENDARIO) ===
    fecha1_var = ctk.StringVar(value="De esta fecha:")
    fecha2_var = ctk.StringVar(value="A esta fecha:")

    btn_fecha1 = ctk.CTkButton(master=sidebar, textvariable=fecha1_var, command=lambda: abrir_calendario(fecha1_var))
    btn_fecha1.pack(pady=5, padx=10)

    btn_fecha2 = ctk.CTkButton(master=sidebar, textvariable=fecha2_var, command=lambda: abrir_calendario(fecha2_var))
    btn_fecha2.pack(pady=5, padx=10)

            # === BOTÓN DE REINICIO DE FILTROS ===
    btn_inicio = ctk.CTkButton(sidebar, text="Quitar filtros", command=lambda: print("Inicio"))
    btn_inicio.pack(pady=10)

            # === BOTÓN DE CONFIGURACION ===
    btn_cf = ctk.CTkButton(sidebar, width=40, text="⚙️",command=configventana)
    btn_cf.pack(pady=10)
    btn_cf.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    
    
    
    # === ÁREA PRINCIPAL ===
    mainarea = ctk.CTkFrame(app, corner_radius=10)
    mainarea.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # Variables para el mes y año actual
    mes_actual = [datetime.today().month]
    año_actual = [datetime.today().year]

    # === NAVBAR del calendario: botones ◀ ▶ y nombre del mes ===
    nav_frame = ctk.CTkFrame(mainarea)
    nav_frame.pack(pady=10)

    btn_anterior = ctk.CTkButton(nav_frame, text="◀", width=40, command=lambda: cambiar_mes(-1))
    btn_anterior.pack(side="left", padx=5)

    titulo_mes = ctk.CTkLabel(nav_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
    titulo_mes.pack(side="left", padx=10)

    btn_siguiente = ctk.CTkButton(nav_frame, text="▶", width=40, command=lambda: cambiar_mes(1))
    btn_siguiente.pack(side="left", padx=5)

    calendario_frame = ctk.CTkFrame(mainarea)
    calendario_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def abrir_ventana_modificar(evento):
        ventana = ctk.CTkToplevel()
        ventana.title("Modificar evento")
        ventana.geometry("400x400")
        ventana.grab_set()          # Hace la ventana modal
        ventana.focus()             # Da el foco a la ventana emergente
        ventana.transient(app) 

        entrada = ctk.CTkEntry(ventana, placeholder_text="Título del evento")
        entrada.pack(padx=10, pady=5)

        emprioridad= ctk.CTkOptionMenu(ventana,values=prioridades, command=lambda valor: print(f"Filtrar por: {valor}"))
        emprioridad.set("Prioridad:")
        emprioridad.pack(padx=10, pady=5)

        emcategoria = ctk.CTkOptionMenu(ventana, values=categoria, command=lambda valor: print(f"Filtrar por: {valor}"))
        emcategoria.set("Tipo de evento:")
        emcategoria.pack(padx=10, pady=5)

        emubicacion = ctk.CTkOptionMenu(ventana,values=ubicacion, command=lambda valor: print(f"Filtrar por: {valor}"))
        emubicacion.set("Ubicacion:")
        emubicacion.pack(padx=10, pady=5)

        emresponsable = ctk.CTkOptionMenu(ventana,values=responsable, command=lambda valor: print(f"Filtrar por: {valor}"))
        emresponsable.set("Responsable:")
        emresponsable.pack(padx=10, pady=5)

        emestado = ctk.CTkOptionMenu(ventana, values=estado, command=lambda valor: print(f"Filtrar por: {valor}"))
        emestado.set("Estado:")
        emestado.pack(padx=10, pady=5)

        emhora = ctk.CTkOptionMenu(ventana, values=horas, command=lambda valor: print(f"Filtrar por: {valor}"))
        emhora.set("Hora:")
        emhora.pack(padx=10, pady=5)




        

    # Botón Guardar
        def guardar_cambios():
            evento["titulo"] = entrada.get()
            evento["hora"] = emhora.get()
            evento["prioridad"] = emprioridad.get()
            print("Evento modificado:", evento)
            ventana.destroy()

        ctk.CTkButton(ventana, text="Guardar cambios", command=guardar_cambios).pack(pady=20)

    def abrir_ventana_evento(fecha):
        ventana = ctk.CTkToplevel()
        ventana.title("Agregar evento")
        ventana.geometry("1000x600")

        ventana.grab_set()          # Hace la ventana modal
        ventana.focus()             # Da el foco a la ventana emergente
        ventana.transient(app)      # La mantiene por encima de la principal

        textagevento = ctk.CTkLabel(ventana, text=f"Agregar evento para el {fecha}", font=ctk.CTkFont(size=15, weight="bold"))
        textagevento.pack(anchor="ne", padx=10, pady=(10, 0))
        
        emprioridad= ctk.CTkOptionMenu(ventana,values=prioridades, command=lambda valor: print(f"Filtrar por: {valor}"))
        emprioridad.set("Prioridad:")
        emprioridad.pack(anchor="ne", padx=10, pady=5)

        emcategoria = ctk.CTkOptionMenu(ventana, values=categoria, command=lambda valor: print(f"Filtrar por: {valor}"))
        emcategoria.set("Tipo de evento:")
        emcategoria.pack(anchor="ne", padx=10, pady=5)

        emubicacion = ctk.CTkOptionMenu(ventana,values=ubicacion, command=lambda valor: print(f"Filtrar por: {valor}"))
        emubicacion.set("Ubicacion:")
        emubicacion.pack(anchor="ne", padx=10, pady=5)

        emresponsable = ctk.CTkOptionMenu(ventana,values=responsable, command=lambda valor: print(f"Filtrar por: {valor}"))
        emresponsable.set("Responsable:")
        emresponsable.pack(anchor="ne", padx=10, pady=5)

        emestado = ctk.CTkOptionMenu(ventana, values=estado, command=lambda valor: print(f"Filtrar por: {valor}"))
        emestado.set("Estado:")
        emestado.pack(anchor="ne", padx=10, pady=5)

        emhora = ctk.CTkOptionMenu(ventana, values=horas, command=lambda valor: print(f"Filtrar por: {valor}"))
        emhora.set("Hora:")
        emhora.pack(anchor="ne", padx=10, pady=5)

        entrada = ctk.CTkEntry(ventana, placeholder_text="Título del evento")
        entrada.pack(anchor="ne", padx=10, pady=5)

        def guardar_evento():
            evento = entrada.get()
            if evento:
                eventos.append({"fecha": fecha,"titulo": entrada.get(),"prioridad": emprioridad.get(),"categoria": emcategoria.get(),"ubicacion": emubicacion.get(),"responsable": emresponsable.get(),"estado": emestado.get(),"hora": emhora.get()})

                print("Evento guardado:", evento)
                actualizar_calendario()
                ventana.destroy()

        guardbutt=ctk.CTkButton(ventana, text="Guardar", command=guardar_evento)
        guardbutt.pack(anchor="ne", padx=10, pady=5)


    # === SCROLLABLE FRAME para mostrar eventos del día ===
        frame_scroll = ctk.CTkScrollableFrame(ventana, width=680, height=500, fg_color="transparent")
        frame_scroll.place(x=10, y=10)

        ctk.CTkLabel(frame_scroll, text="Eventos del día:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="nw", padx=5, pady=(5, 10))

    # Filtrar eventos para la fecha
        eventos_del_dia = [ev for ev in eventos if ev["fecha"] == fecha]

        if eventos_del_dia:
            for i, ev in enumerate(eventos_del_dia):
                evento_frame = ctk.CTkFrame(frame_scroll, fg_color="#333333", corner_radius=8)
                evento_frame.pack(fill="x", padx=5, pady=5)

            # Título del evento
                ctk.CTkLabel(evento_frame, text=ev.get("titulo", "Sin título"), font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(5, 0))

            # Propiedades adicionales (si existen)
                propiedades = [
                    ("Prioridad", ev.get("prioridad")),
                    ("Categoría", ev.get("categoria")),
                    ("Ubicación", ev.get("ubicacion")),
                    ("Responsable", ev.get("responsable")),
                    ("Estado", ev.get("estado")),
                    ("Hora", ev.get("hora")),
                ]

                for nombre, valor in propiedades:
                    if valor:
                        texto = f"{nombre}: {valor}"
                        ctk.CTkLabel(evento_frame, text=texto, font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", padx=20)

                # Botón de eliminar (por ahora sin funcionalidad)
                btn_eliminar = ctk.CTkButton(evento_frame, text="🗑", width=30, fg_color="red", hover_color="#aa0000", text_color="white", command=lambda e=ev: print("Eliminar:", e))
                btn_eliminar.pack(side="right", padx=5, pady=(0, 5))

                # Botón de modificar (por ahora sin funcionalidad)
                btn_modi = ctk.CTkButton(
                evento_frame,
                text="Modificar",
                width=70,
                fg_color="blue",
                hover_color="#519cff",
                text_color="white",
                command=lambda: abrir_ventana_modificar(ev)
                )
                btn_modi.pack(side="right", padx=5, pady=(0, 5))


        else:
            ctk.CTkLabel(frame_scroll, text="No hay eventos aún", font=ctk.CTkFont(size=13), text_color="gray").pack(anchor="nw", padx=10, pady=5)





    def actualizar_calendario():
        for widget in calendario_frame.winfo_children():
            widget.destroy()

        nombre_mes = datetime(año_actual[0], mes_actual[0], 1).strftime("%B %Y")
        titulo_mes.configure(text=nombre_mes.capitalize())

        dias = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            ndia = ctk.CTkLabel(calendario_frame, text=dia, font=ctk.CTkFont(size=15, weight="bold"))
            ndia.grid(row=0, column=i, padx=5, pady=5)

        cal = calendar.Calendar(firstweekday=0)
        fechas_mes = cal.monthdayscalendar(año_actual[0], mes_actual[0])

        for fila, semana in enumerate(fechas_mes, start=1):
            for col, dia in enumerate(semana):
                if dia == 0:
                    continue

                celda = ctk.CTkFrame(calendario_frame, width=147, height=110, fg_color="#2a2a2a", corner_radius=5)
                celda.grid(row=fila, column=col, padx=2, pady=2, sticky="nsew")

                num_label = ctk.CTkLabel(celda, text=str(dia), font=ctk.CTkFont(size=12), text_color="white")
                num_label.place(x=4, y=2)

                fecha_str = f"{año_actual[0]}-{mes_actual[0]:02d}-{dia:02d}"
                celda.bind("<Button-1>", lambda e, f=fecha_str: abrir_ventana_evento(f))

                eventos_del_dia    = [ev for ev in eventos if ev["fecha"] == fecha_str]
                for i, ev in enumerate(eventos_del_dia[:3]):
                    ev_label = ctk.CTkLabel(celda, text=f"• {ev['titulo']}", font=ctk.CTkFont(size=10), text_color="#a0a0a0")
                    ev_label.place(x=4, y=25 + i * 18)
                    ev_label.bind("<Button-1>", lambda e, f=fecha_str: abrir_ventana_evento(f))

                if len(eventos_del_dia) > 3:
                    mas_label = ctk.CTkLabel(celda, text="más...", font=ctk.CTkFont(size=10, slant="italic"), text_color="#6c6c6c")
                    mas_label.place(x=4, y=25 + 3 * 18)
                    mas_label.bind("<Button-1>", lambda e, f=fecha_str: abrir_ventana_evento(f))


    def cambiar_mes(direccion):
        mes_actual[0] += direccion
        if mes_actual[0] < 1:
            mes_actual[0] = 12
            año_actual[0] -= 1
        elif mes_actual[0] > 12:
            mes_actual[0] = 1
            año_actual[0] += 1
        actualizar_calendario()

    # Llama una vez al iniciar
    actualizar_calendario()




    

    


    return app
