import asyncio

from app.utils.threat_intel import (
    check_virustotal,
    check_phishtank
)

from app.utils.reputation import (
    analyze_url_reputation
)

from app.utils.domain_intel import (
    analyze_domain_intelligence
)

from app.services.distilbert_engine import (
    semantic_phishing_check
)

# ---------------------------------------------------
# ASYNC WRAPPERS
# ---------------------------------------------------

async def run_virustotal(url):

    return await asyncio.to_thread(
        check_virustotal,
        url
    )


async def run_phishtank(url):

    return await asyncio.to_thread(
        check_phishtank,
        url
    )


async def run_reputation(url):

    return await asyncio.to_thread(
        analyze_url_reputation,
        url
    )


async def run_domain_intel(url):

    return await asyncio.to_thread(
        analyze_domain_intelligence,
        url
    )


async def run_bert(url):

    return await asyncio.to_thread(
        semantic_phishing_check,
        url
    )

# ---------------------------------------------------
# MAIN ASYNC SCAN ENGINE
# ---------------------------------------------------

async def async_scan(
    url,
    run_bert_model=True
):

    tasks = [

        run_virustotal(url),
        run_phishtank(url),
        run_reputation(url),
        run_domain_intel(url)

    ]

    # ---------------------------------------------------
    # OPTIONAL DISTILBERT
    # ---------------------------------------------------

    if run_bert_model:

        tasks.append(
            run_bert(url)
        )

    results = await asyncio.gather(*tasks)

    output = {

        "virustotal": results[0],

        "phishtank": results[1],

        "reputation": results[2],

        "domain_intel": results[3]

    }

    # ---------------------------------------------------
    # OPTIONAL BERT OUTPUT
    # ---------------------------------------------------

    if run_bert_model:

        output["bert"] = results[4]

    else:

        output["bert"] = {

            "score": 0,

            "reasons": []

        }

    return output