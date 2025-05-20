import flet as ft
from flet_route import Params,Basket
from apartados_dao import ApartadoDao

def EspacioDeportivoView(page:ft.Page,params:Params,basket:Basket):
    print(params)
    print(basket)

    espacio_deportivos=ApartadoDao.get_espacio_deportivo()
    espacio_deportivos_map=map(lambda i:ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(on_click=lambda _: page.go("/equipos/%s" %i["cve_espacio_deportivo"]),content=ft.Row([
        # ft.Image(src="/images/raqueta-de-tenis.png",width=100,),
        ft.Image(src=i["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(i["nombre"],size=30),            
            ft.Divider(),
            ft.Text(i["ubicacion"]),
        ])
    ]),padding=5)),espacio_deportivos)

    page.bgcolor=ft.colors.WHITE
    page.padding=20
    images = ft.Row(
        wrap=True,
        scroll=ft.ScrollMode.AUTO,
       alignment=ft.alignment.center,
       controls=espacio_deportivos_map
    )

    content_=ft.Container(
        expand=True,
        bgcolor=ft.colors.GREY_200,
        border_radius=30,
        padding=20,
        content=images
    )
    

    return ft.View(
        "/",
        controls=[content_]       
    )