# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmpessoas.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmpessoas(object):
    def setupUi(self, frmpessoas):
        frmpessoas.setObjectName("frmpessoas")
        frmpessoas.resize(291, 300)
        self.groupBox = QtWidgets.QGroupBox(frmpessoas)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 271, 281))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnclientes = QtWidgets.QPushButton(self.groupBox)
        self.btnclientes.setGeometry(QtCore.QRect(10, 10, 251, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnclientes.setFont(font)
        self.btnclientes.setObjectName("btnclientes")
        self.btnfuncio = QtWidgets.QPushButton(self.groupBox)
        self.btnfuncio.setGeometry(QtCore.QRect(10, 100, 251, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnfuncio.setFont(font)
        self.btnfuncio.setObjectName("btnfuncio")
        self.btnfornecedor = QtWidgets.QPushButton(self.groupBox)
        self.btnfornecedor.setGeometry(QtCore.QRect(10, 190, 251, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnfornecedor.setFont(font)
        self.btnfornecedor.setObjectName("btnfornecedor")

        self.retranslateUi(frmpessoas)
        QtCore.QMetaObject.connectSlotsByName(frmpessoas)

    def retranslateUi(self, frmpessoas):
        _translate = QtCore.QCoreApplication.translate
        frmpessoas.setWindowTitle(_translate("frmpessoas", "Cadastro de Pessoas"))
        self.btnclientes.setText(_translate("frmpessoas", "Cadastro de Clientes"))
        self.btnfuncio.setText(_translate("frmpessoas", "Cadastro de Funcionarios"))
        self.btnfornecedor.setText(_translate("frmpessoas", "Cadastro de Fornecedores"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmpessoas = QtWidgets.QDialog()
    ui = Ui_frmpessoas()
    ui.setupUi(frmpessoas)
    frmpessoas.show()
    sys.exit(app.exec_())