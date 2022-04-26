from asyncore import write
import csv
from operator import contains
from passlib.hash import sha256_crypt
import datetime

class funciones:
    def diccionarioUsuarios():
        pass
    def lee_archivo_csv(archivo:str)->list:
        '''
        Lee un archivo csv y regresa una lista de renglones 
        (y campos dentro de los renglones)
        '''
        lista = []
        try:
            with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
                csv_reader = csv.reader(fh)
                for linea in csv_reader:
                    lista.append(linea)
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")

        return lista
    def lee_diccionario_usuarios(archivo:str)->dict:
        diccionario = {}
        try:
            with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
                csv_reader = csv.DictReader(fh)
                for renglon in csv_reader:
                    llave = renglon['usuario']
                    diccionario[llave] = renglon
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")
        return diccionario
    def lee_diccionario_servicios(archivo:str)->dict:
        diccionario = {}
        try:
            with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
                csv_reader = csv.DictReader(fh)
                for renglon in csv_reader:
                    llave = renglon['numero']
                    diccionario[llave] = renglon
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")
        return diccionario

    def lee_diccionario_citas(archivo:str)->dict:
        diccionario = {}
        try:
            with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
                csv_reader = csv.DictReader(fh)
                for renglon in csv_reader:
                    llave = renglon['id']
                    diccionario[llave] = renglon
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")
        return diccionario

    def lee_diccionario_medicamentos(archivo:str)->dict:
        diccionario = {}
        try:
            with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
                csv_reader = csv.DictReader(fh)
                for renglon in csv_reader:
                    llave = renglon['codigo']
                    diccionario[llave] = renglon
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")
        return diccionario

    def escribir_archivo(archivo:str,lista:list):
        try:
            with open(archivo,"a",encoding="utf-8") as fh:
                fh.write("")
                writer=csv.writer(fh)
                writer.writerow(lista)
        except IOError:
            print(f"No se pudo abrir el archivo {archivo}")
    
    def generar_id(dictServicio:dict)->str:
        x=datetime.datetime.now()
        id = x.strftime("%y")+x.strftime("%m") + x.strftime("%d")+"000"
        n=0
        for numero, tipo in dictServicio.items():
            temp = numero[0:len(id)-3]
            temp2=id[0:len(id)-3]
            if temp == temp2:
                n+=1
        n+=1
        n = str(n)
        id2= id[0:len(id)-len(n)]+n
        return(id2)