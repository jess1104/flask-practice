# app.py
from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 添加CORS支持

# MySQL配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1qazxsw2'
app.config['MYSQL_DB'] = 'notes_db'

# 创建PyMySQL连接对象
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor  # 使用字典游标，返回字典形式的结果
)


@app.route('/notes', methods=['GET'])
def get_notes():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    cursor.close()
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def add_note():
    note_data = request.json
    cursor = mysql.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (note_data['title'], note_data['content']))
    mysql.commit()
    cursor.close()
    return jsonify({"message": "Note added!"}), 201

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note_data = request.json
    print(note_data)
    cursor = mysql.cursor()
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (note_data['title'], note_data['content'], id))
    mysql.commit()
    cursor.close()
    return jsonify({"message": "Note updated!"})


@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    cursor = mysql.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s", (id,))
    mysql.commit()
    cursor.close()
    return jsonify({"message": "Note deleted!"})

# 在应用上下文销毁时关闭数据库连接
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(mysql, 'close'):
#         mysql.close()

if __name__ == '__main__':
    app.run(debug=True)
