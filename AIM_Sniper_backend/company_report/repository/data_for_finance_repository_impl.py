import json
import os
import dart_fss as dart
from datetime import datetime, timedelta
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup

from company_report.repository.data_for_finance_repository import DataForFinanceRepository

warnings.filterwarnings('ignore')

from dotenv import load_dotenv

load_dotenv()

dartApiKey = os.getenv('DART_API_KEY')
if not dartApiKey:
    raise ValueError("Dart API Key가 준비되어 있지 않습니다.")

class DataForFinanceRepositoryImpl(DataForFinanceRepository):
    __instance = None
    SEARCH_YEAR_GAP = 1
    SEARCH_START_YEAR = f'{(datetime.today() - timedelta(days=365*SEARCH_YEAR_GAP)).year}1231'
    SEARCH_END_YEAR = f'{datetime.today().year}1231'

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            dart.set_api_key(dartApiKey)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def selectIncomeDocument(self, parsedData):
        incomeDf = self.getFinancialStatements(parsedData, "손익계산서")
        comprehensiveIncomeDf = self.getFinancialStatements(parsedData, "포괄손익계산서")

        if comprehensiveIncomeDf is None:
            return incomeDf

        if incomeDf is None:
            return comprehensiveIncomeDf

        return incomeDf


    def parsingFromOpenAPI(self, corpCode):
        url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml"
        params = {
            'crtfc_key': dartApiKey,
            'corp_code': corpCode,
            'bsns_year': 2023,
            'reprt_code': '11011', # 사업보고서
            'fs_div': "OFS" # OFS:재무제표, CFS:연결재무제표
        }
        response = requests.get(url, params=params)
        return BeautifulSoup(response.content, 'lxml-xml')



    def getFinancialStatements(self, parsedData, financialStatementsType):
        tag_dict = {# 'rcept_no':'접수번호', # 'reprt_code':'보고서 코드', # 'bsns_year':'사업 연도', # 'corp_code':'고유번호', # 'sj_div':'재무제표구분', # 'sj_nm':'재무제표명', # 'account_id':'계정ID',
            'account_nm': '계정명', 'account_detail': '계정상세',
            'thstrm_nm': '당기명', 'thstrm_amount': '당기금액', 'thstrm_add_amount': '당기누적금액',
            'frmtrm_nm': '전기명', 'frmtrm_amount': '전기금액', 'frmtrm_q_nm': '전기명(분/반기)', 'frmtrm_q_amount': '전기금액(분/반기)', 'frmtrm_add_amount': '전기누적금액',
            'bfefrmtrm_nm': '전전기명', 'bfefrmtrm_amount': '전전기금액',
            'ord': '계정과목 정렬순서', 'currency': '통화 단위', 'bsns_year':'사업 연도'
        }

        try:
            values = []
            for lst in parsedData.findAll('list'):

                if lst.find('sj_nm').text == financialStatementsType:
                    v = []
                    for tag in tag_dict:
                        try:
                            value = lst.find(tag).text
                        except:
                            value = ''
                        v.append(value)
                    values.append(v)

            temp = pd.DataFrame(values, columns=tag_dict.values())
            df = temp[['계정명', '당기금액', '전기금액', '전전기금액']]

            businessYear = int(temp['사업 연도'].unique()[0])

            df = df.rename(columns={
                '당기금액': (businessYear), '전기금액': (businessYear - 1), '전전기금액': (businessYear - 2)})
            df = df.set_index('계정명')

            return df


        except IndexError:
            pass


    def checkLabelNameInFS(self, dfIndex, *probableNames):
        for index in dfIndex:
            if any(keyword in "".join(index) for keyword in probableNames):
                return index
            else:
                continue

        return 0

    def checkLabelComboNameInFS(self, dfIndex, *comboNames):
        for index in dfIndex:
            if all(keyword in "".join(index) for keyword in comboNames):
                return index
            else:
                continue

        return 0

    def getRevenueTrend(self, income):
        name = self.checkLabelNameInFS(
            income.index, "매출액", "영업수익", "수익(매출액)", "Revenue", "Sales")
        if name == 0:
            name = "매출"

        return income.loc[name].squeeze().to_dict()

    def getReceivableTurnover(self, income, balance):
        revenueName = self.checkLabelNameInFS(
                            income.index, "매출액", "영업수익", "수익(매출액)", "Revenue", "Sales")
        revenueName = "매출" if revenueName == 0 else revenueName
        receivableName = self.checkLabelNameInFS(
                            balance.index, "매출채권", "trade receivables")

        revenue = income.loc[revenueName].astype(float)
        revenue = revenue.squeeze()

        if sum([name==receivableName for name in balance.loc[receivableName].index]) >= 2:
            tradeReceivables = balance.loc[receivableName].astype(float)
            tradeReceivables = tradeReceivables.iloc[0, :].squeeze()
        else:
            tradeReceivables = balance.loc[receivableName].astype(float)
            tradeReceivables = tradeReceivables.squeeze()


        receivableTturnover = (revenue / tradeReceivables)
        averagedReceivableTurnover = revenue / ((tradeReceivables.shift(1) + tradeReceivables) / 2)

        return receivableTturnover.to_dict()

    def getOperatingCashFlow(self, cashFlow):
        name = self.checkLabelComboNameInFS(
                        cashFlow.index, "영업활동", "현금흐름")

        return cashFlow.loc[name].squeeze().to_dict()

    def getProfitDataFromDart(self, corpCodeDict):
        profitDataDict = {}

        for corpName, corpCode in corpCodeDict.items():
            print(f"* FS Extract - {corpName}")
            parsedData = self.parsingFromOpenAPI(corpCode)

            try:
                balance = self.getFinancialStatements(parsedData, "재무상태표")
                income = self.selectIncomeDocument(parsedData)
                cashFlow = self.getFinancialStatements(parsedData, "현금흐름표")

                if all([(balance is None), (income is None), (cashFlow is None)]):
                    print(f"[FS_Docu Not Exist] - '{corpName} ({corpCode})'")

                revenueTrend = self.getRevenueTrend(income)
                receivableTurnover = self.getReceivableTurnover(income, balance)
                operatingCashFlow = self.getOperatingCashFlow(cashFlow)

            except Exception as e:
                print(f"[NOT_PASS '{corpName}({corpCode})-FSValue'] => {e}")
                revenueTrend, receivableTurnover, operatingCashFlow = 0, 0, 0
                pass

            profitDataDict[corpName] = {"revenueTrend": revenueTrend,
                                        "receivableTurnover": receivableTurnover,
                                        "operatingCashFlow": operatingCashFlow}

        return profitDataDict
