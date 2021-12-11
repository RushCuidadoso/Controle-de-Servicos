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
            if easygui.ccbox('N�o foi poss�vel conectar ao servidor, restabele�a a conex�o e clique em continuar', 'Erro de conex�o'):
                self.conectar()
            else:
                sys.exit(0)

    def desconectar(self, con):
        if con:
            con.close()
