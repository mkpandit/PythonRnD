#!/usr/bin/local python
# -*- coding: utf-8 -*-

'''
Dictionary application using Python
GUI implementation in PyQt5
'''

import os
import sys
import json

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog

from ui import Ui_MainWindow

'''
Dictionary class
'''
class Dictionary(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Dictionary, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_to_dictionary)

    def add_to_dictionary(self):
        d = {}

        # load existing dictionary
        dictionary_size = os.path.getsize('dictionary.json')
        if dictionary_size != 0:
            with open('dictionary.json', 'r') as fp:
                d = json.load(fp)

        # Process inputs
        synonym = self.lineEdit_2.text()
        definition = self.lineEdit.text()
        word = self.lineEdit_3.text()

        # Check if word already exists in dictionary
        if word in d:
            d[word]['def'] = definition
            d[word]['syn'] = synonym
        else:
            d[word] = {
                'def': definition,
                'syn': synonym
            }

        # Update dictionary file
        with open('dictionary.json', 'w') as fp:
            json.dump(d, fp)
        
        # self.show_status()

    '''
    def show_status(self):
        modal = QDialog()
        modal.setWindowTitle("Dialog")
        modal.exec_()
    '''

if __name__ == "__main__":
    dictionary = QApplication([])
    view = Dictionary()
    view.show()
    sys.exit(dictionary.exec_())