import json
import os
import zipfile
from io import BytesIO

import dart_fss as dart

from datetime import datetime, timedelta

import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from company_report.repository.data_for_corp_business_repository import DataForCorpBusinessRepository

load_dotenv()

dartApiKey = os.getenv('DART_API_KEY')
if not dartApiKey:
    raise ValueError("Dart API Key가 준비되어 있지 않습니다.")

openaiApiKey = os.getenv('OPENAI_API_KEY')
if not openaiApiKey:
    raise ValueError('API Key가 준비되어 있지 않습니다!')


class DataForCorpBusinessRepositoryImpl(DataForCorpBusinessRepository):
    __instance = None
    WANTED_CORP_LIST = ["SK네트웍스", "삼성전자", "현대자동차", "SK하이닉스", "LG전자", "POSCO홀딩스", "NAVER", "현대모비스", "삼성SDI", "기아", "LG화학", "삼성물산", "롯데케미칼", "SK이노베이션", "S-Oil", "CJ제일제당", "현대건설", "LG디스플레이", "아모레퍼시픽", "한화솔루션", "HD현대중공업", "두산에너빌리티", "SK텔레콤", "케이티", "LG유플러스", "HJ중공업", "삼성전기", "한화에어로스페이스", "효성", "코웨이", "한샘", "신세계", "이마트", "현대백화점", "LG생활건강", "GS리테일", "오뚜기", "농심", "롯데웰푸드", "CJ ENM", "한화", "LG이노텍", "엘에스일렉트릭", "삼성바이오로직스", "셀트리온"]

    SEARCH_YEAR_GAP = 1
    WANTED_SEARCH_YEAR = f'{(datetime.today() - timedelta(days=365*SEARCH_YEAR_GAP)).year}0101'
    WANTED_SEARCH_DOC = 'A'

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            dart.set_api_key(api_key=dartApiKey)
            openai.api_key = openaiApiKey
            cls.__instance.__wantedCorpCodeDict = {}

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def totalCorpCode(self):
        totalCorpCodeDict = {}

        url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={dartApiKey}"
        response = requests.get(url)

        with zipfile.ZipFile(BytesIO(response.content)) as zipRef:
            with zipRef.open('CORPCODE.xml') as xml_file:
                soup = BeautifulSoup(xml_file, 'xml')

                for corp in soup.find_all('list'):
                    corpName = corp.find('corp_name').text
                    corpCode = corp.find('corp_code').text
                    totalCorpCodeDict[corpName] = corpCode

        return totalCorpCodeDict


    def getCorpCode(self):
        totalCorpDict = self.totalCorpCode()
        corpCodeDict = {}
        wrongInput = []

        for name in self.WANTED_CORP_LIST:
            code = totalCorpDict.get(name)
            if code is not None:
                corpCodeDict[name] = code
            else:
                wrongInput.append(name)

        if wrongInput:
            raise ValueError(f"다음 기업명을 찾을 수 없습니다: {wrongInput}")

        self.__wantedCorpCodeDict = corpCodeDict
        return corpCodeDict

    def getCorpReceiptCode(self):
        corpReceiptCodeDict = {}
        for corpName, corpCode in self.__wantedCorpCodeDict.items():
            try:
                corpReportList = dart.filings.search(
                                    corp_code=corpCode,
                                    bgn_de=self.WANTED_SEARCH_YEAR,
                                    pblntf_ty=self.WANTED_SEARCH_DOC
                                ).report_list

                corpReceiptCode = next((report.rcept_no
                                        for report in corpReportList
                                        if ('사업보고서' in report.report_nm) and (r'[첨부정정]' not in report.report_nm))
                                       , None)

                corpReceiptCodeDict[corpName] = corpReceiptCode

            except Exception as e:
                print(f"[ERROR] {corpName} -> \n {e}")
                pass

        return corpReceiptCodeDict

    def apiResponseOfCorpDocument(self, receiptCode):
        url = 'https://opendart.fss.or.kr/api/document.xml'
        params = {
            'crtfc_key': dartApiKey,
            'rcept_no': receiptCode}

        return requests.get(url, params=params)

    def getDataFromZipFile(self, response):
        file = BytesIO(response.content)
        zfile = zipfile.ZipFile(file, 'r')
        corpDocuList = sorted(zfile.namelist(), key=lambda x: len(x))

        return zfile, corpDocuList

    def getOverviewDataFromXml(self, xmlFile, corpName, receiptCode):
        try:
            soup = BeautifulSoup(xmlFile, 'lxml-xml').find_all("SECTION-2")
            index = 0
            for idx, data in enumerate(soup):
                if data.find("TITLE").text[:15] == "1. 사업의 개요":
                    index = idx
                    break

            return soup[index]

        except Exception as e:
            print(f"\n*** getOverviewDataFromXml '{corpName}-{receiptCode}' -> {e}")
            pass

    def getAllDataFromXml(self, xmlFile, wanted_tag):
        soup = BeautifulSoup(xmlFile, 'lxml-xml')
        return soup.find_all(wanted_tag)

    def getRawDataFromDart(self):
        rawDataDict = {}
        rawCorpDataDict = {}
        for corpName, receiptCode in self.getCorpReceiptCode().items():
            print(f"* CB_RAW - {corpName}")
            response = self.apiResponseOfCorpDocument(receiptCode)
            zipFile, corpDocuList = self.getDataFromZipFile(response)
            xmlFile = zipFile.read(corpDocuList[0])

            rawDataDict[corpName] = str(xmlFile)
            rawCorpDataDict[corpName] = str(self.getOverviewDataFromXml(xmlFile, corpName, receiptCode))

        return rawCorpDataDict

    def preprocessTaginParagraph(self, paragraph):
        return paragraph.get_text().replace("\n", "")

    def preprocessRawData(self, rawData):
        preprocessDataDict = {}

        for corpName, corpData in rawData.items():
            print(f"* CB_PREPRO - {corpName}")
            paragraphList = self.getAllDataFromXml(corpData, "P")

            result = [self.preprocessTaginParagraph(paragraph)
                      for paragraph in paragraphList]

            preprocessDataDict[corpName] = "\n".join(result)


        return preprocessDataDict

    def changeContentStyle(self, preprocessedData):
        maxTokenLength = 16385
        promptEngineering = f"""
        사용자 입력 메시지의 내용을 <조건>에 맞춰 5가지 포인트로 정리하라.

        <조건>
        1. 개조식으로 작성할 것.
        2. bullet point로 작성할 것.
        3. bullet point는 기업의 사업 내용으로 나눌 것.
        4. 800 token 내로 작성을 마무리할 것.
        5. 재무제표와 관련된 내용은 최소화할 것. (없으면 더 좋음)
        """

        changedContextDict = {}
        for corpName, doc in preprocessedData.items():
            print(f"* CB_AI - {corpName}")
            if len(doc) >= maxTokenLength:
                print(f"사업내용 토큰 수 초과 -> {corpName}")
                continue

            messages = [
                {"role": "system", "content": promptEngineering},
                {"role": "user", "content": doc}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=800,
                temperature=0.7,
            )

            changedContextDict[corpName] = {"businessSummary": response.choices[0]['message']['content']}

        return changedContextDict