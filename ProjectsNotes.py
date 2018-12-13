# -*- coding: utf-8 -*-
import os
import io
import datetime
import sys
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class ProjectsNotes(QWidget):

    version = '0.1'
    projects_folder_name = 'projects'


    def saveNote(self):

        return 0

    def __init__(self):
        super().__init__()
        self.initUI()


        #progName.setText(u'Установлено')

    def initUI(self):
        global progName
        global nameEdit
        global noteContent
        global selectBox
        global searchInput

        progName = QLabel(u'Projects Notes', self)

        copyright_string = QLabel(u'KLEEEEEER\'s Shitcode 2018', self)

        projectsLabel = QLabel(u'Проект:', self)
        projects = self.getProjects()

        selectBox = QComboBox()
        selectBox.addItems(projects)

        qbtn = QPushButton('Обновить проекты', self)
        qbtn.clicked.connect(self.updateProjects)
        qbtn.resize(qbtn.sizeHint())

        clearbtn = QPushButton('Очистить все поля', self)
        clearbtn.clicked.connect(self.clearInputs)
        clearbtn.resize(qbtn.sizeHint())

        nameChanged = ''
        rowsChanged = ''

        def ChangedName():
            global nameChanged
            global rowsChanged
            nameChanged = nameEdit.text()
            rowsChanged = noteContent.text()
            print('TextChanged and now its: ' + nameEdit.text())
            print('TextChanged and now its: ' + noteContent.toPlainText())

        dobtn = QPushButton('Создать заметку', self)
        dobtn.clicked.connect(self.saveProjectNote)
        dobtn.resize(dobtn.sizeHint())
        dobtn.move(0, 0)


        name = QLabel('Имя:')
        nameEdit = QLineEdit()

        rowsCount = QLabel('Текст:')
        noteContent = QTextEdit()

        searchButton = QPushButton('Найти', self)
        search = QLabel('Поиск')
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
        grid.addWidget(searchInput, 1, 4)
        grid.addWidget(searchContent, 2, 3, 5, 2)
        grid.addWidget(searchButton, 1, 5)

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
            progName.setText(u'Ошибка загрузки папок в ' + self.projects_folder_name)

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
            progName.setText(u'Не введено имя заметки')
            return

        if (str(noteContent.toPlainText()) == ''):
            progName.setText(u'Не введен текст заметки')
            return

        if ( str(selectBox.currentText()) == '' ):
            progName.setText(u'Не создано папок проектов, создайте её в папке ' + self.projects_folder_name + ' и нажмите Обновить проекты')
            return

        if not os.path.isdir(self.projects_folder_name + '/' + str(selectBox.currentText())):
            self.updateProjects()
            progName.setText(u'Проекта ' + str(selectBox.currentText()) + ' больше не существует. Список проектов обновлён.')
            return


        project_path = self.projects_folder_name + '/' + str(selectBox.currentText()) + '/'
        now = datetime.datetime.now()
        file_name = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + ' ' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + ' ' + str(nameEdit.text()) + '.txt'

        document = open(project_path + file_name, 'w')
        document.write(str(noteContent.toPlainText()))
        document.close()
        progName.setText(u'Сохранён файл ' + file_name)

    def searchStringButton(self):
        self.searchString(searchInput.text())

    def searchString(self, string):
        projects = self.getProjects()
        searchResult = []
        for project in projects:
            if os.path.isdir(self.projects_folder_name + '/' + project):
                for file in os.listdir(self.projects_folder_name + '/' + project):
                    if file.endswith('.txt'):
                        with io.open(self.projects_folder_name + '/' + project + '/' + file, encoding='utf-8') as file_txt:
                            for line in file_txt:
                                if string in line:
                                    searchResult.append(self.projects_folder_name + '/' + project + '/' + file)
        return searchResult

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectsNotes()
    sys.exit(app.exec_())
