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
    WANTED_CORP_LIST = ["SK네트웍스", "삼성전자"]
        # , "현대자동차", "SK하이닉스", "LG전자", "POSCO홀딩스", "NAVER", "현대모비스", "삼성SDI", "기아", "LG화학", "삼성물산", "롯데케미칼", "SK이노베이션", "S-Oil", "CJ제일제당", "현대건설", "삼성에스디에스", "LG디스플레이", "아모레퍼시픽", "한화솔루션", "HD현대중공업", "LS", "두산에너빌리티", "SK텔레콤", "케이티", "LG유플러스", "HJ중공업", "삼성전기", "한화에어로스페이스", "효성", "OCI", "코웨이", "한샘", "신세계", "이마트", "현대백화점", "LG생활건강", "GS리테일", "오뚜기", "농심", "롯데웰푸드", "CJ ENM", "한화", "두산밥캣", "LG이노텍", "엘에스일렉트릭", "삼성바이오로직스", "셀트리온"]

    SEARCH_YEAR_GAP = 1
    WANTED_SEARCH_YEAR = f'{(datetime.today() - timedelta(days=365*SEARCH_YEAR_GAP)).year}0101'
    WANTED_SEARCH_DOC = 'A'

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            dart.set_api_key(api_key=dartApiKey)
            openai.api_key = openaiApiKey
            # cls.__instance.__totalCorpDict = {}
            cls.__instance.__wantedCorpCodeDict = {}
            # cls.__instance.__wantedReceiptCodeDict = {}

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
        # totalCorpDict = self.totalCorpCode()
        # corpCodeDict = {}
        # wrongInput = []
        #
        # for name in self.WANTED_CORP_LIST:
        #     print(">", name)
        #     code = totalCorpDict.get(name)
        #     print("--->", code)
        #     if code is not None:
        #         corpCodeDict[name] = code
        #     else:
        #         wrongInput.append(name)
        #
        # if wrongInput:
        #     raise ValueError(f"다음 기업명을 찾을 수 없습니다: {wrongInput}")
        #
        # self.__wantedCorpCodeDict = corpCodeDict
        corpCodeDict = {'SK네트웍스': '00131780', 'LG화학': '00356361'}
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
        # for corpName, doc in preprocessedData.items():
        #     print(f"* CB_AI - {corpName}")
        #     if len(doc) >= maxTokenLength:
        #         print(f"사업내용 토큰 수 초과 -> {corpName}")
        #         continue
        #
        #     messages = [
        #         {"role": "system", "content": promptEngineering},
        #         {"role": "user", "content": doc}
        #     ]
        #
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=messages,
        #         max_tokens=800,
        #         temperature=0.7,
        #     )
        #
        #     changedContextDict[corpName] = {"businessSummary": response.choices[0]['message']['content']}

        changedContextDict = {
            'SK네트웍스': {'businessSummary': "- **SK네트웍스**\n  - 휴대폰 중심의 정보통신 유통 사업\n  - 글로벌 트레이딩 사업\n  - 자동차 렌털 및 경정비 중심의 모빌리티 사업\n  - 환경가전 렌털 사업\n  - 워커힐 호텔앤리조트 운영\n\n- **민팃**\n  - 중고폰 유통 사업\n  - ICT 리사이클 브랜드로 활동\n  - 민팃 ATM을 통한 중고폰 매입 서비스\n  - 전국 생활 거점으로 중고폰 거래 문화 확대\n  - 중고폰 재활용 및 기부 환경 제공\n\n- **스피드메이트**\n  - 자동차 경정비 사업\n  - 수입차 경정비 서비스\n  - 타이어 및 자동차 부품 유통\n  - O2O 플랫폼 '타이어픽' 제공\n  - 고객 중심적인 수입차 정비 문화 확립\n\n- **워커힐 호텔앤리조트**\n  - 레저, 문화, 음식 서비스 제공\n  - 친환경 호텔 전환 활동\n  - 다양한 라이프스타일 경험 제공\n  - 대한민국 호텔 업계 리더\n  - ESG 경영활동 강화\n\n- **글로벌 사업부**\n - 글로벌 마케팅을 위한 화학/소재 중심 사업\n  - SK렌터카를 통한 렌터카 전문 서비스\n  - 친환경 트렌드에 대응한 미래 모빌리티 서비스 개발\n  - SK매직을 통한 렌탈산업 선도\n  - ESG 기반 제품 및 서비스 제공\n\n이상으로 SK네트웍스와 관련된 사업 내용을 5가지 포인트로 정리해보았습니다."},
            'LG화학': {"businessSummary": "- 2023년 매출: 55조 2,498억원 달성\n- 사업부문별 매출액:\n  - LG에너지솔루션: 60.9%\n  - 석유화학 사업부문: 31.1%\n  - 첨단소재 사업부문: 4.4%\n  - 생명과학 사업부문: 2.0%\n  - 공통 및 기타부문: 1.5%\n- 석유화학 사업부문:\n  - PE, PVC, ABS, SAP, 합성고무 등 주요 제품 생산\n  - 친환경 소재 사업 강화: PCR 제품, Bio-SAP, PBAT, PLA 사업화\n  - 'Sustainability' 및 'Nexolution' 사업부 신설\n- 첨단소재 사업부문:\n  - IT/가전, 자동차산업 변화 대응\n  - 리튬 등 메탈 가격 하락으로 수익성 일부 감소\n  - 북미 중심으로 전지재료 출하량 확대 및 수익성 개선 계획\n- 생명과학 사업부문:\n  - 주요 제품 매출 성장, R&D 투자 확대\n  - 항암, 당뇨/대사 영역에 집중 및 카테고리 리더십 강화\n- LG에너지솔루션:\n  - EV, ESS, Micro Mobility 등에 배터리 제품 공급\n  - 성장성 높은 북미 중심 수요 대응 및 수익성 개선\n  - R&D 투자 강화, 제품 안전성 및 품질 향상, 고객별/포트폴리오별 최적 솔루션 제공\n- 공통 및 기타부문:\n  - (주)팜한농: 작물보호제, 종자, 비료 사업\n  - 테라도 중심 작물보호제 해외 판매 강화 및 비료 사업부문 구조개선 계획"},
        }
        return changedContextDict