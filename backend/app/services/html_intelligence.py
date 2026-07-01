import requests

from bs4 import BeautifulSoup


BRANDS = [

    "google",
    "microsoft",
    "paypal",
    "amazon",
    "apple",
    "facebook",
    "instagram",
    "github",
    "linkedin",
    "openai"

]


def analyze_html(url):

    score = 0

    indicators = []

    try:

        response = requests.get(

            url,

            timeout=5,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )


        html = response.text

        soup = BeautifulSoup(

            html,
            "html.parser"

        )

        title = ""

        if soup.title:

            title = soup.title.text.lower()

        # -----------------------------------
        # PASSWORD FIELDS
        # -----------------------------------

        password_fields = len(

            soup.find_all(

                "input",

                {"type": "password"}

            )

        )

        if password_fields > 0:

            indicators.append(

                "Password field detected"

            )

            score += 20

        email_fields = len(

            soup.find_all(

                "input",

                {"type": "email"}

            )

        )

        if email_fields > 0:

            indicators.append(
                "Email field detected"
            )

            score += 10

        # -----------------------------------
        # LOGIN FORMS
        # -----------------------------------

        forms = soup.find_all("form")

        form_count = len(forms)

        if form_count >= 10:

            indicators.append(
                "Large number of forms detected"
            )

            score += 5

        login_forms = 0

        for form in forms:

            action = str(
                form.get(
                    "action",
                    ""
                )
            ).lower()

            # Suspicious form actions

            for keyword in [

                "login",
                "signin",
                "verify",
                "update",
                "auth",
                "secure"

            ]:

                if keyword in action:

                    indicators.append(
                        "Suspicious form action"
                    )

                    score += 10

                    break

            text = form.get_text().lower()

            if (

                "login" in text

                or

                "sign in" in text

                or

                "password" in text

            ):

                login_forms += 1

        if login_forms > 0:

            indicators.append(

                "Login form detected"

            )

            score += 20


        # -----------------------------------
        # HIDDEN INPUTS
        # -----------------------------------

        hidden_fields = len(

            soup.find_all(

                "input",

                {"type": "hidden"}

            )

        )

        if hidden_fields > 20:

            indicators.append(
                "Large number of hidden fields"
            )

            score += 5

        # -----------------------------------
        # BRAND KEYWORDS
        # -----------------------------------

        detected_brand = None

        page_text = soup.get_text().lower()

        combined = title + " " + page_text

        domain_brand = None

        for brand in BRANDS:

            if brand in title:

                domain_brand = brand.title()

                break

        if domain_brand:

            detected_brand = domain_brand

            indicators.append(
                f"Brand reference detected: {detected_brand}"
            )

            score += 10

        else:

            for brand in BRANDS:

                if combined.count(brand) >= 3:

                    detected_brand = brand.title()

                    indicators.append(
                        f"Brand reference detected: {detected_brand}"
                    )

                    score += 10

                    break

                    

        # -----------------------------------
        # TITLE ANALYSIS
        # -----------------------------------

        suspicious_words = [

            "verify",
            "secure",
            "update",
            "account",
            "login"

        ]

        for word in suspicious_words:

            if word in title:

                indicators.append(

                    f"Suspicious title keyword: {word}"

                )

                score += 5

        return {

            "html_score": min(
                score,
                100
            ),

            "brand": detected_brand,

            "password_fields":
                password_fields,

            "email_fields":
                email_fields,

            "hidden_fields":
                hidden_fields,

            "form_count":
                form_count,

            "login_forms":
                login_forms,

            "title":
                title,

            "indicators":
                indicators

        }

    except Exception:

        return {
    "html_score": 0,
    "brand": None,
    "password_fields": 0,
    "email_fields": 0,
    "hidden_fields": 0,
    "form_count": 0,
    "login_forms": 0,
    "title": "",
    "indicators": [
        "HTML analysis failed"
    ]
}