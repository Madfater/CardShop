import pymysql
from datetime import datetime

# 資料輸入順序
User_order = ["Email","User_Name","Password"]

# 資料庫參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "1236987450", # 記得更改密碼
    "db": "mydb",
    "charset": "utf8"
}
# insert dst:table名稱 
def insert(dst:str, args:list):
    return f"INSERT INTO {dst} VALUES{tuple(args)}"

# 取得table內資料數
def countTable(table:str):
    return command(f"Select Count(*) From {table}")[0][0]

# 檢查user有無註冊過 用email檢查
def checkRegistered(email:str):
    return command(f"Select Count(*) From user where email = '{email}'")[0][0] != 0

# 註冊user
def registerUser(data:dict):
    if checkRegistered(data['email']):
        return "User already exist"
    id = countTable("user")
    user_arg = [id]+[data[k] for k in User_order]+[0]+[id]*3
    store_arg = [id,"empty",str(datetime.today().date())]
    order_arg = [id,"empty",0]
    shopping_cart_arg = [id,0]
    command(insert("store",store_arg))
    command(insert("Order_list",order_arg))
    command(insert("shopping_cart",shopping_cart_arg))
    command(insert("user",user_arg))
    return "register success"

# 登陸user
def loginUser(data):
    if not checkRegistered(data['email']):
        return "this email isn\'t register yet"
    cmd = "Select password from user where email = "+ f"'{data['email']}'"
    acuratePassword = command(cmd)[0][0]
    return "login success" if data['password'] == acuratePassword else "login failed"

# 查購物車
def checkCart(data:dict):
    cmd = f"Select * from Shopping_Cart where Cart_ID = {data['User_ID']}"
    result = list(command(cmd)[0])
    return {"Total_Price" : result[1]}

# 查商店
def checkStore(data:dict):
    cmd = f"Select * from Store where Store_ID = {data['User_ID']}"
    result = list(command(cmd)[0])
    return {"Description" : result[1],"ModiefiedDate" : result[2]}

# 處理傳入的json 跟據 json['type']來判斷操作
def manageCommand(data:dict):
    if data['type'] == "register":
        return registerUser(data)
    if data['type'] == "login":
        return loginUser(data)
    if data['type'] == "checkCart":
        return checkCart(data)
    if data['type'] == "checkStore":
        return checkStore(data)
    
# 執行操作
def command(waitting_command:str):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            cursor.execute(waitting_command) # 執行SQL程式碼
            result = cursor.fetchall()
            conn.commit()
            return result # 輸出
    except Exception as ex:
        print('execute:',ex) 
    return None