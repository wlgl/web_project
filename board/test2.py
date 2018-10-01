from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/movie')
def movie():
    movie = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    soup = BeautifulSoup(movie.text,'html.parser')
    
    res = []
    abc = soup.find_all('td','title')

    for i in abc:
        res.append(i.text)
    return render_template('res.html', abc = res)


if __name__ == "__main__":
    app.run(debug=True, port=8181, host='0.0.0.0')
