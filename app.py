from flask import Flask, request
import requests
import os
import gspread

app = Flask(__name__)

#Get environment variables

googleUser = os.environ['guser']
googlePass = os.environ['gpass']

gc = gspread.login(googleUser, googlePass)
wks = gc.add_worksheet(title="SendGrid Demo", rows="100", cols="20")

def getNextRow():
    values_list = wks.col_values(1) #gets all values in first column
    emptyrow = str(len(values_list)+1)
    return emptyrow


def addRow(email, subject, spam_score):
    row = getNextRow()
    emailCell = 'A'+row
    subjectCell = 'B'+row
    spamCell = 'C'+row
    wks.update_acell(emailCell, email)
    wks.update_acell(subjectCell, subject)
    wks.update_acell(spamCell, spam_score)

@app.route('/', methods = ['POST'])
def insertData():
    email = request.form['from']
    subject = request.form['subject']
    spamscore = request.form['spam_score']
    addRow(email, subject, spamscore)
    return "OK"

if __name__ == '__main__':
    app.debug = TRUE
    app.run()


