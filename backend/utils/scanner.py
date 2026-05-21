from playwright.sync_api import sync_playwright
import tldextract

TRACKER_KEYWORDS = [
    "doubleclick", "ads", "adservice", "googlesyndication",
    "google-analytics", "analytics", "facebook", "fbcdn",
    "pixel", "tracker", "metrics", "criteo", "taboola"
]

def scan_website(url, mode="accept", extract_consent=False):
    evidence = {
        "url": url, "cookies": [],
        "third_party_domains": set(),
        "consent_banner": {}, "policy_url": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        if mode == "minimal":
            def block_trackers(route):
                if any(k in route.request.url.lower() for k in TRACKER_KEYWORDS):
                    route.abort()
                else:
                    route.continue_()
            context.route("**/*", block_trackers)

        page = context.new_page()
        network_requests = []
        page.on("request", lambda r: network_requests.append(r.url))

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(5000)
        except Exception:
            browser.close()
            return evidence
        
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
        except:
            pass

        # Cookies
        evidence["cookies"] = context.cookies()

        # Third party domains
        base_domain = tldextract.extract(url).registered_domain
        for req in network_requests:
            rd = tldextract.extract(req).registered_domain
            if rd and rd != base_domain:
                evidence["third_party_domains"].add(rd)

        # Consent banner
        if extract_consent:
            try:
                banner_text = page.inner_text("body")[:3000].lower()
                buttons = page.query_selector_all("button")
                consent_buttons = []
                for btn in buttons[:20]:
                    try:
                        txt = btn.inner_text().strip()
                        if not txt: continue
                        box = btn.bounding_box()
                        bg = page.evaluate("el => window.getComputedStyle(el).backgroundColor", btn)
                        consent_buttons.append({
                            "text": txt,
                            "bg_color": bg or "",
                            "width": round(box["width"]) if box else 0,
                            "height": round(box["height"]) if box else 0
                        })
                    except:
                        continue

                evidence["consent_banner"] = {
                    "banner_detected": any(w in banner_text for w in ["accept cookies", "we use cookies", "cookie consent", "gdpr consent", "manage cookies"]),
                    "text": banner_text[:500],
                    "buttons": consent_buttons,
                    "is_modal": False
                }
            except:
                pass

        # Policy URL
        # Policy URL
        try:
            links = page.query_selector_all("a")
            POLICY_KEYWORDS = ["privacy-notice", "privacy-policy", "privacy_policy", "privacy", "data-policy", "legal/privacy"]
            EXCLUDE_KEYWORDS = ["cookie-policy", "terms", "conditions", "return", "shipping", "help"]

            best_link = None
            for link in links:
                href = (link.get_attribute("href") or "").strip()
                text = (link.inner_text() or "").strip().lower()
                href_lower = href.lower()

                if not href or href == "#": continue
                if any(ex in href_lower for ex in EXCLUDE_KEYWORDS): continue
                if any(ex in text for ex in ["terms", "cookies", "return", "shipping"]): continue

                is_policy = (
                    any(k in href_lower for k in POLICY_KEYWORDS) or
                    any(k in text for k in ["privacy policy", "privacy notice", "data policy", "privacy statement"])
                )

                if is_policy:
                    if href.startswith("http"):
                        best_link = href
                    elif href.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(url)
                        best_link = f"{parsed.scheme}://{parsed.netloc}{href}"
                    else:
                        best_link = url.rstrip("/") + "/" + href.lstrip("/")
                    break

            evidence["policy_url"] = best_link
        except:
            pass

        browser.close()

    evidence["third_party_domains"] = list(evidence["third_party_domains"])
    return evidence


def fetch_policy_text(policy_url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(policy_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            text = page.inner_text("body")[:15000]
            browser.close()
            return text
    except:
        return None