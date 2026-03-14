"""
Citation URL Verifier for 1965 Mustang Deep Research Output
============================================================
Self-contained script that:
1. Tests each unique URL from the Deep Research citation table
2. Checks HTTP status, redirects, and page content relevance
3. Outputs a detailed report

This avoids the token-overflow problem that killed previous agent attempts.
"""

import urllib.request
import urllib.error
import ssl
import time
import json
import re
import os

# Disable SSL verification for testing (some sites may have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ── URL Database ──────────────────────────────────────────────────────────────
# Extracted from the Deep Research table (rows 1-121)
# Format: (url, source_type, rows_that_cite_it, brief_description)

CITATION_URLS = [
    # CJ Pony Parts - Resource Guides
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-restoration-guide-chapter-5",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [1, 4, 5, 22, 28, 43, 44, 46, 47, 49, 52, 76, 77, 97, 98, 105, 112],
        "description": "CJ Pony Parts restoration guide Chapter 5 - Powertrain"
    },
    {
        "url": "https://www.cjponyparts.com/resources/mustang-chrome-thermostat-housing-install",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [26],
        "description": "CJ Pony Parts thermostat housing install guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/1965-1966-mustang-radiator-install",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [27, 29, 30, 100],
        "description": "CJ Pony Parts 1965-1966 radiator install guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-heater-box-install",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [32, 110],
        "description": "CJ Pony Parts heater box install guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-electrical-troubleshooting-guide",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [33, 34, 35, 37, 38, 39, 40, 41, 42, 87, 89, 90, 104],
        "description": "CJ Pony Parts electrical troubleshooting guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-wiring-harness-install",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [36, 94, 101, 109],
        "description": "CJ Pony Parts wiring harness install guide"
    },
    {
        "url": "https://www.cjponyparts.com/media/images/install-pdf/install_tcprckp314.pdf",
        "source_type": "Parts supplier technical guide (PDF)",
        "cited_by_rows": [53],
        "description": "CJ Pony Parts rack & pinion conversion manual"
    },
    {
        "url": "https://www.cjponyparts.com/media/images/install-pdf/install_tcprckp121.pdf",
        "source_type": "Parts supplier technical guide (PDF)",
        "cited_by_rows": [55],
        "description": "CJ Pony Parts steering column bearing guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-restoration-guide-chapter-7",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [62, 63, 64, 65, 66, 67, 118],
        "description": "CJ Pony Parts restoration guide Chapter 7 - Brakes & Suspension"
    },
    {
        "url": "https://www.cjponyparts.com/beltline-weatherstrip-kit-with-black-beads-coupe-convertible-1965/p/WSBL230/",
        "source_type": "Parts supplier product page",
        "cited_by_rows": [78],
        "description": "CJ Pony Parts beltline weatherstrip kit product page"
    },
    {
        "url": "https://www.cjponyparts.com/resources/how-to-seal-windshield",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [79],
        "description": "CJ Pony Parts windshield sealing guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/how-to-fix-headliner",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [82],
        "description": "CJ Pony Parts headliner fix guide"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-door-panel-replacement",
        "source_type": "Parts supplier technical guide",
        "cited_by_rows": [84, 102],
        "description": "CJ Pony Parts door panel replacement guide"
    },
    # Classic Industries
    {
        "url": "https://news.classicindustries.com/top-10-restoration-mistakes-on-the-first-generation-1965-73-ford-mustang",
        "source_type": "Published technical article",
        "cited_by_rows": [11, 12, 13, 60, 61, 68, 69, 70, 71, 75, 93, 103, 106, 116],
        "description": "Classic Industries - Top 10 Restoration Mistakes (1965-73 Mustang)"
    },
    {
        "url": "https://www.classicindustries.com/product/usb40001.html",
        "source_type": "Ford TSB Index",
        "cited_by_rows": [119],
        "description": "Classic Industries product page for Ford TSB index (TSB #1454)"
    },
    # Hemmings
    {
        "url": "https://www.hemmings.com/stories/1964-1-2-1966-mustang/",
        "source_type": "Published technical article",
        "cited_by_rows": [2, 72, 74],
        "description": "Hemmings - 1964½-1966 Mustang buyer's/restoration guide"
    },
    {
        "url": "https://www.hemmings.com/stories/solid-lifter-symphony-1965-ford-mustang/",
        "source_type": "Published technical article",
        "cited_by_rows": [3],
        "description": "Hemmings - Solid-lifter symphony 1965 Mustang article"
    },
    {
        "url": "https://www.hemmings.com/stories/swap-meet-9/",
        "source_type": "Published technical article",
        "cited_by_rows": [113],
        "description": "Hemmings - Swap Meet article mentioning leaf spring sag"
    },
    # Forel Publishing
    {
        "url": "https://www.forelpublishing.com/demo/demo40001.pdf",
        "source_type": "Ford TSB Index (PDF)",
        "cited_by_rows": [85, 91],
        "description": "Forel Publishing Ford TSB demo document"
    },
    # YouTube
    {
        "url": "https://www.youtube.com/watch?v=j_GqRCS3EZE",
        "source_type": "YouTube technical video",
        "cited_by_rows": [96],
        "description": "YouTube - Motor mount replacement video"
    },
    # SAAC Forum
    {
        "url": "https://www.saac.com/forum/index.php?topic=14702.0",
        "source_type": "Forum repair write-up",
        "cited_by_rows": [114],
        "description": "SAAC Forum - Taillight problems thread"
    },
    # Works Cited section (additional URLs not in the table but cited in the essay)
    {
        "url": "https://www.hemmings.com/stories/smart-upgrades-make-this-65-mustang-accessible-to-a-wide-range-of-drivers-2657791453/",
        "source_type": "Published technical article (Works Cited #1)",
        "cited_by_rows": [],
        "description": "Hemmings - Smart Upgrades Ecoboost '65 Mustang (Works Cited)"
    },
    {
        "url": "https://www.cjponyparts.com/resources/1965-mustang-vin-decoder",
        "source_type": "Parts supplier reference (Works Cited #3)",
        "cited_by_rows": [],
        "description": "CJ Pony Parts 1965 Mustang VIN Decoder (Works Cited)"
    },
    {
        "url": "https://www.autoevolution.com/news/1965-ford-mustang-rotting-away-on-private-property-deserves-a-better-fate-226222.html",
        "source_type": "Published article (Works Cited #5)",
        "cited_by_rows": [],
        "description": "AutoEvolution - 1965 Ford Mustang article (Works Cited)"
    },
    {
        "url": "https://www.cjponyparts.com/resources/classic-mustang-restoration-guide",
        "source_type": "Parts supplier guide hub (Works Cited #9)",
        "cited_by_rows": [],
        "description": "CJ Pony Parts restoration guide main page (Works Cited)"
    },
]

