from pyvi import ViTokenizer
import re
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from flask import Flask, render_template, request

#giai nen cac doi tuong
clf = pickle.load(open('C:\\Users\\CAO DUC\\Desktop\\HealthCare_Chatbot\\colab\\NB_ChatBot_model.pkl', 'rb'))
vocabulary_to_load = pickle.load(open('C:\\Users\\CAO DUC\\Desktop\\HealthCare_Chatbot\\colab\\vocab.pkl', 'rb'))
le = pickle.load(open('C:\\Users\\CAO DUC\\Desktop\\HealthCare_Chatbot\\colab\\decode_label.pkl', 'rb'))

app = Flask(__name__) #khoi tao flask



@app.route("/",methods =["GET", "POST"])
def home():
    return render_template('index.html')

@app.route("/get", methods=["POST"])
def chatbot_response():
    if request.method == "POST":
        message = request.form.get("msg")
        ok = prediction(message)
    return ok


def tienxuly(document):
    document = ViTokenizer.tokenize(document)
    # đưa về lower
    document = document.lower()
    # xóa các ký tự không cần thiết 
    document = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    return document


stopword = ["bot","ra"]


def remove_stopwords(line):
    words = []
    for word in line.strip().split():
        if word not in stopword:
            words.append(word)
    return ' '.join(words)


def prediction(input):
    ngram_size = 1
    loaded_vectorizer = CountVectorizer(ngram_range=(ngram_size, ngram_size), min_df=1,
                                        vocabulary=vocabulary_to_load)
    loaded_vectorizer._validate_vocabulary()
    a = tienxuly(input)

    input1 = remove_stopwords(a)
    vect = loaded_vectorizer.transform([input1]).toarray()
    predict = clf.predict(vect)
    predict = le.inverse_transform(predict)[0]
    
    if predict=="noanswer":
        predict= 'Xin lỗi bạn, câu này mình không biết trả lời như thế nào. Bạn vui lòng liện hệ theo số điện thoại 123456 để được tư vấn trực tiếp hoặc nhấn vào nút "Trợ giúp?" ở góc trái trên cùng màn hình để được giúp đỡ.'
    
    return predict


if __name__ == "__main__":
    app.run(debug=True)