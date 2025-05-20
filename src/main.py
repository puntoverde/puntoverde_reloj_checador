#nativos
import base64
import io
from io import BytesIO
import threading
import time
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys

#librerias
import flet as ft #marco de material
import cv2 #acceso a acamara
from PIL import Image as ImagePil #visualizar fotos
import numpy as np # es de mnumero
from playsound3 import playsound #el sonido en la aplicacion
from deepface import DeepFace #reconocimiento facial
from cvzone.FaceMeshModule import FaceMeshDetector#wrap de mediapipe
from usuarios_flet_dao import UsuariosFletDao #"gestion de bd 
import serial # para conectar arduino mediante el puerto serial

#librerias para conectar con java 
import jpype
import jpype.imports
# Pull in types
from jpype.types import *

#inicializa la maquina virtual de java
jpype.startJVM(classpath = ["C:\\Users\\Sistemas2\\Documents\\NetBeansProjects\\prueba_puente_python\\dist\\prueba_puente_python.jar"])

#importaciones de java 
# import java
# import javax
# from javax.swing import *
# from java.awt import Window as Windowjv
# from java.awt import *
# from java.util import *
# from java.lang import *
# from java.lang import *

#llamada de las clases del projecto de java 
# from prueba_puente_python import SocioHuellaDAO
# from prueba_puente_python import DigitalPersona
from prueba_puente_python import ToallasMain

#instancias de las clases del proyecto de java
# socioHuellaDao=SocioHuellaDAO()
# dp=DigitalPersona()

#frame para la aplicacion de java 
# frame = None



# variable de guarda el estado de la camara
cap=None
# para iniciar el video, en un while indica que tiene que estar ciclando los fotogramas
init_video=False
#id de colaborador
id_colaborador=0
# variable que gurada el rostro desde bd
rostro_colaborador=None
# inicia en 15 para que no duere mucho no es 0 porque es mod 0 ejemplo mod de 0 % 30 =0 esto tomaria la imagen enseguida
counter=15
# indica que se esta realizando la validacion por parde de deepface es para el tiempo que tarde y no volver a ejecutar otra vez
is_valid_face=False
# se basa es media pipe y es para tomar la distancia y saber que es un rostro humano
detector_cvzone=FaceMeshDetector(maxFaces=1)

#variable que nos dictara como sera la validacion si por rostro o huella 
print_view=1

#busca el path en un build
def resourse_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

#carga el play sound para dar gracias.
def gracias():
        playsound("./src/assets/sound/thank-you-168416.mp3",block=False)        
        # playsound(resourse_path("assets/sound/thank-you-168416.mp3"),block=False)

#es improvisado realizo una verificacion con los dos modelos que se utilizan para que antes que todo se descarguen los modelos
def init_model():
    print("incia carga de los modelos")
    # imagen1=cv2.imread(resourse_path("assets/images/img1.jpg"))
    imagen1=cv2.imread("./src/assets/images/img1.jpg")
    # imagen2=cv2.imread(resourse_path("assets/images/img2.jpg"))
    imagen2=cv2.imread("./src/assets/images/img2.jpg")
    init_model=DeepFace.verify(img1_path=imagen1,img2_path=imagen2,model_name="VGG-Face",detector_backend="mediapipe",threshold=.55)
    print(init_model["distance"])
    print(init_model["verified"])
    init_model2=DeepFace.verify(img1_path=imagen1,img2_path=imagen2,model_name="Facenet512",detector_backend="mediapipe",threshold=.30)
    print(init_model2["distance"])
    print(init_model2["verified"])

    print("fin carga modelos")



