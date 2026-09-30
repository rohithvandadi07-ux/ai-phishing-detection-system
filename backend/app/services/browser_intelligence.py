from pathlib import Path
from playwright.sync_api import sync_playwright
import time


SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def analyze_browser(url: str):

    start = time.time()

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page(
                viewport={
                    "width": 1440,
                    "height": 900
                },
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            )

            try:

                response = page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=45000
                )

            except Exception:

                response = page.goto(
                    url,
                    wait_until="load",
                    timeout=10000
                )

            page.wait_for_timeout(3000)

            title = page.title()

            final_url = page.url

            filename = (
                final_url
                .replace("https://", "")
                .replace("http://", "")
                .replace("/", "_")
                .replace(":", "_")
            )

            screenshot_path = (
                SCREENSHOT_DIR /
                f"{filename}.png"
            )

            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            browser.close()

            return {

                "success": True,

                "status": (
                    response.status
                    if response
                    else None
                ),

                "title": title,

                "final_url": final_url,

                "screenshot": str(screenshot_path),

                "load_time": round(
                    time.time() - start,
                    3
                )

            }

    except Exception as e:

        return {

            "success": False,

            "status": None,

            "title": "",

            "final_url": url,

            "screenshot": None,

            "load_time": round(
                time.time() - start,
                3
            ),

            "error": str(e)

        }