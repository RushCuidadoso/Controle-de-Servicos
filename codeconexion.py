#!/usr/bin/python
# -*- coding: latin-1 -*-

import psycopg2
import sys
import easygui
#import MySQLdb
class conexion():

    def conectar(self):
        try:
            con = psycopg2.connect("host='localhost' dbname='kosloski' user='postgres' password='motor' connect_timeout=3")
            # con = psycopg2.connect("host='192.168.100.180' dbname='kosloski' user='postgres' password='motor' connect_timeout=3")# Servidor Kosloski
            return con
        except psycopg2.OperationalError:
            if easygui.ccbox('Não foi possível conectar ao servidor, restabeleça a conexão e clique em continuar', 'Erro de conexão'):
                self.conectar()
            else:
                sys.exit(0)

    def desconectar(self, con):
        if con:
            con.close()

    #def serialconfig(self):
        #db_host = '104.28.7.238:13306'
        #usuario = 'serialconfig'
        #clave = 'mYserialcOnfigsQl825'
        #base_de_datos = 'serialconfig'
        #db = MySQLdb.connect("host='104.28.7.238:13306' user='serialconfig' passwd='mYserialcOnfigsQl825' db='serialconfig'")
        
        
        #db = MySQLdb.connect(host="sql5.freemysqlhosting.net",user="sql5105806",passwd="yY2PtQjJx7",db="sql5105806")
        #if db:
            #print 'conectado'
            #return db
        
        #else:
            #print "no se conecto"
            
#cd=conexion()
#cd.serialconfig()
            #       xeT)t$1sFyUDs2V5
            #       yY2PtQjJx7