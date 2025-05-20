import flet as ft
from flet_route import Params,Basket
from apartados_dao import ApartadoDao

def EquipoView(page:ft.Page,params:Params,basket:Basket):
    print(params)
    print(basket)

    basket.id_espacio_deportivo=params.id_espacio_deportivo

    equipos_=ApartadoDao.get_equipos_by_espacio_deportivo(params.id_espacio_deportivo)
    equipos_map=map(lambda i:
                               ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(on_click=lambda _: page.go("/equipos/%s/apartado" %i["cve_equipo"]),content=ft.Row([
        ft.Image(src=i["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(i["nombre"],size=30),
            ft.Text(f"{i['duracion_prestamo']} minutos"),
            ft.Container(border_radius=10, padding=ft.padding.only(top=2,bottom=2,left=5,right=5), bgcolor=ft.colors.GREEN_200 if ApartadoDao.get_hora_disponible(i["cve_equipo"])=="A" else ft.Colors.AMBER_200,content=ft.Text("Dispobible ahora" if ApartadoDao.get_hora_disponible(i["cve_equipo"])=="A" else f" Disponible hasta {ApartadoDao.get_hora_disponible(i['cve_equipo'])}"))
            
        ])
    ]),padding=5)),equipos_)

    page.bgcolor=ft.colors.WHITE
    page.padding=20
    images = ft.Row(
        wrap=True,
        scroll=ft.ScrollMode.AUTO,
       alignment=ft.alignment.center,
       controls=equipos_map
    )


    content_=ft.Container(
        expand=True,
        bgcolor=ft.colors.GREY_200,
        border_radius=30,
        padding=20,
        content=images
    )

    appbar_ = ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,icon_color="white",
                    icon_size=20,
                    tooltip="Pause record",on_click=lambda _: page.go("/")),
        leading_width=50,
        title=ft.Text("Zona de equipos en appbar"),
        center_title=False,
        bgcolor=ft.colors.GREEN,
        actions=[
          
            ft.PopupMenuButton(
                icon=ft.icons.MENU,
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    # ft.PopupMenuItem(text="Item 2"),
                    # ft.PopupMenuItem(text="Item 3"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False
                    ),
                ]
            ),
        ],
    )


    return ft.View(
        # "/equipos/:id_espacio_deportivo",     
        controls=[appbar_,content_]
    )