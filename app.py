from flask import Flask, request, jsonify
from crawling_utils import add_check
from crawling import main
from general_utils import dict_to_variables
from flask_mysqldb import MySQL
import json
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ.get('Capstone_host')
app.config['MYSQL_USER'] = os.environ.get('Capstone_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('Capstone_password')
app.config['MYSQL_DB'] = os.environ.get('Capstone_db')
mysql = MySQL(app)


@app.route('/test', methods=["POST"])
def test():
    print("TEST")

    return "TEST SUCCESSFUL" 


@app.route('/', methods=["POST"]) 
def process():
    param = request.get_json()
    studentNum = param['studentNum']
    password = param['password']

    possiblity = add_check(studentNum, password)
    if not possiblity:
        return "유효하지 않은 학번과 비밀번호"
    else: # 2. 메인 서버로 아이디, 패스워드 보내기
        cur = mysql.connection.cursor()
        
        dict_object = main(studentNum, password)

        name, major, minor, finished_semester, credit, cultures, scores, final_score, exam_papers, foreigns, major_required, minor_required = \
            dict_to_variables(dict_object)

        credit = json.dumps(credit, ensure_ascii=False, indent=4)
        cultures = json.dumps(cultures, ensure_ascii=False, indent=4)
        scores = json.dumps(scores, ensure_ascii=False, indent=4)
        exam_papers = json.dumps(exam_papers, ensure_ascii=False, indent=4)
        foreigns = json.dumps(foreigns, ensure_ascii=False, indent=4)
        major_required = json.dumps(major_required, ensure_ascii=False, indent=4)
        minor_required = json.dumps(minor_required, ensure_ascii=False, indent=4)

        cur.execute('INSERT INTO students (name, major, minor, finished_semester, credit, cultures, scores, final_score, exam_papers, foreigns, major_required, minor_required) VALUES ' + 
                    f"('{name}', '{major}', '{minor}', '{finished_semester}', '{credit}', '{cultures}', '{scores}', '{final_score}', '{exam_papers}', '{foreigns}', '{major_required}', '{minor_required}')")
        
        mysql.connection.commit()

        cur.close()

        return 'Data added successfully'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

