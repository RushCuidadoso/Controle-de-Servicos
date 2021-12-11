#!/usr/bin/python
# -*- coding: latin-1 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import frmproducto
from codeconexion import conexion

class productoApp(QtWidgets.QMainWindow, frmproducto.Ui_frmproducto):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    entertabla=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.bnd=0
        self.consultar()
        self.cancelar()
        #self.setFixedWidth(830)
        #self.setFixedHeight(260)
        self.txtbuscar.textChanged.connect(self.fbuscar)          
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btnmarca.clicked.connect(self.llamarmarca)
        self.btnmedida.clicked.connect(self.llamarmedida)
        self.btneliminar.clicked.connect(self.eliminar)

        self.tabla.doubleClicked.connect(self.devolver)
        self.txtnom.returnPressed.connect(self.tobtnmarca)
        #Test con la tabla
        self.txtbuscar.returnPressed.connect(self.totabla)
        self.tabla.itemSelectionChanged.connect(self.cargar)
        # self.tabla.
        # self.txtbuscar.returnPressed.connect(self.cargar)
        #------------------------------------------
        self.txtprecio.setKeyboardTracking(False)
        self.txtprecio.editingFinished.connect(self.tobtnsalvar)
        self.txtstock.setKeyboardTracking(False)
        self.txtstock.editingFinished.connect(self.totxtprecio)
        self.btnsalvar.setAutoDefault(True)
        self.btnmarca.setAutoDefault(True)
        self.btnmedida.setAutoDefault(True)

    def keyPressEvent(self, e):
        if self.tabla.hasFocus():
            if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                if self.entertabla==1:
                    self.entertabla=0
                    self.devolver()
                else:
                    self.entertabla=1

    def totabla(self):
        self.tabla.setFocus()
        self.tabla.selectRow(0)

    def totxtprecio(self):
        self.txtprecio.setFocus()

    def tobtnmarca(self):
        self.btnmarca.setFocus()

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()


    def closeEvent(self, estado):
        self.caller.setEnabled(True)
        if self.estado != 0:
            self.caller.txtcodprod.setFocus()
        
    def iniciar(self, caller, estado):
        self.caller=caller
        self.estado = estado
        # self.cerrar=0

    def devolver(self):
        # para marca, estado 1
        # para medida, estado 2
        # colocar tambem no codeproducto
        if self.estado == 2:
            self.caller.txtcodprod.setText(str(self.txtcod.text()))
            self.caller.setEnabled(True)
            self.caller.txtcodprod.setFocus()
            self.close()

    def llamarmarca(self):
        #self.cerrar=1
        from codemarca import marcaApp
        self.marca = marcaApp(parent=self)    
        # estado=1
        self.marca.show()   
        #inserir condigo para evitar que el resto del sistema pueda usarse desabilitado
        self.marca.iniciar(self, 1)
        #self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo
        #self.marca.iniciar(self.caller)  
        
    def consultarmarca(self,codmarca):
        con=self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select codmarca, nommarca from marca where codmarca=' + codmarca)
        item = cur.fetchall()
        var = item[0]
        self.codmarca.setText(str(var[0]))
        self.txtmarca.setText(str(var[1]))
        self.btnmedida.setFocus()
        
    def llamarmedida(self):
        #self.cerrar=1
        from codemedida import medidaApp
        self.medida = medidaApp(parent=self)    
        estado=2      
        self.medida.show()   
        #inserir condigo para evitar que el resto del sistema pueda usarse desabilitado
        self.medida.iniciar(self,2) 
        #self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo
        #self.marca.iniciar(self.caller)  
        
    def consultarmedida(self,codmedida):
        con=self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select codmedida, nommedida from medida where codmedida=' + codmedida)
        item = cur.fetchall()
        var = item[0]
        self.codmedida.setText(str(var[0]))
        self.txtmedida.setText(str(var[1]))
        self.txtstock.setFocus()
        
        
        
    def nuevo(self):
        #al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd=0
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnmarca.setEnabled(True)
        self.btnmedida.setEnabled(True)
        self.txtstock.setEnabled(True)
        self.txtprecio.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)    
        
    def editar(self):
        self.bnd=1
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnmarca.setEnabled(True)
        self.btnmedida.setEnabled(True)
        self.txtstock.setEnabled(True)
        self.txtprecio.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)        
        
    def cancelar(self):
        self.txtnom.setEnabled(False)
        self.btnmarca.setEnabled(False)
        self.btnmedida.setEnabled(False)
        self.txtstock.setEnabled(False)
        self.txtprecio.setEnabled(False)
        self.txtnom.clear()
        self.txtcod.clear()
        self.codmarca.clear()
        self.codmedida.clear()
        self.txtmarca.clear()
        self.txtmedida.clear()
        self.txtstock.clear()
        self.txtprecio.clear()
        self.txtstock.setEnabled(False)
        self.txtprecio.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.entertabla=0
        
    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        codmarca = str(self.codmarca.text())
        if len(codmarca)==0:
            codmarca='9999999'
        codmedida = str(self.codmedida.text())
        stock = str(self.txtstock.value())
        precio = str(self.txtprecio.value())
        #----------------------------------
        i=0
        res=''        
        while i != len(precio):
            if precio[i]==",":
                res=res+"."
            else:
                res=res+precio[i]        
            i=i+1    
        #----------------------------------
        if (len(nom) > 1) and (len(stock) >=1) and (len(precio) >=1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into produto (nomproduto,codmarca,codmedida,stock,precio) values(%s,%s,%s,%s,%s)',[nom,codmarca,codmedida,stock,precio])    
                con.commit()                
                self.cancelar()
                self.consultar()                
                row=self.tabla.rowCount()
                self.tabla.selectRow(row-1)                
            else:
                cur.execute('update produto set nomproduto=%s, codmarca=%s, codmedida=%s, stock=%s, precio=%s where codproduto=%s',[nom, codmarca, codmedida, stock, precio, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes","Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txtnom.setFocus()

    def eliminar(self):
        cod = int(self.txtcod.text())
        # con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from serviciodetalle where codprod=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            cur.execute('select count(*) from entradadetalle where codproduto=%s', [cod])
            rows = cur.fetchone()
            if int(rows[0])==0:
                mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                                     QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if (mensaje == QtGui.QMessageBox.Yes):
                    con = self.conexion.conectar()
                    cur = con.cursor()
                    cur.execute('delete from produto where codproduto = %s', [cod])
                    con.commit()
                    self.cancelar()
                    self.consultar()
                    mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                            QtGui.QMessageBox.Ok)
            else:
                mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro",
                                                     "Esse registro tem uma representante registrado", QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem uma representante registrado", QtGui.QMessageBox.Ok)
        
    def fbuscar(self):
        buscado=str(self.txtbuscar.text())
        if len(buscado)>0:
            self.buscar="'%"+buscado+"%'"
            #print self.buscar
        else:
            self.buscar="'%%'"
        self.consultar()        
        
    def config(self,rows):
        lista = 'Codigo', 'Produto', 'Marca', 'Medida', 'Estoque', 'Preço'
        self.tabla.setColumnCount(6)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)   
        #self.tabla.setColumnWidth(0,50)
        #self.tabla.setColumnWidth(1,250) 
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        
    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from produto where nomproduto like' + self.buscar)
        rows = cur.fetchone()
        
        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.codproduto, a.nomproduto, b.codmarca, b.nommarca, c.codmedida, c.nommedida, a.stock, a.precio from produto a, marca b, medida c where a.codmarca=b.codmarca and a.codmedida=c.codmedida and a.nomproduto like' + self.buscar + ' order by a.codproduto asc')
            self.producto = cur.fetchall()
            #print self.producto[3][0] para conseguir una informacion de una tupla [[0][0]]

            for i in range(int(rows[0])):
                item = self.producto[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                produto = QtWidgets.QTableWidgetItem(str(item[1]))
                nommarca = QtWidgets.QTableWidgetItem(str(item[3]))
                nommedida = QtWidgets.QTableWidgetItem(str(item[5]))
                # nommedida = QtWidgets.QTableWidgetItem(str(item[5]))
                stock = QtWidgets.QTableWidgetItem(str(item[6]))
                precio = QtWidgets.QTableWidgetItem(str(item[7]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, produto)
                self.tabla.setItem(i, 2, nommarca)
                self.tabla.setItem(i, 3, nommedida)
                self.tabla.setItem(i, 4, stock)
                self.tabla.setItem(i, 5, precio)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            
    def cargar(self):
        self.cancelar()
        # index = int(self.lblindice.text())
        index = self.tabla.currentRow()
        item = self.producto[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.codmarca.setText(str(item[2]))
        self.txtmarca.setText(str(item[3]))
        self.codmedida.setText(str(item[4]))
        self.txtmedida.setText(str(item[5]))
        self.txtstock.setValue(item[6])
        self.txtprecio.setValue(item[7])
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = productoApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()    