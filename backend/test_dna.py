from app.services.domain_dna_engine import analyze_domain_dna


urls = [

    "https://google.com",

    "https://github.com",

    "https://g00gle-login.com",

    "http://free-bitcoin-login-secure.xyz",

    "https://paypal-security-update.xyz",

    "http://free-bitcoin-login-secure.xyz"

]


for url in urls:

    print("=" * 70)

    print(url)

    print(analyze_domain_dna(url))