# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmcliente.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmcliente(object):
    def setupUi(self, frmcliente):
        frmcliente.setObjectName("frmcliente")
        frmcliente.resize(871, 258)
        frmcliente.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.groupBox = QtWidgets.QGroupBox(frmcliente)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 361, 241))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.txtnom = QtWidgets.QLineEdit(self.groupBox)
        self.txtnom.setGeometry(QtCore.QRect(150, 40, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtnom.setFont(font)
        self.txtnom.setMaxLength(40)
        self.txtnom.setObjectName("txtnom")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnnovo = QtWidgets.QPushButton(self.groupBox)
        self.btnnovo.setGeometry(QtCore.QRect(10, 210, 75, 23))
        self.btnnovo.setObjectName("btnnovo")
        self.btneditar = QtWidgets.QPushButton(self.groupBox)
        self.btneditar.setGeometry(QtCore.QRect(100, 210, 75, 23))
        self.btneditar.setObjectName("btneditar")
        self.btncancelar = QtWidgets.QPushButton(self.groupBox)
        self.btncancelar.setGeometry(QtCore.QRect(190, 210, 75, 23))
        self.btncancelar.setObjectName("btncancelar")
        self.btneliminar = QtWidgets.QPushButton(self.groupBox)
        self.btneliminar.setGeometry(QtCore.QRect(280, 210, 75, 23))
        self.btneliminar.setObjectName("btneliminar")
        self.btnsalvar = QtWidgets.QPushButton(self.groupBox)
        self.btnsalvar.setGeometry(QtCore.QRect(100, 210, 75, 23))
        self.btnsalvar.setObjectName("btnsalvar")
        self.txtcod = QtWidgets.QLineEdit(self.groupBox)
        self.txtcod.setEnabled(False)
        self.txtcod.setGeometry(QtCore.QRect(150, 10, 113, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtcod.setFont(font)
        self.txtcod.setObjectName("txtcod")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 46, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.groupBox_2 = QtWidgets.QGroupBox(frmcliente)
        self.groupBox_2.setGeometry(QtCore.QRect(380, 10, 481, 241))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.tabla = QtWidgets.QTableWidget(self.groupBox_2)
        self.tabla.setEnabled(True)
        self.tabla.setGeometry(QtCore.QRect(10, 40, 461, 191))
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.tabla.horizontalHeader().setHighlightSections(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setHighlightSections(False)
        self.lblsinreg = QtWidgets.QLabel(self.groupBox_2)
        self.lblsinreg.setGeometry(QtCore.QRect(200, 130, 71, 21))
        self.lblsinreg.setObjectName("lblsinreg")
        self.lblindice = QtWidgets.QLabel(self.groupBox_2)
        self.lblindice.setGeometry(QtCore.QRect(340, 0, 46, 13))
        self.lblindice.setObjectName("lblindice")
        self.txtbuscar = QtWidgets.QLineEdit(self.groupBox_2)
        self.txtbuscar.setGeometry(QtCore.QRect(60, 10, 171, 20))
        self.txtbuscar.setObjectName("txtbuscar")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 46, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.txttel = QtWidgets.QLineEdit(frmcliente)
        self.txttel.setGeometry(QtCore.QRect(160, 90, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txttel.setFont(font)
        self.txttel.setMaxLength(20)
        self.txttel.setObjectName("txttel")
        self.label_3 = QtWidgets.QLabel(frmcliente)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.txtcpf = QtWidgets.QLineEdit(frmcliente)
        self.txtcpf.setGeometry(QtCore.QRect(160, 170, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtcpf.setFont(font)
        self.txtcpf.setMaxLength(20)
        self.txtcpf.setObjectName("txtcpf")
        self.label_4 = QtWidgets.QLabel(frmcliente)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.txtrg = QtWidgets.QLineEdit(frmcliente)
        self.txtrg.setGeometry(QtCore.QRect(160, 130, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtrg.setFont(font)
        self.txtrg.setText("")
        self.txtrg.setMaxLength(20)
        self.txtrg.setObjectName("txtrg")
        self.label_5 = QtWidgets.QLabel(frmcliente)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(frmcliente)
        self.tabla.cellClicked['int','int'].connect(self.lblindice.setNum) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(frmcliente)
        frmcliente.setTabOrder(self.txtcod, self.txtbuscar)
        frmcliente.setTabOrder(self.txtbuscar, self.txtnom)
        frmcliente.setTabOrder(self.txtnom, self.txttel)
        frmcliente.setTabOrder(self.txttel, self.txtrg)
        frmcliente.setTabOrder(self.txtrg, self.txtcpf)
        frmcliente.setTabOrder(self.txtcpf, self.btnnovo)
        frmcliente.setTabOrder(self.btnnovo, self.btneditar)
        frmcliente.setTabOrder(self.btneditar, self.btnsalvar)
        frmcliente.setTabOrder(self.btnsalvar, self.btncancelar)
        frmcliente.setTabOrder(self.btncancelar, self.btneliminar)
        frmcliente.setTabOrder(self.btneliminar, self.tabla)

    def retranslateUi(self, frmcliente):
        _translate = QtCore.QCoreApplication.translate
        frmcliente.setWindowTitle(_translate("frmcliente", "Registro de Cliente"))
        self.label.setText(_translate("frmcliente", "Nome do cliente:"))
        self.btnnovo.setText(_translate("frmcliente", "Novo"))
        self.btneditar.setText(_translate("frmcliente", "Editar"))
        self.btncancelar.setText(_translate("frmcliente", "Cancelar"))
        self.btneliminar.setText(_translate("frmcliente", "Eliminar"))
        self.btnsalvar.setText(_translate("frmcliente", "Salvar"))
        self.label_7.setText(_translate("frmcliente", "Código:"))
        self.lblsinreg.setText(_translate("frmcliente", "Sem Registros"))
        self.lblindice.setText(_translate("frmcliente", "TextLabel"))
        self.label_8.setText(_translate("frmcliente", "Buscar:"))
        self.label_3.setText(_translate("frmcliente", "Telefone:"))
        self.label_4.setText(_translate("frmcliente", "C.P.F.:"))
        self.label_5.setText(_translate("frmcliente", "R.G:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmcliente = QtWidgets.QWidget()
    ui = Ui_frmcliente()
    ui.setupUi(frmcliente)
    frmcliente.show()
    sys.exit(app.exec_())
