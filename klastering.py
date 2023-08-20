from flask import Flask, jsonify, request
from flask_cors import CORS

import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize

from IPython.core.display import Math
import math
import re

import nltk
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def index():
    return jsonify(
        is_error=False,
        data='',
        msg="sukses."
    )


@app.route('/preprocessing', methods=['POST'])
def preprocessing():
  # 1
    q = request.form.getlist('q[]')
    qIndex = 0
    qKey = {}
    for kata in q:
        kata = kata.lower()
        kata = re.sub(r"\d+", "", kata)
        kata = kata.translate(str.maketrans("", "", string.punctuation))

        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()

        kata = stopword.remove(kata)

        factory = StemmerFactory()
        Stemmer = factory.create_stemmer()
        kata = Stemmer.stem(kata)
        kata = nltk.tokenize.word_tokenize(kata)

        qKey[f'q{qIndex}'] = kata
        qIndex += 1
    hasil = []
    kamus_kata = {}
    for key in qKey:
        kamus_kata_q = {}
        for kata in qKey[key]:
            kamus_kata_q[kata] = qKey[key].count(kata)
            kamus_kata[key] = kamus_kata_q
    hasil.append(kamus_kata)
    hasil_akhir = {
        'q': q,
        'hasil': hasil[0]
    }
    return jsonify(
        is_error=False,
        data=hasil_akhir,
        msg="sukses."
    )
@app.route('/tfidf', methods=['POST'])
def tfidf():
    # 1
    q = request.form.getlist('q[]')


    return jsonify(
        is_error=False,
        data=hasil,
        msg="sukses."
    )

@app.route('/tfidf-old', methods=['POST'])
def tfidf_old():

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
            kata = kata.lower()
            kata = re.sub(r"\d+", "", kata)
            kata = kata.translate(str.maketrans("", "", string.punctuation))

            factory = StopWordRemoverFactory()
            stopword = factory.create_stop_word_remover()

            kata = stopword.remove(kata)

            factory = StemmerFactory()
            Stemmer = factory.create_stemmer()
            kata = Stemmer.stem(kata)
            kata = nltk.tokenize.word_tokenize(kata)

            

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
    app.run(debug=True, host='0.0.0.0')
