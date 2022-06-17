import os
from datetime import date, datetime, timedelta
import sys

for root, dirs, files in os.walk('.'):
    if dir == "DESAPARECIDO" or "DESATIVADO" or "FORAGIDO" or "PROCURADO":
        for file in files:
            if ((file.endswith(('.png')) or (file.endswith('.jpg')) or (file.endswith('.jpeg')))):
                filepath = (os.path.join(root, file))
                print (filepath)
                print ('File' + filepath + ' deleted!')
                os.remove(filepath)
