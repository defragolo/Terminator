# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Terminator_Interface_05.03.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!
import sys
import os
import csv
import datetime
import tkinter as tk
from tkinter.filedialog import askopenfilename
from io import open
#import Main1103
from MyTable import Mytable
from fonctions_terminator import pseudo_main
from Import_script import export
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QHeaderView, QWidget, QLabel, QApplication, QWidget, QPushButton, QMessageBox

class Ui_MainWindow(object):
    app = QtWidgets.QApplication(sys.argv)
    
    listBuffer=[]
    additionalInfos=[]
    
    
    def add_Item(self):
        print("Adding a new word in the dictionnary : \n")
        ajoute = False
        word = input("What word do you want to add to the dictionnary ? \n")
        word = word.lower() # word in lower case
        
    
        ######################## DICTIONNARY'S CHOICE ########################
    
        print("In which dictionnary ? \n")
        print("1) Organs/Synonyms dictionnary \n")
        print("2) Properties/Values dictionnary \n")
        print("3) Name extensions dictionnary \n")
        
        c = input("Your choice ? 1,2 or 3 ? \n")
        if c == '1': 
            file = 'organsList' # define the file we are working in
            dico = open('organsList') # load the dictionnary
            print("You chose Organs/Synonyms dictionnary. \n")
        elif c == '2': 
            file = 'valuesDico' # define the file we are working in
            dico = open('valuesDico') # load the dictionnary
            print("You chose Properties/Values dictionnary. \n")
        elif c == '3': 
            dico = open('relativeProp') # define the file we are working in
            file = 'relativeProp' # load the dictionnary
            print("You chose Name extensions dictionnary. \n")
        else: # if the user enters something else
            print("Error")
            
        ####################################################################
        
        syno = input("Is this word the synonym for another one ? y/n \n")
        
        if syno == 'y' or syno == 'Y': # if the word is synonym of another one
            newsyno = input("Which one ? \n")
            newsyno = newsyno.lower() # new synonym in lower case
            
            for key in dico: # look in the entire dictionnary
                if newsyno in dico.keys(): # if newsyno is a key in the dictionnary
                    dico[newsyno].append(word) # add word in the values of the newsyno key
                    with open(file,'wb') as newdico: # open the file containing the dico (with 'write' argument)
                        pickle.dump(dico,newdico) # modify the file containing the dico
                        newdico.close() # close the file
                    print("The word is now in the dictionnary. \n")
                    ajoute = True
                    break # exit the loop
                else: # if newsyno is not a key in the dictionnary
                    for i in dico.values(): # we look in the values of the dictionnary
                        if newsyno in i: # if newsyno is in the values of the dictionnary
                            i.append(word) # we add it in the list of the corresponding values
                            with open(file,'wb') as newdico: # open the file containing the dico (with 'write' argument)
                                pickle.dump(dico,newdico) # modify and save the file
                                newdico.close() # close the file 
                            print("The word is now in the dictionnary. \n")
                            ajoute = True
                    break # exit the loop
            if ajoute == False: 
                print("This word is not in the dictionnary. \n")
        
        elif syno == 'n' or syno == 'N': # if word is not a synonym of another word
            dico[word] = [] # add the word as a key in the dictionnary
            with open(file,'wb') as newdico: # open the file containing the dico (with 'write' argument)
                pickle.dump(dico,newdico) # modify and save the file
                newdico.close() # close the file
                print("The word is now in the dictionnary. \n")
                ajoute = True
            if ajoute == False: 
                print("This word is not in the dictionnary. \n")
        else: # if the user enters something else
            print("Error")

      # import a file in the interface  
    def import_Fichier (self,f):  
       # on crée la liste des fichiers
        root = tk.Tk()
        root.withdraw()             # pour ne pas afficher la fenêtre Tk
        filepath = askopenfilename(filetypes=[('txt files','.txt')])   # lance la fenêtre
        print (filepath) 
       #ouverture du fichier test.txt en mode read 'r' (lecture en mode texte)
        name = open(filepath, "r") 
        f = name.readlines() 
        #print (f)
        str1 = ''.join(f)
        self.textEditPublishedDescription.append(str1)

    # Export in the directory a file "TerminatorResults-date-hour.xlsx"
    def exportExcel(self):
        self.labelErrorExecute.setText("")
        self. additionalInfos.append(self.lineEditRefNum.text())
        self.additionalInfos.append(self.lineEditSpeciesNum.text())
        self.additionalInfos.append(self.lineEditRecNum.text())
        self.additionalInfos.append(self.lineEditGenus.text())
        self.additionalInfos.append(self.lineEditSpecies.text())
        self.additionalInfos.append(self.lineEditPopulation.text())
        self.additionalInfos.append(self.lineEditStage.text())
        self.additionalInfos.append(self.lineEditSex.text())
        self.additionalInfos.append(self.lineEditLocality.text())
        self.additionalInfos.append(self.lineEditHost.text())
        
        try:
            export(self.triads, self.additionalInfos) #mauvaise forme de tableau
            self.labelErrorExecute.setText("Export successful")
            
        except:
            print("Fail creation")
            self.labelErrorExecute.setText("Fail creation")
    
    #adds a new line in the Result table with a checkbox in the validated column        
    def addTriad(self):
        self.labelErrorExecute.setText("")
        self.tableViewResultExecute.addRow()
        #cell value can't be empty because else their value can be changed even when validated checkbox is checked
        self.tableViewResultExecute.setValue1(self.tableViewResultExecute.rowCount()-1,"none","none","none","none")


