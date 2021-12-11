#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmmenu
import os
import subprocess

from codeconexion import conexion


class menuApp(QtWidgets.QMainWindow, frmmenu.Ui_frmmenu):
    conexion = conexion()
    caller = None

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnpessoas.clicked.connect(self.llamarpessoas)
        self.btnitems.clicked.connect(self.llamaritems)
        self.btnio.clicked.connect(self.llamario)

    def llamarpessoas(self):
        from codepessoas import pessoasApp
        self.setEnabled(False)
        self.pessoas = pessoasApp(parent=self)
        self.pessoas.show()
        self.pessoas.iniciar(self)
        # self.marca.iniciar(self, 1)

    def llamaritems(self):
        from codeitems import itemsApp
        self.setEnabled(False)
        self.items = itemsApp(parent=self)
        self.items.show()
        self.items.iniciar(self)
        # self.marca.iniciar(self, 1)

    def llamario(self):
        from codeio import ioApp
        self.setEnabled(False)
        self.io = ioApp(parent=self)
        self.io.show()
        self.io.iniciar(self)
        # self.marca.iniciar(self, 1)

    def closeEvent(self, *args, **kwargs):
        self.conexion.conectar()
        os.system(r' if not exist "C:\BackupKosloski\" mkdir C:\BackupKosloski ')
        # direccion = r'-f C:\Users\Denis\Documents\PythonProjects\Kosloski\Backup.dump kosloski'
        direccion = r' -f C:\BackupKosloski\Backup.dump kosloski'
        os.system(r' "C:\Program Files\PostgreSQL\13\bin\pg_dump.exe" -U postgres -C ' + direccion)  # PC Denis
        # os.system(r' "C:\Program Files\PostgreSQL\11\bin\pg_dump.exe" -U postgres -C ' + direccion)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = menuApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
