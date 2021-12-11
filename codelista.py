#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmlista
from codeconexion import conexion

class listaApp(QtWidgets.QMainWindow, frmlista.Ui_frmlista):
    conexion=conexion()
    caller=None
    buscar="'%%'"
    codfuncio="*"
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # self.enabledata()
        # self.setFixedWidth(980)
        # self.setFixedHeight(539)
        self.checkdata.stateChanged.connect(self.enabledata)
        self.txtbuscar.textChanged.connect(self.fbuscar)  
        self.datemin.dateChanged.connect(self.consultar)
        self.datemax.dateChanged.connect(self.consultar)
        self.cboestado.currentIndexChanged.connect(self.consultar)
        self.tabla.doubleClicked.connect(self.devolver)
        self.btnimprimir.clicked.connect(self.imprimir)
        self.cbofuncio.currentIndexChanged.connect(self.cargarfuncio)
        self.checkfuncio.stateChanged.connect(self.enablefuncio)
        self.enablefuncio()
        self.funcio()
        self.cargarfuncio()
        self.consultar()
        #-----
        #self.tabla.setSortingEnabled(True)
        #self.tabla.resizeRowsToContents()
        #self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)        
        
        #header = self.tabla.horizontalHeader()
        #header.setStretchLastSection(True)        
        #-----
        #self.btnimprimir.setEnabled(False)
        #self.checkdata.setChecked(True)
        #self.checkconta.isChecked(True)
        self.txtbuscar.setFocus()

    def imprimir(self):
        from codepdf import pdf
        gen=pdf()
        gen.generar(self.servi, self.fechamin, self.fechamax, self.bndestado, self.bandera, self.rows, self.sumacomissao, self.sumatotal, self.sumacobrado)
        # lista = 'Codigo', 'Nº Servi', 'Cliente', 'Funcionario', 'Equipamento', 'Data', 'Estado', 'Comissão', 'Total', 'Cobrado', 'Obs.'

    def enabledata(self):
        if self.checkdata.isChecked():
            self.datemin.setEnabled(True)
            self.datemax.setEnabled(True)
        else:
            self.datemin.setEnabled(False)
            self.datemax.setEnabled(False)
        self.consultar()
    
    def iniciar(self,caller,servicio):
        self.caller=caller
        if servicio==1:
            self.btnimprimir.setVisible(False)
        # Del menu, poner servicio 0

    def devolver(self):
        row = self.tabla.currentRow()
        cod = self.tabla.item(row, 0).text()
        self.caller.txtcod.setText(cod)
        # self.caller.setEnabled(True)
        self.close()
        self.caller.btnconsultar.click()

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
    
    def enabledata(self):
        if self.checkdata.isChecked():
            self.datemin.setEnabled(True)
            self.datemax.setEnabled(True)
        else:
            self.datemin.setEnabled(False)
            self.datemax.setEnabled(False)   
        self.consultar()

    def fbuscar(self):
        buscado=str(self.txtbuscar.text())
        if len(buscado)>0:
            self.buscar="'"+buscado+"%'"
            #print self.buscar
        else:
            self.buscar="'%%'"
        self.consultar()  
        
    def config(self,rows):
        self.tabla.setColumnCount(10)
        self.tabla.setRowCount(int(self.rows[0]))
        lista = 'Codigo', 'Nº Servi', 'Cliente', 'Funcionario', 'Equipamento', 'Data', 'Estado', 'Comissão', 'Total', 'Cobrado'
        self.tabla.setHorizontalHeaderLabels(lista)
        # self.tabla.resizeRowsToContents()
        # self.tabla.resizeColumnsToContents()
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        # header.setResizeMode(1, QtGui.QHeaderView.Stretch)

    def funcio(self):

        # -------------
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from funcionario')
        rowfuncio = cur.fetchone()
        funcio = int(rowfuncio[0])

        # self.cargarbanco()
        if funcio > 0:
            cur.execute('select nomfuncio, codfuncio from funcionario order by codfuncio')
            self.verfuncio = cur.fetchall()
            self.cbofuncio.setMaxVisibleItems(10)
            for row in range(funcio):
                self.cbofuncio.insertItem(row, self.verfuncio[row][0])
            self.cbofuncio.setCurrentIndex(0)
            # if self.cont > 0:
            #     valor = self.cboconta.currentIndex()
            #     item = self.verbanco[int(valor)]
            #     self.lblconta.setText(str(item[0]))

    def cargarfuncio(self):
        valor=self.cbofuncio.currentIndex()
        self.codfuncio=str(self.verfuncio[int(valor)][1])
        self.consultar()

    def enablefuncio(self):
        if self.checkfuncio.isChecked():
            self.cbofuncio.setEnabled(True)
        else:
            self.cbofuncio.setEnabled(False)
        self.consultar()

    def consultar(self):
        con=None
        con=self.conexion.conectar()
        cur=con.cursor()
        #-------------------- Esta parte lee los datos de la fecha
        self.fechamax=self.datemax.date()
        self.fechamax=str(self.fechamax.toString('dd/MM/yyyy'))
        self.fechamin=self.datemin.date()
        self.fechamin=str(self.fechamin.toString('dd/MM/yyyy'))
        fecha=''
        if self.checkdata.isChecked():
            fecha=" and fecha between '"+self.fechamin+"' and '"+self.fechamax+"'"
        # ----------------------
        codfuncio=' and a.codfuncio>0'
        if self.checkfuncio.isChecked():
            codfuncio = ' and a.codfuncio=' + self.codfuncio
        #---------------------- Esta parte lee los datos del estado del proceso de servicio, Todos, Aberto, Processo, Concluido
        estado=''
        self.bndestado=0
        if self.cboestado.currentIndex()==1:
            estado=" and estado='1'"
            self.bndestado=1
        elif self.cboestado.currentIndex()==2:
            estado=" and estado='2'"
            self.bndestado=2
        elif self.cboestado.currentIndex()==3:
            estado=" and estado='3'"
            self.bndestado=3
        # estado 1 = aberto, estado 2 = processo, estado 3 = concluido
        #---------------------- Esta parte revisa si el selector de fecha está encendido y consigue cuantas lineas
        if self.checkdata.isChecked():
            cur.execute('select count (*) from servicio a where numservi like '+self.buscar+estado+fecha+codfuncio)
            bandera=0
            #print bandera
        elif not self.checkdata.isChecked():
            cur.execute('select count (*) from servicio a where numservi like '+self.buscar+estado+codfuncio)
            bandera=1
            #print bandera
        self.bandera=bandera
        rows=cur.fetchone()
        self.rows=rows
        #-----
        self.sumacomissao = 0
        self.sumatotal = 0
        self.sumacobrado = 0
        if (int(rows[0])>0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            datachar="to_char(a.fecha,'DD/MM/YYYY')"

            if bandera==1:
                cur.execute('select a.codservi, a.numservi, b.nomcliente, c.nomfuncio, d.nomequip,'+datachar+', a.estado, '
                            'a.comissao, a.total, a.cobrado from servicio a, cliente b, funcionario c, equipamento d'
                            ' where a.codcliente=b.codcliente and a.codfuncio=c.codfuncio'+codfuncio+' and a.codequip=d.codequip and a.numservi like'+self.buscar+estado+' order by a.codservi asc')

            elif bandera==0:
                cur.execute('select a.codservi, a.numservi, b.nomcliente, c.nomfuncio, d.nomequip,' + datachar + ', a.estado, '
                        'a.comissao, a.total, a.cobrado from servicio a, cliente b, funcionario c, equipamento d'
                        ' where a.codcliente=b.codcliente and a.codfuncio=c.codfuncio'+codfuncio+' and a.codequip=d.codequip and a.numservi like' + self.buscar + estado + fecha+' order by a.codservi asc')
                
            self.servi=cur.fetchall()
            for i in range(int(rows[0])):
                item=self.servi[i]
                cod=QtWidgets.QTableWidgetItem(str(item[0]))
                num=QtWidgets.QTableWidgetItem(str(item[1]))
                cliente=QtWidgets.QTableWidgetItem(str(item[2]))
                funcio=QtWidgets.QTableWidgetItem(str(item[3]))
                equip=QtWidgets.QTableWidgetItem(str(item[4]))
                fecha=QtWidgets.QTableWidgetItem(str(item[5]))
                comissao=QtWidgets.QTableWidgetItem(str(item[7]))
                total=QtWidgets.QTableWidgetItem(str(item[8]))
                cobrado=QtWidgets.QTableWidgetItem(str(item[9]))
                # obs=QtGui.QTableWidgetItem(str(item[10]))
                self.tabla.setItem(i,0,cod)
                self.tabla.setItem(i,1,num)
                self.tabla.setItem(i,2,cliente)
                self.tabla.setItem(i,3,funcio)
                self.tabla.setItem(i,4,equip)
                self.tabla.setItem(i,5,fecha)
                status = QtWidgets.QTableWidgetItem('')
                #Conversor de estado
                if int(item[6])==1:
                    status=QtWidgets.QTableWidgetItem('Aberto')
                elif int(item[6])==2:
                    status=QtWidgets.QTableWidgetItem('Em processo')
                elif int(item[6])==3:
                    status=QtWidgets.QTableWidgetItem('Concluido')

                self.tabla.setItem(i,6,status)
                self.tabla.setItem(i,7,comissao)
                self.tabla.setItem(i,8,total)
                self.tabla.setItem(i,9,cobrado)
                # self.tabla.setItem(i,10,obs)
                self.sumacomissao = self.sumacomissao + float(item[7])
                self.sumatotal = self.sumatotal + float(item[8])
                self.sumacobrado = self.sumacobrado + float(item[9])
                # print self.sumacomissao
                # print self.sumatotal
                # print self.sumacobrado
            self.total.setText(str(self.sumatotal))
            self.totalcobrado.setText(str(self.sumacobrado))
            self.totalcomissao.setText(str(self.sumacomissao))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = listaApp() 
    form.show()
    app.exec_()
if __name__ == '__main__': 
    main()         