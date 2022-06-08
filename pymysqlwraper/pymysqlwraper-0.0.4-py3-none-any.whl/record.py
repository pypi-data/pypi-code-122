# -- coding: utf-8 --

# 可以从map初始化,必须要有id
# 可以从从数据库初始化; 从数据库查到map,然后用map初始化函数
# 是否在数据库存在函数
# 写库函数,查库函数
# 写csv函数

import warnings
import pymysql


class RecordBase():
    """一条记录基础类型"""
    __host = "127.0.0.1"
    __port = 3306
    __dbname = ""
    __table = ""
    __user = "root"
    __password = "123456"
    __primary_keys = {}  # 该表数据库中的主键以及对应值, 主键可能由多个组成, 用map区分
    __record_data = {}  # 该条数据库中的数据, 不包括主键
    m_KEY_EXCEPTION = False  # 无效key时是警告还是异常

    def set_host(self, host: 'str'):
        self.__host = host
    def get_host(self):
        return self.__host
        
    def set_port(self, port: 'int'):
        self.__port = port
    def get_port(self):
        return self.__port
        
    def set_dbname(self, dbname: 'str'):
        self.__dbname = dbname
    def set_dbname(self, dbname: 'str'):
        self.__dbname = dbname
        
    def set_table(self, table: 'str'):
        self.__table = table
    def get_table(self):
        return self.__table
        
    def set_user(self, user: 'str'):
        self.__user = user

    def set_password(self, password: 'str'):
        self.__password = password

    def set_value(self, key, value):
        """ 设置值, 由于分为普通数据以及主键,所以麻烦些
        进行了值的校验
        bug: 浮点可以转int,会认为是同一个类型吗"""
        # 设置值,对类型进行校验
        if key not in self.__record_data.keys() and key not in self.__primary_keys.keys():
            if self.m_KEY_EXCEPTION:
                raise KeyError(f"没有的键:{key}")
            else:
                # 发出警告
                warnings.warn(f"没有的键{key}, 不会进行写入", UserWarning)
        else:
            # 类型检查
            if key in self.__primary_keys.keys() and isinstance(value, type(self.__primary_keys[key])):
                self.__primary_keys[key] = value
            elif isinstance(value, type(self.__record_data[key])):
                self.__record_data[key] = value
            else:
                raise TypeError("数据类型不同!")

    def get_value(self, key):
        """ 设置值, 由于分为普通数据以及主键,所以麻烦些
        进行了值的校验
        bug: 浮点可以转int,会认为是同一个类型吗"""
        # 设置值,对类型进行校验
        if key  in self.__record_data.keys() :
            return self.__record_data[key]
        elif key in self.__primary_keys.keys():
            return self.__primary_keys[key]
        else:
            if self.m_KEY_EXCEPTION:
                raise KeyError(f"没有的键:{key}")
            else:
                # 发出警告
                warnings.warn(f"没有的键{key}, 返回None", UserWarning)
                return None

    def set_primary_keys(self,primary_keys:'dir'):
        self.__primary_keys = primary_keys
    
    def set_record_data(self,record_data:'dir'):
        self.__record_data = record_data    
    def set_default_value(self):  # 设置默认值
        """该类只作为基类进行继承, 子类需要实现该方法"""
        """调用 set_host set_port set_dbname set_table set_user set_password 等方法进行使用"""
        raise NotImplementedError('You need to define a set_default_value method!')

    # def check_state(self):
    #     """
    #     todo: 放到一个公用方法中? 独属于该类的, 如校验表是否存在, 表的字段等放到该方法中 
    #     校验信息,包括 网络状态, 库是否存在, 表是否存在,字段是否存在,返回的是一个map,其中, true肯定在前面连续, false肯定在后面连续 """
    #     pass
    
    # def create_table(self):
    #     """创建表,存在或者创建成功, 返回true"""
    #     pass
    
    # 检查是否存在该表
    # 是否存在所有列
    # 列数据类型是否无误
    # SELECT * from information_schema.columns where table_schema='wordpress-demo' AND table_name = 'wp_posts' and column_name="order_sn"
    # def check_table():
    #     pass

    def is_in_db(self, *, initFromDB: 'bool' = False):
        """ 根据关键字查库,并且决定是否从数据库中初始化"""
        """todo: 从调用select变为独立的函数, 节省流量"""
        if self.select() != None:
            return True
        else:
            return False

    def update_from_db(self):
        """从数据库获取数据进行初始化,如果数据库没有, 返回False"""
        dataMap = self.select()
        if None == dataMap:
            # self.set_default_value()
            return False
        else:
            # 既然是从数据库中查出来的, 必然已经存了主键
            for one_key in self.__primary_keys.keys():
                del dataMap[one_key]
            for one_key in dataMap.keys():
                self.set_value(one_key, dataMap[one_key])
            return True

    def insert(self, *, printsql: 'bool' = False):
        returnRes = True
        """插入数据库, 如果存在则更新"""
        tempDataMap = {**self.__primary_keys, **self.__record_data}
        keys = list(tempDataMap.keys())
        # 要在字符串中插入变量的值，可在前引号前加上字母f，再将要插入的变量放在花括号内
        insert_sql = f"INSERT INTO {self.__dbname}.{self.__table} ({', '.join(keys)}) VALUES "
        tempdatalist = []
        for onekey in keys:
            tempdata = "'%s'" % tempDataMap[onekey]
            tempdatalist.append(tempdata)
        insert_sql += "(" + ", ".join(tempdatalist)+")"
        if printsql:
            print(insert_sql)

        connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__dbname)  # 数据库选择
        cursor = connection.cursor()
        try:
            cursor.execute(insert_sql)
            connection.commit()
        except Exception as e:
            print("插入数据失败:%s"%e)
            connection.rollback()#发生错误时回滚
            # print("未成功")
            returnRes = False
        finally:
            cursor.close()
            connection.close()
        return returnRes

    def delete(self, *, printsql: 'bool' = False):
        """ 从数据库中删除, 数据库中不存在或者删除返回True """
        returnRes = True
        filter_conditions = []
        for one_primarykey in self.__primary_keys.keys():
            one_keyvalue = self.__primary_keys[one_primarykey]
            condition = f" {one_primarykey} = '{one_keyvalue}' "
            filter_conditions.append(condition)
        delete_sql = f"delete from {self.__dbname}.{self.__table} where " + " and ".join(filter_conditions)
        if printsql:
            print(delete_sql)
            #打开数据库链接
            
        connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__dbname)  
        # 使用cursor()方法获取操作游标
        cursor = connection.cursor()
        try:
            cursor.execute(delete_sql)# 执行SQL语句
            connection.commit()# 提交到数据库执行
        except Exception as e:
            print("删除数据失败:%s"%e)
            connection.rollback()#发生错误时回滚
            returnRes = False
        finally:
            cursor.close()# 关闭游标连接
            connection.close()# 关闭数据库连接
        return returnRes

    def update(self,*, printsql: 'bool' = False):
        """更新语句"""
        returnRes = True
        filter_conditions = []
        for one_primarykey in self.__primary_keys.keys():
            one_keyvalue = self.__primary_keys[one_primarykey]
            condition = f" {one_primarykey} = '{one_keyvalue}' "
            filter_conditions.append(condition)
        value_list = []
        for datakey in self.__record_data.keys():
            datavalue = self.__record_data[datakey]
            datastr = f" {datakey} = '{datavalue}' "
            value_list.append(datastr)
        update_sql = f"update {self.__dbname}.{self.__table} set {','.join(value_list)}   where " + " and ".join(filter_conditions)
        if printsql:
            print(update_sql)
        #打开数据库链接    
        connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__dbname)  
        cursor = connection.cursor()# 使用cursor()方法获取操作游标
        try:
            cursor.execute(update_sql)# 执行SQL语句
            connection.commit()# 提交到数据库执行
        except Exception as e:
            print("更新数据失败:%s"%e)
            connection.rollback()#发生错误时回滚
            returnRes = False
        finally:
            cursor.close()# 关闭游标连接
            connection.close()# 关闭数据库连接
        return returnRes

    def select(self,*, printsql: 'bool' = False):
        DbData = None
        filter_conditions = []
        for one_primarykey in self.__primary_keys.keys():
            one_keyvalue = self.__primary_keys[one_primarykey]
            condition = f" {one_primarykey} = '{one_keyvalue}' "
            filter_conditions.append(condition)
        select_sql = f"select * from {self.__dbname}.{self.__table} where " + " and ".join(filter_conditions)
        if printsql:
            print(select_sql)
        """从数据库中获取该数据"""
        connection = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__dbname,cursorclass=pymysql.cursors.DictCursor)  
        cursor = connection.cursor()# 使用cursor()方法获取操作游标
        try:
            cursor.execute(select_sql)# 执行SQL语句
            DbData = cursor.fetchone()
        except Exception as e:
            print("更新数据失败:%s"%e)
            connection.rollback()#发生错误时回滚
        finally:
            cursor.close()# 关闭游标连接
            connection.close()# 关闭数据库连接
        return DbData

    def __init__(self, *, dataMap: 'dir' = {} ):
        """如果要初始化一个只有id的,传入一个临时map即可"""
        self.set_default_value()
        primarykeyset = set(self.__primary_keys.keys())
        dataMapKetSet = set(dataMap.keys())
        if not primarykeyset.issubset(dataMapKetSet):
            if self.m_KEY_EXCEPTION:
                raise KeyError("传进来的数据中 主键 不完整!:%s" %
                               str(primarykeyset-dataMapKetSet))
            else:
                warnings.warn("传入数据中没有主键!写入默认值", UserWarning)
        for key in dataMap.keys():
            self.set_value(key, dataMap[key])

    def __str__(self):
        return str({"key":self.__primary_keys,"data":self.__record_data})
    

        