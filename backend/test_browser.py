from app.services.browser_intelligence import analyze_browser


URLS = [

    "https://google.com",

    "https://github.com",

    "https://paypal.com"

]


for url in URLS:

    print("=" * 80)

    result = analyze_browser(url)

    print(result)