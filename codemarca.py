#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmmarca
from codeconexion import conexion

class marcaApp(QtWidgets.QMainWindow, frmmarca.Ui_frmmarca):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    entertabla = 0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)        
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.bnd=0
        self.consultar()
        self.cancelar()
        #self.setFixedWidth(830)
        #self.setFixedHeight(260)
        self.txtbuscar.textChanged.connect(self.fbuscar)          
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellDoubleClicked.connect(self.devolver)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        #-----
        #self.tabla.setSortingEnabled(True)
        #self.tabla.resizeRowsToContents()
        #self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)    
        
        #header = self.tabla.horizontalHeader()
        #header.setStretchLastSection(True)                
        #-----        
        #self.cargarbanco()
        self.txtnom.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)
        # Test con la tabla
        self.txtbuscar.returnPressed.connect(self.totabla)
        self.tabla.itemSelectionChanged.connect(self.cargar)

    def totabla(self):
        self.tabla.setFocus()
        self.tabla.selectRow(0)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.nuevo()
        if self.tabla.hasFocus():
            if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                if self.entertabla==1:
                    self.entertabla=0
                    self.devolver()
                else:
                    self.entertabla=1

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
        # if self.estado != 0:
        #     self.caller.txtcodmarca.setFocus()

        
    def iniciar(self,caller,estado):
        self.caller=caller
        self.estado=estado
        #self.cerrar=0        
        
    def devolver(self):
        #para marca, estado 1
        #para medida, estado 2
        #colocar tambem no codeproducto
        if self.estado==1:
            #item=self.marca[int(self.lblindice.text())]            
            self.caller.consultarmarca(str(self.txtcod.text()))
            self.caller.setEnabled(True)
            self.close()    
        
    def nuevo(self):
        #al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd=0
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        
    def cancelar(self):
        self.txtnom.setEnabled(False)
        self.txtnom.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.entertabla=0
        
    def fbuscar(self):
        buscado=str(self.txtbuscar.text())
        if len(buscado)>0:
            self.buscar="'%"+buscado+"%'"
            #print self.buscar
        else:
            self.buscar="'%%'"
        self.consultar()      
        
    def editar(self):
        self.bnd=1
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(True)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)    
        
    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        # if len(nom)==0:
        #     nom = unicode("N/D")

        if (len(nom) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into marca (nommarca) values(%s)',[nom])    
                con.commit()                
                self.cancelar()
                self.consultar()                
                row=self.tabla.rowCount()
                self.tabla.selectRow(row-1)                
            else:
                cur.execute('update marca set nommarca=%s where codmarca=%s',[nom, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes","Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txtnom.setFocus()
            
    def eliminar(self):
        cod = int(self.txtcod.text())
        #con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from produto where codmarca=%s',[cod])
        rows = cur.fetchone()
        if int(rows[0])==0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from marca where codmarca = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado", QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro", "Esse registro tem uma marca registrada",QtGui.QMessageBox.Ok)    
            
    def config(self,rows):
        lista = 'Codigo', 'Marca'
        self.tabla.setColumnCount(2)
        self.tabla.setRowCount(int(rows[0]-1))
        self.tabla.setHorizontalHeaderLabels(lista)   
        # self.tabla.setColumnWidth(0,50)
        # self.tabla.setColumnWidth(1,319)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from marca where nommarca like' + self.buscar)
        rows = cur.fetchone()
        
        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select codmarca, nommarca from marca where nommarca like' + self.buscar + ' order by codmarca asc')
            self.marca = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.marca[i]
                if item[0]==9999999:
                    break
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                marca = QtWidgets.QTableWidgetItem(str(item[1]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, marca)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            
    def cargar(self):
        self.cancelar()
        index = self.tabla.currentRow()
        # index = int(self.lblindice.text())
        item = self.marca[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)    

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = marcaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()