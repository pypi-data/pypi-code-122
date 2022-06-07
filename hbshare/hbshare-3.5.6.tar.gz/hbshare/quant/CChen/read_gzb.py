import numpy as np
import pdfplumber
import pandas as pd
import os
from datetime import datetime
from hbshare.quant.CChen.sql_cons import gtja_gzb_col_sql
from hbshare.quant.CChen.func import generate_table


# 用于读取国泰君安估值表（仅读取PDF格式）
def gtja_gzb(file_path):
    pdf = pdfplumber.open(file_path)

    df = pd.DataFrame()
    i_name = None
    i_date = None

    for i in pdf.pages:
        if i.page_number == 1:
            i_text = i.extract_text()
            i_date = datetime.strptime(i_text[i_text.index('估值日期'):][5:13], '%Y%m%d').date()
            i_name_index0 = i_text.index('国泰君安证券股份有限公司__')
            i_name_index1 = i_text.index('__专用表')
            i_name = i_text[
                     i_name_index0 + 14: i_name_index1
                     ].replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
        table_raw = i.extract_tables()
        table_df = pd.DataFrame(table_raw[0][1:], columns=table_raw[0][0])
        df = pd.concat([df, table_df])
    df.applymap(lambda x: x.replace('\n', ''))
    df['科目名称'] = df['科目名称'].apply(lambda x: x.replace('\n', ''))
    df['科目代码'] = df['科目代码'].apply(lambda x: x.replace('\n', ''))
    df['停牌信息'] = df['停牌信息'].apply(lambda x: x.replace('\n', ''))
    df = df.rename(
        columns={
            '成本占净值%': '成本占净值',
            '市值占净值%': '市值占净值'
        }
    )
    df_col = df.columns.tolist()
    df['基金名称'] = i_name
    df['日期'] = i_date
    df['数量'] = df['数量'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['单位成本'] = df['单位成本'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['市价'] = df['市价'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['估值增值'] = df['估值增值'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['成本'] = df['成本'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['市值'] = df['市值'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['成本占净值'] = df['成本占净值'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    df['市值占净值'] = df['市值占净值'].apply(lambda x: np.nan if x == '' else float(x.replace(',', '')))
    return df[['基金名称', '日期'] + df_col].reset_index(drop=True)


# 国泰君安估值表录入数据库
def gtja_gzb_to_db(table, ftype, fpath, db, db_path, sql_info):
    generate_table(
        database=db,
        table=table,
        generate_sql=gtja_gzb_col_sql,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass'],
        table_comment='基金估值表'
    )
    print(table + ' generated')

    data_exists = pd.read_sql_query('select `日期`, `基金名称` from ' + table, db_path)
    data_exists['label'] = data_exists['基金名称'] + data_exists['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    data_exists = data_exists['label'].tolist()

    file_list = os.listdir(fpath)
    for f in file_list:
        if f[-3:].lower() == ftype:
            file = fpath + '/' + f
            df = gtja_gzb(file_path=file)
            name = df['基金名称'][0]
            date = df['日期'][0]

            if name + date.strftime('%Y%m%d') not in data_exists:
                df.to_sql(table, db_path, index=False, if_exists='append')
                data_exists.append(name + date.strftime('%Y%m%d'))
                print(f)
            else:
                print(name + ' ' + date.strftime('%Y%m%d') + ' exists')



