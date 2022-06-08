# -- coding: utf-8 --
# 对于如何使用record.py的示例

# 建库建表语句
# CREATE DATABASE `wrapertest` CHARACTER SET 'utf8mb4';
# CREATE TABLE `wrapertest`.`tabletest`  (
#   `pkey1` int(10) NOT NULL,
#   `pkey2` int(10) NOT NULL,
#   `words` varchar(255) NULL,
#   PRIMARY KEY (`pkey1`, `pkey2`)
# );
from record import RecordBase
class Tabletest(RecordBase):
    def set_default_value(self):  # 设置默认值,如果有需要,选择性set
        """ 重写方法 """
        self.set_host("127.0.0.1")
        self.set_port(3306)
        self.set_dbname("wrapertest")
        self.set_table("tabletest")
        self.set_user("root")
        self.set_password("123456")
        self.set_primary_keys({"pkey1":0,"pkey2":0}) # 只需要给出主键以及默认值(默认值用来对应类型)
        self.set_record_data({"words":""}) # 给出非主键的定义


if __name__ == '__main__':
    oneT = Tabletest(dataMap={"pkey1":1,"pkey2":2,"words":"hello world"})
    oneT.insert(printsql=True) # 是否在控制台打印插入语句
