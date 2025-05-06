import pandas as pd
import pymysql
import os
from sqlalchemy import create_engine

class JobDataManager:
    def __init__(self, host='localhost', user='dream', password='dream', database='boss_job'):
        # MySQL 连接参数
        self.connection_params = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        # 创建 SQLAlchemy 引擎
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

        self.connection = pymysql.connect(**self.connection_params)
        
        # 表名
        # self.table_name = 'job_data' # md5没加city
        self.table_name = 'job_data_city' # md5加了city
        
        # 检查表是否存在，若不存在则创建
        self._create_table_if_not_exists()
        
        # 初始化缓存 DataFrame
        self.df = pd.DataFrame(
            columns=[
                "Idx",
                "title",
                "salary",
                "position",
                "experience",
                "degree",
                "tags",
                "describe",
                "company_name",
                "scale",
                "industry",
            ]
        )

    def _create_table_if_not_exists(self):
        # 使用 pymysql 连接以执行 DDL 语句
        connection = pymysql.connect(**self.connection_params)
        try:
            with connection.cursor() as cursor:
                # 创建表的 SQL 语句，index 为主键
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    `Idx` CHAR(32) PRIMARY KEY,
                    title VARCHAR(255),
                    salary VARCHAR(100),
                    position VARCHAR(255),
                    experience VARCHAR(100),
                    degree VARCHAR(100),
                    tags TEXT,
                    `describe` TEXT,
                    company_name VARCHAR(255),
                    scale VARCHAR(100),
                    industry VARCHAR(255)
                )
                """
                cursor.execute(create_table_sql)
            connection.commit()
        finally:
            connection.close()

    def add_job(self, job_dict):
        if job_dict:
            try:
                with self.connection.cursor() as cursor:
                    # 构建插入数据的 SQL 语句，使用 INSERT IGNORE 保证主键唯一
                    columns = ', '.join(f'`{col}`' for col in job_dict.keys())
                    values = ', '.join('%s' for _ in job_dict.values())
                    insert_sql = f"INSERT IGNORE INTO {self.table_name} ({columns}) VALUES ({values})"
                    cursor.execute(insert_sql, tuple(job_dict.values()))
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                print(f"Error inserting row with Idx {job_dict.get('Idx')}: {e}")
    
    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            try:
                self.connection.close()
            except Exception:
                print("Error closing connection")

    # def save(self):
    #     # 将 DataFrame 中的数据逐条插入到 MySQL 表
    #     if not self.df.empty:
    #         connection = self.engine.connect()
    #         try:
    #             for index, row in self.df.iterrows():
    #                 idx = row['Idx']
    #                 # 检查 Idx 是否已存在
    #                 check_sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE `Idx` = '{idx}'"
    #                 result = connection.execute(check_sql).scalar()
    #                 if result > 0:
    #                     print(f"Idx {idx} already exists, skipping.")
    #                     continue  # 如果 Idx 已存在，则跳过当前记录

    #                 # 构建插入数据的 SQL 语句
    #                 columns = ', '.join(f'`{col}`' for col in row.index)
    #                 values = ', '.join(f"'{str(value).replace('\'', '\'\'')}'" for value in row.values)  # Fix: Escape single quotes

    #                 insert_sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
    #                 try:
    #                     connection.execute(insert_sql)
    #                 except Exception as e:
    #                     print(f"Error inserting row with Idx {idx}: {e}")

    #             connection.commit()  # 提交事务
    #         except Exception as e:
    #             connection.rollback()  # 发生错误时回滚事务
    #             print(f"Transaction failed: {e}")
    #         finally:
    #             connection.close()  # 关闭连接

    #         # 清空缓存
    #         self.df = pd.DataFrame(
    #             columns=[
    #                 "Idx",
    #                 "title",
    #                 "salary",
    #                 "position",
    #                 "experience",
    #                 "degree",
    #                 "tags",
    #                 "describe",
    #                 "company_name",
    #                 "scale",
    #                 "industry",
    #             ]
    #         )

# 存入excel中
# class JobDataManager:
#     def __init__(self):
#         if os.path.exists("job_data.xlsx"):
#             self.df = pd.read_excel("job_data.xlsx")
#         else:
#             self.df = pd.DataFrame(
#                 columns=[
#                     "index",
#                     "title",
#                     "salary",
#                     "position",
#                     "experience",
#                     "degree",
#                     "tags",
#                     "describe",
#                     "company_name",
#                     "scale",
#                     "industry",
#                 ]
#             )

#     def add_job(self, job_dict):
#         if job_dict:
#             self.df = pd.concat([self.df, pd.DataFrame([job_dict])], ignore_index=True)

#     def save(self):
#         self.df.to_excel("job_data.xlsx", index=False)

