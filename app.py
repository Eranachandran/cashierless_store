import face_recognition
from PIL import Image
import pytesseract, re
from datetime import date
from flask import Flask, render_template, request
import os.path

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def show_index_html():
    return render_template('index.html')

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        Photo = request.form['Photo']
        ID = request.form['ID']
        Photo_available = (os.path.isfile(Photo))
        ID_available = (os.path.isfile(ID))
        if Photo_available == True and ID_available == True:
           # file exists
           known_image = face_recognition.load_image_file(Photo)
           unknown_image = face_recognition.load_image_file(ID)

           biden_encoding = face_recognition.face_encodings(known_image)[0]
           unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

           results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

           if results == [True]:

               # creating the date object of today's date
               todays_date = date.today()

               f = request.form['ID']
               t = pytesseract.image_to_string(Image.open(f))
               parse_dob = re.findall(r"D.O.B.  : [\db/]+", t)
               dob = parse_dob[0].split(":")

               dob_year = dob[1].split("/")

               # creating the date object of today's date
               todays_date = date.today()

               # Finding age
               age = int(todays_date.year) - int(dob_year[2])

               if age >= 18:
                   return render_template('purchase.html')
               else:
                   return render_template('age.html')
           else:
               return render_template('age.html')
        else:
            return render_template('not_scanned.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
