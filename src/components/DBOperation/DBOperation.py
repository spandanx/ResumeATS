from datetime import datetime

from config.database.MySQLDB import MysqlDB

mysqlDB = MysqlDB()

def update_stock_token_controller(token, username):
    print("Calling update_stock_token_controller()")
    print(token)
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    mysqlDB.update_stock_token(token, current_time, username)
    return {"message": "Successfully Updated the stock token"}

def get_stock_token_controller(username):
    return mysqlDB.get_basic_user_info(username)

if __name__ == "__main__":
    # end_date = datetime.today().strftime('%Y-%m-%d')
    # current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    # print(current_time)
    update_stock_token_controller("MNO", "adm_90")