# ── Verification Logic ────────────────────────────────────────────────────────

def verify_url(entry, timeout=20):
    """
    Verify a single URL. Returns a result dict with:
    - status: 'LIVE', 'REDIRECT', 'DEAD', 'ERROR', 'TIMEOUT', 'CLOUDFLARE_BLOCK'
    - http_code: the HTTP status code (if available)
    - final_url: the final URL after redirects
    - content_check: whether the page content seems relevant
    - notes: human-readable notes
    """
    url = entry["url"]
    result = {
        "url": url,
        "source_type": entry["source_type"],
        "cited_by_rows": entry["cited_by_rows"],
        "description": entry["description"],
        "status": "UNKNOWN",
        "http_code": None,
        "final_url": None,
        "content_check": "NOT CHECKED",
        "content_length": None,
        "notes": ""
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        http_code = response.getcode()
        final_url = response.geturl()
        
        result["http_code"] = http_code
        result["final_url"] = final_url
        
        # Check for redirect
        if final_url != url:
            result["notes"] += f"Redirected to: {final_url}. "
        
        # Read response body (limit to first 50KB to avoid memory issues)
        try:
            body = response.read(50000).decode("utf-8", errors="ignore").lower()
            result["content_length"] = len(body)
        except Exception as e:
            body = ""
            result["notes"] += f"Could not read body: {e}. "
        
        if http_code == 200:
            # Check for Cloudflare/bot protection pages
            if "cloudflare" in body and ("challenge" in body or "ray id" in body):
                result["status"] = "CLOUDFLARE_BLOCK"
                result["content_check"] = "BLOCKED"
                result["notes"] += "Cloudflare protection detected. "
            elif "just a moment" in body and len(body) < 5000:
                result["status"] = "CLOUDFLARE_BLOCK"
                result["content_check"] = "BLOCKED"
                result["notes"] += "Anti-bot challenge page detected. "
            elif "access denied" in body and len(body) < 3000:
                result["status"] = "BLOCKED"
                result["content_check"] = "BLOCKED"
                result["notes"] += "Access denied page. "
            else:
                result["status"] = "LIVE"
                # Content relevance check
                relevance_keywords = ["mustang", "ford", "1965", "restoration", 
                                      "engine", "brake", "electrical", "wiring",
                                      "exhaust", "carburetor", "cooling"]
                found_keywords = [kw for kw in relevance_keywords if kw in body]
                if found_keywords:
                    result["content_check"] = f"RELEVANT ({', '.join(found_keywords[:5])})"
                elif url.endswith(".pdf"):
                    result["content_check"] = "PDF (content not parsed)"
                else:
                    result["content_check"] = "NO RELEVANT KEYWORDS FOUND"
                    result["notes"] += "Page loaded but no Mustang/Ford-related keywords found. "
        else:
            result["status"] = f"HTTP_{http_code}"

    except urllib.error.HTTPError as e:
        result["http_code"] = e.code
        result["status"] = f"HTTP_{e.code}"
        if e.code == 403:
            result["notes"] = "403 Forbidden - may be bot-blocked but page likely exists"
        elif e.code == 404:
            result["notes"] = "404 Not Found - page does NOT exist"
        elif e.code == 503:
            result["notes"] = "503 Service Unavailable - may be temporarily down or bot-blocked"
        else:
            result["notes"] = f"HTTP error: {e.reason}"
    
    except urllib.error.URLError as e:
        result["status"] = "ERROR"
        result["notes"] = f"URL error: {e.reason}"
    
    except TimeoutError:
        result["status"] = "TIMEOUT"
        result["notes"] = f"Request timed out after {timeout}s"
    
    except Exception as e:
        result["status"] = "ERROR"
        result["notes"] = f"Unexpected error: {type(e).__name__}: {e}"
    
    return result


def run_verification():
    """Run verification on all URLs and generate report."""
    
    print(f"{'='*80}")
    print(f"  CITATION URL VERIFICATION REPORT")
    print(f"  1965 Ford Mustang Deep Research Output")
    print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    print()
    
    results = []
    total = len(CITATION_URLS)
    
    for i, entry in enumerate(CITATION_URLS):
        print(f"[{i+1}/{total}] Checking: {entry['url'][:80]}...")
        result = verify_url(entry)
        results.append(result)
        print(f"         -> {result['status']} (HTTP {result['http_code']})")
        if result["notes"]:
            print(f"         -> {result['notes'][:100]}")
        # Small delay to be polite to servers
        time.sleep(1.0)
    
    print()
    print(f"{'='*80}")
    print(f"  SUMMARY")
    print(f"{'='*80}")
    
    # Categorize results
    live = [r for r in results if r["status"] == "LIVE"]
    cloudflare = [r for r in results if r["status"] == "CLOUDFLARE_BLOCK"]
    blocked = [r for r in results if r["status"] == "BLOCKED"]
    dead_404 = [r for r in results if r["http_code"] == 404]
    dead_other = [r for r in results if r["status"].startswith("HTTP_") and r["http_code"] != 404 and r["status"] != "LIVE"]
    errors = [r for r in results if r["status"] in ("ERROR", "TIMEOUT")]
    
    print(f"\n  Total URLs checked:        {total}")
    print(f"  LIVE (200 OK):             {len(live)}")
    print(f"  CLOUDFLARE BLOCKED:        {len(cloudflare)}")
    print(f"  ACCESS BLOCKED:            {len(blocked)}")
    print(f"  DEAD (404):                {len(dead_404)}")
    print(f"  OTHER HTTP ERRORS:         {len(dead_other)}")
    print(f"  ERRORS/TIMEOUTS:           {len(errors)}")
    
    # Count rows covered
    all_cited_rows = set()
    live_cited_rows = set()
    for r in results:
        for row in r["cited_by_rows"]:
            all_cited_rows.add(row)
        if r["status"] in ("LIVE", "CLOUDFLARE_BLOCK"):
            for row in r["cited_by_rows"]:
                live_cited_rows.add(row)
    
    print(f"\n  Table rows with citations: {len(all_cited_rows)} of 121")
    print(f"  Rows with LIVE citations:  {len(live_cited_rows)} of 121")
    
    # Detailed results
    print(f"\n{'='*80}")
    print(f"  DETAILED RESULTS")
    print(f"{'='*80}")
    
    for i, r in enumerate(results):
        print(f"\n  [{i+1}] {r['url']}")
        print(f"      Status:        {r['status']}")
        print(f"      HTTP Code:     {r['http_code']}")
        print(f"      Source Type:   {r['source_type']}")
        print(f"      Cited by rows: {r['cited_by_rows']}")
        print(f"      Content:       {r['content_check']}")
        if r["final_url"] and r["final_url"] != r["url"]:
            print(f"      Redirected to: {r['final_url']}")
        if r["notes"]:
            print(f"      Notes:         {r['notes']}")
    
    # Write JSON results for downstream processing
    output_path = os.path.join(os.path.dirname(__file__), "..", "results", "citation_verification_results.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_urls": total,
            "summary": {
                "live": len(live),
                "cloudflare_blocked": len(cloudflare),
                "access_blocked": len(blocked),
                "dead_404": len(dead_404),
                "other_http_errors": len(dead_other),
                "errors_timeouts": len(errors),
                "table_rows_with_citations": len(all_cited_rows),
                "table_rows_with_live_citations": len(live_cited_rows),
            },
            "results": results
        }, f, indent=2)
    print(f"\n  JSON results written to: {output_path}")
    
    # Write markdown report
    md_path = os.path.join(os.path.dirname(__file__), "..", "results", "citation_verification_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Citation Verification Report\n")
        f.write(f"## 1965 Ford Mustang Deep Research Output\n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total URLs checked | {total} |\n")
        f.write(f"| **LIVE (200 OK)** | **{len(live)}** |\n")
        f.write(f"| Cloudflare blocked | {len(cloudflare)} |\n")
        f.write(f"| Access blocked | {len(blocked)} |\n")
        f.write(f"| Dead (404) | {len(dead_404)} |\n")
        f.write(f"| Other HTTP errors | {len(dead_other)} |\n")
        f.write(f"| Errors/timeouts | {len(errors)} |\n")
        f.write(f"| **Table rows with citations** | **{len(all_cited_rows)}/121** |\n")
        f.write(f"| **Rows with live citations** | **{len(live_cited_rows)}/121** |\n")
        f.write(f"\n")
        
        # LIVE URLs
        f.write("## ✅ LIVE URLs\n\n")
        for r in live:
            f.write(f"### {r['description']}\n")
            f.write(f"- **URL:** [{r['url']}]({r['url']})\n")
            f.write(f"- **Type:** {r['source_type']}\n")
            f.write(f"- **Cited by rows:** {r['cited_by_rows']}\n")
            f.write(f"- **Content check:** {r['content_check']}\n")
            if r["notes"]:
                f.write(f"- **Notes:** {r['notes']}\n")
            f.write("\n")
        
        # CLOUDFLARE BLOCKED
        if cloudflare:
            f.write("## ⚠️ Cloudflare Blocked (URL likely exists but bot-protected)\n\n")
            for r in cloudflare:
                f.write(f"### {r['description']}\n")
                f.write(f"- **URL:** [{r['url']}]({r['url']})\n")
                f.write(f"- **Type:** {r['source_type']}\n")
                f.write(f"- **Cited by rows:** {r['cited_by_rows']}\n")
                f.write(f"- **Notes:** {r['notes']}\n")
                f.write("\n")
        
        # DEAD URLs
        if dead_404:
            f.write("## ❌ DEAD URLs (404 Not Found)\n\n")
            for r in dead_404:
                f.write(f"### {r['description']}\n")
                f.write(f"- **URL:** {r['url']}\n")
                f.write(f"- **Type:** {r['source_type']}\n")
                f.write(f"- **Cited by rows:** {r['cited_by_rows']}\n")
                f.write(f"- **Notes:** {r['notes']}\n")
                f.write("\n")
        
        # OTHER ISSUES
        problem_urls = dead_other + errors + blocked
        if problem_urls:
            f.write("## ⚠️ Other Issues\n\n")
            for r in problem_urls:
                f.write(f"### {r['description']}\n")
                f.write(f"- **URL:** {r['url']}\n")
                f.write(f"- **Status:** {r['status']}\n")
                f.write(f"- **Type:** {r['source_type']}\n")
                f.write(f"- **Cited by rows:** {r['cited_by_rows']}\n")
                f.write(f"- **Notes:** {r['notes']}\n")
                f.write("\n")
        
        # NO SOURCE FOUND issues
        all_rows = set(range(1, 122))
        no_source_rows = sorted(all_rows - all_cited_rows)
        f.write(f"## 📋 Issues with NO SOURCE FOUND ({len(no_source_rows)} of 121)\n\n")
        f.write("These are the row numbers from the original table marked 'NO SOURCE FOUND':\n\n")
        f.write(f"{no_source_rows}\n")
    
    print(f"  Markdown report written to: {md_path}")
    print(f"\n{'='*80}")
    print(f"  VERIFICATION COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    run_verification()
