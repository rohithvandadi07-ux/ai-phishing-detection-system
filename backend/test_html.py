from app.services.html_intelligence import (
    analyze_html
)

urls = [

    "https://google.com",

    "https://github.com",

    "https://paypal.com"

]

for url in urls:

    print("=" * 70)

    print(url)

    print(
        analyze_html(url)
    )