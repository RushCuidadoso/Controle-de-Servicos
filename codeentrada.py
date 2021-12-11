#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmentrada
from codeconexion import conexion

class entradaApp(QtWidgets.QMainWindow, frmentrada.Ui_frmentrada):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    cod=0
    sumalinea=0
    edit=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancel.clicked.connect(self.cancelar)
        self.txtcodprod.returnPressed.connect(self.actualizar)
        self.txtcodproveedor.returnPressed.connect(self.consultafornecedor)
        self.datedata.editingFinished.connect(self.iracodprod)
        self.txtcantidad.returnPressed.connect(self.cargarcantidad)
        self.btngrabar.clicked.connect(self.gravar)
        self.btnanular.clicked.connect(self.anular)
        #---------
        self.btnconsultar.clicked.connect(self.tocod)
        self.btnbuscar.clicked.connect(self.llamarprod)
        self.btnproveedor.clicked.connect(self.llamarfornecedor)
        self.txtcod.returnPressed.connect(self.consultar)
        #---------------
        self.btnnovo.setFocus()
        self.cancelar()
        self.config(0)

    def iniciar(self, caller):
        self.caller = caller
        # self.caller.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)

    def tocod(self):
        self.txtcod.setEnabled(True)
        self.txtcod.setFocus()

    def consultar(self):
        if len(str(self.txtcod.text()))>0:
            self.txtcod.setEnabled(False)
            cod = str(self.txtcod.text())
            con = self.conexion.conectar()
            cur = con.cursor()
            # cur.execute("""SET DateStyle To 'sql, dmy'""")
            cur.execute('select count(*) from entrada where codentrada=%s', [cod])
            exist = cur.fetchone()
            if int(exist[0])>=1:
                cur.execute('''select a.fecha, a.codfornecedor, b.nomfornecedor from entrada a, fornecedor b where a.codfornecedor=b.codfornecedor and codentrada=%s''',[cod])
                item = cur.fetchall()
                self.datedata.setDate(item[0][0])
                self.txtcodproveedor.setText(str(item[0][1]))
                self.txtnomfornecedor.setText(str(item[0][2]))
                cur.execute('select count(*) from entradadetalle where codentrada=%s', [cod])
                rows=cur.fetchone()
                cur.execute('select a.codproduto, b.nomproduto, a.cantidad from entradadetalle a, produto b where a.codproduto=b.codproduto and a.codentrada=%s', [cod])
                tabla=cur.fetchall()
                self.config(rows[0])
                for i in range(rows[0]):
                    codprod = QtWidgets.QTableWidgetItem(str(tabla[i][0]))
                    nomprod = QtWidgets.QTableWidgetItem(str(tabla[i][1]))
                    cantidad = QtWidgets.QTableWidgetItem(str(tabla[i][2]))
                    self.tabla.setItem(i, 0, codprod)
                    self.tabla.setItem(i, 1, nomprod)
                    self.tabla.setItem(i, 2, cantidad)
                self.btnanular.setEnabled(True)
                self.tabla.setEnabled(False)
            else:
                QtGui.QMessageBox.information(self, "Erro", "Esse registro não existe!",
                                                    QtGui.QMessageBox.Ok)
                self.txtcod.clear()
                self.txtcod.setEnabled(True)
                self.txtcod.setFocus()
        else:
            QtGui.QMessageBox.information(self, "Erro", "Digite um código válido!",
                                                    QtGui.QMessageBox.Ok)
            self.txtcod.clear()
            self.txtcod.setEnabled(True)
            self.txtcod.setFocus()

    def anular(self):
        cod = str(self.txtcod.text())
        mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                             QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if (mensaje == QtGui.QMessageBox.Yes):
            rows = self.tabla.rowCount()
            con = self.conexion.conectar()
            cur = con.cursor()
            for i in range(rows):
                cantidad = float(self.tabla.item(i, 2).text())
                codprod = str(self.tabla.item(i, 0).text())
                cur.execute('select stock from produto where codproduto=%s', [str(codprod)])
                stock = cur.fetchone()
                cantidad = float(stock[0]) - float(cantidad)
                cur.execute('update produto set stock=%s where codproduto=%s', [cantidad, str(codprod)])
                con.commit()

            cur.execute('delete from entradadetalle where codentrada = %s', [cod])
            con.commit()
            cur.execute('delete from entrada where codentrada=%s', [cod])
            con.commit()
            self.cancelar()
            QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                    QtGui.QMessageBox.Ok)
        else:
            self.cancelar()


    def gravar(self):
        self.txtcodprod.clear()
        self.txtnomprod.clear()
        self.txtcantidad.clear()
        codfornecedor = str(self.txtcodproveedor.text())
        if len(codfornecedor)>0:
            if self.tabla.rowCount()>=1:
                fecha = str(self.datedata.text())
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute(
                    'insert into entrada (fecha, codfornecedor) values(%s,%s)', [fecha, codfornecedor])
                con.commit()
                cur.execute('select max(codentrada) from entrada')
                cod = cur.fetchone()
                for i in range(int(self.tabla.rowCount())):
                    codprod = str(self.tabla.item(i,0).text())
                    cantidad = str(self.tabla.item(i,2).text())
                    # ---------------------------------------- algoritmo que cambia la coma por punto en los decimales
                    p = 0
                    res = ''
                    while p != len(cantidad):
                        if cantidad[p] == ",":
                            res = res + "."
                        else:
                            res = res + cantidad[p]
                        p = p + 1
                    # ----------------------------------------
                    cur.execute('insert into entradadetalle (codentrada, codproduto, cantidad) values(%s,%s,%s)', [cod, codprod, res])
                    con.commit()
                    cur.execute('select stock from produto where codproduto=%s', [codprod])
                    con.commit()
                    stock = cur.fetchone()
                    suma = float(stock[0]) + float(res)
                    cur.execute('update produto set stock = %s where codproduto = %s', [suma, codprod])
                    con.commit()
                QtGui.QMessageBox.question(self, "Cadastro de entrada de materiais",
                                           "Cadastro com sucesso", QtGui.QMessageBox.Ok)
                self.cancelar()
            else:
                QtGui.QMessageBox.question(self, "Erro",
                                           "Lista de produtos vazia!", QtGui.QMessageBox.Ok)
                self.txtcodprod.setFocus()
        else:
            QtGui.QMessageBox.question(self, "Erro",
                                       "Favor digite um fornecedor!", QtGui.QMessageBox.Ok)
            self.txtcodproveedor.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Delete:
                mensaje = QtGui.QMessageBox.question(self, "Excluyendo producto",
                                                     "Esta seguro que quiere eliminar el producto seleccionado?",
                                                     QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if (mensaje == QtGui.QMessageBox.Yes):
                    self.excluir()

    def excluir(self):
        row = self.tabla.currentRow()
        self.tabla.removeRow(row)
        self.sumalinea = self.sumalinea-1
        self.txtcodprod.setFocus()


    def cargarcantidad(self):
        if len(self.txtcodprod.text())>0:
            #--------------
            number = self.txtcantidad.text()
            bandera = 0
            #-----
            p = 0
            res = ''
            while p != len(number):
                if number[p] == ",":
                    res = res + "."
                else:
                    res = res + number[p]
                p = p + 1
            #-----
            try:
                res = float(res)
            except Exception:
                QtGui.QMessageBox.about(self, 'Erro', 'Os dados somente podem ser numéricos')
                bandera = 1
            if bandera != 1:
                # --------------------------------------------------------------
                # Cargar a la tabla y crear una linea nueva para la proxima carga
                if len(self.txtcantidad.text()) > 0:
                    var = QtWidgets.QTableWidgetItem(str(self.txtcodprod.text()))
                    nom = QtWidgets.QTableWidgetItem(str(self.txtnomprod.text()))
                    cantidad = QtWidgets.QTableWidgetItem(str(self.txtcantidad.text()))
                    self.sumalinea = self.sumalinea + 1
                    self.tabla.setRowCount(self.sumalinea)
                    linea = int(self.tabla.rowCount()) - 1
                    self.tabla.setItem(linea, 0, var)
                    self.tabla.setItem(linea, 1, nom)
                    self.tabla.setItem(linea, 2, cantidad)
                    #---------------
                    self.txtcantidad.clear()
                    self.txtnomprod.clear()
                    self.txtcodprod.clear()
                    self.txtcodprod.setFocus()
                else:
                    QtGui.QMessageBox.question(self, "Erro ao cadastrar item",
                                                         "Favor digite a quantidade", QtGui.QMessageBox.Ok)
            else:
                self.txtcantidad.clear()
                self.txtcantidad.setFocus()
        else:
            QtGui.QMessageBox.question(self, "Erro ao cadastrar item",
                                       "Favor digite o produto!", QtGui.QMessageBox.Ok)
            self.txtcodprod.setFocus()


    def config(self,rows):
        lista = 'Codigo', 'Nome', 'Quantidade'
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(rows)
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0,182)
        self.tabla.setColumnWidth(1,631)
        # self.tabla.setColumnWidth(2,150)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def actualizar(self):
        number = self.txtcodprod.text()
        bandera = 0
        try:
            number = int(number)
        except Exception:
            QtGui.QMessageBox.about(self, 'Erro', 'Os dados somente podem ser numéricos')
            bandera = 1
        if bandera != 1:
            if len(str(self.txtcodprod.text()))>0:
                con = None
                con = self.conexion.conectar()
                cur = con.cursor()
                row = len(str(self.txtcodprod.text()))
                var = str(self.txtcodprod.text())
                cur.execute('select count(*) from produto where codproduto=%s', [var])
                con.commit()
                row = cur.fetchone()
                if row[0] > 0:
                    #Cargar el nombre del producto al campo nomprod y pasar a txtcantidad
                    cur.execute('select nomproduto from produto where codproduto=%s', [var])
                    con.commit()
                    nom = cur.fetchone()
                    self.txtnomprod.setText(str(nom[0]))
                    self.txtcantidad.setFocus()
                    # #--------------------------------------------------------------
                    # #Cargar a la tabla y crear una linea nueva para la proxima carga
                    # var = QtGui.QTableWidgetItem(var)
                    # self.sumalinea = self.sumalinea+1
                    # nom = QtGui.QTableWidgetItem(str(nom[0]))
                    # self.tabla.setRowCount(self.sumalinea)
                    # linea = int(self.tabla.rowCount())-1
                    # self.tabla.setItem(linea, 0, var)
                    # self.tabla.setItem(linea, 1, nom)
                else:
                    mensaje = QtGui.QMessageBox.question(self, "Erro",
                                               "Código não existe, deseja abrir o cadastro de produtos?",
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if (mensaje == QtGui.QMessageBox.Yes):
                        self.llamarprod()
                    else:
                        self.txtcodprod.clear()
                        self.txtcodprod.setFocus()
        else:
            self.txtcodprod.clear()
            self.txtcodprod.setFocus()

    def llamarprod(self):
        from codeproducto import productoApp
        self.producto = productoApp()
        self.producto.show()
        self.setEnabled(False)
        self.producto.iniciar(self, 2)

    def iracodprod(self):
        self.txtcodprod.setEnabled(True)
        self.txtcantidad.setEnabled(True)
        self.txtcodprod.setFocus()

    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.txtcodproveedor.setEnabled(True)
        self.datedata.setEnabled(True)
        # self.txtcodprod.setEnabled(True)
        self.btnproveedor.setEnabled(True)
        self.btnbuscar.setEnabled(True)
        self.btngrabar.setEnabled(True)
        self.btnconsultar.setEnabled(False)
        self.btncancel.setEnabled(True)
        self.btnanular.setEnabled(False)
        self.txtcodproveedor.setFocus()
        self.tabla.setEnabled(True)
    #
    # def acthora(self):
    #     self.txtfecha.setText(time.strftime("%d/%m/%y"))
    #     self.txthora.setText(time.strftime("%H:%M"))

    def cancelar(self):
        self.datedata.setDate(QtCore.QDate.currentDate())
        self.txtcodproveedor.setEnabled(False)
        self.datedata.setEnabled(False)
        self.txtcodprod.setEnabled(False)
        self.btnproveedor.setEnabled(False)
        self.btnbuscar.setEnabled(False)
        self.txtcantidad.setEnabled(False)
        self.btngrabar.setEnabled(False)
        self.btnconsultar.setEnabled(True)
        self.btncancel.setEnabled(False)
        self.btnanular.setEnabled(False)
        self.txtcod.clear()
        self.txtcodproveedor.clear()
        self.txtnomfornecedor.clear()
        self.tabla.clear()
        self.config(0)
        self.sumalinea=0
        self.txtcodprod.clear()
        self.txtnomprod.clear()
        self.txtcantidad.clear()
        self.datedata.clear()
        self.btnnovo.setFocus()
        self.btnnovo.setEnabled(True)

    def consultafornecedor(self):

        cod = int(self.txtcodproveedor.text())
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from fornecedor where codfornecedor = %s', [cod])
        con.commit()
        rows = cur.fetchone()
        if int(rows[0]) > 0:

            cur.execute('select nomfornecedor from fornecedor where codfornecedor = %s', [cod])
            con.commit()
            rows2 = cur.fetchone()
            self.txtnomfornecedor.setText(rows2[0])
            self.datedata.setFocus()
        else:
            mensaje = QtGui.QMessageBox.question(self, "Fornecedor nao encontrado",
                                                 "Deseja abrir o Registro de Fornecedores?", QtGui.QMessageBox.Yes,
                                                 QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                self.llamarfornecedor()

    def llamarfornecedor(self):
        # self.cerrar=1
        from codefornecedor import fornecedorApp
        self.setEnabled(False)
        self.fornecedor = fornecedorApp(parent=self)
        self.fornecedor.iniciar(self, 0)
        self.fornecedor.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo

    def consultarfornecedor(self, codfornecedor):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select codfornecedor, nomfornecedor from fornecedor where codfornecedor=' + codfornecedor)
        item = cur.fetchall()
        var = item[0]
        self.txtcodproveedor.setText(str(var[0]))
        self.txtnomfornecedor.setText(str(var[1]))
        self.datedata.setFocus()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = entradaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()