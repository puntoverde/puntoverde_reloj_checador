import flet as ft
from apartados_dao import ApartadoDao


def main(page: ft.Page):

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_50,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False,
                    ),
                ]
            ),
        ],
    )

    espacio_deportivos=ApartadoDao.get_espacio_deportivo()
    espacio_deportivos_map=map(lambda i:ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(content=ft.Row([
        ft.Image(src="images/raqueta-de-tenis.png",width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(i["nombre"],size=30),
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
    
    page.add(ft.Container(
        expand=True,
        bgcolor=ft.colors.GREY_200,
        border_radius=30,
        padding=20,
        content=images
    ))

ft.app(main)