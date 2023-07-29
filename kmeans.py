from flask import Flask, jsonify, request
from flask_cors import CORS

from IPython.core.display import Math
import math
import re

import nltk
nltk.download('punkt')

app = Flask(__name__)
CORS(app)


@app.route('/preprocessing', methods=['POST'])
def preprocessing():
  # 1
    q = request.form.getlist('q[]')

    d_string = (' ').join(q).lower()

  # 2
    d_string = re.sub(r"\d+", "", d_string)


@app.route('/tfidf', methods=['POST'])
def index():

    # 1
    q = request.form.getlist('q[]')

    d_string = (' ').join(q).lower()
    # 2
    string_splited = d_string.split()

    # 3
    kamus_kata = {}
    for string in string_splited:
        kamus_kata[string] = d_string.count(string)

    # 4
    data_dict = {}
    data_list = []
    for kalimat in q:
        for kata in string_splited:
            data_dict[kata] = kalimat.count(kata)
            data_list.append(data_dict)
            data_dict = {}

    # 5
    term_frequencies = []
    for i in range(len(data_list)):
        term_frequencies.append(f"Data {i+1} : {data_list[i]}")

    # 6
    data_idf = {}
    for kata in kamus_kata:
        hitung = math.log(len(q)/kamus_kata[kata], 10)
        data_idf[kata] = hitung
    # 7
    hasil = []
    data_sementara = {}
    for index in range(len(data_list)):
        for i in data_list[index]:
            hitung = data_list[index][i]*data_idf[i]
            data_sementara[i] = round(hitung, 3)
            hasil.append(data_sementara)

    return jsonify(
        is_error=False,
        data=hasil,
        msg="sukses."
    )


if __name__ == '__main__':
    app.run(debug=True)
