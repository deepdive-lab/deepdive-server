"""
HTML 파싱 서비스 모듈
URL 키워드에 따라 다른 HTML element를 파싱하여 markdown으로 변환
"""
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from typing import Dict, Optional, Tuple


# URL 키워드별 파싱 규칙 정의
# key: URL에 포함될 키워드
# value: (selector_type, selector_value) 튜플
# selector_type: "class" 또는 "tag" 등
PARSING_RULES: Dict[str, Dict[str, str]] = {
    "chroma": {
        "parent_selector": "div.markdown-content.col-2.pt-8.md\\:pt-12.marketing-root",
        "child_selector": ".max-w-3xl.mx-auto"
    },
    "redis": {
        "parent_selector": "div.styles_content__c2rWV",
        "child_selector": None  # parent 자체를 파싱
    }
}


async def fetch_article_html(url: str) -> str:
    """
    Playwright를 사용하여 JavaScript가 실행된 후의 HTML을 가져옵니다.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # DOM이 완전히 로드될 때까지 대기
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)            
            html = await page.content()
            return html
        finally:
            await browser.close()


def parse_html_by_keyword(html: str, keyword: str) -> Optional[str]:
    """
    HTML을 파싱하여 markdown으로 변환합니다.
    """
    if keyword not in PARSING_RULES:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    rule = PARSING_RULES[keyword]
    
    # parent element 찾기
    parent = soup.select_one(rule["parent_selector"])
    if not parent:
        return None
    
    # child selector가 있으면 child를, 없으면 parent를 사용
    target = parent.select_one(rule["child_selector"]) if rule["child_selector"] else parent
    
    if not target:
        return None
    
    # markdown으로 변환
    markdown = md(str(target), heading_style="ATX")
    return markdown.strip()


def detect_keyword_from_url(url: str) -> Optional[str]:
    """
    URL에서 키워드를 감지합니다.
    
    Args:
        url: 확인할 URL
        
    Returns:
        감지된 키워드, 없으면 None
    """
    url_lower = url.lower()
    for keyword in PARSING_RULES.keys():
        if keyword in url_lower:
            return keyword
    return None


async def parse_url_to_markdown(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    URL을 받아서 HTML을 가져오고 파싱하여 markdown으로 변환합니다.
    
    Args:
        url: 파싱할 URL
        
    Returns:
        (markdown, error_message) 튜플
        성공 시: (markdown_string, None)
        실패 시: (None, error_message)
    """
    try:
        # URL에서 키워드 감지
        keyword = detect_keyword_from_url(url)
        if not keyword:
            return None, f"URL에 지원하는 키워드가 없습니다. 지원 키워드: {', '.join(PARSING_RULES.keys())}"
        
        # HTML 가져오기
        html = await fetch_article_html(url)
        
        # HTML 파싱
        markdown = parse_html_by_keyword(html, keyword)
        if not markdown:
            return None, f"키워드 '{keyword}'에 해당하는 HTML element를 찾을 수 없습니다."
        
        return markdown, None
        
    except Exception as e:
        return None, f"파싱 중 오류 발생: {str(e)}"
