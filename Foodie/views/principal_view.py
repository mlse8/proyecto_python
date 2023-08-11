import os # para acceder al path y obtener las rutas
import customtkinter # importa el cusotmtkinter
import uuid # importo una libreria para usarun id generado
from tkintermapview import TkinterMapView # importa las utilidades necesarias para el mapa
from PIL import Image, ImageTk # con esto manipulo las imagenes
from tkinter import messagebox # importa las ventanas de mensajes emergentes
import tkinter as tk # importa tkinter para alguna que otra funcion
import json # Importa json para la manipulacion de los archivos
from datetime import datetime # importo la libreria datetime para manipular fechas

# Obtengo todas las direcciones necesarias (imagenes y jsons)
direccion_actual = os.path.dirname(os.path.abspath(__file__))
json_dir = os.path.join(direccion_actual, "..", "data", "destinos.json")
json_rese = os.path.join(direccion_actual, "..", "data", "reseñas.json")
json_usuarios = os.path.join(direccion_actual, "..", "data", "usuarios.json")
assets_dir = os.path.join(direccion_actual, "..", "assets")
destinos_imgs = os.path.join(direccion_actual, "..", "assets", "destinos")

# Establezco el tema y el color por defecto
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    """Utilizo la funcion de la documentacion para que me cree una tarjeta en los frames scrolleables que tengo en las diferentes ventanas"""
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item):
        label = customtkinter.CTkLabel(
            self, text=item, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Command", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class App():
    """Clase principal encargada de vista de los metodos principales"""
    def __init__(self):

        self.users = []

        self.ventana = customtkinter.CTk()
        self.ventana.title("Food Travel")
        self.ventana.geometry("1100x600")
        self.ventana.resizable(False, False)

        # Establezco grid 1x2
        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=1)

        self.list_dest, self.list_dest_even = [], []

        self.user_id_iniciado = ""
        self.user_iniciado = ""

        # Cargo la imagen del logo desde assets para usarla despues
        self.img_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(assets_dir, "logo-r.png")),
                                                dark_image=Image.open(os.path.join(assets_dir, "logo-r.png")),
                                                size=(75, 75))

        # Creo un frame donde van a ir todos los botones que estan en el lado izquierdo
        self.izq_frame_inic = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color=("red", "#333333"))
        self.izq_frame_inic.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
        self.izq_frame_inic.grid_rowconfigure(5, weight=1)

        # Es un label que muestra el nombre junto con el logo
        self.lbl_foddie = customtkinter.CTkLabel(self.izq_frame_inic, text="  FODDIE TOUR",
                                                 image=self.img_logo, compound="left",
                                                 font=("Roboto Condensed", 20, "bold"))
        self.lbl_foddie.grid(row=0, column=0, padx=20, pady=(50, 50))

        self.lbl_foddie = customtkinter.CTkLabel(master=self.izq_frame_inic, text="""BIENVENIDOS!!\n
Foodie Tour te ayuda a 
descubrir y 
planificar visitas a destinos 
culinarios de manera 
eficiente y organizada""", font=("Roboto Condensed", 20, "bold"))
        self.lbl_foddie.grid(row=1, column=0, padx=20, pady=(20, 50))

        # Frame encargado de explorar los destinos
        self.der_login = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color="#333333")
        self.der_login.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))

        self.lbl_login = customtkinter.CTkLabel(self.der_login, text="Iniciar sesión",
                                                text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.lbl_login.place(relx=0.40, rely=0.030)

        self.lbl1_login = customtkinter.CTkLabel(self.der_login, text="Usuario",
                                                 text_color="white", font=("Roboto Condensed", 18))
        self.lbl1_login.place(relx=0.46, rely=0.23)

        self.entry_usuario_log = customtkinter.CTkEntry(master=self.der_login, corner_radius=15,
                                                        width=250, text_color="white")
        self.entry_usuario_log.place(relx=0.345, rely=0.30)

        self.lbl2_login = customtkinter.CTkLabel(self.der_login, text="Contraseña",
                                                 text_color="white", font=("Roboto Condensed", 18))
        self.lbl2_login.place(relx=0.444, rely=0.389)

        self.entry_contra_log = customtkinter.CTkEntry(master=self.der_login, corner_radius=15,
                                                       width=250, text_color="white", show="*")
        self.entry_contra_log.place(relx=0.345, rely=0.465)

        self.boton_registrarse = customtkinter.CTkButton(master=self.der_login, fg_color="#333333", text="Registrarse",
                                                         text_color="white", command=self.regist,
                                                         font=("Roboto Condensed", 18), hover=False)
        self.boton_registrarse.place(relx=0.513, rely=0.54)

        self.boton_inicia = customtkinter.CTkButton(master=self.der_login, text="Iniciar sesión", width=250,
                                                    text_color="white",
                                                    font=("Roboto Condensed", 18),
                                                    command=self.iniciar_sesion)
        self.boton_inicia.place(relx=0.345, rely=0.70)

        # Frame encargado de registrar un usuario
        self.der_regist = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color="#333333")
        self.der_regist.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))

        self.lbl_registrar = customtkinter.CTkLabel(self.der_regist, text="Registrarse",
                                                    text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.lbl_registrar.place(relx=0.412, rely=0.030)

        self.lbl1_regist = customtkinter.CTkLabel(self.der_regist, text="Usuario",
                                                  text_color="white", font=("Roboto Condensed", 18))
        self.lbl1_regist.place(relx=0.46, rely=0.23)

        self.entry_usuario_registra = customtkinter.CTkEntry(master=self.der_regist, corner_radius=15,
                                                             width=250, text_color="white")
        self.entry_usuario_registra.place(relx=0.345, rely=0.30)

        self.lbl2_regist = customtkinter.CTkLabel(self.der_regist, text="Contraseña",
                                                  text_color="white", font=("Roboto Condensed", 18))
        self.lbl2_regist.place(relx=0.444, rely=0.389)

        self.entry_contra_registra = customtkinter.CTkEntry(master=self.der_regist, corner_radius=15,
                                                            width=250, text_color="white", show="*")
        self.entry_contra_registra.place(relx=0.345, rely=0.465)

        self.boton_volver = customtkinter.CTkButton(master=self.der_regist, fg_color="#333333", text="Volver",
                                                    text_color="white", command=self.volver,
                                                    font=("Roboto Condensed", 18), hover=False)
        self.boton_volver.place(relx=0.5445, rely=0.54)

        self.boton_registra = customtkinter.CTkButton(master=self.der_regist, text="Registrar usuario", width=250,
                                                      text_color="white",
                                                      font=("Roboto Condensed", 18),
                                                      command=self.registrar_usuario)
        self.boton_registra.place(relx=0.345, rely=0.70)

        # Creo un frame donde van a ir todos los botones que estan en el lado izquierdo
        self.izq_frame = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color=("red", "#333333"))
        self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
        self.izq_frame.grid_rowconfigure(5, weight=1)

        # Es un label que muestra el nombre junto con el logo
        self.lbl_foddie = customtkinter.CTkLabel(self.izq_frame, text="  FODDIE TOUR",
                                                    image=self.img_logo, compound="left",
                                                    font=("Roboto Condensed", 20, "bold"))
        self.lbl_foddie.grid(row=0, column=0, padx=20, pady=(50, 50))

        # Boton que ejecuta el label derecho de "Explorar destinos"
        self.btn_explorar = customtkinter.CTkButton(self.izq_frame, corner_radius=0, height=40, border_spacing=10,
                                                        text="     Explorar destinos",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray35"),
                                                        anchor="nsew", command=self.mostrar_frame_explo,
                                                        font=("Roboto Condensed", 20))
        self.btn_explorar.grid(row=1, column=0, sticky="ew")

        # Boton que ejecuta el label derecho de "Buscar destinos"
        self.btn_buscar_dest = customtkinter.CTkButton(self.izq_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="     Buscar destinos",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray35"),
                                                        anchor="nsew", font=("Roboto Condensed", 20),
                                                        command=self.mostrar_frame_busc)
        self.btn_buscar_dest.grid(row=2, column=0, sticky="ew")

        # Boton que ejecuta el label derecho de "Planificar Visitas"
        self.btn_planificar = customtkinter.CTkButton(self.izq_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="     Planificar visitas",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray35"),
                                                        anchor="nsew",
                                                        command=self.mostrar_frame_planif,
                                                        font=("Roboto Condensed", 20))
        self.btn_planificar.grid(row=3, column=0, sticky="ew")

        # Boton que ejecuta el label derecho de los "Reviews"
        self.btn_review = customtkinter.CTkButton(self.izq_frame, corner_radius=0, height=40,
                                                  border_spacing=10, text="     Reviews",
                                                  fg_color="transparent", text_color=("black", "white"),
                                                  hover_color=("gray70", "gray35"),
                                                  anchor="nsew", #command=self.mostrar_frame_revi
                                                  font=("Roboto Condensed", 20))
        self.btn_review.grid(row=4, column=0, sticky="ew")

        # Boton que una vez presionado cierra la sesión
        self.btn_cerrar_sesion = customtkinter.CTkButton(self.izq_frame, corner_radius=0, height=40,
                                                         border_spacing=10, text="     Cerrar Sesion",
                                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                                         hover_color=("gray70", "gray35"),
                                                         anchor="nsew",
                                                         font=("Roboto Condensed", 20),
                                                         command=self.cerrar_sesion)
        self.btn_cerrar_sesion.grid(row=5, column=0, sticky="sew", pady=(0, 20))

        # Frame encargado de explorar los destinos
        self.der_explorar = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color="#333333")
        self.der_explorar.grid_columnconfigure(1, weight=1)

        self.lbl_explorar = customtkinter.CTkLabel(self.der_explorar, text="Explorar Destinos",
                                                    text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.lbl_explorar.grid(row=0, column=1, pady=(30, 10))

        # Coloco un mapa y establezco la posicion en salta aprox pq por defecto es en berlin
        self.der_explorar_mapa = TkinterMapView(master=self.der_explorar, corner_radius=15,
                                                               width=420, height=465)
        self.der_explorar_mapa.set_position(-24.78863258809092, -65.42464163143842)
        self.der_explorar_mapa.set_zoom(16)
        #self.der_explorar_mapa.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.der_explorar_mapa.place(relx=0.025, rely=0.15)
        #
        self.tabview = customtkinter.CTkTabview(self.der_explorar, width=328, height=485)
        self.tabview.place(relx=0.57, rely=0.121)
        self.tabview.add("Destinos")
        self.tabview.add("Eventos")

        self.tabview.tab("Destinos").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Eventos").grid_columnconfigure(0, weight=1)

        # Pongo un Frame que se puede hacer scroll para mostrar los destinos
        self.der_scroll_dest = customtkinter.CTkScrollableFrame(self.tabview.tab("Destinos"), width=280, height=400)
        self.der_scroll_dest.place(relx=0.02, rely=0.02)

        self.der_scroll_act = customtkinter.CTkScrollableFrame(self.tabview.tab("Eventos"), width=280, height=400)
        self.der_scroll_act.place(relx=0.02, rely=0.02)

        # Frame encargado de buscar los destinos
        self.der_buscar = customtkinter.CTkFrame(master=self.ventana, corner_radius=15, fg_color="#333333")
        self.der_buscar.grid_columnconfigure(3, weight=1)

        self.der_lbl_buscar = customtkinter.CTkLabel(self.der_buscar, text="Buscar Destinos",
                                                     text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.der_lbl_buscar.grid(row=0, column=3, pady=(30, 10))

        # Leer los destinos desde el archivo JSON
        with open(json_dir, encoding="utf-8") as file:
            destinos_data = json.load(file)

        # Obtener los nombres de los destinos 
        self.destinos_tipoC = [destino["tipo_cocina"] for destino in destinos_data]
        # Con el list y el set lo que hago es eliminar los elementos repetidos de la lista que traigo
        # ya que como es un for comun se llena de repetidos ya que hay varis destinos con el mismo tipo
        self.destinos_tipo = list(set(self.destinos_tipoC))

        # Creo un menu de opciones para que pueda mostrar el tipo de cocina
        self.menu_opciones_cocina = customtkinter.CTkOptionMenu(master=self.der_buscar, values=self.destinos_tipo,
                                                        corner_radius=15, dynamic_resizing=False, width=105)
        self.menu_opciones_cocina.set("Cocina")
        self.menu_opciones_cocina.place(relx=0.27, rely=0.15)

        ingredientes = []
        for ingr in destinos_data:
            ingre = ingr["ingredientes"]
            for ingred in ingre:
                ingredientes.append(ingred)

        ingres_sin_repetidos = list(set(ingredientes))

        self.menu_opciones_ingre = customtkinter.CTkOptionMenu(master=self.der_buscar, values=ingres_sin_repetidos,
                                                        dynamic_resizing=False,
                                                        corner_radius=15, width=123)
        self.menu_opciones_ingre.place(relx=0.404, rely=0.15)
        self.menu_opciones_ingre.set("Ingredientes")

        # Creo otro menu de opciones para establecer los rangos de precios por los que puedo filtrar
        destinos_preciomin = ["1000", "2000", "3000", "4000", "5000"]
        self.menu_opciones_precio_min = customtkinter.CTkOptionMenu(master=self.der_buscar, values=destinos_preciomin,
                                                        dynamic_resizing=False,
                                                        corner_radius=15, width=123)
        self.menu_opciones_precio_min.place(relx=0.559, rely=0.125)
        self.menu_opciones_precio_min.set("Precio MIN")

        destinos_preciomax = ["1000", "2000", "3000", "4000", "5000"]
        self.menu_opciones_precio_max = customtkinter.CTkOptionMenu(master=self.der_buscar, values=destinos_preciomax,
                                                                dynamic_resizing=False,
                                                                corner_radius=15, width=123)
        self.menu_opciones_precio_max.place(relx=0.559, rely=0.18)
        self.menu_opciones_precio_max.set("Precio MAX")

        # Creo un menu de opciones con la puntuacion por la que quiero filtrar
        destinos_estrellas = ['0', '1', '2', '3', '4', '5']
        self.menu_opciones_estre = customtkinter.CTkOptionMenu(master=self.der_buscar, values=destinos_estrellas,
                                                        dynamic_resizing=False,
                                                        corner_radius=15, width=115)
        self.menu_opciones_estre.place(relx=0.715, rely=0.15)
        self.menu_opciones_estre.set("Puntuación")

        # Agregar un botón para obtener los filtros aplicados
        self.btn_aplicar_filtros = customtkinter.CTkButton(master=self.der_buscar, text="Aplicar filtros",
                                                            command=self.aplicar_filtros, corner_radius=15,
                                                            width=105)
        self.btn_aplicar_filtros.place(relx=0.86, rely=0.125)

        self.btn_borrar_filtros = customtkinter.CTkButton(master=self.der_buscar, text="Borrar filtros",
                                                           command=self.cancelar_filtros, corner_radius=15,
                                                           width=105)
        self.btn_borrar_filtros.place(relx=0.86, rely=0.18)

        # Agregar un botón para obtener el destino seleccionado
        self.btn_buscar = customtkinter.CTkButton(master=self.der_buscar, text="Buscar",
                                                  command=self.buscar_destinos_por_nombre, width=30, corner_radius=15)
        self.btn_buscar.place(relx=0.177, rely=0.125)

        self.btn_buscar = customtkinter.CTkButton(master=self.der_buscar, text="Cancelar",
                                                  command=self.cancelar_busqueda, width=30, corner_radius=15)
        self.btn_buscar.place(relx=0.171, rely=0.18)

        # Creo el mapa que va en la seccion de buscar destinos
        self.der_buscar_mapa = TkinterMapView(master=self.der_buscar, corner_radius=15,
                                                             width=420, height=420)
        self.der_buscar_mapa.set_position(-24.78863258809092, -65.42464163143842)
        self.der_buscar_mapa.set_zoom(16)
        #self.der_buscar_mapa.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.der_buscar_mapa.place(relx=0.025, rely=0.253)

        for dest in destinos_data:
            coordenadas = [float(coord.strip()) for coord in dest["coordenadas"].split(",")]
            self.der_buscar_mapa.set_marker(coordenadas[0], coordenadas[1], text=dest["nombre"],
                                            marker_color_circle="white")

        # Creo el frame que se puede hacer scroll para que vayan las tarjetas de los destinos encontrados
        self.der_scroll_busc = customtkinter.CTkScrollableFrame(self.der_buscar, width=280, height=420)
        self.der_scroll_busc.place(relx=0.59, rely=0.253)

        # Pongo un entry adicional por si quiero buscar por nombre algun destino
        self.entry_nom_busc = customtkinter.CTkEntry(master=self.der_buscar, placeholder_text="Destino",
                                                     corner_radius=15, width=130)
        self.entry_nom_busc.place(relx=0.010, rely=0.15)

        # Frame encargado de planificar un ruta 
        self.der_planificar = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color="#333333")
        self.der_planificar.grid_columnconfigure(1, weight=1)

        self.der_lbl_planif = customtkinter.CTkLabel(self.der_planificar, text="Planificar Rutas",
                                                     text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.der_lbl_planif.grid(row=0, column=1, pady=(30, 10))

        self.der_planificar_mapa = TkinterMapView(master=self.der_planificar, corner_radius=15,
                                                                 width=420, height=465)
        self.der_planificar_mapa.set_position(-24.78863258809092, -65.42464163143842)
        self.der_planificar_mapa.set_zoom(16)
        #self.der_buscar_mapa.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.der_planificar_mapa.place(relx=0.025, rely=0.15)

        # Frame encargado de los reviews de los destinos
        self.der_review = customtkinter.CTkFrame(self.ventana, corner_radius=15, fg_color="#333333")
        self.der_review.grid_columnconfigure(1, weight=1)

        self.der_lbl_review = customtkinter.CTkLabel(self.der_review, text="Reviews",
                                                    text_color="white", font=("Roboto Condensed", 25, "bold"))
        self.der_lbl_review.grid(row=0, column=1, pady=(30, 10))
        
        # Frame scroleable para ver los reviews 
        self.der_scroll_revie = customtkinter.CTkScrollableFrame(self.der_review, width=300, height=460)
        self.der_scroll_revie.place(relx=0.025, rely=0.149)

        # Pongo los elementos para dejar un review
        self.lbl_res = customtkinter.CTkLabel(self.der_review, text="¿Desea dejar una reseña sobre un destino?",
                                              text_color="white", font=("Roboto Condensed", 15, "bold"))
        self.lbl_res.place(relx=0.53, rely=0.20)

        self.entry_nom_ = customtkinter.CTkEntry(master=self.der_review, placeholder_text="Nombre",
                                                 corner_radius=15,
                                                 width=300, fg_color="white", text_color="black")
        self.entry_nom_.place(relx=0.539, rely=0.30)

        self.entry_desac = customtkinter.CTkEntry(master=self.der_review, corner_radius=15,
                                                  width=145, fg_color="white", text_color="black", justify="center")
        self.entry_desac.place(relx=0.539, rely=0.37)

        estrellas = ['0', '1', '2', '3', '4', '5']
        self.menu_estre_revie = customtkinter.CTkOptionMenu(master=self.der_review, values=estrellas,
                                                            dynamic_resizing=False,
                                                            corner_radius=15, width=145)
        self.menu_estre_revie.place(relx=0.732, rely=0.37)
        self.menu_estre_revie.set("Puntuacion")

        self.lbl_resen = customtkinter.CTkLabel(self.der_review, text="Escribir una reseña:",
                                                text_color="white", font=("Roboto Condensed", 12))
        self.lbl_resen.place(relx=0.539, rely=0.43)

        self.txt_rese = customtkinter.CTkTextbox(master=self.der_review, width=300, height=180,
                                                 font=("Roboto Condensed", 13), corner_radius=15,
                                                 text_color="black", fg_color="white")
        self.txt_rese.place(relx=0.539, rely=0.485)

        btn_mostrar_coordenadas = customtkinter.CTkButton(master=self.der_review,
                                                          text="Guardar reseña",
                                                          command=self.guardar_resena,
                                                          corner_radius=30,
                                                          text_color="white",
                                                          font=("Roboto Condensed", 12),
                                                          width=30)
        btn_mostrar_coordenadas.place(relx=0.765, rely=0.82)
        # Selecciono el frame que quiero que se muestre al abrir la ventana
        self.mostrar_frame_por_nom("login")
        # Cargo los datos desde los json (esplorar y buscar y reviews)
        self.cargar_datos_json()
        self.cargar_datos_json_en_reviews()
        self.cargar_datos_json_en_actividades()
        self.cargar_usuarios()

    def mostrar_frame_por_nom(self, nombre_frame):
        """Funcion encargada de mostrar los frames que seleccione a traves de los botones que tengo ubicados 
        en el frame de la izquierda de la ventana"""
        # Coloco un color adicionar a los botones para que cuando esten presionados se note
        self.btn_explorar.configure(fg_color=("gray75", "gray30") if nombre_frame == "explorar" else "transparent")
        self.btn_buscar_dest.configure(fg_color=("gray75", "gray30") if nombre_frame == "buscar" else "transparent")
        self.btn_planificar.configure(fg_color=("gray75", "gray30") if nombre_frame == "planificar" else "transparent")
        self.btn_review.configure(fg_color=("gray75", "gray30") if nombre_frame == "review" else "transparent")

        # Muestro el frame seleccionado a travez de los botones
        if nombre_frame == "login":
            self.cerrar_sesion()
        else:
            self.der_login.grid_forget()
        if nombre_frame == "regist":
            self.der_regist.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
        else:
            self.der_regist.grid_forget()
        if nombre_frame == "explorar":
            self.izq_frame_inic.grid_forget()
            self.der_explorar.grid(row=0, column=1, columnspan=3, sticky="nsew", pady=10, padx=(5, 10))
            self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
            self.izq_frame.grid_rowconfigure(5, weight=1)
        else:
            self.der_explorar.grid_forget()
        if nombre_frame == "buscar":
            self.izq_frame_inic.grid_forget()
            self.der_buscar.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
            self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
            self.izq_frame.grid_rowconfigure(5, weight=1)
        else:
            self.der_buscar.grid_forget()
        if nombre_frame == "planificar":
            self.izq_frame_inic.grid_forget()
            self.der_planificar.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
            self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
            self.izq_frame.grid_rowconfigure(5, weight=1)
        else:
            self.der_planificar.grid_forget()
        if nombre_frame == "review":
            self.izq_frame_inic.grid_forget()
            self.der_review.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
            self.izq_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
            self.izq_frame.grid_rowconfigure(5, weight=1)
        else:
            self.der_review.grid_forget()

    def mostrar_frame_explo(self):
        """Funcion encargada de acceder al frame explorar"""
        self.mostrar_frame_por_nom("explorar")

    def mostrar_frame_busc(self):
        """Funcion encargada de acceder al frame buscar"""
        self.mostrar_frame_por_nom("buscar")

    def mostrar_frame_planif(self):
        """Funcion encargada de acceder al frame planificar"""
        self.mostrar_frame_por_nom("planificar")

    def mostrar_frame_revi(self):
        """Funcion encargada de acceder al frame reviews"""
        self.mostrar_frame_por_nom("review")

    def cargar_datos_json(self):
        """Funcion encargada de cargar los datos desde el json en la direccion 'json_dir'"""
        current_dire = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta completa al archivo JSON
        json_dire = os.path.join(current_dire, "../data/destinos.json")

        # Carga los datos desde el json
        with open(json_dire, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        # Crea las tarjetas para cada destino
        for destination in data:
            self.crea_tarj_desti(destination)
            self.list_dest.append(destination["nombre"])

    def crea_tarj_desti(self, destination):
        """Creo las tarjetas que van a ser almacenadas en el scrollbarFrame de los destinos"""
        # Creo un Frame para contener los datos del destino
        tarj_destinos = customtkinter.CTkFrame(self.der_scroll_dest, fg_color="white", corner_radius=10,
                                               width=250, height=100)
        tarj_destinos.pack(pady=10, padx=5, fill="x")

        # Cargo las imagenes a travez de la ruta que esta en el json
        current_direc = os.path.dirname(os.path.abspath(__file__))

        # Construir la ruta a la imagen
        imagen_path = os.path.join(current_direc, "..", "assets", destination["imagen"])

        # Cargar la imagen
        image = customtkinter.CTkImage(light_image=Image.open(imagen_path),
                                       dark_image=Image.open(imagen_path),
                                       size=(85, 85))
        image_lbl_exp = customtkinter.CTkLabel(master=tarj_destinos, text="",
                                               image=image)
        image_lbl_exp.place(relx=0.03, rely=0.08)

        # Muestro el nombre del destino en la tarjeta
        nombre_dest = destination.get("nombre", "Nombre no disponible")
        lbl_nombre_dest = customtkinter.CTkLabel(master=tarj_destinos, text=nombre_dest,
                                                 font=("Roboto Condensed", 16, "bold"),
                                                 text_color="black")
        lbl_nombre_dest.place(relx=0.36, rely=0.08)

        # Muestro el tipo de cocina en la tarjeta
        tipo_cocina = destination.get("tipo_cocina", "Tipo de cocina no disponible")
        lbl_tip_cocina = customtkinter.CTkLabel(master=tarj_destinos, text="Tipo de Cocina: " + tipo_cocina,
                                                font=("Roboto Condensed", 12), text_color="black")
        lbl_tip_cocina.place(relx=0.36, rely=0.33)

        # Creo un boton para mostrar el destino en el mapa
        btn_mostrar_coordenadas = customtkinter.CTkButton(master=tarj_destinos,
                                                          text="Ubicacion",
                                                          command=lambda dest=destination: self.show_coordinates_on_map(dest),
                                                          corner_radius=30,
                                                          text_color="white",
                                                          font=("Roboto Condensed", 12),
                                                          fg_color="#333333", width=30)
        btn_mostrar_coordenadas.place(relx=0.36, rely=0.65)

        # Creo un boton para mostrar una ventana emergente con los detalles del destino
        btn_mostrar_detalles = customtkinter.CTkButton(master=tarj_destinos,
                                                       text="Detalles",
                                                       command=lambda dest=destination: self.show_details(dest),
                                                       corner_radius=30,
                                                       text_color="white",
                                                       font=("Roboto Condensed", 12),
                                                       fg_color="#333333", width=30)
        btn_mostrar_detalles.place(relx=0.685, rely=0.65)

        # Aqui creo la carta que se encuentra en buscar destinos
        frame_carta_buscar = customtkinter.CTkFrame(self.der_scroll_busc, fg_color="white", corner_radius=10,
                                            width=250, height=100)
        frame_carta_buscar.pack(pady=10, padx=5, fill="x")

        imagen_lbl_busc = customtkinter.CTkLabel(master=frame_carta_buscar, text="",
                                        image=image)
        imagen_lbl_busc.place(relx=0.03, rely=0.08)

        # Mostramos el nombre del destino
        get_destino_busc = destination.get("nombre", "Nombre no disponible")
        lbl_nombre_dest_busc = customtkinter.CTkLabel(master=frame_carta_buscar, text=get_destino_busc,
                                             font=("Roboto Condensed", 16, "bold"),
                                             text_color="black")
        lbl_nombre_dest_busc.place(relx=0.36, rely=0.08)

        # Mostramos el tipo de cocina
        get_cocina_busc = destination.get("tipo_cocina", "Tipo de cocina no disponible")
        lbl_cocina_dest_busc = customtkinter.CTkLabel(master=frame_carta_buscar, 
                                                      text="Tipo de Cocina: " + get_cocina_busc,
                                                      font=("Roboto Condensed", 12), text_color="black")
        lbl_cocina_dest_busc.place(relx=0.36, rely=0.33)

        btn_mostrar_detalles = customtkinter.CTkButton(master=frame_carta_buscar,
                                                       text="Detalles",
                                                       command=lambda dest=destination: self.show_details(dest),
                                                       corner_radius=30,
                                                       text_color="white",
                                                       font=("Roboto Condensed", 12),
                                                       fg_color="#333333", width=30)
        btn_mostrar_detalles.place(relx=0.36, rely=0.65)

        btn_mostrar_reviews = customtkinter.CTkButton(master=frame_carta_buscar,
                                                      text="Reviews",
                                                      command=lambda dest=destination: self.show_reviews(dest),
                                                      corner_radius=30,
                                                      text_color="white",
                                                      font=("Roboto Condensed", 12),
                                                      fg_color="#333333", width=30)
        btn_mostrar_reviews.place(relx=0.66, rely=0.65)

    def cancelar_filtros(self):
        """Cancelo la busqueda a traves de los filtros"""
        self.menu_opciones_cocina.set("Cocina")
        self.menu_opciones_ingre.set("Ingredientes")
        self.menu_opciones_precio_min.set("Precio MIN")
        self.menu_opciones_precio_max.set("Precio MAX")
        self.menu_opciones_estre.set("Puntuación")

        # Carga los datos desde el json
        with open(json_dir, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        # Crea las tarjetas para cada destino
        for widget in self.der_scroll_busc.winfo_children():
            widget.destroy()
        for destination in data:
            self.crea_tarj_desti(destination)

    def cancelar_busqueda(self):
        """Cancelo la busqueda a traves del entry"""
        # Carga los datos desde el json
        with open(json_dir, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        # Crea las tarjetas para cada destino
        for widget in self.der_scroll_busc.winfo_children():
            widget.destroy()
        for destination in data:
            self.crea_tarj_desti(destination)

        self.entry_nom_busc.delete(0, tk.END)

    def aplicar_filtros(self):
        """Obtengo los valores seleccionados en los filtros"""
        # Obtener los valores seleccionados en los menús desplegables y el campo de entrada
        destinos_filtrados = []

        tipo_cocina = self.menu_opciones_cocina.get()
        ingrediente = self.menu_opciones_ingre.get()
        precio_mini = self.menu_opciones_precio_min.get()
        precio_maxi = self.menu_opciones_precio_max.get()
        puntuacioni = self.menu_opciones_estre.get()

        with open(json_dir, encoding="utf-8") as file:
            destinos_data = json.load(file)

        if tipo_cocina == "Cocina" and ingrediente == "Ingredientes" and precio_mini == "Precio MIN" and \
            precio_maxi == "Precio MAX" and puntuacioni == "Puntuación":
            messagebox.showerror("Error", "Seleccione minimo 1(uno) filtro.")
        else:
            for dest_dato in destinos_data:
                if ((tipo_cocina == "Cocina") or (dest_dato["tipo_cocina"] == tipo_cocina)) and \
                        ((ingrediente == "Ingredientes") or (ingrediente in dest_dato["ingredientes"])) and \
                        ((precio_mini == "Precio MIN") or (int(str(precio_mini)) >= dest_dato["precio_minimo"])) and \
                        ((precio_maxi == "Precio MAX") or (int(str(precio_maxi)) <= dest_dato["precio_maximo"])) and \
                        ((puntuacioni == "Puntuación") or (int(str(puntuacioni)) == dest_dato["popularidad"])):
                    destinos_filtrados.append(dest_dato)

            if len(destinos_filtrados) == 0:
                messagebox.showerror("Error", "No hubo coincidencias.")
                self.cancelar_filtros()
            else:
                # Borro cualquier tarjeta existente en el scroll para colocar las coincidencias de la busqueda
                for widget in self.der_scroll_busc.winfo_children():
                    widget.destroy()
                # Mostrar los destinos encontrados en tarjetas y en el mapa
                for destino in destinos_filtrados:
                    # Crear tarjeta y mostrar información (código de la tarjeta aquí...)
                    self.crea_tarj_desti(destino)

                    # Cargar la ubicación en el mapa
                    coordenadas = [float(coord.strip()) for coord in destino["coordenadas"].split(",")]
                    self.der_buscar_mapa.set_position(coordenadas[0], coordenadas[1])

    def buscar_destinos_por_nombre(self):
        """Busco los destinos que fueron ingresados en el entry"""
        nombre_buscado = self.entry_nom_busc.get().lower().capitalize()

        with open(json_dir, encoding="utf-8") as file:
            destinos_data = json.load(file)

        resultados = []

        if str(nombre_buscado) == "":
            messagebox.showerror("Error", "Ingrese como minímo 1(una) letra.")
            self.entry_nom_busc.delete(0, tk.END)
        else:
            for dest_dato in destinos_data:
                if nombre_buscado in dest_dato["nombre"].lower().capitalize():
                    resultados.append(dest_dato)

            if len(resultados) == 0:
                messagebox.showerror("Error", "No hubo coincidencias.")
            else:
                for widget in self.der_scroll_busc.winfo_children():
                    widget.destroy()
                # Mostrar los destinos encontrados en tarjetas y en el mapa
                for resultado in resultados:
                    # Crear tarjeta y mostrar información
                    self.crea_tarj_desti(resultado)

                    # Cargar la ubicación en el mapa
                    coordenadas = [float(coord.strip()) for coord in resultado["coordenadas"].split(",")]
                    self.der_buscar_mapa.set_position(coordenadas[0], coordenadas[1])

    def cargar_datos_json_en_reviews(self):
        """Funcion encargada de cargar los datos en el scrollbarFrame de Reviews"""
        # Cargar los datos desde el archivo JSON
        with open(json_rese, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        # Crear las tarjetas para cada destino culinario
        for destination in data:
            self.crear_tarj_reviews(destination)

    def crear_tarj_reviews(self, destination):
        """Creo las tarjetas que van a ser utilizadas en los reviews"""
        # Creamos un Frame para contener los datos del destino en el frame que esta en Reviews
        tarj_reviews = customtkinter.CTkFrame(self.der_scroll_revie, fg_color="white", corner_radius=10,
                                              width=250, height=150)
        tarj_reviews.pack(pady=10, padx=5, fill="x")

        # Mostramos el nombre del destino
        nombre_revie = destination.get("username", "Nombre no disponible")
        lbl_nombre_revie = customtkinter.CTkLabel(master=tarj_reviews, text=nombre_revie,
                                                  font=("Roboto Condensed", 18, "bold"),
                                                  text_color="black")
        lbl_nombre_revie.place(relx=0.030, rely=0.010)

        # Mostramos el nombre del destino
        destino_revie = destination.get("destino", "Tipo de cocina no disponible")
        lbl_review_revie = customtkinter.CTkLabel(master=tarj_reviews, text=destino_revie,
                                                font=("Roboto Condensed", 18), text_color="black")
        lbl_review_revie.place(relx=0.030, rely=0.20)

        # Mostramos la reseña almacenada
        resena_revie = destination.get("resena", "Tipo de cocina no disponible")
        lbl_resena_revie = customtkinter.CTkTextbox(master=tarj_reviews, width=270, height=80,
                                          font=("Roboto Condensed", 13), fg_color="#333333",
                                          text_color="white")
        lbl_resena_revie.place(relx=0.030, rely=0.40)
        lbl_resena_revie.insert("0.0", resena_revie)

        # Mostramos la calificacion almacenada
        califi_revie = destination.get("calificacion", "Tipo de cocina no disponible")
        lbl_califi_revie = customtkinter.CTkLabel(master=tarj_reviews, text=califi_revie + " ★",
                                               font=("Roboto Condensed", 18), text_color="black")
        lbl_califi_revie.place(relx=0.88, rely=0.12)

    def cargar_datos_json_en_actividades(self):
        """Cargo los datos de los eventos que se van a realizar"""
        # Obtener la ruta absoluta del directorio actual del archivo Python
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargar los datos desde el archivo JSON de eventos
        json_even = os.path.join(current_dir, "..", "data", "eventos.json")
        with open(json_even, "r", encoding="utf-8") as json_file:
            data_eventos = json.load(json_file)

        # Cargar los datos desde el archivo JSON de destinos
        json_destinos = os.path.join(current_dir, "..", "data", "destinos.json") 
        with open(json_destinos, "r", encoding="utf-8") as json_file:
            data_destinos = json.load(json_file)

        # Crear un diccionario para almacenar las rutas de las imágenes por nombre de destino
        rutas_imagenes = {imagen["nombre"]: imagen["imagen"] for imagen in data_destinos}
        coordenadas_y_nombre = {destino["nombre"]: {
            "coordenadas": destino["coordenadas"],
            "nombre": destino["nombre"]
        } for destino in data_destinos}

        # Crear las tarjetas para cada evento
        for evento in data_eventos:
            self.crear_tarj_acti(evento, rutas_imagenes, coordenadas_y_nombre)


    def crear_tarj_acti(self, destinationn, rutas_imagenes, coordenadas_y_nombre):
        """Creo las tarjetas que van a ser utilizadas en los eventos"""
        # Creamos un Frame para contener los datos del destino
        tarj_destinos = customtkinter.CTkFrame(self.der_scroll_act, fg_color="white", corner_radius=10,
                                               width=250, height=110)
        tarj_destinos.pack(pady=10, padx=5, fill="x")

        # Muestro el nombre del destino en la tarjeta
        nombre_dest = destinationn.get("nombre", "Nombre no disponible")
        lbl_nombre_dest = customtkinter.CTkLabel(master=tarj_destinos, text=nombre_dest,
                                                 font=("Roboto Condensed", 16, "bold"),
                                                 text_color="black")
        lbl_nombre_dest.place(relx=0.36, rely=0.001)

        # Muestro el evento en la tarjeta
        nom_evento = destinationn.get("evento", "Evento no disponible")
        lbl_nom_evento = customtkinter.CTkLabel(master=tarj_destinos, text=nom_evento,
                                                font=("Roboto Condensed", 12), text_color="black")
        lbl_nom_evento.place(relx=0.36, rely=0.21)

        # Muestro la fecha en la tarjeta
        fecha = destinationn.get("fecha", "Fecha no disponible")

        fecha_salida = "%d/%m/%Y"
        hora_salida = "%H:%M"

        fecha_objeto = datetime.fromisoformat(fecha)
        fecha_legible = fecha_objeto.strftime(fecha_salida)
        hora_legible = fecha_objeto.strftime(hora_salida)

        fecha_lbl = customtkinter.CTkLabel(master=tarj_destinos, text=fecha_legible,
                                           font=("Roboto Condensed", 13), text_color="black")
        fecha_lbl.place(relx=0.36, rely=0.41)

        hora_lbl = customtkinter.CTkLabel(master=tarj_destinos, text=hora_legible,
                                          font=("Roboto Condensed", 13), text_color="black")
        hora_lbl.place(relx=0.76, rely=0.41)

        # Creo un boton para mostrar la ubicación en el mapa
        btn_mostrar_coordenadas = customtkinter.CTkButton(master=tarj_destinos,
                                                          text="Ubicación",
                                                          corner_radius=30,
                                                          text_color="white",
                                                          font=("Roboto Condensed", 12),
                                                          fg_color="#333333", width=165)
        btn_mostrar_coordenadas.place(relx=0.36, rely=0.67)

        if nombre_dest in rutas_imagenes:
            ruta_imagen = rutas_imagenes[nombre_dest]
            nombre_dest_event = coordenadas_y_nombre.get(nombre_dest)
            if nombre_dest_event:
                coorde_event = nombre_dest_event["coordenadas"]
                direccion_event = nombre_dest_event["nombre"]
                btn_mostrar_coordenadas.configure(
                    command=lambda coord=coorde_event, dire=direccion_event: self.show_coordinates_evento(coord, dire)
                )
                # Cargar la imagen y crear un label para mostrarla
                imagen_path = os.path.join(direccion_actual, "..", "assets", ruta_imagen)

                image = customtkinter.CTkImage(light_image=Image.open(imagen_path),
                                               dark_image=Image.open(imagen_path),
                                               size=(87, 87))
                image_lbl_exp = customtkinter.CTkLabel(master=tarj_destinos, text="",
                                                       image=image)
                image_lbl_exp.place(relx=0.02, rely=0.1225)
            else:
                print(f"No se encontró información para el destino: {nombre_dest}")
        else:
            print(f"No se encontró imagen para el destino: {nombre_dest}")

    def show_coordinates_on_map(self, destination):
        """Funcion que muestra las coordenadas del destino en el mapa"""
        # Obtenemos las coordenadas del destino desde el JSON
        coordenadas_json = destination.get("coordenadas")
        nombre_json = destination.get("nombre")
        if coordenadas_json:
            coordenadas = [float(coord.strip()) for coord in coordenadas_json.split(",")]
            self.der_explorar_mapa.set_marker(coordenadas[0], coordenadas[1], text=nombre_json,
                                              marker_color_circle="white")
            self.der_explorar_mapa.set_position(coordenadas[0], coordenadas[1])
            self.der_explorar_mapa.set_zoom(16)

    def show_coordinates_evento(self, coordenadas, direccion):
        """Funcion que muestra las coordenadas del destino en el mapa"""
        coordenadas = [float(coord.strip()) for coord in coordenadas.split(",")]
        self.der_explorar_mapa.set_marker(coordenadas[0], coordenadas[1], text=direccion,
                                          marker_color_circle="white")
        self.der_explorar_mapa.set_address(direccion)
        self.der_explorar_mapa.set_position(coordenadas[0], coordenadas[1])
        self.der_explorar_mapa.set_zoom(16)

    def show_details(self, destination):
        """Funcion que muestra los detalles en una Messagebox"""
        mensaje = f"\t\t{destination.get('nombre')}\n"
        mensaje += f"Cocina: {destination.get('tipo_cocina')}\n"
        mensaje += f"Ingredientes: {', '.join(destination.get('ingredientes'))}\n"
        mensaje += f"Precio Min: ${destination.get('precio_minimo')}   "
        mensaje += f"Precio Max: ${destination.get('precio_maximo')}\n"
        mensaje += f"Popularidad: {destination.get('popularidad')} estrellas\n"
        mensaje += f"Disponibilidad: {'Disponible' if destination.get('disponibilidad') else 'No disponible'}\n"
        mensaje += f"Coordenadas: {destination.get('coordenadas')}\n"
        mensaje += f"Dirección: {destination.get('direccion')}"
        # Mostrar el messagebox
        messagebox.showinfo("Información del Restaurante", mensaje, icon='info', type='ok')

    def show_reviews(self, destination):
        """Funcion que muestra los detalles en una Messagebox"""

        reviews_destino = []

        mensaje = destination.get('nombre')
        # Mostrar el messagebox
        self.entry_desac.configure(state="normal")
        self.mostrar_frame_revi()
        self.entry_desac.delete(0, tk.END)
        self.entry_desac.insert(0, mensaje)
        self.entry_desac.configure(state="disabled")

        self.entry_nom_.configure(state="normal")
        self.entry_nom_.delete(0, tk.END)
        self.entry_nom_.insert(0, self.user_iniciado)
        self.entry_nom_.configure(state="disabled")

        with open(json_rese, "r", encoding="utf-8") as json_file:
            data_destinos = json.load(json_file)

        for reviews in data_destinos:
            if reviews["destino"] == mensaje:
                reviews_destino.append(reviews)

        for widget in self.der_scroll_revie.winfo_children():
            widget.destroy()

        for review in reviews_destino:
            self.crear_tarj_reviews(review)

    def guardar_resena(self):
        """Funcion encargada de guardar las reseñas ingresadas"""
        reviews_destino = []

        mensaje = self.entry_desac.get()

        destino = self.entry_desac.get()
        resena = self.txt_rese.get("1.0", "end-1c")
        calificacion = self.menu_estre_revie.get()

        if not destino or not resena or calificacion == "Puntuacion":
            messagebox.showerror("Error", "Complete los campos")


        nueva_resena = {
            "id": self.user_id_iniciado,
            "username": self.user_iniciado,
            "destino": destino,
            "resena": resena,
            "calificacion": calificacion
        }

        try:
            with open(json_rese, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(nueva_resena)

        with open(json_rese, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        # Limpiar los campos después de guardar la reseña
        self.entry_nom_.delete(0, "end")
        self.txt_rese.delete("1.0", "end")
        self.menu_estre_revie.set("Puntuacion")

        with open(json_rese, "r", encoding="utf-8") as json_file:
            data_destinos = json.load(json_file)

        for reviews in data_destinos:
            if reviews["destino"] == mensaje:
                reviews_destino.append(reviews)

        for widget in self.der_scroll_revie.winfo_children():
            widget.destroy()

        for review in reviews_destino:
            self.crear_tarj_reviews(review)

    def cargar_usuarios(self):
        """Cargar los usuarios a traves del json"""
        try:
            with open(json_usuarios, "r", encoding="utf-8") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []

    def verificar(self, username, password):
        """Verificar si los datos son validos"""
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return user["id"]
        return None

    def iniciar_sesion(self):
        """Funcion encargada de iniciar sesion con los datos obtenidos"""
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
        """Funcion encargada de registrar un usuario"""
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
        """Funcion encargada de guardar los datos del usuario en el json"""
        with open(json_usuarios, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=2)

    def cerrar_sesion(self):
        """Funcion encargada de cerrar sesion cuando se presiona el boton"""
        self.izq_frame.grid_forget()
        self.der_explorar.grid_forget()
        self.der_buscar.grid_forget()
        self.der_review.grid_forget()
        self.der_planificar.grid_forget()

        self.izq_frame_inic.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
        self.izq_frame_inic.grid_rowconfigure(5, weight=1)

        self.der_login.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))

        self.user_id_iniciado = ""
        self.user_iniciado = ""

    def regist(self):
        self.der_regist.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
        self.izq_frame_inic.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
        self.izq_frame_inic.grid_rowconfigure(5, weight=1)

    def volver(self):
        self.der_regist.grid_forget()

        self.der_login.grid(row=0, column=1, sticky="nsew", pady=10, padx=(5, 10))
        self.izq_frame_inic.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 5))
        self.izq_frame_inic.grid_rowconfigure(5, weight=1)