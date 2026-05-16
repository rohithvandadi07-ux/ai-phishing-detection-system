import re, math
from collections import Counter

def extract_features(url):
    length = len(url)

    try:
        domain = url.split('/')[2] if '//' in url else url.split('/')[0]
    except:
        domain = url.split('/')[0]

    digits = sum(c.isdigit() for c in url)
    special_chars = sum(not c.isalnum() for c in url)

    freq = Counter(url)
    entropy = -sum((f/length) * math.log2(f/length + 1e-9) for f in freq.values()) if length > 0 else 0

    suspicious_kw = ['login','verify','secure','account','update','banking',
                     'confirm','password','signin','paypal','ebay','amazon',
                     'free','lucky','service','support']

    return [
        length, url.count('.'), url.count('-'), url.count('_'),
        url.count('/'), url.count('?'), url.count('='), url.count('@'),
        url.count('%'), url.count('&'), int('https' in url),
        int('http://' in url), int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', domain))),
        len(domain), domain.count('.'), digits / (length + 1e-6),
        special_chars / (length + 1e-6), entropy,
        sum(kw in url.lower() for kw in suspicious_kw),
        int('www' in url), sum(c.isdigit() for c in domain),
        digits, special_chars, len(re.findall(r'\d+', url)),
        len(url.split('/')),
    ]