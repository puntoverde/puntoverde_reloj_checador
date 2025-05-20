from datetime import date, datetime, timedelta
import flet as ft
from flet_route import Params,Basket
from apartados_dao import ApartadoDao
import moment

def ApartadoEquiposDetalleView(page:ft.Page,params:Params,basket:Basket):
    print(params)
    print(basket)

    def fnAddEquipo(equipo_):
        basket.equipo=equipo_
        page.go("/login")

    id_espacio_deportivo=basket.id_espacio_deportivo

    equipo_apartados=ApartadoDao.get_equipo_apartado(params.id_equipo)

    espacio_deportivos_map=map(lambda i:
                               ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(content=ft.Row([
        # ft.Image(src="images/raqueta-de-tenis.png",width=100,),
        ft.Image(src=i["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(f"{i['nombre']}",size=30),
            ft.Text(i["duracion_prestamo"]),
            ft.Container(border_radius=10, padding=ft.padding.only(top=2,bottom=2,left=5,right=5),bgcolor=ft.Colors.AMBER_100,content=ft.Row([ft.Text(i["fecha_inicio"]),ft.Text(" a "),ft.Text(i["fecha_fin"])],alignment=ft.MainAxisAlignment.CENTER))
            # ft.Container(bgcolor=ft.Colors.AMBER_100,content=ft.Row([ft.Text(fecha_inicio.strftime("%H:%M")),ft.Text(" a "),ft.Text(fecha_fin.strftime("%H:%M"))],alignment=ft.MainAxisAlignment.CENTER))
        ])
    ]),padding=5)),equipo_apartados)

    
    page.bgcolor=ft.colors.WHITE
    page.padding=20
    images = ft.Row(
        wrap=True,
        scroll=ft.ScrollMode.AUTO,
       alignment=ft.alignment.center,
       controls=espacio_deportivos_map
    )

    # esta libre tengo que llamara a el equipo
    if(len(equipo_apartados)==0):

        equipo_find=ApartadoDao.get_equipo_by_id(params.id_equipo)
        print(equipo_find)
        nombre=equipo_find["nombre"]
        tiempo_=equipo_find["duracion_prestamo"]
        fecha_inicio=datetime.now()+timedelta(minutes=5)
        fecha_fin=datetime.now()+timedelta(minutes=tiempo_)+timedelta(minutes=5)


        equipo_find["fecha_registro"]= datetime.now()
        equipo_find["fecha_inicio"]= fecha_inicio    
        equipo_find["fecha_fin"]= fecha_fin

        card_equipo=ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(on_click=lambda _:fnAddEquipo(equipo_find),content=ft.Row([
        ft.Image(src=equipo_find["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(nombre,size=30),
            ft.Text(tiempo_),
            ft.Container(border_radius=10, padding=ft.padding.only(top=2,bottom=2,left=5,right=5),bgcolor=ft.Colors.BLUE_100,content=ft.Row([ft.Text(fecha_inicio.strftime("%H:%M")),ft.Text(" a "),ft.Text(fecha_fin.strftime("%H:%M"))],alignment=ft.MainAxisAlignment.CENTER))
        ])
        ]),padding=5))
        
        images.controls.append(card_equipo)

    elif(len(equipo_apartados)==1):
        print("fecha del ultimo apartado")
        nombre=equipo_apartados[0]["nombre"]
        tiempo_=equipo_apartados[0]["duracion_prestamo"]
        fecha_inicio=datetime.strptime(f"{date.today()} {equipo_apartados[0]['fecha_fin']}", "%Y-%m-%d %H:%M:%S")+timedelta(minutes=5)
        fecha_fin=datetime.strptime(f"{date.today()} {equipo_apartados[0]['fecha_fin']}", "%Y-%m-%d %H:%M:%S")+timedelta(minutes=tiempo_)+timedelta(minutes=5)

        equipo_find=equipo_apartados[0]
        equipo_find["fecha_registro"]= datetime.now
        equipo_find["fecha_inicio"]= fecha_inicio 	    
        equipo_find["fecha_fin"]= fecha_fin

        card_equipo=ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(on_click=lambda _:fnAddEquipo(equipo_find),content=ft.Row([
        ft.Image(src=equipo_find["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(nombre,size=30),
            ft.Text(f"duracion prestamo {tiempo_}"),
            ft.Container(border_radius=10, padding=ft.padding.only(top=2,bottom=2,left=5,right=5),bgcolor=ft.Colors.BLUE_100,content=ft.Row([ft.Text(fecha_inicio.strftime("%H:%M")),ft.Text(" a "),ft.Text(fecha_fin.strftime("%H:%M"))],alignment=ft.MainAxisAlignment.CENTER))
            
        ])
        ]),padding=5))

        images.controls.append(card_equipo)
    
    elif(len(equipo_apartados)==2):
        print("fecha del ultimo apartado")
        nombre=equipo_apartados[1]["nombre"]
        tiempo_=equipo_apartados[1]["duracion_prestamo"]
        fecha_inicio=datetime.strptime(f"{date.today()} {equipo_apartados[1]['fecha_fin']}", "%Y-%m-%d %H:%M:%S")+timedelta(minutes=5)
        fecha_fin=datetime.strptime(f"{date.today()} {equipo_apartados[1]['fecha_fin']}", "%Y-%m-%d %H:%M:%S")+timedelta(minutes=tiempo_)+timedelta(minutes=5)

        equipo_find=equipo_apartados[1]
        equipo_find["fecha_registro"]= datetime.now
        equipo_find["fecha_inicio"]= fecha_inicio 	    
        equipo_find["fecha_fin"]= fecha_fin

        card_equipo=ft.Card(width=400,height=150,color=ft.colors.WHITE,content=ft.Container(on_click=lambda _:fnAddEquipo(equipo_find),content=ft.Row([
        ft.Image(src=equipo_find["ruta_app"],width=100,),
        ft.Column(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, 
                 controls=[
            ft.Text(nombre,size=30),
            ft.Text(f"duracion prestamo {tiempo_}"),
            ft.Container(border_radius=10, padding=ft.padding.only(top=2,bottom=2,left=5,right=5),bgcolor=ft.Colors.BLUE_100,content=ft.Row([ft.Text(fecha_inicio.strftime("%H:%M")),ft.Text(" a "),ft.Text(fecha_fin.strftime("%H:%M"))],alignment=ft.MainAxisAlignment.CENTER))
            
        ])
        ]),padding=5))
        
        images.controls.append(card_equipo)


    content_=ft.Container(
        expand=True,
        bgcolor=ft.colors.GREY_200,
        border_radius=30,
        padding=20,
        content=images
    )

    appbar_ = ft.AppBar(
        # leading=ft.Icon(ft.icons.HOME),
        leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,icon_color="white",
                    icon_size=20,
                    tooltip="Pause record",on_click=lambda _: page.go("/equipos/%s" %id_espacio_deportivo)),
        leading_width=50,
        title=ft.Text("Apartados Tenis"),
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
        "equipos/:id_equipo/apartado",
        controls=[appbar_,content_]
    )