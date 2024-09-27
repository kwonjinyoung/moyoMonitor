import asyncio
from playwright.async_api import async_playwright

async def scrape_plans():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.moyoplan.com/plans?voice=150-9999&fee=0-10000&excludeDiscount=5-9999&message=9999-9999%2C300-500%2C100-300&data=5-500&sorting=fee_asc&page=1')
        
        # 페이지에서 요금제 목록을 선택하는 CSS 선택자를 조정해야 할 수 있습니다.
        plan_elements = await page.query_selector_all('div.css-79elbk.e127i66c0') # 예제 선택자
        for plan_element in plan_elements:
            # 각 요금제에 대한 정보를 추출
            plan_name = await (await plan_element.query_selector('div.css-c1pqc9.e3509g011')).text_content()
            plan_data = await (await plan_element.query_selector('div.css-em89nk.e3509g022')).text_content()
            plan_price = await (await plan_element.query_selector('span.css-1djsysu.efajixh3')).text_content()
            print(f"Plan Name: {plan_name}, Data: {plan_data}, Price: {plan_price}")

        await browser.close()

asyncio.run(scrape_plans())
