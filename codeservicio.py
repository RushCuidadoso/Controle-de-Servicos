#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmservicio
from codeconexion import conexion

class servicioApp(QtWidgets.QMainWindow, frmservicio.Ui_frmservicio):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    cod=0
    sumalinea=0
    mod=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.bnd=0
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancel.clicked.connect(self.cancelar)
        #---------
        self.txtnum.returnPressed.connect(self.todate)
        self.datedata.editingFinished.connect(self.tofuncio)
        self.txtcomissao.returnPressed.connect(self.tocobrado)
        self.btnconsultar.clicked.connect(self.tocod)
        self.btnanular.clicked.connect(self.anular)
        self.btnmodificar.clicked.connect(self.modificar)
        self.btngrabar.clicked.connect(self.botongrabar)
        self.btnfuncio.clicked.connect(self.llamarfuncionario)
        self.btnequip.clicked.connect(self.llamarequip)
        self.btncliente.clicked.connect(self.llamarcliente)
        #-------------------------
        self.txtcodfuncio.returnPressed.connect(self.consultafuncio)
        self.txtcodequip.returnPressed.connect(self.consultaequip)
        self.txtcodcliente.returnPressed.connect(self.consultacliente)
        self.txtcod.returnPressed.connect(self.consultar)
        #---------------
        self.radabierto.pressed.connect(self.abierto)
        self.radproceso.pressed.connect(self.proceso)
        self.radconcluido.pressed.connect(self.concluido)
        #-----------------
        self.txtcodprod.returnPressed.connect(self.actualizar)
        self.txtcantidad.returnPressed.connect(self.cargarcantidad)
        self.txtcobrado.returnPressed.connect(self.gravar)
        #-----------------
        self.btnnovo.setFocus()
        self.cancelar()
        self.config(0)
        self.txttotalete.setText('0')
        self.txtsubtotal.setText('0')

    def botongrabar(self):
        if len(self.txtcobrado.text())<1:
            if self.mod == 1:
                self.gravarmod()
            self.txtcomissao.setEnabled(True)
            self.txtcomissao.setFocus()
        else:
            if not float(self.txttotalete.text())==0:
                self.gravar()
            else:
                QtGui.QMessageBox.question(self, "Erro", "Total do serviço é igual a Zero!", QtGui.QMessageBox.Ok)
                self.txtcodprod.setFocus()

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)

    def modificar(self):
        self.mod=1
        self.txtnum.setEnabled(True)
        self.datedata.setEnabled(True)
        self.txtcodfuncio.setEnabled(True)
        self.txtcodcliente.setEnabled(True)
        self.txtcodequip.setEnabled(True)

        self.grouprad.setEnabled(True)
        self.radabierto.setFocus()
        self.radabierto.setChecked(True)

    def gravarmod(self):
        cod = str(self.txtcod.text())
        if self.radabierto.isChecked():
            estado = '1'
        elif self.radproceso.isChecked():
            estado = '2'
        elif self.radconcluido.isChecked():
            estado = '3'
        #----------------------------------------------
        orcamento = str(self.txtnum.text())
        codfuncio = str(self.txtcodfuncio.text())
        codcliente = str(self.txtcodcliente.text())
        fecha = str(self.datedata.text())
        codequip = str(self.txtcodequip.text())
        #----------------------------------------------
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('update servicio set estado = %s, numservi =%s, codfuncio =%s, codcliente = %s, fecha =%s, codequip =%s where codservi=%s', [estado,orcamento,codfuncio,codcliente,fecha,codequip,cod])
        con.commit()
        QtGui.QMessageBox.question(self, "Cadastro de ordem de serviço","Cadastro atualizado com sucesso", QtGui.QMessageBox.Ok)
        self.cancelar()

    def tocod(self):
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
                cantidad = float(self.tabla.item(i, 3).text())
                codprod = str(self.tabla.item(i, 0).text())
                cur.execute('select stock from produto where codproduto=%s', [codprod])
                stock = cur.fetchone()
                cantidad = float(stock[0]) + float(cantidad)
                cur.execute('update produto set stock=%s where codproduto=%s', [cantidad, str(codprod)])
                con.commit()

            cur.execute('delete from serviciodetalle where codservi = %s', [cod])
            con.commit()
            cur.execute('delete from servicio where codservi=%s', [cod])
            con.commit()
            self.cancelar()
            QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                          QtGui.QMessageBox.Ok)
        else:
            self.cancelar()

    def consultar(self):
        # if len(self.codlista)==0:
        #     cod = self.codlista
        if len(str(self.txtcod.text()))>0:
            self.txtcod.setEnabled(False)
            cod = str(self.txtcod.text())
            con = self.conexion.conectar()
            cur = con.cursor()
            # cur.execute("""SET DateStyle To 'sql, dmy'""")
            cur.execute('select count(*) from servicio where codservi=%s', [cod])
            exist = cur.fetchone()
            if int(exist[0])>=1:
                cur.execute('''select a.fecha, a.numservi, a.codfuncio, b.nomfuncio, a.codequip, c.nomequip, 
                a.codcliente, d.nomcliente, a.estado, a.comissao, a.cobrado, a.total from servicio a, funcionario b, 
                equipamento c, cliente d where a.codfuncio=b.codfuncio and a.codequip=c.codequip and a.codcliente=d.codcliente
                and codservi=%s''',[cod])
                item = cur.fetchall()
                self.datedata.setDate(item[0][0])
                self.txtnum.setText(str(item[0][1]))
                self.txtcodfuncio.setText(str(item[0][2]))
                self.txtnomfuncio.setText(str(item[0][3]))
                self.txtcodequip.setText(str(item[0][4]))
                self.txtnomequip.setText(str(item[0][5]))
                self.txtcodcliente.setText(str(item[0][6]))
                self.txtnomcliente.setText(str(item[0][7]))
                #-----
                if item[0][8]==1:
                    self.radabierto.setChecked(True)
                elif item[0][8]==2:
                    self.radproceso.setChecked(True)
                elif item[0][8]==3:
                    self.radconcluido.setChecked(True)
                #-----
                self.txtcomissao.setText(str(item[0][9]))
                self.txtcobrado.setText(str(item[0][10]))
                self.txttotalete.setText(str(item[0][11]))
                cur.execute('select count(*) from serviciodetalle where codservi=%s', [cod])
                rows=cur.fetchone()
                cur.execute('select a.codprod, b.nomproduto, a.precio, a.cantidad, a.subtotal from serviciodetalle a, produto b where a.codprod=b.codproduto and a.codservi=%s', [cod])
                tabla=cur.fetchall()
                self.config(rows[0])
                for i in range(rows[0]):
                    codprod = QtGui.QTableWidgetItem(str(tabla[i][0]))
                    nomprod = QtGui.QTableWidgetItem(str(tabla[i][1]))
                    precio = QtGui.QTableWidgetItem(str(tabla[i][2]))
                    cantidad = QtGui.QTableWidgetItem(str(tabla[i][3]))
                    subtotal = QtGui.QTableWidgetItem(str(tabla[i][4]))
                    self.tabla.setItem(i, 0, codprod)
                    self.tabla.setItem(i, 1, nomprod)
                    self.tabla.setItem(i, 2, precio)
                    self.tabla.setItem(i, 3, cantidad)
                    self.tabla.setItem(i, 4, subtotal)
                self.btnanular.setEnabled(True)
                self.tabla.setEnabled(False)
                self.btnmodificar.setEnabled(True)
                self.btncancel.setEnabled(True)
            else:
                mensaje = QtGui.QMessageBox.question(self, "Erro",
                                                     "Esse registro não existe! Deseja abrir a lista de serviços?", QtGui.QMessageBox.Yes,
                                                     QtGui.QMessageBox.No)
                if (mensaje == QtGui.QMessageBox.Yes):
                    self.llamarlista()

                # QtGui.QMessageBox.question(self, "Erro", "Esse registro não existe!",
                #                                     QtGui.QMessageBox.Ok)
                # self.txtcod.clear()
                # self.txtcod.setEnabled(True)
                # self.txtcod.setFocus()
        else:
            QtGui.QMessageBox.information(self, "Erro", "Digite um código válido!",
                                                    QtGui.QMessageBox.Ok)
            self.txtcod.clear()
            self.txtcod.setEnabled(True)
            self.txtcod.setFocus()

    def llamarlista(self):
        # self.cerrar=1
        from codelista import listaApp
        self.setEnabled(False)
        self.lista = listaApp(parent=self)
        self.lista.iniciar(self,1)
        self.lista.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo


    def abierto(self):
        self.radabierto.setChecked(True)
        self.txtcodprod.setFocus()
    def proceso(self):
        self.radproceso.setChecked(True)
        self.txtcodprod.setFocus()

    def concluido(self):
        self.radconcluido.setChecked(True)
        self.txtcodprod.setFocus()


    def consultacliente(self):
        if len(str(self.txtcodcliente.text())) > 0:
            cod = int(self.txtcodcliente.text())
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from cliente where codcliente = %s', [cod])
        con.commit()
        rows = cur.fetchone()
        if int(rows[0]) > 0:

            cur.execute('select nomcliente from cliente where codcliente = %s', [cod])
            con.commit()
            rows2 = cur.fetchone()
            self.txtnomcliente.setText(rows2[0])
            self.radabierto.setChecked(True)
            self.radabierto.setFocus()
        else:
            mensaje = QtGui.QMessageBox.question(self, "Cliente não encontrado",
                                                 "Deseja abrir o Registro de Clientes?", QtGui.QMessageBox.Yes,
                                                 QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                self.llamarcliente()

    def llamarcliente(self):
        # self.cerrar=1
        from codecliente import clienteApp
        self.setEnabled(False)
        self.cliente = clienteApp(parent=self)
        self.cliente.iniciar(self,0)
        self.cliente.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo

    def consultaequip(self):
        if len(str(self.txtcodequip.text())) > 0:
            cod = int(self.txtcodequip.text())
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from equipamento where codequip = %s', [cod])
        con.commit()
        rows = cur.fetchone()
        if int(rows[0]) > 0:

            cur.execute('select nomequip from equipamento where codequip = %s', [cod])
            con.commit()
            rows2 = cur.fetchone()
            self.txtnomequip.setText(str(rows2[0]))
            self.txtcodcliente.setFocus()
        else:
            mensaje = QtGui.QMessageBox.question(self, "Equipamento não encontrado",
                                                 "Deseja abrir o Registro de Equipamentos?", QtGui.QMessageBox.Yes,
                                                 QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                self.llamarequip()

    def llamarequip(self):
        # self.cerrar=1
        from codeequip import equipApp
        self.setEnabled(False)
        self.equip = equipApp(parent=self)
        self.equip.iniciar(self, 1)
        self.equip.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo


    def consultafuncio(self):

        cod = int(self.txtcodfuncio.text())
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from funcionario where codfuncio = %s', [cod])
        con.commit()
        rows = cur.fetchone()
        if int(rows[0]) > 0:

            cur.execute('select nomfuncio from funcionario where codfuncio = %s', [cod])
            con.commit()
            rows2 = cur.fetchone()
            self.txtnomfuncio.setText(rows2[0])
            self.txtcodequip.setFocus()
        else:
            mensaje = QtGui.QMessageBox.question(self, "Fornecedor nao encontrado",
                                                 "Deseja abrir o Registro de Fornecedores?", QtGui.QMessageBox.Yes,
                                                 QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                self.llamarfuncionario()

    def llamarfuncionario(self):
        # self.cerrar=1
        from codefuncionario import funcionarioApp
        self.setEnabled(False)
        self.funcionario = funcionarioApp(parent=self)
        self.funcionario.iniciar(self,0)
        self.funcionario.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo


    def todate(self):
        self.datedata.setFocus()
    def tofuncio(self):
        self.txtcodfuncio.setFocus()
    def tocobrado(self):

        valor = str(self.txtcomissao.text())
        bnd = 0
        p = 0
        res = ''
        while p != len(valor):
            if valor[p] == ",":
                res = res + "."
            else:
                res = res + valor[p]
            p = p + 1
        try:
            float(res)
        except Exception:
            QtGui.QMessageBox.about(self, 'Erro', 'Os dados somente podem ser numéricos')
            bnd = 1
        if bnd != 1:
            self.txtcobrado.setFocus()
            self.txttotalete.setText(str(float(self.txtsubtotal.text())+float(res)))
        else:
            # bnd == 0
            self.txtcomissao.clear()
            self.txtcomissao.setFocus()

    def gravar(self):
        cobrado = str(self.txtcobrado.text())
        comissao = str(self.txtcomissao.text())
        # ----
        p = 0
        res = ''
        while p != len(comissao):
            if comissao[p] == ",":
                res = res + "."
            else:
                res = res + comissao[p]
            p = p + 1
        comissao = res

        #---
        p = 0
        res = ''
        while p != len(cobrado):
            if cobrado[p] == ",":
                res = res + "."
            else:
                res = res + cobrado[p]
            p = p + 1
        cobrado = res

        if float(cobrado) >= float(self.txttotalete.text()):
            self.txtcodprod.clear()
            self.txtnomprod.clear()
            self.txtcantidad.clear()
            self.txtprecio.clear()
            codcliente = str(self.txtcodcliente.text())
            codfuncio = str(self.txtcodfuncio.text())
            codequip = str(self.txtcodequip.text())
            fecha = str(self.datedata.text())
            numservi = str(self.txtnum.text())
            if self.radabierto.isChecked():
                estado = '1'
            elif self.radproceso.isChecked():
                estado = '2'
            elif self.radconcluido.isChecked():
                estado = '3'

            #-----
            total = float(self.txttotalete.text())
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into servicio (codcliente, codfuncio, codequip, fecha, numservi, estado, cobrado, comissao,'
                    ' total) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', [codcliente, codfuncio, codequip, fecha, numservi,
                                                                   estado, cobrado, comissao, total])
                con.commit()
                cur.execute('select max(codservi) from servicio')
                cod = cur.fetchone()
                for i in range(int(self.tabla.rowCount())):
                    codprod = str(self.tabla.item(i,0).text())
                    cantidad = str(self.tabla.item(i,3).text())
                    precio = str(self.tabla.item(i, 2).text())
                    subtotal = str(self.tabla.item(i, 4).text())
                    # ---------------------------------------- algoritmo que cambia la coma por punto en los decimales
                    p = 0
                    res = ''
                    while p != len(cantidad):
                        if cantidad[p] == ",":
                            res = res + "."
                        else:
                            res = res + cantidad[p]
                        p = p + 1

                    p = 0
                    resprecio = ''
                    while p != len(precio):
                        if precio[p] == ",":
                            resprecio = resprecio + "."
                        else:
                            resprecio = resprecio + precio[p]
                        p = p + 1
                    # ----------------------------------------
                    cur.execute('insert into serviciodetalle (codservi, codprod, cantidad, precio, subtotal) values(%s,%s,%s,%s,%s)', [cod, codprod, res, precio, subtotal])
                    con.commit()
                    cur.execute('select stock from produto where codproduto=%s', [codprod])
                    con.commit()
                    stock = cur.fetchone()
                    suma = float(stock[0]) - float(res)
                    cur.execute('update produto set stock = %s where codproduto = %s', [suma, codprod])
                    con.commit()
            QtGui.QMessageBox.question(self, "Cadastro de ordem de serviço",
                                       "Cadastro com sucesso. Número da Ordem de Serviço: "+str(cod[0]), QtGui.QMessageBox.Ok)
            self.cancelar()
        else:
            QtGui.QMessageBox.question(self, "Erro na gravação",
                                       "O valor cobrado não pode ser menor que o valor total!", QtGui.QMessageBox.Ok)
            self.txtcobrado.setText('0')
            self.txtcomissao.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Delete:
                mensaje = QtGui.QMessageBox.question(self, "Excluindo produto",
                                                     "Deseja eliminar o produto selecionado?",
                                                     QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if (mensaje == QtGui.QMessageBox.Yes):
                    self.excluir()

        if e.key() == QtCore.Qt.Key_F5:
            if self.mod==1:
                self.gravarmod()

            self.txtcomissao.setEnabled(True)
            self.txtcobrado.setEnabled(True)
            self.txtcomissao.setFocus()

        if e.key() == QtCore.Qt.Key_F9:
            self.btnconsultar.click()


    def excluir(self):
        row = self.tabla.currentRow()
        numero = self.tabla.item(row,4).text()
        self.txtsubtotal.setText(str(float(self.txtsubtotal.text())-float(numero)))
        self.txttotalete.setText(str(float(self.txttotalete.text())-float(numero)))
        self.tabla.removeRow(row)
        self.sumalinea = self.sumalinea-1
        self.txtcodprod.setFocus()


    def cargarcantidad(self):
        #--------------
        number = self.txtcantidad.text()
        bandera = 0
        #-----
        p = 0
        suma = 0
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
                var = QtGui.QTableWidgetItem(str(self.txtcodprod.text()))
                nom = QtGui.QTableWidgetItem(str(self.txtnomprod.text()))
                cantidad = QtGui.QTableWidgetItem(str(self.txtcantidad.text()))
                precio = QtGui.QTableWidgetItem(str(self.txtprecio.text()))
                # subtotal = float(self.txtcantidad.text()) * float(self.txtprecio.text())
                subtotal = res * float(self.txtprecio.text())
                subtotal = QtGui.QTableWidgetItem(str(subtotal))
                self.sumalinea = self.sumalinea + 1
                self.tabla.setRowCount(self.sumalinea)
                linea = int(self.tabla.rowCount()) - 1
                self.tabla.setItem(linea, 0, var)
                self.tabla.setItem(linea, 1, nom)
                self.tabla.setItem(linea, 2, precio)
                self.tabla.setItem(linea, 3, cantidad)
                self.tabla.setItem(linea, 4, subtotal)
                #---------------
                self.txtcantidad.clear()
                self.txtnomprod.clear()
                self.txtcodprod.clear()
                self.txtprecio.clear()
                self.txtcodprod.setFocus()
                #----------------
                for i in range(self.sumalinea):
                    num = float(self.tabla.item(i, 4).text())
                    suma = num + suma
                self.txtsubtotal.setText(str(suma))
                self.txttotalete.setText(str(suma))
            else:
                QtGui.QMessageBox.question(self, "Erro ao cadastrar item",
                                                     "Favor digite a quantidade", QtGui.QMessageBox.Ok)
        else:
            self.txtcantidad.clear()
            self.txtcantidad.setFocus()


    def config(self,rows):
        lista = 'Codigo', 'Nome', 'Preço', 'Quantidade', 'Subtotal'
        self.tabla.setColumnCount(5)
        self.tabla.setRowCount(rows)
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0,182)
        self.tabla.setColumnWidth(1,541)
        self.tabla.setColumnWidth(3,150)
        self.tabla.setColumnWidth(2,201)
        self.tabla.setColumnWidth(4,241)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

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
                    cur.execute('select nomproduto, precio from produto where codproduto=%s', [var])
                    con.commit()
                    nom = cur.fetchone()
                    self.txtnomprod.setText(str(nom[0]))
                    self.txtprecio.setText(str(nom[1]))
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
        self.txtcodprod.setFocus()

    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        # self.cancelar()
        self.bnd = 0
        self.cancelar()
        self.txtnum.setEnabled(True)
        self.datedata.setEnabled(True)
        self.txtcodfuncio.setEnabled(True)
        self.btnfuncio.setEnabled(True)
        self.txtcodequip.setEnabled(True)
        self.btnequip.setEnabled(True)
        self.txtcodcliente.setEnabled(True)
        self.btncliente.setEnabled(True)
        self.grouprad.setEnabled(True)
        self.txtcodprod.setEnabled(True)
        self.txtcantidad.setEnabled(True)
        self.txtprecio.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btngrabar.setEnabled(True)
        self.btnmodificar.setEnabled(False)
        self.btnanular.setEnabled(False)
        self.btnlimpiar.setEnabled(True)
        self.btncancel.setEnabled(True)
        self.btnconsultar.setEnabled(False)
        # self.txtcobrado.setEnabled(True)
        self.txtnum.setFocus()


    #
    # def acthora(self):
    #     self.txtfecha.setText(time.strftime("%d/%m/%y"))
    #     self.txthora.setText(time.strftime("%H:%M"))

    def cancelar(self):
        self.datedata.setDate(QtCore.QDate.currentDate())
        #---------
        self.txtcod.setEnabled(False)
        self.txtnum.setEnabled(False)
        self.datedata.setEnabled(False)
        self.txtcodfuncio.setEnabled(False)
        self.btnfuncio.setEnabled(False)
        self.txtcodequip.setEnabled(False)
        self.btnequip.setEnabled(False)
        self.txtcodcliente.setEnabled(False)
        self.btncliente.setEnabled(False)
        self.grouprad.setEnabled(False)
        self.txtcodprod.setEnabled(False)
        self.txtcantidad.setEnabled(False)
        self.txtprecio.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btngrabar.setEnabled(False)
        self.btnmodificar.setEnabled(False)
        self.btnanular.setEnabled(False)
        self.btnlimpiar.setEnabled(False)
        self.btncancel.setEnabled(False)
        self.btnconsultar.setEnabled(True)
        self.btnmodificar.setEnabled(False)
        self.txtcobrado.setEnabled(False)
        self.txtcomissao.setEnabled(False)
        #---------
        self.sumalinea=0
        self.mod=0
        self.codlista=''
        self.txtcod.clear()
        self.txtnum.clear()
        self.txtcodfuncio.clear()
        self.txtnomfuncio.clear()
        self.txtcodequip.clear()
        self.txtnomequip.clear()
        self.txtcodcliente.clear()
        self.txtnomcliente.clear()
        self.tabla.clear()
        self.config(0)
        self.txtcodprod.clear()
        self.txtnomprod.clear()
        self.txtprecio.clear()
        self.txtcantidad.clear()
        self.txtsubtotal.clear()
        self.txtcomissao.clear()
        self.txtcobrado.clear()
        self.txttotalete.setText('0')
        self.txtsubtotal.setText('0')
        self.txtcomissao.setText('0')
        self.txtcobrado.setText('0')




def main():
    app = QtWidgets.QApplication(sys.argv)
    form = servicioApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()