def main(page: ft.Page):
    #propiedades de la ventana
    page.title = "Reloj checador v2"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width=900
    page.window.height=900

    #realizo verificaciones de inicio para que cargue de forma forzosa los modelos
    threading.Thread(target=init_model).start()
    
    #es para mostrar la hora 
    now =lambda:time.strftime("%H:%M:%S",time.localtime())


    #bottonsheet componente 
    bs = ft.Ref[ft.BottomSheet]()

    #inicia la camara 
    def init_camara(flag=1):
        global cap,init_video
        #se usa cv2.CAP_DSHOW por que la camara logitech lo necesitaba
        cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #se pone en fullHD
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        init_video=True
        #while para estar leyendo los fotogramas
        while init_video:
            fn_init_video(flag)


    #proceso de pintar y mostrar la imagen con los cambios de distancia y ovalo etc
    def fn_init_video(flag):        
        ret,frame=cap.read()#lee el fotograma 
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)#pone el fotograma a bgr para que se vea correctamente 
        frame=cv2.flip(frame,1)# se pone como espejo
        frame=frame[0:640,460:820]#recorta solo esl centro de la camara y que se vea como celular
        #ejemplo la camara toma 1280 x 720 y pasaremos un recorte de 640 x 360 -- 1280/2=640 ese es el centro y queremos 360 de ancho esto lo dividimos en 2 = 180
        #del punto central es 640-180=460 y 640+180=820 entonces el punto x es 460 a 820 y el punto y es 0 lo mas alto y llegar a 640 

        mask=np.zeros((640, 360),dtype=np.uint8) #se crea un aimagen en negro de la misma dimesion punto en y - x=640 360
        mask=cv2.ellipse(mask,(180,320),(150,200) ,0,0,360,(255),-1)#se crea un ellipse en la imagen de negro llamada mascara 
        mask2=cv2.bitwise_not(mask)##con bitwise solo se muestra el interior  del ovalo

        image_mask_ovalo=cv2.bitwise_and(frame,frame,mask=mask)  

        # fondo=cv2.imread(resourse_path("assets/images/wp.jpeg"))
        fondo=cv2.imread("./src/assets/images/wp.jpeg")
        fondo=fondo[0:640,460:820]
        # imagen que muestra fuera del ovalo y lo convina con fondo para que se vea como opacidad
        image_mask_ovalo_inverso=cv2.addWeighted(frame,0.9,fondo,0.1,0)        
        image_mask_ovalo_inverso=cv2.bitwise_and(image_mask_ovalo_inverso,image_mask_ovalo_inverso,mask=mask2)
        image_final_ovalo=cv2.add(image_mask_ovalo, image_mask_ovalo_inverso)
        
        #1 es que tiene foto y entra a validar
        if flag==1:
            visualizar(image_final_ovalo,frame)
        #en caso contrario muetra para capturar foto y guardar
        else: tomarRostro(image_final_ovalo,frame)

    def visualizar(imagen_,image_origin):
        global counter,is_valid_face
        # busca un rostro con cvzone(mediapipe)
        _,faces_cv_zone=detector_cvzone.findFaceMesh(imagen_,draw=False)
        if faces_cv_zone:
            # el primer rostro encontrado
            face_=faces_cv_zone[0]
            # ojo izq
            pointLeft=face_[145]
            # ojo der
            pointRigth=face_[374]
            #punto de la nariz
            pointNose=face_[4] 
            # proceso para calcular la distanca y guardar en variale d
            w,_=detector_cvzone.findDistance(pointLeft,pointRigth)
            W=6.3
            f=840
            d=(W*f)/w
            cv2.circle(imagen_,pointNose,5,(250, 193, 19),cv2.FILLED)#dibuja circulo en la nariz
            #estas dos llineas dibujan la cruz en medio de la imagen como guia
            cv2.line(imagen_,(180,320),(180,380),(250, 193, 19),2)
            cv2.line(imagen_,(150,350),(210,350),(250, 193, 19),2)

            # valida la distancia entre un rango de 40 a 70 cm de distancia y que la nariz este en el punto central mayor a 150 y menor a 210 en x y mayor a 320 y menor a 380b en y
            if(d>35 and d<70 and pointNose[0]>150 and pointNose[0]<210 and pointNose[1]>320 and pointNose[1]<380):
                #se pinta un rectangulo en la orilla de color amarilllo para indicar que se esta leyendo el rostro
                imagen_=cv2.rectangle(imagen_,(0,0),(360,640),(250, 193, 19),30)
                #inicia con la captura cada 30 segundos y siepre no este ya en proceso una verificacion
                if counter % 30 == 0  and is_valid_face==False:
                    # ejecuta el hilo para verificar pasandole la imagen original
                    threading.Thread(target=match,kwargs={'frame':image_origin}).start()                    
                counter=counter+1
        #proceso para convertir la imagen a base64 y mostrarla 
        im =ImagePil.fromarray(imagen_)
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        imagen_video.src_base64=img_str
        imagen_video.update() 

    def tomarRostro(imagen_,image_origin):
        global counter,is_valid_face
        # busca un rostro con cvzone(mediapipe)
        _,faces_cv_zone=detector_cvzone.findFaceMesh(imagen_,draw=False)
        if faces_cv_zone:
            # el primer rostro encontrado
            face_=faces_cv_zone[0]
            # ojo izq
            pointLeft=face_[145]
            # ojo der
            pointRigth=face_[374]
            #punto de la nariz
            pointNose=face_[4] 
            # proceso para calcular la distanca y guardar en variale d
            w,_=detector_cvzone.findDistance(pointLeft,pointRigth)
            W=6.3
            f=840
            d=(W*f)/w
            cv2.circle(imagen_,pointNose,2,(250, 193, 19),cv2.FILLED)                             
            cv2.line(imagen_,(180,320),(180,380),(250, 193, 19),1)
            cv2.line(imagen_,(150,350),(210,350),(250, 193, 19),1)

            # valida la distancia entre un rango de 40 a 70 cm de distancia y que la nariz este en el punto central mayor a 150 y menor a 210 en x y mayor a 320 y menor a 380b en y
            if(d>35 and d<70 and pointNose[0]>150 and pointNose[0]<210 and pointNose[1]>320 and pointNose[1]<380):
                #se pinta un rectangulo en la orilla de color amarilllo para indicar que se esta leyendo el rostro
                imagen_=cv2.rectangle(imagen_,(0,0),(360,640),(250, 193, 19),30)
                #inicia con la captura cada 30 segundos y siepre no este ya en proceso una verificacion
                if counter % 30 == 0  and is_valid_face==False:
                    # ejecuta el hilo para verificar pasandole la imagen original
                    print("aqui guarda la imagen al colaborador...")         
                    image_origin2=image_origin[50:540,0:460]#recorta solo esl centro de la camara y que se vea como celular         
                    threading.Thread(target=guardar_rostro,kwargs={'frame':image_origin2}).start() 
                counter=counter+1
        #proceso para convertir la imagen a base64 y mostrarla 
        im =ImagePil.fromarray(imagen_)
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        imagen_video.src_base64=img_str
        imagen_video.update()
                

    def setTextInput(e):
        txt_nomina.value="%s%s"%(txt_nomina.value,e)
        txt_nomina.focus()
        txt_nomina.update()

    def clear():
        global init_video,id_colaborador,is_valid_face,counter
        init_video=False#cancela con esto el while que muestra los fotogramas
        id_colaborador=0#se regresa el id de colaborador a 0
        is_valid_face=False#indica que no se esta en proceso de verificacion
        counter=20# se reinicia el contador a el origen 
        # se verifica que la camara no este encendida 
        if cap is not None and cap.isOpened():
            cap.release()

        txt_nomina.value=''#se borra del input la nomina
        txt_nomina.focus()#se regresa el foco
        txt_nombre.value='Nombre de Empleado.'
        
        time.sleep(1)
        imagen_video.src_base64=None
        imagen_video.src=None
        imagen_video.src="images/capture_rostro.png"
        page.update()

    def init_facial():  
        global id_colaborador,rostro_colaborador
        page.close(bs.current)
        image=UsuariosFletDao.get_foto(id_colaborador)
        if(image[0] is not None):
            image_ = ImagePil.open(io.BytesIO(image[0])).convert("RGB")
            rostro_colaborador = np.array(image_)
            init_camara()                
        else: 
            page.snack_bar = ft.SnackBar(content=ft.Text("Empleado con numero "+txt_nomina.value+" no tiene aún foto registrada, se habilita cámara para registrar.",style=ft.TextStyle(size=30,color="#000000")),action="",bgcolor="#F48430",duration=10000)
            page.snack_bar.open = True
            page.update()
            txt_nomina.focus()
            #se registra el rostro porque no tiene rostro el empleado
            init_camara(0)

    def init_fingerprint():
        global id_colaborador
        page.close(bs.current)
        # if(frame is None):
            # Windowjv.System

        # print(toallas_)
        wind__=ToallasMain(id_colaborador)
        print(wind__)
        # if(f1rame is None):
            # frame=ToallasMain()

        wind__.setVisible(True)
        clear()


        # print(Windowjv.getWindows())

        # huella_=socioHuellaDao.getHuellaService(11499)
        # print(huella_)
        # frame.setVisible(True)        
        # frame.setFocusable(True)
        # frame.requestFocus()
        # frame.requestFocusInWindow()
        # frame.requestFocus(True)
        # while True:
            
        #     activo=dp.getActivo()
        #     if activo:
        #         valid=dp.verificarHuella(huella_)
        #         print("valido")
        #         print(valid)
        #         if valid:
        #             print("es valido")                
        #             frame.setVisible(False)
        #         dp.clear()

        #     time.sleep(1)

        
    def buscar(_):
        global id_colaborador,rostro_colaborador,init_video

        if(len(txt_nomina.value)!=4):
            print("no puede buscar debe de ser de 4 digitos incluyendo 0 al inicio ")
            page.snack_bar = ft.SnackBar(content=ft.Text("El número de empleado debe tener 4 dígitos, empezando por cero, si así fuera ejemplo: 0001",style=ft.TextStyle(size=30,color="#000000")),action="",bgcolor="#FFB300",duration=10000)
            page.snack_bar.open = True
            page.update()
            txt_nomina.focus()
            return      

        if cap is not None and cap.isOpened():
            init_video=False
            cap.release()

        tolerancia=UsuariosFletDao.get_tolerancia_entrada(txt_nomina.value)
        print("tolerancia:",tolerancia)

        if(tolerancia is not None and tolerancia["aplica_tiempo"]==1 and tolerancia["flag"]==0):
            print('no puedes acceder')
            # self.msg.configure(text="15 minutos antes de entrada",fg='#F48430')
            page.snack_bar = ft.SnackBar(content=ft.Text("Esperé 15 minutos antes de su entrada para poder checar",style=ft.TextStyle(size=30,color="#000000")),action="",bgcolor="#FFB300",duration=10000)
            page.snack_bar.open = True
            page.update()
            txt_nomina.focus()
            return
        
        data=UsuariosFletDao.get_colaborador(txt_nomina.value)
        if data is not None:
            id_colaborador=data["id_colaborador"]
            txt_nombre.value="%s %s %s" %(data["apellido_paterno"],data["apellido_materno"],data["nombre"])
            txt_nombre.update()
            
            #bottonsheet componente 
            ft.BottomSheet(
                ref=bs,
                on_dismiss=lambda _:print("se cerro"),
                dismissible=False,
                content=ft.Container(
                    width=1300,
                    height=430,
                    padding=50,
                    content=ft.Column(
                        tight=True,
                        controls=[
                            ft.Row(controls=[
                                # ft.Button(content=ft.Image(src="images/facial-recognition_6877256.png",width=260)),
                                ft.Button(content=ft.Image(src="images/facial-recognition_6877256.png",width=260),style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),on_click=lambda _:init_facial()),
                                # ft.Card(content=ft.Image(src="images/facial-recognition_6877256.png",width=260),elevation=4,on_click=init_camara),
                                ft.Button(content=ft.Image(src="images/fingerprint-scan.png",width=260),style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),on_click=lambda _:init_fingerprint()),
                            ]),
                            ft.Row(controls=[
                                ft.Text("1",size=40,width=260,text_align=ft.TextAlign.CENTER),
                                ft.Text("2",size=40,width=260,text_align=ft.TextAlign.CENTER),
                            ]),
                            ft.Text("Elige como autenticarte! 1- rostro 2- huella",size=20),
                            # ft.ElevatedButton("Close bottom sheet", on_click=lambda _: page.close(bs)),
                            ]
                            ),),)
            
            page.open(bs.current)

            # id_colaborador=data["id_colaborador"]
            # txt_nombre.value="%s %s %s" %(data["apellido_paterno"],data["apellido_materno"],data["nombre"])
            # txt_nombre.update()
            
            # image=UsuariosFletDao.get_foto(id_colaborador)
            # if(image[0] is not None):
            #     image_ = Image.open(io.BytesIO(image[0])).convert("RGB")
            #     rostro_colaborador = np.array(image_)
            #     init_camara()                
            # else: 

            #     page.snack_bar = ft.SnackBar(content=ft.Text("Empleado con numero "+txt_nomina.value+" no tiene aún foto registrada, se habilita cámara para registrar.",style=ft.TextStyle(size=30,color="#000000")),action="",bgcolor="#F48430",duration=10000)

            #     page.snack_bar.open = True
            #     page.update()
            #     txt_nomina.focus()
            #     #se registra el rostro porque no tiene rostro el empleado
            #     init_camara(0)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("No existe empleado con este numero "+txt_nomina.value,style=ft.TextStyle(size=30,color="#000000")),action="",bgcolor="#F50057",duration=10000)
            page.snack_bar.open = True
            page.update()
            txt_nomina.focus()
    

    def match(frame):
        global is_valid_face

        # indeica que emepieza la validacion 
        is_valid_face=True

        is_success, im_buf_arr = cv2.imencode(".jpg", cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY))
        byte_im = im_buf_arr.tobytes()

        print("inicia verificacion")
        print(counter)
        # DeepFace.build_model("VGG-Face")
        DeepFace.build_model('VGG-Face')
        data=DeepFace.verify(img1_path=frame,img2_path=rostro_colaborador,model_name="VGG-Face",detector_backend="mediapipe",threshold=.55)
        print("VGG-Face: ")
        print(data["distance"])
        if data is not None and data["verified"]: 
            UsuariosFletDao.registrar_acceso(id_colaborador,byte_im,data["distance"],data["model"],data["threshold"])
            page.snack_bar = ft.SnackBar(content=ft.Text("Gracias",style=ft.TextStyle(size=30)),action="",bgcolor="#00695C",duration=2500)
            page.snack_bar.open = True            
            page.update()
            audio=threading.Thread(target=gracias)
            audio.start()
            time.sleep(3)
            clear()
        else: 
            data2=DeepFace.verify(img1_path=frame,img2_path=rostro_colaborador,model_name="Facenet512",detector_backend="mediapipe",threshold=.30)
            print("Facenet512: ")
            print(data2["distance"])
            if data2 is not None and data2["verified"]:
                UsuariosFletDao.registrar_acceso(id_colaborador,byte_im,data2["distance"],data2["model"],data2["threshold"])
                page.snack_bar = ft.SnackBar(content=ft.Text("Gracias",style=ft.TextStyle(size=30)),action="",bgcolor="#00695C",duration=2500)
                page.snack_bar.open = True            
                page.update()
                audio=threading.Thread(target=gracias)
                audio.start()
                time.sleep(3)
                clear()

        print("finaliza verificacion")
        is_valid_face=False

    def guardar_rostro(frame):
        global is_valid_face

        # indeica que emepieza la validacion 
        is_valid_face=True

        is_success, im_buf_arr = cv2.imencode(".jpg", cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY))
        # is_success, im_buf_arr = cv2.imencode(".jpg",frame)
        byte_im = im_buf_arr.tobytes()

        print("inicia verificacion")
        id=UsuariosFletDao.save_foto(id_colaborador,byte_im)
        page.snack_bar = ft.SnackBar(content=ft.Text("Se registró correctamente la foto del empleado. Vuelva a intentar checar",style=ft.TextStyle(size=30)),action="exito",bgcolor="#5a98de",duration=2500)
        page.snack_bar.open = True            
        page.update()
            # audio=threading.Thread(target=gracias)
            # audio.start()
        time.sleep(3)
        clear()
        print("finaliza verificacion")
        is_valid_face=False

    mytime=ft.Text(value=now(),size=60,weight=ft.FontWeight("bold"),text_align=ft.TextAlign.CENTER,width=300)
    imagen_video=ft.Image(src="images/capture_rostro.png",width=360,height=640,border_radius=10)
    txt_nomina=ft.TextField(hint_text="Numero Empleado",hint_style=ft.TextStyle(size=20),text_align="center",text_size=50,max_length=4,content_padding=ft.Padding(top=2,bottom=2,right=0,left=0),autofocus=True,on_submit=buscar,read_only=True)
    txt_nombre=ft.Text("nombre del colaborador.",theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    btn_buscar=ft.ElevatedButton(content=ft.Icon(name=ft.icons.CHECK,size=40),style=ft.ButtonStyle(shape=ft.CircleBorder()),bgcolor=ft.colors.TEAL_ACCENT,color=ft.colors.WHITE,width=90,height=90,on_click=buscar)

    # def validarActivo():
    #     activo=dp.getActivo()
    #     if activo:
    #         valid=dp.verificarHuella(huella_)
    #         print("valido")
    #         print(valid)
    #         if valid:
    #             print("es valido")
                
    #             frame.setVisible(False)
    #             # frame.dispose()
    #             # jpype.shutdownJVM()
    #             # java.lang.System.exit(0)

                

    #         dp.clear()

    # def runClock():
    #     print("entra a el while")
    #     while True:
    #         mytime.value=now()
    #         mytime.update()
    #         time.sleep(1)

    def on_keyboard(e: ft.KeyboardEvent):
        print(e)
        print(bs.current)
        if((e.key =="Numpad 1" or e.key=="1") and bs.current is not None and bs.current.open):            
            init_facial()            
        elif((e.key =="Numpad 2" or e.key=="2") and bs.current is not None and bs.current.open):        
            init_fingerprint()
        elif(e.key =="Numpad 1" or e.key=="1"):
            print("text 1")
            txt_nomina.value="%s%s"%(txt_nomina.value,1)
            txt_nomina.update()
        elif(e.key =="Numpad 2" or e.key=="2"):
            print("text 2")
            txt_nomina.value="%s%s"%(txt_nomina.value,2)
            txt_nomina.update()
        elif(e.key =="Numpad 3" or e.key=="3"):
            print("text 3")
            txt_nomina.value="%s%s"%(txt_nomina.value,3)
            txt_nomina.update()
        elif(e.key =="Numpad 4" or e.key=="4"):
            print("text 4")
            txt_nomina.value="%s%s"%(txt_nomina.value,4)
            txt_nomina.update()
        elif(e.key =="Numpad 5" or e.key=="5"):
            print("text 5")
            txt_nomina.value="%s%s"%(txt_nomina.value,5)
            txt_nomina.update()
        elif(e.key =="Numpad 6" or e.key=="6"):
            print("text 6")
            txt_nomina.value="%s%s"%(txt_nomina.value,6)
            txt_nomina.update()
        elif(e.key =="Numpad 7" or e.key=="7"):
            print("text 7")
            txt_nomina.value="%s%s"%(txt_nomina.value,7)
            txt_nomina.update()
        elif(e.key =="Numpad 8" or e.key=="8"):
            print("text 8")
            txt_nomina.value="%s%s"%(txt_nomina.value,8)
            txt_nomina.update()
        elif(e.key =="Numpad 9" or e.key=="9"):
            print("text 9")
            txt_nomina.value="%s%s"%(txt_nomina.value,9)
            txt_nomina.update()
        elif(e.key =="Numpad 0" or e.key=="0"):
            print("text 0")
            txt_nomina.value="%s%s"%(txt_nomina.value,0)
            txt_nomina.update()
        elif(e.key =="Enter"):
            print("enter")
            buscar(0)          
        elif(e.key=="Numpad Multiply"):
            clear()

    page.on_keyboard_event=on_keyboard
    

    page.add(
        ft.Column(controls=[
        ft.Row([
                ft.Card(content=
                        ft.Container(content=
                    ft.Column(
                        [
                        ft.Card(content=ft.Container(content=imagen_video),color=ft.colors.BLUE_GREY),
                        ft.Row([
                        ]),
                        
                        
                        ]
                ),padding=5)),
            ft.Column([
                mytime,
                ft.Container(width=300,height=60,bgcolor=ft.colors.BLUE_GREY_100,content=txt_nombre,alignment=ft.alignment.center,border_radius=10,padding=5),
                ft.Container(width=300,content=txt_nomina),
            ft.Row(
            controls=[
                ft.ElevatedButton(text="7",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(7)),
                ft.ElevatedButton(text="8",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(8)),
                ft.ElevatedButton(text="9",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(9)),
            ]
        ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="4",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(4)),
                    ft.ElevatedButton(text="5",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(5)),
                    ft.ElevatedButton(text="6",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(6)),
                ]
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="1",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(1)),
                    ft.ElevatedButton(text="2",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(2)),
                    ft.ElevatedButton(text="3",style=ft.ButtonStyle(shape=ft.CircleBorder(),padding=35,text_style=ft.TextStyle(size=40)),on_click=lambda _:setTextInput(3)),                    
                ]
            ),
            ft.Row(
                 controls=[
                    ft.ElevatedButton(text="0",style=ft.ButtonStyle(shape=ft.CircleBorder(),text_style=ft.TextStyle(size=40)),width=90,height=90,on_click=lambda _:setTextInput(0)),
                    ft.ElevatedButton(content=ft.Icon(name=ft.icons.CLEAR,size=40),style=ft.ButtonStyle(shape=ft.CircleBorder()),bgcolor=ft.colors.RED_ACCENT,color=ft.colors.WHITE,width=90,height=90,on_click=lambda _:threading.Thread(target=clear).start()),
                    btn_buscar,
                ]
            )
            ])
            # )
            
            ],alignment=ft.MainAxisAlignment.CENTER),
        
        ])
    )

    def runClock():
        while True:
            mytime.value=now()
            mytime.update()
            time.sleep(1)
    runClock()

ft.app(target=main,assets_dir="assets")