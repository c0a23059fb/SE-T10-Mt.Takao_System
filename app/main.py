import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import mysql.connector
from pydantic import BaseModel


app = FastAPI()

# MySQL 接続設定
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "main_db"
}


class Item(BaseModel):
    name: str
    description: str


class Account(BaseModel):
    username: str
    email: str
    password: str


class QRCode(BaseModel):
    qr_code: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        # ファイルパスを取得(ファイルパス変わるので、今後変更が必要)
        file_path = os.path.join(os.path.dirname(__file__), "../app_html/test.html")
        with open(file_path, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"Error: {e}", status_code=500)


@app.post("/items/")
def create_item(item: Item):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (item.name, item.description))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Item created", "item": item}


#アカウントの作成
@app.post("/accounts/")
def create_account(account: Account):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)", (account.username, account.email, account.password))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Account created", "account": account}


#QRコードの検証
@app.post("/verify_qr/")
def verify_qr(qr_code: QRCode):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT route_name, is_peak FROM stamps WHERE qr_code = %s", (qr_code.qr_code,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        route_name, is_peak = result
        if is_peak:
            return {"message": "QRコードが正しいです", "route_name": route_name, "is_peak": True}
        else:
            return {"message": "QRコードが正しいです", "route_name": route_name, "is_peak": False}
    else:
        return {"message": "QRコードが無効です"}


# 特典の取得
@app.post("/get_gift/")
def get_gift(account: Account):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM stamps WHERE username = %s AND is_peak = True", (account.username,))
    peak_count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    print(peak_count)

    # if peak_count >= 10:
    #     return {"message": "特典を獲得しました", "gift": "Special Gift"}
    # else:
    #     return {"message": "特典を獲得するには、10個のピークスタンプが必要です", "current_peak_count": peak_count}


if __name__ == "__main__":
    user_init = Account(username="test", email="test@test.te", password="test")
    create_account(user_init)
    get_gift(user_init)