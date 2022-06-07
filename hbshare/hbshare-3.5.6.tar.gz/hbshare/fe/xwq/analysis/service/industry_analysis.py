# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.fedb import FEDB
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
import pymysql
import sqlalchemy
import sys
import time
import traceback
import warnings
warnings.filterwarnings('ignore', category=pymysql.Warning)

class InsertTable:
    def __init__(self):
        self.engine = None
        self.connection = None
        self.create_connection()

    def create_connection(self):
        vaild = False
        while not vaild:
            try:
                self.engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
                                            'admin', 'mysql', '192.168.223.152', '3306', 'fe_temp_data'),
                                   connect_args={'charset': 'utf8'}, pool_recycle=360,
                                   pool_size=2, max_overflow=10, pool_timeout=360)
                self.connection = self.engine.connect()
                vaild = True
            except Exception as e:
                self.close_connection()
                print('[InsertTable] mysql connect error')
                time.sleep(5)
        return

    def close_connection(self):
        # 1) close connection
        try:
            if self.connection is not None:
                self.connection.close()
        except Exception as e:
            print('[InsertTable] close connect error')
        # 2) dispose engine
        try:
            if self.engine is not None:
                self.engine.dispose()
        except Exception as e:
            print('[InsertTable] dispose engine error')
        return

    def create_metadata(self, metadata):
        valid = False
        while not valid:
            try:
                metadata.create_all(self.engine)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] create metadata error')
            return metadata

    def insert_data(self, table, params):
        try:
            self.connection.execute(table.insert(), params)
        except Exception as e:
            conn = self.engine.connect()
            conn.execute(table.insert(), params)
            self.connection = conn
            exc_type, exc_value, exc_trackback = sys.exc_info()
            print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
            print('[InsertTable] insert data error')
        return

    def replace_data(self, table, params):
        # @compiles(Insert)
        def replace_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            s = s.replace("INSERT INTO", "REPLACE INTO")
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.connection.execute(table.insert(replace_string=""), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] replace data error')
            return

    def update_data(self, table, params):
        # @compiles(Insert)
        def append_string(insert, compiler, **kw):
            s = compiler.visit_insert(insert, **kw)
            if insert.kwards.get('on_duplicates_key_update'):
                fields = s[s.find("(") + 1:s.find(")")].replace(" ", "").split(",")
                generated_directive = ["{0}=VALUES({0})".format(field) for field in fields]
                return s + " ON DUPLICATES KEY UPDATE " + ",".join(generated_directive)
            return s

        valid = False
        times = 0
        while not valid and times < 5:
            try:
                times += 1
                self.connection.execute(table.insert(on_duplicates_key_update=True), params)
                valid = True
            except Exception as e:
                self.close_connection()
                self.create_connection()
                time.sleep(2)
                exc_type, exc_value, exc_trackback = sys.exc_info()
                print(repr(traceback.format_exception(exc_type, exc_value, exc_trackback)))
                print('[InsertTable] update data error')
            return

    def insert_industry_technology_df(self, factor_df, cols):
        table_name = 'industry_technology'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('RET'),
            sqlalchemy.Column('VOL'),
            sqlalchemy.Column('BETA'),
            sqlalchemy.Column('MARKET_VALUE')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_valuation_df(self, factor_df, cols):
        table_name = 'industry_valuation'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('PE_TTM'),
            sqlalchemy.Column('PB_LF'),
            sqlalchemy.Column('PEG'),
            sqlalchemy.Column('DIVIDEND_RATIO_TTM')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_fundamental_df(self, factor_df, cols):
        table_name = 'industry_fundamental'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('NET_PROFIT'),
            sqlalchemy.Column('NET_PROFIT_TTM'),
            sqlalchemy.Column('MAIN_INCOME'),
            sqlalchemy.Column('MAIN_INCOME_TTM'),
            sqlalchemy.Column('ROE_TTM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM'),
            sqlalchemy.Column('EPS_TTM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM'),
            sqlalchemy.Column('NET_ASSET_PS')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

    def insert_industry_fundamental_derive_df(self, factor_df, cols):
        table_name = 'industry_fundamental_derive'
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            table_name, metadata,
            sqlalchemy.Column('REPORT_DATE'),
            sqlalchemy.Column('INDUSTRY_ID'),
            sqlalchemy.Column('INDUSTRY_NAME'),
            sqlalchemy.Column('INDUSTRY_TYPE'),
            sqlalchemy.Column('NET_PROFIT_YOY'),
            sqlalchemy.Column('NET_PROFIT_TTM_YOY'),
            sqlalchemy.Column('MAIN_INCOME_YOY'),
            sqlalchemy.Column('MAIN_INCOME_TTM_YOY'),
            sqlalchemy.Column('ROE_TTM_YOY'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY'),
            sqlalchemy.Column('EPS_TTM_YOY'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY'),
            sqlalchemy.Column('NET_ASSET_PS_YOY'),
            sqlalchemy.Column('NET_PROFIT_MOM'),
            sqlalchemy.Column('NET_PROFIT_TTM_MOM'),
            sqlalchemy.Column('MAIN_INCOME_MOM'),
            sqlalchemy.Column('MAIN_INCOME_TTM_MOM'),
            sqlalchemy.Column('ROE_TTM_MOM'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM'),
            sqlalchemy.Column('EPS_TTM_MOM'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM'),
            sqlalchemy.Column('NET_ASSET_PS_MOM'),
            sqlalchemy.Column('ROE_TTM_YOY_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_YOY_ABS'),
            sqlalchemy.Column('EPS_TTM_YOY_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_YOY_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_YOY_ABS'),
            sqlalchemy.Column('ROE_TTM_MOM_ABS'),
            sqlalchemy.Column('GROSS_INCOME_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_PROFIT_RATIO_TTM_MOM_ABS'),
            sqlalchemy.Column('EPS_TTM_MOM_ABS'),
            sqlalchemy.Column('OPER_CASH_FLOW_PS_TTM_MOM_ABS'),
            sqlalchemy.Column('NET_ASSET_PS_MOM_ABS')
        )
        metadata = self.create_metadata(metadata)
        params = []
        for idx in range(len(factor_df)):
            rows = factor_df.iloc[idx]
            param = dict()
            for col in cols:
                param[col] = rows[col]
            params.append(param)
            if len(params) > 1000:
                self.update_data(table, params)
                del params
                params = []
        if len(params) > 0:
            self.update_data(table, params)
        self.close_connection()
        return

def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df

def get_stock_industry():
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna('20990101')
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].str.len() == 6]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    return stock_industry

def get_industry_info():
    industry_info = HBDB().read_industry_info()
    industry_info = industry_info.rename(columns={'flmc': 'INDUSTRY_NAME', 'zsdm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    industry_info = industry_info.dropna(subset=['BEGIN_DATE'])
    industry_info['END_DATE'] = industry_info['END_DATE'].replace('', np.nan).fillna('20990101')
    industry_info['BEGIN_DATE'] = industry_info['BEGIN_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
    industry_info['END_DATE'] = industry_info['END_DATE'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d').strftime('%Y%m%d') if '/' in x else x)
    industry_info['BEGIN_DATE'] = industry_info['BEGIN_DATE'].astype(int).astype(str)
    industry_info['END_DATE'] = industry_info['END_DATE'].astype(int).astype(str)
    industry_info['INDUSTRY_VERSION'] = industry_info['INDUSTRY_VERSION'].astype(int)
    industry_info['INDUSTRY_TYPE'] = industry_info['INDUSTRY_TYPE'].astype(int)
    industry_info['IS_NEW'] = industry_info['IS_NEW'].astype(int)
    industry_info = industry_info[industry_info['INDUSTRY_VERSION'] == 3]
    return industry_info

def get_stock_info():
    stock_info = HBDB().read_stock_info()
    stock_info = stock_info.rename(columns={'zqdm': 'TICKER_SYMBOL', 'zqjc': 'SEC_SHORT_NAME', 'ssrq': 'ESTABLISH_DATE'})
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].dropna()
    stock_info['ESTABLISH_DATE'] = stock_info['ESTABLISH_DATE'].astype(int).astype(str)
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].str.len() == 6]
    stock_info = stock_info.loc[stock_info['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    stock_info['SAMPLE_DATE'] = stock_info['ESTABLISH_DATE'].apply(lambda x: (datetime.strptime(x, '%Y%m%d') + timedelta(365)).strftime('%Y%m%d'))
    return stock_info

class IndustryTechnology:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.industry_daily_k = HBDB().read_index_daily_k_given_date_and_indexs(self.data_start_date, self.industry_info['INDUSTRY_ID'].unique().tolist())
        self.industry_daily_k = self.industry_daily_k.rename(columns={'zqdm': 'INDUSTRY_ID', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        self.industry_daily_k['TRADE_DATE'] = self.industry_daily_k['TRADE_DATE'].astype(str)
        self.industry_daily_k = self.industry_daily_k.sort_values('TRADE_DATE')
        self.industry_daily_k = self.industry_daily_k.pivot(index='TRADE_DATE', columns='INDUSTRY_ID', values='CLOSE_INDEX').sort_index()
        self.industry_daily_k.columns = [self.industry_id_name_dic[col] for col in self.industry_daily_k]

        self.benchmark_daily_k = HBDB().read_index_daily_k_given_date_and_indexs(self.data_start_date, ['000001'])
        self.benchmark_daily_k = self.benchmark_daily_k.rename(columns={'zqmc': 'BENCHMARK_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX'})
        self.benchmark_daily_k['TRADE_DATE'] = self.benchmark_daily_k['TRADE_DATE'].astype(str)
        self.benchmark_daily_k = self.benchmark_daily_k.sort_values('TRADE_DATE')
        self.benchmark_daily_k = self.benchmark_daily_k.pivot(index='TRADE_DATE', columns='BENCHMARK_NAME', values='CLOSE_INDEX').sort_index()

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        stock_market_value_list, star_stock_market_value_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            stock_market_value_list.append(stock_market_value_date)
            star_stock_market_value_list.append(star_stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat(stock_market_value_list)
        self.star_stock_market_value = pd.concat(star_stock_market_value_list)
        self.stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_market_value.hdf', key='table', mode='w')
        self.star_stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_market_value.hdf', key='table', mode='w')
        self.stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_market_value.hdf', key='table')
        self.star_stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_market_value.hdf', key='table')
        self.stock_market_value = pd.concat([self.stock_market_value, self.star_stock_market_value])

    def get_ret(self):
        industry_daily_k = self.industry_daily_k[self.industry_daily_k.index.isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        industry_quarter_ret = (industry_daily_k / industry_daily_k.shift() - 1).dropna(how='all')
        industry_quarter_ret.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_ret.index)
        industry_quarter_ret = industry_quarter_ret[(industry_quarter_ret.index >= self.start_date) & (industry_quarter_ret.index <= self.end_date)]
        return industry_quarter_ret

    def get_vol(self):
        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        industry_daily_ret['REPORT_DATE'] = industry_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_vol = industry_daily_ret[['REPORT_DATE', 'INDUSTRY_NAME', 'DAILY_RET']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).std(ddof=1).reset_index().rename(columns={'DAILY_RET': 'VOL'})
        industry_quarter_vol = industry_quarter_vol.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='VOL').sort_index()
        industry_quarter_vol = industry_quarter_vol[(industry_quarter_vol.index >= self.start_date) & (industry_quarter_vol.index <= self.end_date)]
        return industry_quarter_vol

    def get_beta(self):
        industry_daily_ret = (self.industry_daily_k / self.industry_daily_k.shift() - 1).dropna(how='all')
        industry_daily_ret = industry_daily_ret.unstack().reset_index()
        industry_daily_ret.columns = ['INDUSTRY_NAME', 'TRADE_DATE', 'DAILY_RET']
        benchmark_daily_ret = (self.benchmark_daily_k / self.benchmark_daily_k.shift() - 1).dropna(how='all')
        benchmark_daily_ret = benchmark_daily_ret.unstack().reset_index()
        benchmark_daily_ret.columns = ['BENCHMARK_NAME', 'TRADE_DATE', 'BENCHMARK_DAILY_RET']
        industry_daily_ret = industry_daily_ret.merge(benchmark_daily_ret, on=['TRADE_DATE'], how='inner')
        industry_daily_ret['REPORT_DATE'] = industry_daily_ret['TRADE_DATE'].apply(lambda x: x[:4] + '0331' if x[4:6] <= '03' else x[:4] + '0630' if x[4:6] > '03' and x[4:6] <= '06' else x[:4] + '0930' if x[4:6] > '06' and x[4:6] <= '09' else x[:4] + '1231')
        industry_quarter_beta = industry_daily_ret[['REPORT_DATE', 'INDUSTRY_NAME', 'DAILY_RET', 'BENCHMARK_DAILY_RET']].groupby(['REPORT_DATE', 'INDUSTRY_NAME']).apply(lambda x: np.cov(x['DAILY_RET'], x['BENCHMARK_DAILY_RET'])[0, 1] / np.var(x['BENCHMARK_DAILY_RET'])).reset_index().rename(columns={0: 'BETA'})
        industry_quarter_beta = industry_quarter_beta.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values='BETA').sort_index()
        industry_quarter_beta = industry_quarter_beta[(industry_quarter_beta.index >= self.start_date) & (industry_quarter_beta.index <= self.end_date)]
        return industry_quarter_beta

    def get_market_value(self):
        stock_market_value = self.stock_market_value[self.stock_market_value['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_market_value = stock_market_value.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_market_value = stock_market_value.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE'])
        industry_quarter_market_value = stock_market_value[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_market_value = industry_quarter_market_value.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values='MARKET_VALUE').sort_index()
        industry_quarter_market_value.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_market_value.index)
        industry_quarter_market_value = industry_quarter_market_value[(industry_quarter_market_value.index >= self.start_date) & (industry_quarter_market_value.index <= self.end_date)]
        return industry_quarter_market_value

    def get_all(self):
        ret = self.get_ret()
        ret = ret.unstack().reset_index()
        ret.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'RET']
        vol = self.get_vol()
        vol = vol.unstack().reset_index()
        vol.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'VOL']
        beta = self.get_beta()
        beta = beta.unstack().reset_index()
        beta.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'BETA']
        market_value = self.get_market_value()
        market_value = market_value.unstack().reset_index()
        market_value.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MARKET_VALUE']
        industry_technology = ret.merge(vol, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(beta, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                 .merge(market_value, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_technology['INDUSTRY_ID'] = industry_technology['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_technology['INDUSTRY_TYPE'] = self.sw_type
        industry_technology = industry_technology[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'RET', 'VOL', 'BETA', 'MARKET_VALUE']]
        industry_technology_columns = industry_technology.columns
        industry_technology[industry_technology_columns[4:]] = industry_technology[industry_technology_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_technology_df(industry_technology, list(industry_technology.columns))

class IndustryValuation:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        self.stock_info = get_stock_info()

        stock_valuation_list, star_stock_valuation_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            stock_valuation_list.append(stock_valuation_date)
            star_stock_valuation_list.append(star_stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat(stock_valuation_list)
        self.star_stock_valuation = pd.concat(star_stock_valuation_list)
        self.stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_valuation.hdf', key='table', mode='w')
        self.star_stock_valuation.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_valuation.hdf', key='table', mode='w')
        self.stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_valuation.hdf', key='table')
        self.star_stock_valuation = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_valuation.hdf', key='table')
        self.stock_valuation = pd.concat([self.stock_valuation, self.star_stock_valuation])

    def get_industry_valuation_index_data(self, index_name):
        stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'].isin(self.report_trade_df['TRADE_DATE'].unique().tolist())]
        stock_valuation = stock_valuation.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_valuation = stock_valuation[stock_valuation['TRADE_DATE'] >= stock_valuation['SAMPLE_DATE']]
        stock_valuation = stock_valuation.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_valuation = stock_valuation.merge(industry_market_value, on=['TRADE_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_valuation['WEIGHT_' + index_name] = stock_valuation[index_name] * stock_valuation['MARKET_VALUE'] / stock_valuation['TOTAL_MARKET_VALUE']
        industry_quarter_valuation = stock_valuation[['TRADE_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['TRADE_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_valuation = industry_quarter_valuation.pivot(index='TRADE_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_valuation.index = map(lambda x: x[:4] + '0331' if x[4:6] == '03' else x[:4] + '0630' if x[4:6] == '06' else x[:4] + '0930' if x[4:6] == '09' else x[:4] + '1231', industry_quarter_valuation.index)
        industry_quarter_valuation = industry_quarter_valuation[(industry_quarter_valuation.index >= self.start_date) & (industry_quarter_valuation.index <= self.end_date)]
        return industry_quarter_valuation

    def get_all(self):
        pe_ttm = self.get_industry_valuation_index_data('PE_TTM')
        pe_ttm = pe_ttm.unstack().reset_index()
        pe_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PE_TTM']
        pb_lf = self.get_industry_valuation_index_data('PB_LF')
        pb_lf = pb_lf.unstack().reset_index()
        pb_lf.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PB_LF']
        peg = self.get_industry_valuation_index_data('PEG')
        peg = peg.unstack().reset_index()
        peg.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'PEG']
        dividend_ratio_ttm = self.get_industry_valuation_index_data('DIVIDEND_RATIO_TTM')
        dividend_ratio_ttm = dividend_ratio_ttm.unstack().reset_index()
        dividend_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'DIVIDEND_RATIO_TTM']
        industry_valuation = pe_ttm.merge(pb_lf, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                   .merge(peg, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                   .merge(dividend_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_valuation['INDUSTRY_ID'] = industry_valuation['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_valuation['INDUSTRY_TYPE'] = self.sw_type
        industry_valuation = industry_valuation[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM']]
        industry_valuation_columns = industry_valuation.columns
        industry_valuation[industry_valuation_columns[4:]] = industry_valuation[industry_valuation_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_valuation_df(industry_valuation, list(industry_valuation.columns))

class IndustryFundamental:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.stock_industry = get_stock_industry()
        self.stock_industry = self.stock_industry[self.stock_industry['INDUSTRY_TYPE'] == self.sw_type]
        self.stock_industry = self.stock_industry[self.stock_industry['IS_NEW'] == 1]
        self.stock_industry = self.stock_industry[['INDUSTRY_NAME', 'TICKER_SYMBOL', 'BEGIN_DATE', 'END_DATE']]

        self.stock_info = get_stock_info()

        stock_finance_list, star_stock_finance_list = [], []
        for date in self.report_df['REPORT_DATE'].unique().tolist():
            stock_finance_date = HBDB().read_stock_finance_given_date(date)
            star_stock_finance_date = HBDB().read_star_stock_finance_given_date(date)
            stock_finance_list.append(stock_finance_date)
            star_stock_finance_list.append(star_stock_finance_date)
            print(date)
        self.stock_finance = pd.concat(stock_finance_list)
        self.star_stock_finance = pd.concat(star_stock_finance_list)
        self.stock_finance.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_finance.hdf', key='table', mode='w')
        self.star_stock_finance.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_finance.hdf', key='table', mode='w')
        self.stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_finance.hdf', key='table')
        self.star_stock_finance = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_finance.hdf', key='table')
        self.stock_finance = pd.concat([self.stock_finance, self.star_stock_finance])

        stock_market_value_list, star_stock_market_value_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_market_value_date = HBDB().read_stock_market_value_given_date(date)
            star_stock_market_value_date = HBDB().read_star_stock_market_value_given_date(date)
            stock_market_value_list.append(stock_market_value_date)
            star_stock_market_value_list.append(star_stock_market_value_date)
            print(date)
        self.stock_market_value = pd.concat(stock_market_value_list)
        self.star_stock_market_value = pd.concat(star_stock_market_value_list)
        self.stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_market_value.hdf', key='table', mode='w')
        self.star_stock_market_value.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_market_value.hdf', key='table', mode='w')
        self.stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_market_value.hdf', key='table')
        self.star_stock_market_value = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_market_value.hdf', key='table')
        self.stock_market_value = pd.concat([self.stock_market_value, self.star_stock_market_value])

        stock_daily_k_list, star_stock_daily_k_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_daily_k_date = HBDB().read_stock_daily_k_given_date(date)
            star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(date)
            stock_daily_k_list.append(stock_daily_k_date)
            star_stock_daily_k_list.append(star_stock_daily_k_date)
            print(date)
        self.stock_daily_k = pd.concat(stock_daily_k_list)
        self.star_stock_daily_k = pd.concat(star_stock_daily_k_list)
        self.stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_daily_k.hdf', key='table', mode='w')
        self.star_stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_daily_k.hdf', key='table', mode='w')
        self.stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_daily_k.hdf', key='table')
        self.star_stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_daily_k.hdf', key='table')
        self.stock_daily_k = pd.concat([self.stock_daily_k, self.star_stock_daily_k])

    def get_net_profit(self):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        accum_net_profit = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='NET_PROFIT')
        accum_net_profit = accum_net_profit.sort_index()
        net_profit_Q1 = accum_net_profit.loc[accum_net_profit.index.str.slice(4, 6) == '03']
        net_profit = accum_net_profit - accum_net_profit.shift()
        net_profit = net_profit.loc[net_profit.index.str.slice(4, 6) != '03']
        net_profit = pd.concat([net_profit_Q1, net_profit])
        net_profit = net_profit.sort_index()
        net_profit = net_profit.unstack().reset_index()
        net_profit.columns = ['TICKER_SYMBOL', 'END_DATE', 'NET_PROFIT']
        net_profit = net_profit.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        net_profit = net_profit.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'NET_PROFIT'])
        industry_quarter_net_profit = net_profit[['END_DATE', 'INDUSTRY_NAME', 'NET_PROFIT']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_net_profit = industry_quarter_net_profit.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='NET_PROFIT').sort_index()
        industry_quarter_net_profit_ttm = industry_quarter_net_profit.rolling(window=4, min_periods=4).sum()
        industry_quarter_net_profit = industry_quarter_net_profit[(industry_quarter_net_profit.index >= self.start_date) & (industry_quarter_net_profit.index <= self.end_date)]
        industry_quarter_net_profit_ttm = industry_quarter_net_profit_ttm[(industry_quarter_net_profit_ttm.index >= self.start_date) & (industry_quarter_net_profit_ttm.index <= self.end_date)]
        return industry_quarter_net_profit, industry_quarter_net_profit_ttm

    def get_main_income(self):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='inner')
        stock_finance = stock_finance.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_daily_k[['TRADE_DATE', 'TICKER_SYMBOL', 'CLOSE_PRICE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance['MAIN_INCOME'] = stock_finance['MAIN_INCOME_PS'] * (stock_finance['MARKET_VALUE'] / stock_finance['CLOSE_PRICE'])
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        accum_main_income = stock_finance.pivot(index='END_DATE', columns='TICKER_SYMBOL', values='MAIN_INCOME')
        accum_main_income = accum_main_income.sort_index()
        main_income_Q1 = accum_main_income.loc[accum_main_income.index.str.slice(4, 6) == '03']
        main_income = accum_main_income - accum_main_income.shift()
        main_income = main_income.loc[main_income.index.str.slice(4, 6) != '03']
        main_income = pd.concat([main_income_Q1, main_income])
        main_income = main_income.sort_index()
        main_income = main_income.unstack().reset_index()
        main_income.columns = ['TICKER_SYMBOL', 'END_DATE', 'MAIN_INCOME']
        main_income = main_income.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        main_income = main_income.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MAIN_INCOME'])
        industry_quarter_main_income = main_income[['END_DATE', 'INDUSTRY_NAME', 'MAIN_INCOME']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index()
        industry_quarter_main_income = industry_quarter_main_income.pivot(index='END_DATE', columns='INDUSTRY_NAME', values='MAIN_INCOME').sort_index()
        industry_quarter_main_income_ttm = industry_quarter_main_income.rolling(window=4, min_periods=4).sum()
        industry_quarter_main_income = industry_quarter_main_income[(industry_quarter_main_income.index >= self.start_date) & (industry_quarter_main_income.index <= self.end_date)]
        industry_quarter_main_income_ttm = industry_quarter_main_income_ttm[(industry_quarter_main_income_ttm.index >= self.start_date) & (industry_quarter_main_income_ttm.index <= self.end_date)]
        return industry_quarter_main_income, industry_quarter_main_income_ttm

    def get_industry_fundamental_index_data(self, index_name):
        stock_finance = self.stock_finance[self.stock_finance['END_DATE'].isin(self.report_df['REPORT_DATE'].unique().tolist())]
        stock_finance = stock_finance.sort_values(['TICKER_SYMBOL', 'END_DATE', 'PUBLISH_DATE']).drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='last')
        stock_finance = stock_finance.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'END_DATE'}), on=['END_DATE'], how='inner')
        stock_finance = stock_finance.merge(self.stock_market_value[['TRADE_DATE', 'TICKER_SYMBOL', 'MARKET_VALUE']], on=['TRADE_DATE', 'TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_industry[['TICKER_SYMBOL', 'INDUSTRY_NAME']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance.merge(self.stock_info[['TICKER_SYMBOL', 'SAMPLE_DATE']], on=['TICKER_SYMBOL'], how='inner')
        stock_finance = stock_finance[stock_finance['END_DATE'] >= stock_finance['SAMPLE_DATE']]
        stock_finance = stock_finance.dropna(subset=['TICKER_SYMBOL', 'INDUSTRY_NAME', 'MARKET_VALUE', index_name])
        industry_market_value = stock_finance[['END_DATE', 'INDUSTRY_NAME', 'MARKET_VALUE']].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'MARKET_VALUE': 'TOTAL_MARKET_VALUE'})
        stock_finance = stock_finance.merge(industry_market_value, on=['END_DATE', 'INDUSTRY_NAME'], how='inner')
        stock_finance['WEIGHT_' + index_name] = stock_finance[index_name] * stock_finance['MARKET_VALUE'] / stock_finance['TOTAL_MARKET_VALUE']
        industry_quarter_fundamental = stock_finance[['END_DATE', 'INDUSTRY_NAME', 'WEIGHT_' + index_name]].groupby(['END_DATE', 'INDUSTRY_NAME']).sum().reset_index().rename(columns={'WEIGHT_' + index_name: index_name})
        industry_quarter_fundamental = industry_quarter_fundamental.pivot(index='END_DATE', columns='INDUSTRY_NAME', values=index_name).sort_index()
        industry_quarter_fundamental = industry_quarter_fundamental[(industry_quarter_fundamental.index >= self.start_date) & (industry_quarter_fundamental.index <= self.end_date)]
        return industry_quarter_fundamental

    def get_all(self):
        net_profit, net_profit_ttm = self.get_net_profit()
        net_profit = net_profit.unstack().reset_index()
        net_profit.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT']
        net_profit_ttm = net_profit_ttm.unstack().reset_index()
        net_profit_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT_TTM']
        main_income, main_income_ttm = self.get_main_income()
        main_income = main_income.unstack().reset_index()
        main_income.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MAIN_INCOME']
        main_income_ttm = main_income_ttm.unstack().reset_index()
        main_income_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'MAIN_INCOME_TTM']
        roe_ttm = self.get_industry_fundamental_index_data('ROE_TTM')
        roe_ttm = roe_ttm.unstack().reset_index()
        roe_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'ROE_TTM']
        gross_income_ratio_ttm = self.get_industry_fundamental_index_data('GROSS_INCOME_RATIO_TTM')
        gross_income_ratio_ttm = gross_income_ratio_ttm.unstack().reset_index()
        gross_income_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'GROSS_INCOME_RATIO_TTM']
        net_profit_ratio_ttm = self.get_industry_fundamental_index_data('NET_PROFIT_RATIO_TTM')
        net_profit_ratio_ttm = net_profit_ratio_ttm.unstack().reset_index()
        net_profit_ratio_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_PROFIT_RATIO_TTM']
        eps_ttm = self.get_industry_fundamental_index_data('EPS_TTM')
        eps_ttm = eps_ttm.unstack().reset_index()
        eps_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'EPS_TTM']
        oper_cash_flow_ps_ttm = self.get_industry_fundamental_index_data('OPER_CASH_FLOW_PS_TTM')
        oper_cash_flow_ps_ttm = oper_cash_flow_ps_ttm.unstack().reset_index()
        oper_cash_flow_ps_ttm.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'OPER_CASH_FLOW_PS_TTM']
        net_asset_ps = self.get_industry_fundamental_index_data('NET_ASSET_PS')
        net_asset_ps = net_asset_ps.unstack().reset_index()
        net_asset_ps.columns = ['INDUSTRY_NAME', 'REPORT_DATE', 'NET_ASSET_PS']
        industry_fundamental = net_profit.merge(net_profit_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(main_income, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(main_income_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(roe_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(gross_income_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(net_profit_ratio_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(eps_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(oper_cash_flow_ps_ttm, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer') \
                                         .merge(net_asset_ps, on=['INDUSTRY_NAME', 'REPORT_DATE'], how='outer')
        industry_fundamental['INDUSTRY_ID'] = industry_fundamental['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_fundamental['INDUSTRY_TYPE'] = self.sw_type
        industry_fundamental = industry_fundamental[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE', 'NET_PROFIT', 'NET_PROFIT_TTM', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'ROE_TTM', 'GROSS_INCOME_RATIO_TTM', 'NET_PROFIT_RATIO_TTM', 'EPS_TTM', 'OPER_CASH_FLOW_PS_TTM', 'NET_ASSET_PS']]
        industry_fundamental_columns = industry_fundamental.columns
        industry_fundamental[industry_fundamental_columns[4:]] = industry_fundamental[industry_fundamental_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_fundamental_df(industry_fundamental, list(industry_fundamental.columns))

class IndustryFundamentalDerive:
    def __init__(self, sw_type, start_date, end_date):
        self.sw_type = sw_type
        self.start_date = start_date
        self.end_date = end_date
        self.data_start_date = (datetime.strptime(self.start_date, '%Y%m%d') - timedelta(500)).strftime('%Y%m%d')
        self.load_data()

    def load_data(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.data_start_date, self.end_date)

        self.industry_info = get_industry_info()
        self.industry_info = self.industry_info[self.industry_info['INDUSTRY_TYPE'] == self.sw_type]
        self.industry_info = self.industry_info[self.industry_info['IS_NEW'] == 1]
        self.industry_info = self.industry_info[['INDUSTRY_NAME', 'INDUSTRY_ID', 'BEGIN_DATE', 'END_DATE']]
        self.industry_id_name_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_ID')['INDUSTRY_NAME'].to_dict()
        self.industry_name_id_dic = self.industry_info[['INDUSTRY_ID', 'INDUSTRY_NAME']].set_index('INDUSTRY_NAME')['INDUSTRY_ID'].to_dict()

        self.index_data = FEDB().read_industry_fundamental(self.sw_type)

        stock_daily_k_list, star_stock_daily_k_list = [], []
        for date in self.report_trade_df['TRADE_DATE'].unique().tolist():
            stock_daily_k_date = HBDB().read_stock_daily_k_given_date(date)
            star_stock_daily_k_date = HBDB().read_star_stock_daily_k_given_date(date)
            stock_daily_k_list.append(stock_daily_k_date)
            star_stock_daily_k_list.append(star_stock_daily_k_date)
            print(date)
        self.stock_daily_k = pd.concat(stock_daily_k_list)
        self.star_stock_daily_k = pd.concat(star_stock_daily_k_list)
        self.stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_daily_k.hdf', key='table', mode='w')
        self.star_stock_daily_k.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_daily_k.hdf', key='table', mode='w')
        self.stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/stock_daily_k.hdf', key='table')
        self.star_stock_daily_k = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/inudstry_analysis/star_stock_daily_k.hdf', key='table')
        self.stock_daily_k = pd.concat([self.stock_daily_k, self.star_stock_daily_k])

    def get_yoy(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        yoy_ratio = (index_data / index_data.shift(4) - 1).dropna(how='all')
        return yoy_ratio

    def get_mom(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        mom_ratio = (index_data / index_data.shift() - 1).dropna(how='all')
        return mom_ratio

    def get_yoy_abs(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        yoy_abs = (index_data - index_data.shift(4)).dropna(how='all')
        return yoy_abs

    def get_mom_abs(self, index):
        index_data = self.index_data[['REPORT_DATE', 'INDUSTRY_NAME', index]]
        index_data = index_data.pivot(index='REPORT_DATE', columns='INDUSTRY_NAME', values=index).sort_index()
        mom_abs = (index_data - index_data.shift()).dropna(how='all')
        return mom_abs

    def get_all(self):
        index_list = list(self.index_data.columns)[5: -2]
        yoy_list, mom_list = [], []
        for index in index_list:
            yoy = self.get_yoy(index)
            yoy = pd.DataFrame(yoy.unstack())
            yoy.columns = ['{0}_YOY'.format(index)]
            yoy_list.append(yoy)
            mom = self.get_mom(index)
            mom = pd.DataFrame(mom.unstack())
            mom.columns = ['{0}_MOM'.format(index)]
            mom_list.append(mom)
        yoy_abs_list, mom_abs_list = [], []
        for index in index_list[4:]:
            yoy_abs = self.get_yoy_abs(index)
            yoy_abs = pd.DataFrame(yoy_abs.unstack())
            yoy_abs.columns = ['{0}_YOY_ABS'.format(index)]
            yoy_abs_list.append(yoy_abs)
            mom_abs = self.get_mom_abs(index)
            mom_abs = pd.DataFrame(mom_abs.unstack())
            mom_abs.columns = ['{0}_MOM_ABS'.format(index)]
            mom_abs_list.append(mom_abs)
        industry_fundamental_derive = pd.concat(yoy_list + mom_list + yoy_abs_list + mom_abs_list, axis=1)
        industry_fundamental_derive_columns = list(industry_fundamental_derive.columns)
        industry_fundamental_derive = industry_fundamental_derive.reset_index()
        industry_fundamental_derive['INDUSTRY_ID'] = industry_fundamental_derive['INDUSTRY_NAME'].apply(lambda x: self.industry_name_id_dic[x])
        industry_fundamental_derive['INDUSTRY_TYPE'] = self.sw_type
        industry_fundamental_derive = industry_fundamental_derive[['REPORT_DATE', 'INDUSTRY_ID', 'INDUSTRY_NAME', 'INDUSTRY_TYPE'] + industry_fundamental_derive_columns]
        industry_fundamental_derive_columns = industry_fundamental_derive.columns
        industry_fundamental_derive[industry_fundamental_derive_columns[4:]] = industry_fundamental_derive[industry_fundamental_derive_columns[4:]].replace(np.nan, None)
        InsertTable().insert_industry_fundamental_derive_df(industry_fundamental_derive, list(industry_fundamental_derive.columns))

if __name__ == "__main__":
    start_date = '20170101'
    end_date = '20220331'
    for sw_type in [1, 2, 3]:
        IndustryTechnology(sw_type, start_date, end_date).get_all()
        IndustryValuation(sw_type, start_date, end_date).get_all()
        IndustryFundamental(sw_type, start_date, end_date).get_all()
        IndustryFundamentalDerive(sw_type, start_date, end_date).get_all()