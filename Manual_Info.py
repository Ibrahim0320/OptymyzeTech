import sqlite3
import pandas as pd

'''
# Establish connection
conn = sqlite3.connect('cv_database.db')
# Cursor object to start implementing SQL commands
cursor = conn.cursor()
'''

data= pd.read_csv('CV_database.csv')


pd.options.display.max_columns= None
pd.options.display.max_rows= None



