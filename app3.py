import asyncio
from playwright.async_api import async_playwright
import json

plans_data = []

async def scrape_plans():
    global plans_data
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.moyoplan.com/plans?voice=150-9999&fee=0-10000&excludeDiscount=5-9999&message=9999-9999%2C300-500%2C100-300&data=5-500&sorting=fee_asc&page=1')
        
        plan_elements = await page.query_selector_all('div.css-79elbk.e127i66c0')  # 예제 선택자
        for plan_element in plan_elements:
            plan_name = await (await plan_element.query_selector('div.css-c1pqc9.e3509g011')).text_content()
            plan_data = await (await plan_element.query_selector('div.css-em89nk.e3509g022')).text_content()
            plan_price = await (await plan_element.query_selector('span.css-1djsysu.efajixh3')).text_content()
            
            # 각 요금제 정보를 JSON 객체로 변환
            plans_data.append({
                "plan_name": plan_name.strip(),
                "plan_data": plan_data.strip(),
                "plan_price": plan_price.strip()
            })

        await browser.close()
    
    #지금 now() 날짜 시간을 얻어서 data에 추가
    import datetime
    now = datetime.datetime.now()
    plans_data.append({
        "date": now.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    
    # JSON 객체를 문자열로 변환하여 출력
    print(json.dumps(plans_data, indent=2, ensure_ascii=False))

    #json 파일에 저장하고 누적하자
    with open("plans.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(plans_data, ensure_ascii=False))
        f.write("\n")
    return plans_data

asyncio.run(scrape_plans())

def getdata():
    global plans_data
    return plans_data