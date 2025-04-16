import customtkinter as ctk

def crear_interfaz():
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")  

    app = ctk.CTk()
    app.title("Sistema de Gestión Hospitalaria")
    app.geometry("1280x720")

    label = ctk.CTkLabel(app, text="Bienvenido al Sistema", font=("Arial", 20))
    label.pack(pady=20)

    button = ctk.CTkButton(app, text="Iniciar Sesion", command=lambda: print("El usuario quiere acceder"))
    button.pack(pady=10)

    return app
