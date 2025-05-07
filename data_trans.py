import pymysql
import sys
from tqdm import tqdm  # 进度条库

# 源数据库配置
source_config = {
    "host": "localhost",
    "user": "dream",
    "password": "dream",
    "database": "boss_job",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

# 目标数据库配置（不指定 database，先连接服务器）
dest_config = {
    "host": "gz-cdb-ax3kzpc9.sql.tencentcdb.com",
    "port": 26985,
    "user": "dream",
    "password": "Dream123.",  # 替换为实际密码
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def connect_db(config):
    """连接数据库并返回连接对象"""
    try:
        connection = pymysql.connect(**config)
        print(f"连接 {config['host']} 成功")
        return connection
    except pymysql.MySQLError as e:
        print(f"连接 {config['host']} 失败: {e}")
        sys.exit(1)


def create_database_and_table(dest_conn):
    """在目标数据库中创建 boss_job 数据库和 job_data 表"""
    try:
        cursor = dest_conn.cursor()
        # 创建数据库
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS boss_job CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print("数据库 boss_job 创建成功或已存在")

        # 切换到 boss_job 数据库
        cursor.execute("USE boss_job")

        # 创建 job_data 表
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS job_data (
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
        print("表 job_data 创建成功或已存在")

        dest_conn.commit()
    except pymysql.MySQLError as e:
        print(f"创建数据库或表失败: {e}")
        sys.exit(1)
    finally:
        cursor.close()


def migrate_data():
    # 连接源数据库
    source_conn = connect_db(source_config)

    # 连接目标数据库（不指定数据库）
    dest_conn = connect_db(dest_config)

    try:
        # 创建数据库和表
        create_database_and_table(dest_conn)

        # 重新连接到 boss_job 数据库
        dest_config_with_db = dest_config.copy()
        dest_config_with_db["database"] = "boss_job"
        dest_conn = connect_db(dest_config_with_db)

        # 创建游标
        source_cursor = source_conn.cursor()
        dest_cursor = dest_conn.cursor()

        # 获取源表数据
        source_cursor.execute(
            "SELECT Idx, title, salary, position, experience, degree, tags, `describe`, company_name, scale, industry FROM job_data_city"
        )
        rows = source_cursor.fetchall()
        total_rows = len(rows)
        print(f"源表 job_data_city 共 {total_rows} 条数据")

        if total_rows == 0:
            print("源表为空，无需迁移")
            return

        # 批量插入到目标表
        batch_size = 1000  # 每批插入 1000 条
        for i in tqdm(range(0, total_rows, batch_size), desc="迁移进度"):
            batch = rows[i : i + batch_size]
            # 插入所有字段，包括 Idx
            insert_sql = """
                INSERT IGNORE INTO job_data (Idx, title, salary, position, experience, degree, tags, `describe`, company_name, scale, industry)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # 提取字段值
            values = [
                (
                    row["Idx"],
                    row["title"],
                    row["salary"],
                    row["position"],
                    row["experience"],
                    row["degree"],
                    row["tags"],
                    row["describe"],
                    row["company_name"],
                    row["scale"],
                    row["industry"],
                )
                for row in batch
            ]
            try:
                dest_cursor.executemany(insert_sql, values)
                dest_conn.commit()
            except pymysql.MySQLError as e:
                print(f"插入批次 {i // batch_size + 1} 失败: {e}")
                dest_conn.rollback()

        print("数据迁移完成！")

    except pymysql.MySQLError as e:
        print(f"迁移错误: {e}")
        sys.exit(1)

    finally:
        # 关闭游标和连接
        if "source_cursor" in locals():
            source_cursor.close()
        if "dest_cursor" in locals():
            dest_cursor.close()
        source_conn.close()
        dest_conn.close()
        print("所有数据库连接已关闭")


if __name__ == "__main__":
    migrate_data()
