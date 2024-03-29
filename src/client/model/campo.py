

class Campo():
    
    #Constantes
    LOCACION_RESOURCES = "../../../resources/"
    """Constante string que tiene la ruta basica y plana de la imagen que representa el jugador"""
    IMAGEN_CAMPO = f"{LOCACION_RESOURCES}images/soccer_field"
    """Constante string que tiene el tipo de extencion de la imagen del campo"""
    EXTENCION_DE_IMAGEN = ".jpg"
    
    #Atributos
    """Atributo string que contiene la ruta de la imagen del campo"""
    __ruta_imagen = None
    
    def __init__(self, numero_campo):
        """Constructor que recibe el numero de campo de imagen a cargar, por defecto es el 3"""
        numero_campo = numero_campo if (numero_campo>0 and numero_campo<3) else 1
        self.__ruta_imagen = f"{self.IMAGEN_CAMPO}{numero_campo}{self.EXTENCION_DE_IMAGEN}"
    
    def esta_jugador_dentro_campo(self, coordenadas_campo, coordenadas_jugador, equipo):
        """Metodo que verifica si un jugador esta dentro de las coordenadas del campo.
        Recibe coordenadas_campo y coordenadas_jugador que son un arreglo conteniendo informacion respectiva de las coordenas [x,y]"""
        if equipo=="A":
            campo_x = coordenadas_campo[0]
            campo_y = coordenadas_campo[1]
            jugador_x = coordenadas_jugador[0]
            jugador_y = coordenadas_jugador[1]
            if jugador_x>0 and jugador_x+65<campo_x:
                if jugador_y>3 and jugador_y+60<campo_y:
                    return True
            return False
        elif equipo=="B":
            campo_x = coordenadas_campo[0]
            campo_y = coordenadas_campo[1]
            jugador_x = coordenadas_jugador[0]
            jugador_y = coordenadas_jugador[1]
            if jugador_x>38 and jugador_x+30<campo_x:
                if jugador_y>3 and jugador_y+60<campo_y:
                    return True
            return False
        
    def esta_balon_dentro_campo(self,coordenadas_campo, coordenadas_balon):
        campo_x = coordenadas_campo[0]
        campo_y = coordenadas_campo[1]
        balon_x = coordenadas_balon[0]
        balon_y = coordenadas_balon[1]
        if balon_x>30 and balon_x+40<campo_x:
            if balon_y>4 and balon_y<campo_y:
                return True
        return False
    
    def get_ruta_imagen(self):
        """Metodo que retorna la ruta de la imagen que representa el campo"""
        return self.__ruta_imagen