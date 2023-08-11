import os # para acceder al path y obtener las rutas
import customtkinter # importa el cusotmtkinter
import uuid
from tkintermapview import TkinterMapView # importa las utilidades necesarias para el mapa
from PIL import Image, ImageTk # con esto podes manipular imagenes
from tkinter import messagebox # importa las ventanas de mensajes emergentes
import tkinter as tk # importa tkinter para alguna que otra funcion
import json # Importa json para la manipulacion de los archivos
from datetime import datetime

from views.principal_view import App

class Logsign(App):
    def __init__(self):
        self.users = []

    def cargar_usuarios(self):
        try:
            with open(json_usuarios, "r", encoding="utf-8") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []

    def verificar(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return user["id"]
        return None

    def iniciar_sesion(self):
        username = self.entry_usuario_log.get().strip()
        password = self.entry_contra_log.get().strip()

        user_id = self.verificar(username, password)
        if user_id is not None:
            messagebox.showinfo("Exito", "Inicio de sesión correcto")
            self.der_login.grid_forget()
            self.izq_frame_inic.grid_forget()
            self.der_explorar.grid(row=0, column=1, columnspan=3, sticky="nsew", pady=10, padx=(5, 10))
            self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
            self.izq_frame.grid_rowconfigure(5, weight=1)
            self.user_id_iniciado = user_id
            self.user_iniciado = username
            self.btn_explorar.configure(fg_color=("gray75", "gray30"))
        else:
            messagebox.showerror("Error", "Las credenciales son incorrectas")
        self.entry_usuario_log.delete(0, tk.END)
        self.entry_contra_log.delete(0, tk.END)

    def registrar_usuario(self):
        username = self.entry_usuario_registra.get().strip()
        password = self.entry_contra_registra.get()

        if not username or not password:
            messagebox.showerror("Error", "Ingresa un nombre de usuario y contraseña válidos")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres")
            return

        if any(user["username"] == username for user in self.users):
            messagebox.showerror("Error", "El nombre de usuario ya está registrado")
            return

        new_user = {"id": str(uuid.uuid4()), "username": username, "password": password}
        self.users.append(new_user)
        self.guardar_usuario()
        messagebox.showinfo("Éxito", "Registro exitoso")
        self.der_regist.grid_forget()
        self.der_login.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
        self.entry_usuario_registra.delete(0, tk.END)
        self.entry_contra_registra.delete(0, tk.END)

    def guardar_usuario(self):
        with open(json_usuarios, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=2)