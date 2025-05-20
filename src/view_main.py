import flet as ft
from flet_route import Routing,path
from views.espacios_deportivos_view import EspacioDeportivoView # Here IndexView is imported from views/index_view.py
from views.equipos_view import EquipoView # Here NextView is imported from views/next_view.py
from views.apartado_equipos_view import ApartadoEquiposDetalleView # Here NextView is imported from views/next_view.py
from views.login_view import LoginView # Here NextView is imported from views/next_view.py

def main(page: ft.Page):


    appbar_ = ft.AppBar(
        leading=ft.Icon(ft.icons.HOME),
        leading_width=40,
        title=ft.Text(""),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
          
            ft.PopupMenuButton(
                icon=ft.icons.MENU,
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(text="Item 2"),
                    ft.PopupMenuItem(text="Item 3"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False
                    ),
                ]
            ),
        ],
    )

    app_routes = [
        path(
            url="/", # Here you have to give that url which will call your view on mach
            clear=True, # If you want to clear all the routes you have passed so far, then pass True otherwise False.
            view=EspacioDeportivoView # Here you have to pass a function or method which will take page,params and basket and return ft.View (If you are using function based view then you just have to give the name of the function.)
            ), 
        path(url="/equipos/:id_espacio_deportivo", clear=False, view=EquipoView),
        path(url="/equipos/:id_equipo/apartado", clear=False, view=ApartadoEquiposDetalleView),
        path(url="/login", clear=False, view=LoginView),
    ]

    Routing(
        page=page, # Here you have to pass the page. Which will be found as a parameter in all your views
        app_routes=app_routes, # Here a list has to be passed in which we have defined app routing like app_routes
        appbar=appbar_
        )
    
    page.go(page.route)
   

ft.app(target=main)