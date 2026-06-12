from app.services.brand_engine import detect_brand_impersonation


urls = [

    "https://google.com",

    "https://g00gle-login.com",

    "https://paypal-secure.xyz",

    "https://amazon-verification.net",

    "https://github.com",

    "https://micr0soft-login.com",

    "https://openai.com"

]

for url in urls:

    print("=" * 60)

    print(url)

    print(
        detect_brand_impersonation(url)
    )