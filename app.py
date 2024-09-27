import asyncio
from playwright.async_api import async_playwright
import json
import markdown
import datetime
import requests
from openai import OpenAI
client = OpenAI()
plans_data = []

saveFilename = "plans.json"

async def scrape_plans(url):
    global plans_data
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        plan_elements = await page.query_selector_all('div.css-79elbk.e127i66c0')  # 예제 선택자
        for plan_element in plan_elements:
    
            # 기본 정보 추출
            plan_name_element = await plan_element.query_selector('div.css-c1pqc9.e3509g011')
            plan_name = await plan_name_element.text_content() if plan_name_element else "Unknown Plan Name"
            
            plan_data_element = await plan_element.query_selector('div.css-em89nk.e3509g022')
            plan_data = await plan_data_element.text_content() if plan_data_element else "Unknown Data"
            
            plan_price_element = await plan_element.query_selector('span.css-1djsysu.efajixh3')
            plan_price = await plan_price_element.text_content() if plan_price_element else "Unknown Price"
            
            # 프로모션 기간 정보 추출
            promotion_info_element = await plan_element.query_selector('div.css-infalx.efajixh4')
            promotion_info = await promotion_info_element.text_content() if promotion_info_element else "No Promotion Info"
            
            # 네트워크 정보 처리 로직
            network_info_elements = await plan_element.query_selector_all('div.css-1pdnyll.e3509g013')
            network_info = [await element.text_content() for element in network_info_elements] if network_info_elements else ["Unknown Network Info"]

            # Extract plan number
            plan_number_element = await plan_element.query_selector('a.e3509g015')
            plan_number_attr = await plan_number_element.get_attribute('href') if plan_number_element else None
            plan_number = plan_number_attr.split('/')[-1] if plan_number_attr else "Unknown Plan Number"

            # 통신사 이름 추출
            network_provider_element = await plan_element.query_selector('img.tw-object-contain')
            network_provider = await network_provider_element.get_attribute('alt') if network_provider_element else "Unknown Network Provider"

            # 모든 정보를 포함하여 plans_data 리스트에 추가
            plans_data.append({
                "plan_name": plan_name.strip(),
                "promotion_info": promotion_info.strip(),  # "promotion_info": promotion_info.strip(),
                "plan_data": plan_data.strip(),
                "plan_price": plan_price.strip(),
                "network_info": network_info,
                "network_provider": network_provider.strip(),
                "plan_number": plan_number.strip()
            })
 




        await browser.close()
    
    now = datetime.datetime.now()
    plans_data.append({
        "date": now.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(saveFilename, "a", encoding="utf-8") as f:
        f.write(json.dumps(plans_data, ensure_ascii=False))
        f.write("\n")
    return plans_data


def getdata(getLatestCount=5):
    global plans_data
    # for plan in plans_data:
    #     print(json.dumps(plan, ensure_ascii=False, indent=4))
    
    result = None
    #만약 plans_data 변수가 비어 있지 않다면, plans.json 파일을 읽고 가장 마지막 5개의 항목을 반환해야 합니다. json파일의 구조는 대략 다음과 같음에 유의해야 한다.
    #[{"plan_name": "티플 가성비(300분/6GB)", "plan_data": "월 6GB", "plan_price": "월 1,600원", "network_provider": "SKT망"}, {"plan_name": "티플 가성비(300분/6GB)", "plan_data": "월 6GB", "plan_price": "월 2,920원", "network_provider": "LG U+망"}, {"plan_name": "아이즈우정(300분/5G)", "plan_data": "월 5GB", "plan_price": "월 4,800원", "network_provider": "SKT망"}, {"plan_name": "아이즈포스트(500분/5G)", "plan_data": "월 5GB", "plan_price": "월 4,900원", "network_provider": "SKT망"}, {"plan_name": "[S]벤티(200분/7GB)", "plan_data": "월 7GB", "plan_price": "월 5,100원", "network_provider": "SKT망"}, {"plan_name": "5G 스마트플러스 (300분+5GB)", "plan_data": "월 5GB", "plan_price": "월 5,100원", "network_provider": "LG U+망"}, {"plan_name": "LTE 아이즈팡팡 (200분/6G)", "plan_data": "월 6GB", "plan_price": "월 5,500원", "network_provider": "SKT망"}, {"plan_name": "5G 음성300분15GB", "plan_data": "월 15GB", "plan_price": "월 5,500원", "network_provider": "LG U+망"}, {"plan_name": "스마일플러스 (200분+5GB)", "plan_data": "월 5GB", "plan_price": "월 5,500원", "network_provider": "SKT망"}, {"plan_name": "우체국 티플 데이터6G", "plan_data": "월 6GB", "plan_price": "월 6,000원", "network_provider": "KT망"}, {"date": "2024-03-30 23:12:32"}]
    #[{"plan_name": "티플 가성비(300분/6GB)", "plan_data": "월 6GB", "plan_price": "월 1,600원", "network_provider": "SKT망"}, {"plan_name": "티플 가성비(300분/6GB)", "plan_data": "월 6GB", "plan_price": "월 2,920원", "network_provider": "LG U+망"}, {"plan_name": "아이즈우정(300분/5G)", "plan_data": "월 5GB", "plan_price": "월 4,800원", "network_provider": "SKT망"}, {"plan_name": "아이즈포스트(500분/5G)", "plan_data": "월 5GB", "plan_price": "월 4,900원", "network_provider": "SKT망"}, {"plan_name": "[S]벤티(200분/7GB)", "plan_data": "월 7GB", "plan_price": "월 5,100원", "network_provider": "SKT망"}, {"plan_name": "5G 스마트플러스 (300분+5GB)", "plan_data": "월 5GB", "plan_price": "월 5,100원", "network_provider": "LG U+망"}, {"plan_name": "LTE 아이즈팡팡 (200분/6G)", "plan_data": "월 6GB", "plan_price": "월 5,500원", "network_provider": "SKT망"}, {"plan_name": "5G 음성300분15GB", "plan_data": "월 15GB", "plan_price": "월 5,500원", "network_provider": "LG U+망"}, {"plan_name": "스마일플러스 (200분+5GB)", "plan_data": "월 5GB", "plan_price": "월 5,500원", "network_provider": "SKT망"}, {"plan_name": "우체국 티플 데이터6G", "plan_data": "월 6GB", "plan_price": "월 6,000원", "network_provider": "KT망"}, {"date": "2024-03-30 23:12:47"}]
    with open(saveFilename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) >= 1:
            last_lines = lines[-min(len(lines), getLatestCount):]
            result = [json.loads(line) for line in last_lines]
    
    return result, plans_data


# .env 를 위해 처리하는 로직 추가
import os
from dotenv import load_dotenv
load_dotenv()


def MakeMessage_GetLatestList(data):
    
    if len(data) == 0:
        return "empty context"
    
    systemPrompt = """System Prompt: context는 요금제와 관련된 정보가 있습니다. 
    각 요금제는 요금제 이름(plan_name), 매달 제공되는 데이터 양(plan_data), 월 요금(plan_price), 통신망(network_provider) ... 정보를 포함합니다.
    다른 설명을 필요 없으며 결과 표만 작성 하십시오.
    
    context: {context}

    output example(make markdown): 
        | 월 요금 | 프로모션 |     요금제명            | 통신사 | 통신망  |  데이터  |  통화량  | 문자량 |   특징 |
        |-------|-------|-----------------------|-----|---------|---------|----------|-------|-----------|
        | 7,700 | 6개월 | 모요only 모두이야기해 6GB+  |tplus|  U+  |  6GB + 1Mbps  |  200분  | 100건 | LTE |
        | 8,800 | 5개월 | 세이브머니유심(200분/6GB+)  |스마텔|  SKT  |  6GB + 1Mbps  |  200분  | 100건 | LTE |
        | 9,000 | 8개월 | 세이브머니유심(200분/6GB+)  |아이즈모바일|  KT  |  6GB + 1Mbps  |  200분  | 100건 | LTE |
        ...
        ..
        .
    
    """
    
    systemPrompt = systemPrompt.format(context=data) if data else "empty context"
    completion = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": "context 정보를 확인하고 output example 예시 같은 양식의 결과를 만들어 주세요."}
        ]
    )

    result = completion.choices[0].message.content
    return result