################################################################################
   ###########################################################
   #méthode pour le bouton undo a corriger 
   ############################################################
    def undo1(self):
        self.tableViewResultExecute.addRow()
        buffer1=self.listBuffer[len(self.listBuffer)-1]
        i=self.tableViewResultExecute.rowCount()
        print("i:")
        print(i)
        
        organ=buffer1[0]
        properti=buffer1[1]
        value=buffer1[2]
        self.tableViewResultExecute.setValue1((i-1),organ,properti,value)
        self.tableViewResultExecute.update()
        del self.listBuffer[-1]

    #deletes all the selected rows
    def deleteTriad(self):
        deletion = self.tableViewResultExecute.deleteLines()
        if(not(deletion)):
            self.labelErrorExecute.setText("No selected line")
   
        
   #############################################
   # méthode bouton next ok 
   ############################################
    def boutonNext(self):
        #On ne peut pas cliquer sur next si Published description est vide
        if(self.textEditPublishedDescription.toPlainText() != ""):
            self.tab.setCurrentIndex(2)
            self.processImport()
            self.labelEmptyField.setText("")
            self.textEditPublishedDescriptionExecutePage.setText(self.findCurrentSentence())
            self.displayCurrentTriads()
        else:
            self.labelEmptyField.setText("The field Published Description cannot be empty.")
            
            
    def findCurrentSentence(self):
        i = 0
        for j in self.sentences:
            if(i==self.currentSentence):
                return (j)
            i=i+1
            
        
    #displays the triads of the currently analysed sentence            
    def displayCurrentTriads(self):
        i = 0
        self.tableViewResultExecute.resetTable()
        for j in self.triads:
            if(i==self.currentSentence):
                self.displayTriads(j)
                return
            i=i+1
            
    
    #displays in the table in Execute all the given triads         
    def displayTriads(self, triads):
        triadNumber = 0
        for triad in triads:
                self.tableViewResultExecute.addRow()
                organ = triad[0]
                prop = triad[1]
                val = triad[2]
                #Modifier value is "None" because if the cell is empty, it can be modified even if validated is checked
                self.tableViewResultExecute.setValue1(triadNumber, organ, prop, val, "none")
                triadNumber += 1
                               
            
    #when the user clicks on the Next button in Execute, the next triad appears
    def buttonNextExecute(self):
        self.labelErrorExecute.setText("")
        self.currentSentence += 1
        self.textEditPublishedDescriptionExecutePage.setText(self.findCurrentSentence())
        self.displayCurrentTriads()
        #disables the buttons Previous and Next when needed
        if(self.currentSentence != 0):
            self.pushButtonPreviousExecute.setEnabled(True)
        if(self.currentSentence == len(self.sentences)-1):
            self.pushButtonNextExecute.setEnabled(False)
        

    #when the user clicks on the Previous button in Execute, the previous triad appears
    def buttonPreviousExecute(self):
        self.labelErrorExecute.setText("")
        self.currentSentence -= 1
        self.textEditPublishedDescriptionExecutePage.setText(self.findCurrentSentence())
        self.displayCurrentTriads()
        #Disables the buttons Previous and Next when needed
        if(self.currentSentence == 0):
            self.pushButtonPreviousExecute.setEnabled(False)
        if(self.currentSentence != len(self.sentences)-1):
            self.pushButtonNextExecute.setEnabled(True)
        
