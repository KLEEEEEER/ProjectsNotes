# -*- coding: utf-8 -*-
import os
import io
import datetime
import sys
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class ProjectsNotes(QWidget):

    version = '0.3'
    projects_folder_name = 'projects'

    def saveNote(self):

        return 0

    def __init__(self):
        super().__init__()
        self.init_ui()


        #progName.setText(u'Установлено')

    def init_ui(self):
        global progName
        global nameEdit
        global noteContent
        global selectBox
        global searchInput
        global searchContent

        progName = QLabel(u'ProjectsNotes', self)

        copyright_string = QLabel(u'<a href="https://github.com/KLEEEEEER">https://github.com/KLEEEEEER</a>', self)
        copyright_string.setOpenExternalLinks(True)

        projectsLabel = QLabel(u'Project:', self)
        projects = self.getProjects()

        selectBox = QComboBox()
        selectBox.addItems(projects)

        qbtn = QPushButton('Update projects', self)
        qbtn.clicked.connect(self.updateProjects)
        qbtn.resize(qbtn.sizeHint())

        clearbtn = QPushButton('Clear all fields', self)
        clearbtn.clicked.connect(self.clearInputs)
        clearbtn.resize(qbtn.sizeHint())

        nameChanged = ''
        rowsChanged = ''

        def ChangedName():
            global nameChanged
            global rowsChanged
            nameChanged = nameEdit.text()
            rowsChanged = noteContent.text()
            #print('TextChanged and now its: ' + nameEdit.text())
            #print('TextChanged and now its: ' + noteContent.toPlainText())

        dobtn = QPushButton('Create note', self)
        dobtn.clicked.connect(self.saveProjectNote)
        dobtn.resize(dobtn.sizeHint())
        dobtn.move(0, 0)


        name = QLabel('Name:')
        nameEdit = QLineEdit()

        rowsCount = QLabel('Text:')
        noteContent = QTextEdit()

        searchButton = QPushButton('Search', self)
        search = QLabel('Search:')
        searchInput = QLineEdit()
        searchContent = QTextEdit()
        searchButton.clicked.connect(self.searchStringButton)

       # nameEdit.textChanged[str].connect(ChangedName)
        #noteContent.textChanged[str].connect(ChangedName)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(name, 1, 0)
        grid.addWidget(clearbtn, 1, 2)
        grid.addWidget(nameEdit, 1, 1)
        grid.addWidget(rowsCount, 2, 0)
        grid.addWidget(noteContent, 2, 1)
        grid.addWidget(projectsLabel, 3, 0)
        grid.addWidget(selectBox, 3, 1)
        grid.addWidget(progName, 4, 1)
        grid.addWidget(dobtn, 5, 1)
        grid.addWidget(search, 1, 3)
        grid.addWidget(searchInput, 1, 4, 1, 2)
        grid.addWidget(searchContent, 2, 3, 5, 3)
        grid.addWidget(searchButton, 7, 5)

        grid.addWidget(qbtn, 3, 2)
        grid.addWidget(copyright_string, 8, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Projects Notes v' + self.version)
        self.setWindowIcon(QIcon('icon.png'))
        self.show()


    def getProjects(self):
        try:
            os.makedirs(self.projects_folder_name)
        except OSError:
            progName.setText(u'Files loaded from ./' + self.projects_folder_name)

        projects = []
        projects_array = os.listdir(self.projects_folder_name)
        for project in projects_array:
            if os.path.isdir(self.projects_folder_name + '/' + project):
                projects.append(project)
        return projects

    def updateProjects(self):
        projects = self.getProjects()
        selectBox.clear()
        selectBox.addItems(projects)

    def clearInputs(self):
        nameEdit.setText('')
        noteContent.setText('')
        return


    def saveProjectNote(self):

        if (str(nameEdit.text()) == ''):
            progName.setText(u'Name is empty')
            return

        if (str(noteContent.toPlainText()) == ''):
            progName.setText(u'Text is empty')
            return

        if ( str(selectBox.currentText()) == '' ):
            progName.setText(u'You have no projects, add them in folder ' + self.projects_folder_name + ' and press "Update projects"')
            return

        if not os.path.isdir(self.projects_folder_name + '/' + str(selectBox.currentText())):
            self.updateProjects()
            progName.setText(u'Project ' + str(selectBox.currentText()) + ' is no longer exists. Projects list updated.')
            return


        project_path = self.projects_folder_name + '/' + str(selectBox.currentText()) + '/'
        now = datetime.datetime.now()
        file_name = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + ' ' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + ' ' + str(nameEdit.text()) + '.txt'

        document = open(project_path + file_name, 'w')
        document.write(str(noteContent.toPlainText()))
        document.close()
        progName.setText(u'Saved file ' + file_name)

    def searchStringButton(self):
        print('start')
        searchResult = self.searchString(searchInput.text())
        print('start2')
        self.fillSearchResult(searchResult)

    def searchString(self, string):
        searchContent.setText('')
        searchResult = []

        if (string == ''):
            searchResult.append('Search input is empty')
            return searchResult

        projects = self.getProjects()
        for project in projects:
            if os.path.isdir(self.projects_folder_name + '/' + project):
                for file in os.listdir(self.projects_folder_name + '/' + project):
                    if file.endswith('.txt'):
                        line_number = 1
                        with io.open(self.projects_folder_name + '/' + project + '/' + file) as file_txt: # , encoding='utf-8'
                            if (file_txt):
                                for line in file_txt:
                                    if line.find(string) != -1:
                                        print('found ' + string)
                                        searchResult.append('- '+self.projects_folder_name + '/' + project + '/' + file + ' : line ' + str(line_number))
                                        searchResult.append('\n')
                                    line_number += 1
        return searchResult

    def fillSearchResult(self, searchResult):
        for result in searchResult:
            searchContent.setText(searchContent.toPlainText() + result + '\n')
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectsNotes()
    sys.exit(app.exec_())
