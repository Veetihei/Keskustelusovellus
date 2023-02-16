from flask import Flask #Jää tänne
from os import getenv #Jää tänne

app = Flask(__name__) #Jää tänne
app.secret_key = getenv("SECRET_KEY") #Jää tänne

import routes #jää tänne

