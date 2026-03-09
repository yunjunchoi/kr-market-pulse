"""
KR Market Pulse — ECOS Daily Data Fetcher
한국은행 ECOS Open API 데이터 수집 스크립트
"""

import os, json, requests
from datetime import datetime, timedelta
from pathlib import Path

API_KEY   = os.environ.get("ECOS_API_KEY", "sample")
BASE_URL  = "https://ecos.bok.or.kr/api"
DATA_DIR  = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

NOW = datetime.now()
Y   = NOW.strftime("%Y")
YM  = NOW.strftime("%Y%m")
YM6 = (NOW - timedelta(days=180)).strftime("%Y%m")

def ecos(stat_code, period, start, end, item_code1="", item_code2="", item_code3=""):
    url = f"{BASE_URL}/StatisticSearch/{API_KEY}/json/kr/1/5000/{stat_code}/{period}/{start}/{end}/{item_code1}/{item_code2}/{item_code3}"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        rows = data.get("StatisticSearch", {}).get("row", [])
        return [{"TIME": row["TIME"], "DATA_VALUE": row["DATA_VALUE"]} for row in rows]
    except Exception as e:
        print(f"  ⚠ {stat_code} 실패: {e}")
        return []

def save(filename, payload):
    path = DATA_DIR / filename
    payload["updated"] = NOW.strftime("%Y-%m-%dT%H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename} 저장 완료")


print("=" * 50)
print("  KR Market Pulse — ECOS Data Fetch")
print(f"  {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# ── 금리 ────────────────────────────────────────────────
print("\n[1/8] 금리 데이터...")
save("rates.json", {"data": {
    "base_rate": ecos("722Y001", "M", "200501", YM, "0101000"),
    "bond_3y":   ecos("817Y002", "M", "200501", YM, "010200000"),
    "bond_10y":  ecos("817Y002", "M", "200501", YM, "010210000"),
    "cd_91":     ecos("817Y002", "M", "200501", YM, "010300000"),
    "corp_3y":   ecos("817Y002", "M", "200501", YM, "010400000"),
}})

# ── 통화량 ──────────────────────────────────────────────
print("\n[2/8] M1/M2 통화량...")
save("money.json", {"data": {
    "m1": ecos("101Y004", "M", "201001", YM, "BBLA00"),
    "m2": ecos("101Y004", "M", "201001", YM, "BBMC00"),
}})

# ── 환율 ────────────────────────────────────────────────
print("\n[3/8] 환율...")
save("forex.json", {"data": {
    "usd_krw": ecos("731Y001", "M", "200501", YM, "0000001"),
    "jpy_krw": ecos("731Y001", "M", "200501", YM, "0000002"),
    "eur_krw": ecos("731Y001", "M", "200501", YM, "0000003"),
}})

# ── 기업경영분석 ─────────────────────────────────────────
print("\n[4/8] 기업경영분석...")
def biz(code, item):
    return ecos(code, "A", "2000", Y, item)

save("biz_analysis.json", {"data": {
    "manufacturing": {
        "op_margin":   biz("502Y002", "M206000"),
        "roa":         biz("502Y002", "M208000"),
        "roe":         biz("502Y002", "M209000"),
        "debt_ratio":  biz("502Y002", "M211000"),
        "interest_cov":biz("502Y002", "M210000"),
        "sales_growth":biz("502Y002", "M201000"),
        "net_margin":  biz("502Y002", "M207000"),
    },
    "non_manufacturing": {
        "op_margin":  biz("502Y003", "M206000"),
        "roe":        biz("502Y003", "M209000"),
        "debt_ratio": biz("502Y003", "M211000"),
    },
    "by_size": {
        "large_opm":  ecos("502Y003", "A", "2000", Y, "M206000", "1"),
        "small_opm":  ecos("502Y003", "A", "2000", Y, "M206000", "3"),
        "large_roe":  ecos("502Y003", "A", "2000", Y, "M209000", "1"),
        "small_roe":  ecos("502Y003", "A", "2000", Y, "M209000", "3"),
    }
}})

# ── 자금순환 ────────────────────────────────────────────
print("\n[5/8] 자금순환...")
def fof(item):
    return ecos("221Y011", "A", "2010", Y, item)

save("flow_of_funds.json", {"data": {
    "household_deposit": fof("10111100"),
    "household_stock":   fof("10112100"),
    "household_bond":    fof("10113100"),
    "household_insure":  fof("10114100"),
    "corp_bank_loan":    fof("20211100"),
    "corp_bond":         fof("20212100"),
    "corp_equity":       fof("20213100"),
    "govt_net":          fof("30111100"),
    "foreign_net":       fof("40111100"),
}})

# ── 국제수지 ────────────────────────────────────────────
print("\n[6/8] 국제수지...")
save("bop.json", {"data": {
    "current_account": ecos("901Y032", "M", "201001", YM, "10000000"),
    "goods":           ecos("901Y032", "M", "201001", YM, "11000000"),
    "services":        ecos("901Y032", "M", "201001", YM, "12000000"),
    "income":          ecos("901Y032", "M", "201001", YM, "13000000"),
    "financial_acct":  ecos("901Y032", "M", "201001", YM, "20000000"),
}})

# ── 수출입 ──────────────────────────────────────────────
print("\n[7/8] 수출입...")
save("trade.json", {"data": {
    "exports":  ecos("403Y003", "M", "201001", YM, "X"),
    "imports":  ecos("403Y003", "M", "201001", YM, "M"),
    "balance":  ecos("403Y003", "M", "201001", YM, "T"),
    "by_product": {
        "semiconductor": ecos("403Y003", "M", "201801", YM, "X", "P1E"),
        "auto":          ecos("403Y003", "M", "201801", YM, "X", "P3B"),
        "ship":          ecos("403Y003", "M", "201801", YM, "X", "P3E"),
        "display":       ecos("403Y003", "M", "201801", YM, "X", "P1I"),
        "petrochem":     ecos("403Y003", "M", "201801", YM, "X", "P2A"),
        "steel":         ecos("403Y003", "M", "201801", YM, "X", "P2C"),
    },
    "by_region": {
        "china":    ecos("403Y003", "M", "201801", YM, "X", "", "C"),
        "usa":      ecos("403Y003", "M", "201801", YM, "X", "", "U"),
        "eu":       ecos("403Y003", "M", "201801", YM, "X", "", "E"),
        "asean":    ecos("403Y003", "M", "201801", YM, "X", "", "A"),
        "japan":    ecos("403Y003", "M", "201801", YM, "X", "", "J"),
    }
}})

# ── 거시 (GDP·CPI·PPI·소비자심리) ─────────────────────
print("\n[8/8] GDP / CPI / PPI / 소비자심리...")
save("macro.json", {"data": {
    "gdp":         ecos("200Y001", "Q", "20001", f"{Y}4",   "10111"),
    "cpi":         ecos("901Y009", "M", "200501",  YM,       "0"),
    "ppi":         ecos("404Y014", "M", "200501",  YM,       "총지수"),
    "consumer_si": ecos("511Y002", "M", "200501",  YM,       "CSI63"),
}})

print("\n✅ KR Market Pulse 데이터 수집 완료!")
print(f"   업데이트 시각: {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
