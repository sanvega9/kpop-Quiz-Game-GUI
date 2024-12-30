import sys 
import random
import json
from PyQt5.QtWidgets import(QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QButtonGroup, QInputDialog, QPushButton) # type: ignore
from PyQt5.QtCore import QTimer, Qt # type: ignore
from PyQt5.QtGui import QMovie
import os
class Kpopapp(QWidget):
    def __init__(self):
        super().__init__()
    # setting the game 
        self.score = 0
        self.kpop_question = 0
        self.hint_skip_used = {'50-50':False, 'skip': False}
        self.level = 'easy'
        self.time_left = 30
        self.username = None
        self.high_scores = []
        self.question = [
            {'question': 'What is the name of BTS\'s fandom?',
            'options': ['ARMY', 'BLINK','EXO-L', 'ONCE'],
            'answer':'ARMY'             
            }, 
            {'question': 'What is Stray Kids debut song?',
            'options': {'God\'s Menu','Hellevator','Back Door','Thunderous'},
            'answer':'Hellevator'
            },
            {'question': 'What is Blackpink’s debut song?',
            'options': { 'Boombayah', 'Kill This Love','How You Like That','DDU-DU DDU-DU'},
            'answer':'Boombayah'
            },
            {'question': 'Who is the leader of Ateez?',
            'options': { 'San', 'Hongjoong','Mingi','Yeosang'},
            'answer':'Hongjoong'
            }
        ]
        self.loading()

        self.setWindowTitle("Kpop trivia Quiz")
        self.setGeometry(100,100,800,600)
        #username input 
        self.username, x = QInputDialog.getText(self,'UserName', 'Enter your Username:')

        if not x or not self.username:
            self.username = "Player"
        self.init_kpop()
    def init_kpop(self):
        self.gif_image = QLabel(self)
        self.gif_image.setGeometry(0,0,self.width(),self.height())
        self.gif = QMovie("kpop.gif")
        self.gif.setScaledSize(self.size())
        self.gif_image.setMovie(self.gif)
        self.gif.start()
        
        self.layout_kpop =QVBoxLayout(self)
        #User welcome 
        self.user_welcome = QLabel(f"Welcome {self.username} to Kpop trivia Quiz")
        self.user_welcome.setStyleSheet("color:white;font-size: 30px;font-weight: bold;")
        self.user_welcome.setAlignment(Qt.AlignCenter)
        self.layout_kpop.addWidget(self.user_welcome)

        self.questions = QLabel(self.question[self.kpop_question]['question'])
        self.questions.setStyleSheet("color:white;font-size: 20px;font-weight: bold;")
        self.user_welcome.setAlignment(Qt.AlignCenter)
        self.layout_kpop.addWidget(self.questions)

        # Answer button
        self.buttons = QButtonGroup(self)
        self.layout_buttons = QHBoxLayout()
        for i, option in enumerate(self.question[self.kpop_question]['options']):
            btn = QPushButton(option)
            btn.clicked.connect(self.answer_correct)
            self.buttons.addButton(btn, i)
            self.layout_buttons.addWidget(btn)
        self.layout_kpop.addLayout(self.layout_buttons)
        #Timer UI
        self.timer_label = QLabel(f"Time Left:{self.time_left} seconds")
        self.timer_label.setStyleSheet('color: pink;font-size:24px;font-weight:bold')
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout_kpop.addWidget(self.timer_label)

        self.timer_game = QTimer(self)
        self.timer_game.timeout.connect(self.timer_update)
        self.timer_game.start(1000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gif_image.setGeometry(0,0,self.width(),self.height())
        self.gif.setScaledSize(self.size())
        
    def answer_correct(self):
        button_answer = self.sender()
        selected = button_answer.text()
        correct = self.question[self.kpop_question]['answer']
        if selected == correct:
             self.score += 10
             QMessageBox.information(self,"Correct!", "That's the correct answer!")
        else:
            QMessageBox.warning(self,"INCORRECT","Sorry that's not correct.")
        self.kpop_question += 1
        if self.kpop_question < len(self.question):
            self.new_question()
        else:
            self.end_game()            

    def new_question(self):
        self.questions.setText(self.question[self.kpop_question]['question'])
        for i, option in enumerate(self.question[self.kpop_question]['options']):
            self.buttons.button(i).setText(option)
    
    def timer_update(self):
        self.time_left -=1
        self.timer_label.setText(f"Time Left: {self.time_left} seconds")
        if self.time_left<=0:
            self.end_game()

    def end_game(self):
        self.timer_game.stop()
        QMessageBox.information(self,"Game Over",f"Your final score is {self.score} points!")
        self.save_score()
        self.close()
    #Loading high scores into JSON File
    # These will create a json file and allow to open the file to view high scores 
    # when the user finish 
    def loading(self):
        """Load High Scores from a file."""
        if os.path.exists('high_scores.json'):
            with open('high_scores.json', 'r') as file:
                self.high_scores = json.load(file)
        else:
            self.high_scores=[]

    def save_score(self):
        self.high_scores.append({'username':self.username, 'score':self.score})
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        with open('high_scores.json','w') as file:
            json.dump(self.high_scores,file)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    KPOPQuiz = Kpopapp()
    KPOPQuiz.show()
    sys.exit(app.exec_())