async def process(addr):
    print("app.py77")
    await scrape_plans(addr)
    datas, nowResult = getdata(3)

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
   
    # 요약할 텍스트
    text_to_summarize = "Your long text to summarize goes here..."
    

    systemPrompt = """System Prompt: 당신은 통신사별 요금제 정보를 담고 있는 데이터를 분석해서 검색 조건, 조사 일시 등을 작성 하십시오. 항목은 작성하지 마십시오.
    마크다운 양식을 사용하며 중요한 것은 항상 **중요** 와도 같이 '**'를 사용 하십시오. 이모티콘을 적시 적소에 사용하여 강조, 의미를 간결히 전달할 수 있도록 하십시오.
    검색 조건은 다음의 url을 분석하여 만드십시오.
    
    url: {url}

    url의 구성은 검색 조건이며 다음의 항목을 참고하여 작성하십시오.: 
     - 프로모션(excludeDiscount): N개월 이상
     - 통화 시간: N분 ~
     - 월 요금: N ~ M원
     - 문자 메시지: 무제한
     - 데이터 사용량: 5GB ~ 500GB
     - QoS: N
    
    Input Data (Context):
    {context}

    This dataset includes thrifty plan information collected over various time points. Each plan information contains the following attributes:
     - plan_name: The name of the plan.
     - plan_data: The amount of data provided (e.g., "월 6GB").
     - plan_price: The price of the plan (e.g., "월 1,600원").
     - network_provider: The network provider (e.g., "SKT망").
     - The date and time when the data was collected are included at the end of each dataset (e.g., "2024-03-30 23:10:16").

    Output Requirements: 
     - If there is only one item in the list, provide a summarized description analyzing the main features of the single plan included in the dataset.
     - If there are two or more items in the list, analyze and compare each dataset in chronological order. Identify and explain the major differences, such as changes in price, the amount of data provided, and changes in network providers. If there are no significant changes or notable features in the most recent data, it's acceptable to write concisely.

    Processing Method: 
     - Analyze the changes between the provided datasets.
     - Compare based on the name, price, amount of data provided, and the network provider of each plan.
     - Identify any changes or notable features to provide to the user.
     - Especially for the most recent data, there's no need to list all information items. Focus on major features or changes.
     - And importantly, always answer in Korean.
     - Utilize Markdown formatting and Telegram emoji styling to enhance readability. 
    
    
    가독성을 높이기 위해 항목을 나열 하십시오.
    """

    systemPrompt = systemPrompt.format(url=addr, context=datas) if datas else systemPrompt.format(context="empty context")
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": "시스템 프롬프트의 요구사항에 충실한 결과를 작성하십시오."}
        ]
    )
    # '티플 가성비(300분/6GB) 요금제는 SKT망과 LG U+망에서 제공되며, LG U+망에서는 가격이 더 높습니다. 아이즈우정(300분/5G) 요금제와 아이즈포스트(500분/5G) 요금제는 SKT망에서 제공되며 데이터양은 5GB로 동일하지만 가격에 차이가 있습니다. [S]벤티(200분/7GB) 요금제는 SKT망에서 월 7GB 데이터를 가장 저렴한 가격에 제공하고 있습니다. 5G 음성300분15GB 요금제는 LG U+망에서 가장 높은 데이터 양을 제공하며, 현재로서는 SKT망을 사용할 수 없습니다. 스마일플러스 (200분+5GB) 요금제와 LTE 아이즈팡팡 (200분/6GB) 요금제는 SKT망에서 동일한 데이터양을 제공하지만 가격에 차이가 있습니다. LU U+망에서는 5G 스마트플러스 (300분+5GB) 요금제를 통해 같은 가격으로 5GB 데이터를 얻을 수 있습니다. 마지막으로, KT망을 사용하는 우체국 티플 데이터6G 요금제는 월 6GB 데이터를 가장 높은 가격으로 제공하고 있습니다.'
    # 올바른 속성 사용
    summary = completion.choices[0].message.content

    # 마크다운을 HTML로 변환
    html1 = markdown.markdown(summary)
    # 파일명을 위한 랜덤 문자열 생성
    now = datetime.datetime.now()
    random_string = now.strftime("%Y%m%d_%H%M%S")
    
    
    from bs4 import BeautifulSoup

    def apply_style_to_html_table(html_table_string):
        # HTML 파싱
        soup = BeautifulSoup(html_table_string, 'html.parser')
        
        # 테이블 요소 탐색
        tables = soup.find_all('table')
        
        # 테이블에 대한 스타일 설정
        for table in tables:
            table['style'] = "border-collapse: collapse; width: 100%;"
            
        # 모든 th, td 요소에 스타일 적용
        for cell in soup.find_all(['th', 'td']):
            cell['style'] = "border: 1px solid black; padding: 8px;"
            
        return str(soup)


    
    # html 파일로 저장
    with open(f"{random_string}_1.html", "w", encoding="utf-8") as f:
        f.write(html1)

    listinfo = MakeMessage_GetLatestList(nowResult)
    html2 = markdown.markdown(listinfo, extensions=['tables'])

    html2 = apply_style_to_html_table(html2)

    # html 파일로 저장
    with open(f"{random_string}_2.html", "w", encoding="utf-8") as f:
        f.write(html2)

    # 텔레그램 봇에 메시지를 전송하는 함수를 정의합니다.
    def send_message_to_telegram_bot(message):
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            #'parse_mode': 'markdown',  # 마크다운 문법을 사용합니다.
            'parse_mode': 'html',
            'text': message
        }
        response = requests.post(url, data=data)
        return response.json()
    
    # addr을 markdown 양식으로 [링크](주소)로 만들어서 출력]
    link = f"[링크]({addr})"
    
    query = "*알뜰 요금제 모니터링*\n" + html1 + "\n\n" + html2
    
    
    #+ f"\n{link}" "\n\n다음 해야 할 일. 하이퍼 링크, 프로모션 기간, gpt4 아웃풋 정돈을 위한 프롬프트 정리. 결과 최상단에 검색 조건 서술."
    
    #결과 년월일 등 정보 파일명으로 html로 저장
    with open(f"{random_string}_result.html", "w", encoding="utf-8") as f:
        f.write(query)
    
    import html2text
    result_for_telegram = html2text.html2text(query)
    result_for_ppomppu = query
    
    print(result_for_telegram)
    print(send_message_to_telegram_bot(result_for_telegram))

# main 추가 
if __name__ == "__main__": 
    
    #조건 2
    addr = ['https://www.moyoplan.com/plans?data=5-500&speedWhenExhausted=1000-2999&voice=150-9999&fee=0-10000&excludeDiscount=5-9999&sorting=fee_asc&page=1']
    
    #조건 1
    #addr = ['https://www.moyoplan.com/plans?voice=150-9999&fee=0-10000&excludeDiscount=5-9999&message=9999-9999%2C300-500%2C100-300&data=5-500&sorting=fee_asc&page=1']
    
    # addr의 요소를중 파일명으로 사용할 수 있는 것은 모두 추출하여 파일명으로
    
    for a in addr:
        plans_data = []
        saveFilename = a.split("/")[-1].replace("?", "_") + ".json"
        
        # 이미 실행 중인 이벤트 루프를 사용하여 비동기 함수 실행
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            loop.run_until_complete(process(a))
        else:
            asyncio.create_task(process(a))      
        
        
        