############################################################
    def open_dialog(self):
        dialog = QtWidgets.QDialog()
        # dialog.ui = Form()
        # dialog.ui.setupUi(dialog)
        # dialog.exec_()
        dialog.show()

    def processImport(self):
        dicotampon = pseudo_main(self.textEditPublishedDescription.toPlainText())
        self.textEditPublishedDescriptionExecutePage.clear()
        # self.textEditPublishedDescriptionExecutePage.insertPlainText(tampon)
        self.currentSentence = 0
        self.sentences = dicotampon.keys()
        self.lastSentence = len(self.sentences)
        self.triads = dicotampon.values()
        print(self.triads)
        #if there is only one sentence to analyse, the Next button in Execute is disabled
        if(len(self.sentences) == 1):
            self.pushButtonNextExecute.setEnabled(False)


    def setupUi(self, MainWindow):
        # setting of the window and the home page 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(975, 676)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.tab = QtWidgets.QTabWidget(self.centralwidget)
        self.tab.setToolTipDuration(-5)
        self.tab.setObjectName("tab")
        self.home_page = QtWidgets.QWidget()
        self.home_page.setObjectName("home_page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.home_page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layoutHome = QtWidgets.QVBoxLayout()               
        self.layoutHome.setObjectName("layoutHome")
        self.labelHome4 = QtWidgets.QLabel(self.home_page)
        self.labelHome4.setObjectName("labelHome4")
        self.layoutHome.addWidget(self.labelHome4)                        
        self.labelHome1 = QtWidgets.QLabel(self.home_page)
        self.labelHome1.setObjectName("labelHome1")
        self.layoutHome.addWidget(self.labelHome1)
        self.labelHome2 = QtWidgets.QLabel(self.home_page)
        self.labelHome2.setObjectName("labelHome2")
        self.layoutHome.addWidget(self.labelHome2)
        self.horizontalLayout.addLayout(self.layoutHome)
        self.tab.addTab(self.home_page, "")
        self.importText_page = QtWidgets.QWidget()
        self.importText_page.setToolTip("")
        
        # import text part 
        self.importText_page.setObjectName("importText_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.importText_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layoutImportText1 = QtWidgets.QVBoxLayout()
        self.layoutImportText1.setObjectName("layoutImportText1")
        self.layoutImportText2 = QtWidgets.QFormLayout()
        self.layoutImportText2.setObjectName("layoutImportText2")
        
        
        self.layoutImportText3 = QtWidgets.QFormLayout()
        self.layoutImportText3.setObjectName("layoutImportText3")
        self.labelRefNum = QtWidgets.QLabel(self.importText_page)       

        ##ref num
        self.labelRefNum.setObjectName("labelRefNum")
        self.layoutImportText3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelRefNum)
        self.lineEditRefNum = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditRefNum.setObjectName("lineEditRefNum")
        self.layoutImportText3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditRefNum)
     
        ## specie num
        self.labelSpeciesNum = QtWidgets.QLabel(self.importText_page)
        self.labelSpeciesNum.setObjectName("labelSpeciesNum")
        self.layoutImportText3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelSpeciesNum)
        self.lineEditSpeciesNum = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditSpeciesNum.setObjectName("lineEditSpeciesNum")
        self.layoutImportText3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditSpeciesNum)
       
        ## rec num 
        self.labelRecNum = QtWidgets.QLabel(self.importText_page)     
        self.labelRecNum.setObjectName("labelRecNum")
        self.layoutImportText3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelRecNum)
        self.lineEditRecNum = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditRecNum.setObjectName("lineEditRecNum")
        self.layoutImportText3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEditRecNum)
        
        ##genus
        self.labelGenus = QtWidgets.QLabel(self.importText_page)     
        self.labelGenus.setObjectName("labelGenus")
        self.layoutImportText3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelGenus)
        self.lineEditGenus = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditGenus.setObjectName("lineEditGenus")
        self.layoutImportText3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEditGenus)
        
        #specie 
        self.labelSpecies = QtWidgets.QLabel(self.importText_page)
        self.labelSpecies.setObjectName("labelSpecies")
        self.layoutImportText3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.labelSpecies)
        self.lineEditSpecies = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditSpecies.setObjectName("lineEditSpecies")
        self.layoutImportText3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEditSpecies)
        
        #population
        self.labelPopulation = QtWidgets.QLabel(self.importText_page)
        self.labelPopulation.setObjectName("labelPopulation")
        self.layoutImportText3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.labelPopulation)
        self.lineEditPopulation = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditPopulation.setObjectName("lineEditPopulation")
        self.layoutImportText3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEditPopulation)
        
        #sexe
        self.labelSex = QtWidgets.QLabel(self.importText_page)
        self.labelSex.setObjectName("labelSex")
        self.layoutImportText3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.labelSex)
        self.lineEditSex = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditSex.setObjectName("lineEditSex")
        self.layoutImportText3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEditSex)
        
        #stage
        self.labelStage = QtWidgets.QLabel(self.importText_page)
        self.labelStage.setObjectName("labelStage")
        self.layoutImportText3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.labelStage)
        self.lineEditStage = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditStage.setObjectName("lineEditStage")
        self.layoutImportText3.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEditStage)

        #Locality
        self.labelLocality = QtWidgets.QLabel(self.importText_page)
        self.labelLocality.setObjectName("labelLocality")
        self.layoutImportText3.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.labelLocality)
        self.lineEditLocality = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditLocality.setObjectName("lineEditLocality")
        self.layoutImportText3.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lineEditLocality)
        
        #Host
        self.labelHost = QtWidgets.QLabel(self.importText_page)
        self.labelHost.setObjectName("labelHost")
        self.layoutImportText3.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.labelHost)
        self.lineEditHost = QtWidgets.QLineEdit(self.importText_page)
        self.lineEditHost.setObjectName("lineEditHost")
        self.layoutImportText3.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEditHost)
        
        #espace entre age et published description
        spacerItem = QtWidgets.QSpacerItem(20, 9, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutImportText3.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem)
        
        # zone de texte
        self.layoutImportText2.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.layoutImportText3)
        self.layoutDescription = QtWidgets.QVBoxLayout()
        self.layoutDescription.setObjectName("layoutDescription")
        self.labelPublishedDescription = QtWidgets.QLabel(self.importText_page)
        self.labelPublishedDescription.setObjectName("labelPublishedDescription")
        self.layoutDescription.addWidget(self.labelPublishedDescription)
        
        #espace entre la zone de texte et les boutons
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutDescription.addItem(spacerItem1)
        
        self.textEditPublishedDescription = QtWidgets.QTextEdit(self.importText_page)
        self.textEditPublishedDescription.setObjectName("textEditPublishedDescription")
        self.layoutDescription.addWidget(self.textEditPublishedDescription)
        
        ##bouton next et import file:
        self.layoutImportFileAndnextButtons = QtWidgets.QHBoxLayout()
        self.layoutImportFileAndnextButtons.setObjectName("layoutImportFileAndnextButtons")
        
        #import file bouton
        self.pushButtonImportFile = QtWidgets.QPushButton(self.importText_page)
        self.pushButtonImportFile.setObjectName("pushButtonImportFile")
        self.pushButtonImportFile.clicked.connect(self.import_Fichier)        
        self.layoutImportFileAndnextButtons.addWidget(self.pushButtonImportFile)
        
        #Next button
        self.pushButtonNext = QtWidgets.QPushButton(self.importText_page)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.layoutImportFileAndnextButtons.addWidget(self.pushButtonNext)
        self.pushButtonNext.clicked.connect(self.boutonNext)
        
        #Message quand Published description est vide
        self.labelEmptyField = QtWidgets.QLabel(self.importText_page)
        self.labelEmptyField.setObjectName("labelEmptyField")
        self.layoutImportText2.setWidget(30, QtWidgets.QFormLayout.LabelRole, self.labelEmptyField)
        self.layoutDescription.addLayout(self.layoutImportFileAndnextButtons)
        self.layoutImportText2.setLayout(2, QtWidgets.QFormLayout.SpanningRole, self.layoutDescription)
        self.layoutImportText1.addLayout(self.layoutImportText2)
        self.verticalLayout_2.addLayout(self.layoutImportText1)
        self.tab.addTab(self.importText_page, "")
        
        
        #execute_page
        self.execute_page = QtWidgets.QWidget()
        self.execute_page.setObjectName("execute_page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.execute_page)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.layoutExecute1 = QtWidgets.QVBoxLayout()
        self.layoutExecute1.setObjectName("layoutExecute1")
        self.groupBoxExecute1 = QtWidgets.QGroupBox(self.execute_page)
        self.groupBoxExecute1.setObjectName("groupBoxExecute1")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBoxExecute1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.layoutExecute2 = QtWidgets.QVBoxLayout()
        self.layoutExecute2.setObjectName("layoutExecute2")
        
        
        #################
        self.textEditPublishedDescriptionExecutePage = QtWidgets.QTextEdit(self.groupBoxExecute1)
        self.textEditPublishedDescriptionExecutePage.setObjectName("textEditPublishedDescriptionExecutePage")
        self.layoutExecute2.addWidget(self.textEditPublishedDescriptionExecutePage)
        self.layoutExecute3 = QtWidgets.QHBoxLayout()
        self.textEditPublishedDescriptionExecutePage.setDisabled(True);
        ###################
        
        
        self.layoutExecute3.setObjectName("layoutExecute3")
        self.layoutExecute2.addLayout(self.layoutExecute3)
        self.verticalLayout_13.addLayout(self.layoutExecute2)
        self.groupBoxExecute2 = QtWidgets.QGroupBox(self.groupBoxExecute1)
        self.groupBoxExecute2.setObjectName("groupBoxExecute2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBoxExecute2)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.layoutExecute4 = QtWidgets.QVBoxLayout()
        self.layoutExecute4.setObjectName("layoutExecute4")
        
        
        
        ###########################
        # table of results
        self.tableViewResultExecute = Mytable(0,6)#QtWidgets.QTableView(self.groupBoxExecute2)
        colonne_header=["Selection","Organ","Property","Value","Modifyer","Validated"]#,"Validated:"
        self.tableViewResultExecute.setHorizontalHeaderLabels(colonne_header)
        header= self.tableViewResultExecute.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableViewResultExecute.setObjectName("tableViewResultExecute")
        self.layoutExecute4.addWidget(self.tableViewResultExecute)
        self.tableViewResultExecute.setFocusPolicy(QtCore.Qt.NoFocus)
        
        
        #############################
        self.layoutExecute5 = QtWidgets.QHBoxLayout()
        self.layoutExecute5.setObjectName("layoutExecute5")
        
        ################################
        # button delete
        ################################
        self.pushButtonDelete=QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonDelete.setText("Delete Triads")
        
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDelete.clicked.connect(self.deleteTriad)
        
        #        
        #############################
        
        ################################
        # button add
        ################################
        self.pushButtonAdd=QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonAdd.setText("Add Triad")
        
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.pushButtonAdd.clicked.connect(self.addTriad)
        self.layoutExecute5.addWidget(self.pushButtonAdd)
        self.layoutExecute5.addWidget(self.pushButtonDelete)        
        
        ## bouton save a job
        self.pushButtonSaveAJobExecute = QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonSaveAJobExecute.setObjectName("pushButtonSaveAJobExecute")
        self.layoutExecute5.addWidget(self.pushButtonSaveAJobExecute)
        
        #Previous button in Execute
        self.pushButtonPreviousExecute = QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonPreviousExecute.setObjectName("pushButtonPreviousExecute")
        self.layoutExecute5.addWidget(self.pushButtonPreviousExecute)
        self.layoutExecute4.addLayout(self.layoutExecute5)
        self.pushButtonPreviousExecute.setEnabled(False)
        self.pushButtonPreviousExecute.clicked.connect(self.buttonPreviousExecute)
        
        #Next button in Execute
        self.pushButtonNextExecute = QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonNextExecute.setObjectName("pushButtonNextExecute")
        self.layoutExecute5.addWidget(self.pushButtonNextExecute)
        self.layoutExecute4.addLayout(self.layoutExecute5)
        self.pushButtonPreviousExecute.setEnabled(True)
        self.pushButtonNextExecute.clicked.connect(self.buttonNextExecute)
        
        #button export
        self.pushButtonExportExecute = QtWidgets.QPushButton(self.groupBoxExecute2)
        self.pushButtonExportExecute.setObjectName("pushButtonExportExecute")
        self.layoutExecute5.addWidget(self.pushButtonExportExecute)
        self.pushButtonExportExecute.clicked.connect(self.exportExcel)
 

        #Label for error messages of the Execute page
        self.labelErrorExecute = QtWidgets.QLabel(self.groupBoxExecute2)
        self.labelErrorExecute.setObjectName("labelErrorExecute")
        self.layoutExecute4.addWidget(self.labelErrorExecute)
        
        
        self.horizontalLayout_14.addLayout(self.layoutExecute4)
        self.verticalLayout_13.addWidget(self.groupBoxExecute2)
        self.layoutExecute1.addWidget(self.groupBoxExecute1)
        self.verticalLayout_5.addLayout(self.layoutExecute1)
        self.tab.addTab(self.execute_page, "")
        
        ## page schema
        self.schema_page = QtWidgets.QWidget()
        self.schema_page.setObjectName("schema_page")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.schema_page)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.layoutSchema1 = QtWidgets.QVBoxLayout()
        self.layoutSchema1.setObjectName("layoutSchema1")
        self.groupBoxSchema1 = QtWidgets.QGroupBox(self.schema_page)
        self.groupBoxSchema1.setObjectName("groupBoxSchema1")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.groupBoxSchema1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.layoutSchema2 = QtWidgets.QVBoxLayout()
        self.layoutSchema2.setObjectName("layoutSchema2")
        self.tableViewSchema = QtWidgets.QTableView(self.groupBoxSchema1)
        self.tableViewSchema.setObjectName("tableViewSchema")
        self.layoutSchema2.addWidget(self.tableViewSchema)
        self.layoutSchema3 = QtWidgets.QHBoxLayout()
        self.layoutSchema3.setObjectName("layoutSchema3")
        
        ## bouton add schema
        self.pushButtonAddSchema = QtWidgets.QPushButton(self.groupBoxSchema1)
        self.pushButtonAddSchema.setObjectName("pushButtonAddSchema")
        self.layoutSchema3.addWidget(self.pushButtonAddSchema)
        self.pushButtonAddSchema.clicked.connect(self.add_Item)
        
        
        ##bouton modify schema
        self.pushButtoModifySchema = QtWidgets.QPushButton(self.groupBoxSchema1)
        self.pushButtoModifySchema.setObjectName("pushButtoModifySchema")
        self.layoutSchema3.addWidget(self.pushButtoModifySchema)
        
        ## bouton modifier un schema
        self.pushButtonDeleteSchema = QtWidgets.QPushButton(self.groupBoxSchema1)
        self.pushButtonDeleteSchema.setObjectName("pushButtonDeleteSchema")
        self.layoutSchema3.addWidget(self.pushButtonDeleteSchema)
        self.layoutSchema2.addLayout(self.layoutSchema3)
        self.horizontalLayout_16.addLayout(self.layoutSchema2)
        self.layoutSchema1.addWidget(self.groupBoxSchema1)
        self.verticalLayout_7.addLayout(self.layoutSchema1)
        self.tab.addTab(self.schema_page, "")
        self.verticalLayout_17.addWidget(self.tab)
        
        
        ## partie help
        self.help_page = QtWidgets.QWidget()
        self.help_page.setObjectName("help_page")
        self.verticalLayout_77 = QtWidgets.QVBoxLayout(self.help_page)
        self.verticalLayout_77.setObjectName("verticalLayout_77")
        #*
        self.labelHelp = QtWidgets.QLabel(self.help_page)
        self.labelHelp.setObjectName("labelHelp")
        #*
        self.verticalLayout_77.addWidget(self.labelHelp)        
        self.verticalLayout_77.addStretch()        
        self.tab.addTab(self.help_page, "")
        
        ## ?? 
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 975, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.quit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.labelHelp.setText(_translate("MainWindow", "To use this program:\n\n\n\n- Firstly, you must either enter a text or click on the button: \"Import File\" in order to import your text.\n\n- Then, after clicking on the button \"Next\", you will have the possibility to validate, add or even delete the Triads\nthat you found in this text using the buttons in the execute tab. The triads will be displayed sentence by sentence.\n\n- Finally, you could export your result in the same tab and show them in a file that will have \"FinalResults\" as a name."
        ""))
        #self.labelHelp.move(0, 0)        
        self.labelHome4.setPixmap(QtGui.QPixmap(_translate("MainWindow", 'nematode.png')))
        #self.labelHome4.move(50, 50)        
        MainWindow.setWindowTitle(_translate("MainWindow", "Terminator 2.0"))
        self.labelHome1.setText(_translate("MainWindow", "Terminator 2.0\n"
"Author: Name and email\n"
"Contributors: …\n"
""))
        self.labelHome2.setText(_translate("MainWindow", "Link of the previous versions of Terminator:\n"
"Le Terminator 1.0 = Diederich, J., Fortuner, R. & Milton, J. 1999a.\n"
"Computer-assisted data extraction from the taxonomical literature.\n"
"http://genisys.prd.fr/Diederich_etal_1999b.html>Vi\n"
"\n"
"Link which describes the terminator schema:\n"
"Diederich, J., Fortuner, R. & Milton, J. 1997. Construction and\n"
"integration of large character sets for nematode morpho-anatomical data\n"
"http://genisys.prd.fr/Diederich_etal_1997.html>. \n"
"Diederich, J., Fortuner, R. & Milton, J. 2000b. A uniform representation\n"
"for the plan of organization of nematodes of the order Tylenchida\n"
"http://genisys.prd.fr/Diederich_etal_2000b.html\n"
""))
        #page d'accueil
        self.tab.setTabText(self.tab.indexOf(self.home_page), _translate("MainWindow", "Home"))
        #table import text  partie description de lespèce
        self.labelRefNum.setText(_translate("MainWindow", "REF_N°"))
        self.labelSpeciesNum.setText(_translate("MainWindow", "SPECIES_N°"))
        self.labelRecNum.setText(_translate("MainWindow", "REC_N°"))
        self.labelGenus.setText(_translate("MainWindow", "Genus"))
        self.labelSpecies.setText(_translate("MainWindow", "Species"))
        self.labelPopulation.setText(_translate("MainWindow", "Population"))
        self.labelSex.setText(_translate("MainWindow", "Sex"))
        self.labelStage.setText(_translate("MainWindow", "Stage"))
        self.labelLocality.setText(_translate("MainWindow", "Locality"))
        self.labelHost.setText(_translate("MainWindow", "Host"))
        self.labelEmptyField.setText(_translate("MainWindow", ""))
        
        # import text 
        self.labelPublishedDescription.setText(_translate("MainWindow", "Published description"))
        self.pushButtonImportFile.setText(_translate("MainWindow", "Import file"))
        self.pushButtonNext.setText(_translate("MainWindow", "Next"))
        self.tab.setTabText(self.tab.indexOf(self.importText_page), _translate("MainWindow", "Import text"))
        #partie resultat
        self.groupBoxExecute1.setTitle(_translate("MainWindow", "Published description"))
        self.groupBoxExecute2.setTitle(_translate("MainWindow", "Result :"))
        self.pushButtonSaveAJobExecute.setText(_translate("MainWindow", "Save a job"))
        self.pushButtonPreviousExecute.setText(_translate("MainWindow", "Previous"))
        self.pushButtonNextExecute.setText(_translate("MainWindow", "Next"))
        self.pushButtonExportExecute.setText(_translate("MainWindow", "Export"))
        
        # partie schema 
        self.tab.setTabText(self.tab.indexOf(self.execute_page), _translate("MainWindow", "Execute"))
        self.groupBoxSchema1.setTitle(_translate("MainWindow", "Schema of the organs and their associated properties"))
        self.pushButtonAddSchema.setText(_translate("MainWindow", "Add"))
        self.pushButtoModifySchema.setText(_translate("MainWindow", "Modify"))
        self.pushButtonDeleteSchema.setText(_translate("MainWindow", "Delete"))
        self.tab.setTabText(self.tab.indexOf(self.schema_page), _translate("MainWindow", "Schema"))
        # partie help
        self.tab.setTabText(self.tab.indexOf(self.help_page), _translate("MainWindow", "Help"))

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #MainWindow.setGeometry(400,400,400,400)
    MainWindow.show()
    #MainWindow.destroy()
    sys.exit(app.exec_())
  #  os.close(Python 3.6)
    #sys.exit(0)
    

