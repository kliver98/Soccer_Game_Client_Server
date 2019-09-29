from client.model import aplicacion

class Jugador():

    #Constantes
    """Constante string que contiene la ruta basica y plana del recurso de imagen que representa el jugador A, sin numero de imagen ni extension"""
    IMAGEN_JUGADOR_A = f"{aplicacion.LOCACION_RESOURCES}images/playerBlack"
    """Constante string que contiene la ruta basica y plana del recurso de imagen que representa el jugador B, sin numero de imagen ni extension"""
    IMAGEN_JUGADOR_B = f"{aplicacion.LOCACION_RESOURCES}images/playerWhite"
    """Constante string del tipo de extension de las imagenes que representan al jugador"""
    EXTENCION_DE_IMAGEN = ".png"
    """Constante numero que representa que tantos pixeles se mueve el jugador cuando se presiona una tecla"""
    VELOCIDAD = 1
        
    #Atributos
    """Atributo string para identificar al jugador"""
    __usuario = None #Las dos lineas bajas son para hacer las variables privadas
    """Atributo boleano para identificar a que equipo pertenece el jugador"""
    __equipo = None
    """Atributo tupla para almacenar las coordenadas x,y donde esta la imagen del jugador"""
    __coordenadas = None
    """Atributo numero entero para identificar la imagen del juegador. Son tres imagenes para simular el movimiento"""
    __numero_de_imagen = None
    """Atributo numero para identificar el angulo de rotacion de la imagen del jugador"""
    __angulo_de_imagen = None
    
    def __init__(self, usuario, equipo):
        """Constructor que recibe el nombre de usuario y el equipo al cual pertenece"""
        self.__usuario = usuario
        self.__equipo = equipo
        self.__coordenadas = (250,250) #Ver como se cuadra lo de las coordenadas que aparece el jugador
        self.__numero_de_imagen = 1 
        self.__angulo_de_imagen = 270 if self.team else 90
    
    def configurar_imagen(self):
        """Metodo que crea la ruta de imagen del jugador dependiendo de que imagen cargar, de las tres disponibles, y retorna la ruta generada"""
        imagen = self.IMAGEN_JUGADOR_A+self.numero_de_imagen+self.EXTENCION_DE_IMAGEN if self.equipo else self.IMAGEN_JUGADOR_B+self.numero_de_imagen+self.EXTENCION_DE_IMAGEN 
        self.numero_de_imagen = 1 if self.numero_de_imagen>3 else self.numero_de_imagen+1
        return imagen
    
    def mover(self, izquierda, derecha, arriba, abajo):
        """Metodo que mueve las coordenadas de la imagen del jugador, cambia el numero de imagen y retorna ruta generada con angulo de imagen"""
        imagen = self.configurar_imagen() #Siempre mueve los pies
        
        if izquierda:
            self.set_coordenadas(self.__coordenadas[0]-self.VELOCIDAD, 0)
        if derecha:
            self.set_coordenadas(self.__coordenadas[0]+self.VELOCIDAD, 0)
        if arriba:
            self.set_coordenadas(0, self.__coordenadas[1]-self.VELOCIDAD)
        if abajo:
            self.set_coordenadas(0, self.__coordenadas[1]+self.VELOCIDAD)
            
        return (imagen,self.__angulo_de_imagen)
    
    def set_coordenadas(self,x,y):
        self.__coordenadas = (x,y)
        
    def get_coordenadas(self):
        return self.__coordenadas