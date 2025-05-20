from mysql_conexion import Conexion
import time
import moment
import datetime as dt

class ApartadoDao:

    @staticmethod
    def get_espacio_deportivo():
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                       SELECT
                            espacio_deportivo.cve_espacio_deportivo,
                            espacio_deportivo.nombre,
                            espacio_deportivo.descripcion,
                            imagenes.ruta_app,
                            espacio_deportivo.ubicacion,
                            espacio_deportivo.estatus
                        FROM espacio_deportivo
                        INNER JOIN imagenes ON espacio_deportivo.cve_imagen = imagenes.cve_imagen
                        INNER JOIN espacio_deportivo_horario ON espacio_deportivo_horario.cve_espacio_deortivo = espacio_deportivo.cve_espacio_deportivo
                        WHERE espacio_deportivo.estatus = 1 AND espacio_deportivo.terminal IN (1) AND WEEKDAY(NOW()) = espacio_deportivo_horario.dia_semana  AND now() >= espacio_deportivo_horario.hora2 AND now() <= espacio_deportivo_horario.hora3

                       """)
                    #    WHERE espacio_deportivo.estatus = 1 AND espacio_deportivo.terminal IN (1) AND WEEKDAY(NOW()) = espacio_deportivo_horario.dia_semana  AND now() >= espacio_deportivo_horario.hora1 AND now() <= espacio_deportivo_horario.hora2
        data=cursor.fetchall()
        
        con.close_conexion()
        return data
    
    @staticmethod
    def get_equipos_by_espacio_deportivo(id_espacio_deportivo):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                        SELECT 
                            equipo.cve_equipo, 
                            equipo.cve_espacio_deportivo, 
                            equipo.nombre, 
                            equipo.descripcion, 
                            equipo.min_socios, 
                            equipo.duracion_prestamo, 
                            imagenes.ruta_app, 
                            equipo.estatus 
                        FROM equipo 
                        INNER JOIN imagenes ON equipo.cve_imagen = imagenes.cve_imagen 
                        WHERE equipo.estatus = 1 AND equipo.cve_espacio_deportivo = %s
                       """,(id_espacio_deportivo,))
        data=cursor.fetchall() 
        con.close_conexion()
        # print(data)
        return data
    
    @staticmethod
    def get_hora_disponible(id_equipo):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                        SELECT * FROM apartados INNER JOIN equipo USING(cve_equipo) WHERE cve_equipo = %s AND fecha_fin > now() AND apartados.estatus = 1
                       """,(id_equipo,))
        data=cursor.fetchall() 
        con.close_conexion()

        if(len(data)==0):
            return "A"
        elif(len(data)==1):            
            hora_final= moment.date(data[0]['fecha_fin']).add(minute=5)
            return f"{hora_final.hours}:{hora_final.minutes}"
        elif(len(data)==2):
            hora_final= moment.date(data[1]['fecha_fin']).add(minute=5)
            return f"{hora_final.hours}:{hora_final.minutes}"
        else:
            hora_final= moment.date(data[2]['fecha_fin']).add(minute=5)
            return f"{hora_final.hours}:{hora_final.minutes}"
    
    @staticmethod
    def get_equipo_apartado(id_equipo):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                        SELECT 
	                        equipo.cve_equipo,
	                        equipo.cve_espacio_deportivo,
	                        equipo.cve_imagen,
	                        equipo.nombre,
	                        equipo.descripcion,
	                        equipo.min_socios,
	                        equipo.duracion_prestamo,
	                        equipo.estatus,
	                        apartados.cve_apartado,
	                        TIME(apartados.fecha_registro) as fecha_registro,
	                        TIME(apartados.fecha_inicio) AS fecha_inicio,
	                        TIME(apartados.fecha_fin) AS fecha_fin,
                            # apartados.fecha_registro,
	                        # apartados.fecha_inicio,
	                        # apartados.fecha_fin,
	                        imagenes.ruta_app 
                        FROM equipo 
                        INNER JOIN imagenes ON equipo.cve_imagen = imagenes.cve_imagen 
                        LEFT JOIN apartados ON apartados.cve_equipo = equipo.cve_equipo 
                        WHERE equipo.cve_equipo = %s AND apartados.fecha_fin > now() AND apartados.estatus = 1 
                        ORDER BY fecha_inicio ASC
                       """,(id_equipo,))
        data=cursor.fetchall() 
        con.close_conexion()
        return data
    
    
    @staticmethod
    def get_equipo_by_id(id_equipo):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                        SELECT 
                            equipo.cve_equipo,
                            equipo.cve_espacio_deportivo,
                            equipo.cve_imagen,
                            equipo.nombre,
                            equipo.descripcion,
                            equipo.min_socios,
                            equipo.duracion_prestamo,
                            equipo.estatus,
                            equipo.motivo_inhabilitacion,
                            imagenes.nombre as nombre_imagen,
                            imagenes.ruta_web,
                            imagenes.ruta_app,
                            imagenes.tipo,
                            imagenes.estatus
                        FROM equipo 
                        INNER JOIN imagenes ON equipo.cve_imagen = imagenes.cve_imagen 
                        WHERE cve_equipo = %s
                       """,(id_equipo,))
        data=cursor.fetchone() 
        con.close_conexion()
        return data
    

    @staticmethod
    def get_socio(numero_accion,clasificacion,posicion):
        # SELECT 
	        # socios.estatus,
	        # acciones.numero_accion,
	        # socios.cve_socio,
	        # IF(huella.huella IS NULL,0,1) AS is_huella,
            # IF(socios.foto_socio IS NULL,0,1) AS is_foto,
	        # huella.maskFinger, 
	        # persona.nombre,	
	        # persona.apellido_paterno,	
	        # persona.apellido_materno,	
	        # persona.sexo,	
	        # socios.correo_electronico,	
	        # socios.fecha_alta, 
	        # socios.posicion
        # FROM 	socios
        # INNER JOIN acciones ON socios.cve_accion = acciones.cve_accion
        # INNER JOIN persona ON socios.cve_persona = persona.cve_persona
        # LEFT JOIN huella ON huella.cveSocio = socios.cve_socio
        # WHERE acciones.numero_accion = 100 AND acciones.clasificacion = 1 AND socios.posicion = 3 AND socios.estatus=1
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(dictionary=True)
        cursor.execute("""
                    SELECT 
                        socios.estatus,
                        acciones.numero_accion,
                        socios.cve_socio,
                        IF(huella.huella IS NULL,0,1) AS is_huella,
                        IF(socios.foto_socio IS NULL,0,1) AS is_foto,
                        huella.maskFinger, 
                        persona.nombre,	
                        persona.apellido_paterno,	
                        persona.apellido_materno,	
                        persona.sexo,	
                        socios.correo_electronico,	
                        socios.fecha_alta, 
                        socios.posicion
                    FROM socios
                    INNER JOIN acciones ON socios.cve_accion = acciones.cve_accion
                    INNER JOIN persona ON socios.cve_persona = persona.cve_persona
                    LEFT JOIN huella ON huella.cveSocio = socios.cve_socio
                    WHERE acciones.numero_accion = %s AND acciones.clasificacion = %s AND socios.posicion = %s AND socios.estatus=1
                       """,(numero_accion,clasificacion,posicion,))
        data=cursor.fetchone()        
        # for base in data:
            # print(base)
        con.close_conexion()
        return data

    @staticmethod
    def get_foto(id_socio):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor()
        # select socios.foto_socio from socios where socios.cve_socio =11499 and socios.estatus=1 limit 1
        cursor.execute("SELECT socios.foto_socio FROM socios WHERE socios.cve_socio=%s AND socios.estatus=1 LIMIT 1",(id_socio,))
        data=cursor.fetchone()
        con.close_conexion()
        return data






    @staticmethod
    def registrar_apartado(id_usuario,id_equipo,tiempo,inicio,fin):
   
        print("en el dao colaborador")
        print(id_usuario)
        print(id_equipo)
        print(tiempo)
        print(inicio)
        print(fin)
        print("en el dao colaborador fin")
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor()            
        cursor.execute("""
                        INSERT INTO apartados(cve_equipo,cve_socio,fecha_registro,fecha_inicio,fecha_fin,estatus) 
                        VALUES (%s, %s, NOW(), %s ,%s,1)
                       """,(id_equipo,id_usuario,inicio,fin,))
        # cursor.execute("""
        #                 INSERT INTO apartados(cve_equipo,cve_socio,fecha_registro,fecha_inicio,fecha_fin,estatus) 
        #                 VALUES (%s, %s, NOW(), (NOW() - INTERVAL(SECOND(NOW())) SECOND) ,((NOW() - INTERVAL(SECOND(NOW())) SECOND) + INTERVAL %s MINUTE),1)
        #                """,(id_equipo,id_usuario,tiempo,))
        id_apartado=cursor.lastrowid

        cursor.execute("""
                        INSERT INTO validacion_apartado(cve_apartado,cve_socio,fecha_registro) VALUES(%s,%s,now())
                       """,(id_apartado,id_usuario,))

        con.conexion.commit()
        # cursor.close()
        con.close_conexion()

        return cursor.rowcount
    

    @staticmethod
    def registrar_apartado_dos(id_usuarios,id_equipo,tiempo,inicio,fin):
        print("en el dao colaborador")        
        print(id_usuarios)
        print(id_equipo)
        print(tiempo)
        print(inicio)
        print(fin)
        print("en el dao colaborador fin")
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor()            
        cursor.execute("""
                        INSERT INTO apartados(cve_equipo,cve_socio,fecha_registro,fecha_inicio,fecha_fin,estatus) 
                        VALUES (%s, %s, NOW(), %s ,%s,1)
                       """,(id_equipo,id_usuarios[0],inicio,fin,))
        id_apartado=cursor.lastrowid

        for u in id_usuarios:
            cursor.execute("""
                        INSERT INTO validacion_apartado(cve_apartado,cve_socio,fecha_registro) VALUES(%s,%s,now())
                       """,(id_apartado,u,))

        con.conexion.commit()
        # cursor.close()
        con.close_conexion()

        return cursor.rowcount
    
    @staticmethod
    def validad_apartado(id_socio):
        # SELECT 
            # apartados.cve_apartado,
            # apartados.fecha_fin,
            # apartados.fecha_inicio
        # FROM punto_verde_v2.apartados 
        # INNER JOIN punto_verde_v2.validacion_apartado ON validacion_apartado.cve_apartado = apartados.cve_apartado
        # WHERE now() < apartados.fecha_fin
        # AND (apartados.cve_socio = 11499 OR validacion_apartado.cve_socio = 11499)
        # AND apartados.estatus = 1

        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor()            
        cursor.execute("""
                        SELECT 
                            apartados.cve_apartado,
                            apartados.fecha_fin,
                            apartados.fecha_inicio
                        FROM punto_verde_v2.apartados 
                        INNER JOIN punto_verde_v2.validacion_apartado ON validacion_apartado.cve_apartado = apartados.cve_apartado
                        WHERE now() < apartados.fecha_fin
                        AND (apartados.cve_socio = %(id_socio)s OR validacion_apartado.cve_socio = %(id_socio)s)
                        AND apartados.estatus = 1
                       """,{'id_socio':id_socio})
    
        data=cursor.fetchone()
        con.close_conexion()

        return data
    
    @staticmethod
    def get_socio_terminal(id_socio):
        con=Conexion()
        con.get_conexion()
        cursor=con.conexion.cursor(named_tuple=True) 
        cursor.execute("""
                        select count(*) as exist from terminal_permiso_colaborador where cve_terminal=1 and cve_socio=%s
                       """,(id_socio,))
        data=cursor.fetchone()
        con.close_conexion()
        return data.exist