import pymysql


class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS business (
            News_Origin VARCHAR(255), 
            News_URL VARCHAR(255), 
            Active_Flag INT
        );
        """
        self.cursor.execute(create_table_query)

    def insert_data(self):
        insert_query = """
        INSERT INTO business (News_Origin, News_URL, Active_Flag)
        VALUES ('TOI', 'https://timesofindia.indiatimes.com/', 1);
        """
        self.cursor.execute(insert_query)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


config = {
    'host': 'database-1.cl2kmkc8ogep.ap-south-1.rds.amazonaws.com',
    'user': 'admin1',
    'password': 'akashatre',
    'database': 'mydb1'
}


def lambda_handler(event, context):
    db_handler = DatabaseHandler(**config)

    try:

        db_handler.create_table()
        db_handler.insert_data()
    finally:

        db_handler.close()
