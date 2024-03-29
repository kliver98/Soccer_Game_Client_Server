#librerias
import numpy as np
from keras.models import model_from_json
from client.bots import red_neuronal_1 as rn1
import constantesCompartidas as cc
from client.bots import entreno_red_gol as rn2
from math import fabs
import time

NOMBRE_ARCHIVO_1 = "modeloAgarrar"
NOMBRE_ARCHIVO_2 = "modeloGol"

import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)

def iniciar():
    modelos = []
    mod_1 = cargar_modelo(NOMBRE_ARCHIVO_1)
    if mod_1==None: #Si no habia ningun modelo guardado, se crea
            mod_1 = rn1.entrenar()
            guardar_modelo(mod_1,NOMBRE_ARCHIVO_1)
    modelos.append(mod_1)
    
    mod_2 = cargar_modelo(NOMBRE_ARCHIVO_2)
    if mod_2==None: #Si no habia ningun modelo guardado, se crea
            mod_2 = rn2.entrenar()
            guardar_modelo(mod_2,NOMBRE_ARCHIVO_2)
    modelos.append(mod_2)
    #Poner el otro modelo por que se deben cargar una sola vez, si no el juego se ve lagueado
    return modelos

def calcular(jugadores, balon, modelos):
    #Este metodo es el encargado de actualizar las posicinoes de los jugadores pasados por parametro. No devuelve nada, actualiza los mismo objetos del model
    mover = cc.DIFICULTAD[0]-1
    user_balon = balon.get_usuario()
    if user_balon!=jugadores[0].get_usuario() or user_balon==jugadores[0].get_usuario(): #la red 1 tiene que hacer que atrape el balon
        for i,jugador in enumerate(jugadores):
            if i==0 or balon.get_usuario()==jugador.get_usuario():
                continue
            entrada = np.array(convertir_a_entrada(0,jugador,balon))
            salida = modelos[0].predict(entrada)
            x = mover if salida[0][0]>0 else -mover if salida[0][0]<0 else 0
            y = mover if salida[0][1]<0 else -mover if salida[0][1]>0 else 0
            jugador.set_coordenadas(x,y)
    if user_balon==jugadores[1].get_usuario(): #la red 2 tiene que hacer gol
        for i,jugador in enumerate(jugadores):
            if i==0 or balon.get_usuario() is not jugador.get_usuario():
                continue
            entrada = np.array(convertir_a_entrada_gol(jugadores))
            salida = modelos[1].predict(entrada)
            y = 1 if salida[0][0]>0.25 else -mover
            x = -mover if salida[0][1]> 0.25 else mover*2 if salida[0][1]< -0.25 else 0
            patear= True if salida[0][2]>=0.5 else False #and balon.get_coordenadas()[1]>=cc.ALTO_VENTANA*0.4 and balon.get_coordenadas()[1]<=cc.ALTO_VENTANA*0.6 else False
            #print(patear)
            if patear:
                balon.set_coordenadas(cc.ANCHO_VENTANA*0.15, 0)
                balon.set_usuario("/")
                time.sleep(0.15)
            else:
                mover_a_porteria(jugador, x, y, mover)
            
def convertir_a_entrada_gol(jugadores):
    coor_persona=jugadores[0].get_coordenadas()
    coor_bot=jugadores[1].get_coordenadas()
    calc_x= coor_bot[0]-coor_persona[0]
    calc_y= coor_bot[1]-coor_persona[1]
    calc_patear=True if coor_bot[0]- (cc.ANCHO_VENTANA*0.15)<=0 else False
    
    x=1 if 0<=calc_x<100 else -1 
    y=-1 if 0<fabs( calc_y)<30 else 1 
    patear=1 if calc_patear else -1 if fabs(coor_bot[0] - cc.ANCHO_VENTANA) <=50  else 0
    return [[y,x,patear]]
    
def mover_a_porteria(bot,act_x,act_y,mover):
        y=act_y
        if act_y==1:
            coordenadas=bot.get_coordenadas()
            direccion_y= 193-coordenadas[1]
            y= -mover if direccion_y<0 else mover if direccion_y>0 else 0
        bot.set_coordenadas(act_x,y)
    
def convertir_a_entrada(tipo,jugador,balon):
    #de acuerdo al tipo (0 para agarrar balon, 1 para hacer gol) devuelve un arreglo en formato de  estimulo
    if tipo==0:
        distX = (jugador.get_coordenadas()[0]-balon.get_coordenadas()[0])/cc.ANCHO_VENTANA
        distY = (jugador.get_coordenadas()[1]-balon.get_coordenadas()[1])/cc.ALTO_VENTANA
        return [[distX,distY]]
    elif tipo==1:
        pass

def guardar_modelo(model,nombre_archivo):
    # serializar el modelo a JSON
    model_json = model.to_json()
    with open(f"{nombre_archivo}.json", "w") as json_file:
        json_file.write(model_json)
    # serializar los pesos a HDF5
    model.save_weights(f"{nombre_archivo}.h5")
    print("Modelo Guardado!")

def cargar_modelo(nombre_archivo):
    # cargar json y crear el modelo
    file_name = f'{nombre_archivo}.json'
    try:
        json_file = open(file_name, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # cargar pesos al nuevo modelo
        loaded_model.load_weights(f"{nombre_archivo}.h5")
        print("Cargado modelo desde disco.")
        # Compilar modelo cargado y listo para usar.
        loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])
    except Exception as e:
        return None
    return loaded_model