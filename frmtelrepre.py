# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmtelrepre.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmtelrepre(object):
    def setupUi(self, frmtelrepre):
        frmtelrepre.setObjectName("frmtelrepre")
        frmtelrepre.resize(810, 258)
        frmtelrepre.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.groupBox = QtWidgets.QGroupBox(frmtelrepre)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 381, 241))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnnovo = QtWidgets.QPushButton(self.groupBox)
        self.btnnovo.setGeometry(QtCore.QRect(20, 210, 75, 23))
        self.btnnovo.setObjectName("btnnovo")
        self.btneditar = QtWidgets.QPushButton(self.groupBox)
        self.btneditar.setGeometry(QtCore.QRect(110, 210, 75, 23))
        self.btneditar.setObjectName("btneditar")
        self.btncancelar = QtWidgets.QPushButton(self.groupBox)
        self.btncancelar.setGeometry(QtCore.QRect(200, 210, 75, 23))
        self.btncancelar.setObjectName("btncancelar")
        self.btneliminar = QtWidgets.QPushButton(self.groupBox)
        self.btneliminar.setGeometry(QtCore.QRect(290, 210, 75, 23))
        self.btneliminar.setObjectName("btneliminar")
        self.btnsalvar = QtWidgets.QPushButton(self.groupBox)
        self.btnsalvar.setGeometry(QtCore.QRect(110, 210, 75, 23))
        self.btnsalvar.setObjectName("btnsalvar")
        self.txtcod = QtWidgets.QLineEdit(self.groupBox)
        self.txtcod.setEnabled(False)
        self.txtcod.setGeometry(QtCore.QRect(170, 10, 113, 20))
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
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.txtrepre = QtWidgets.QLineEdit(self.groupBox)
        self.txtrepre.setEnabled(False)
        self.txtrepre.setGeometry(QtCore.QRect(170, 40, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtrepre.setFont(font)
        self.txtrepre.setText("")
        self.txtrepre.setMaxLength(40)
        self.txtrepre.setObjectName("txtrepre")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.txttelefone = QtWidgets.QLineEdit(self.groupBox)
        self.txttelefone.setGeometry(QtCore.QRect(170, 80, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txttelefone.setFont(font)
        self.txttelefone.setText("")
        self.txttelefone.setMaxLength(40)
        self.txttelefone.setObjectName("txttelefone")
        self.groupBox_2 = QtWidgets.QGroupBox(frmtelrepre)
        self.groupBox_2.setGeometry(QtCore.QRect(400, 10, 401, 241))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.tabla = QtWidgets.QTableWidget(self.groupBox_2)
        self.tabla.setEnabled(True)
        self.tabla.setGeometry(QtCore.QRect(10, 40, 381, 191))
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.tabla.horizontalHeader().setHighlightSections(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setHighlightSections(False)
        self.lblsinreg = QtWidgets.QLabel(self.groupBox_2)
        self.lblsinreg.setGeometry(QtCore.QRect(160, 130, 71, 21))
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

        self.retranslateUi(frmtelrepre)
        self.tabla.cellClicked['int','int'].connect(self.lblindice.setNum) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(frmtelrepre)
        frmtelrepre.setTabOrder(self.txtbuscar, self.txtrepre)
        frmtelrepre.setTabOrder(self.txtrepre, self.txttelefone)
        frmtelrepre.setTabOrder(self.txttelefone, self.btnnovo)
        frmtelrepre.setTabOrder(self.btnnovo, self.btneditar)
        frmtelrepre.setTabOrder(self.btneditar, self.btnsalvar)
        frmtelrepre.setTabOrder(self.btnsalvar, self.btncancelar)
        frmtelrepre.setTabOrder(self.btncancelar, self.btneliminar)
        frmtelrepre.setTabOrder(self.btneliminar, self.tabla)
        frmtelrepre.setTabOrder(self.tabla, self.txtcod)

    def retranslateUi(self, frmtelrepre):
        _translate = QtCore.QCoreApplication.translate
        frmtelrepre.setWindowTitle(_translate("frmtelrepre", "Registro de Fornecedor"))
        self.btnnovo.setText(_translate("frmtelrepre", "Novo"))
        self.btneditar.setText(_translate("frmtelrepre", "Editar"))
        self.btncancelar.setText(_translate("frmtelrepre", "Cancelar"))
        self.btneliminar.setText(_translate("frmtelrepre", "Eliminar"))
        self.btnsalvar.setText(_translate("frmtelrepre", "Salvar"))
        self.label_7.setText(_translate("frmtelrepre", "Código:"))
        self.label_2.setText(_translate("frmtelrepre", "Nome do Representante:"))
        self.label_3.setText(_translate("frmtelrepre", "Telefone:"))
        self.lblsinreg.setText(_translate("frmtelrepre", "Sem Registros"))
        self.lblindice.setText(_translate("frmtelrepre", "TextLabel"))
        self.label_8.setText(_translate("frmtelrepre", "Buscar:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmtelrepre = QtWidgets.QWidget()
    ui = Ui_frmtelrepre()
    ui.setupUi(frmtelrepre)
    frmtelrepre.show()
    sys.exit(app.exec_())
