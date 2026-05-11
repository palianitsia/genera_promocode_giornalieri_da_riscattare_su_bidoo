import re
from datetime import datetime
from typing import List, Set, Dict, Tuple
import asyncio
import aiohttp

SOCIAL_PREFIXES = ['fb', 'ig', 'yt', 'tg']

PRODUCT_CODES = [
    'i tuoi pattern', 
 ]

BIDS_PATTERNS = [
    "{}bids{}man{}",
    "{}bidsmasterchef{}",
    "{}bidsnotte{}pctablet",
    "{}bids{}manbids{}",
    "bids{}",
    "{}bidsman{}",
    "black{}bidsbidoo",
    "fast{}{}",
    "{}topmaster{}",
    "{}bidstrip{}",
    "emmm{}man",
]

INFLU_PATTERNS = [
    "influ{}complbidoo",
]

def get_date_formats(date: datetime) -> List[str]:
    day = date.strftime('%d')
    month = date.strftime('%m')
    year_short = date.strftime('%y')
    year_long = date.strftime('%Y')
    
    day_no_zero = str(int(day))
    month_no_zero = str(int(month))
    
    formats = [
        f"{day}{month}{year_short}",
        f"{day}{month}{year_long}",
        f"{day_no_zero}{month}{year_short}",
        f"{day}{month_no_zero}{year_short}",
        f"{day_no_zero}{month_no_zero}{year_short}",
        f"{day}{month}{year_short[1]}",
    ]
    
    return list(set(formats))
    
def generate_promocodes(date: datetime = None) -> Set[str]:
    if date is None:
        date = datetime.now()
    
    date_formats = get_date_formats(date)
    date_short = date.strftime('%d%m%y')
    date_long = date.strftime('%d%m%Y')
    year_short = date.strftime('%y')
    day = date.strftime('%d')
    month = date.strftime('%m')
    day_no_zero = str(int(day))
    month_no_zero = str(int(month)) #inserito
    month_names = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
    month_name_str = month_names[int(date.strftime('%m')) - 1]
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    promocodes = set()
    
    for df in date_formats:
        for product in PRODUCT_CODES:
            promocodes.add(f"{df}{product}")
    
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            for product in PRODUCT_CODES:
                promocodes.add(f"{social}{df}{product}")
    
    for df in date_formats:
        for social in SOCIAL_PREFIXES:
            for product in PRODUCT_CODES:
                promocodes.add(f"{df}{social}{product}")
    
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            promocodes.add(f"{social}{df}")
    
    promocodes.update([
        f"5bids{date_short}",
        f"2bidnott{date_short}",
        f"2bidsnott{date_short}",
        f"2bidnot{date_short}",
        f"2bidsnot{date_short}",
        f"5bids300man{date_short}",
        f"6bidsman{date_short}",
        f"2bids22mastman{date_short}",
        f"2bidsmasterchef{date_short}",
        f"3bids250manbids{date_short}",
        f"3bidstripsmart{date_short}j",
        f"6bidblack{date_short}",
        "black7bidsbidoo",
        f"3bis{date_short}masterchef",
        f"3bids{date_short}masterchef",
        f"fast{date_long}bhu",
        f"3bidspush{date_short}",
        f"influ{date_short}complbidoo",
        "emmm500man",
        f"300p{date_short}jh",
        f"{date_short}pet1",
        f"fb{date_short}",
        f"ig{date_short}",
        f"yt{date_short}",
        f"tg{date_short}",
        f"fast{date_short}",
        f"linkfast{date_short}",
        f"special{date_short}pt",
        f"trustPilot{date_short}",
        f"BlackfridayBidoo{date_short}",
        f"sanval{date_short}bd",
        f"3bids{date_short}man",
        f"bids{date_short}",
    ])
    
    promocodes.update([
        f"1puntata{date_short}",
        f"2puntate{date_short}",
        f"3puntate{date_short}",
        f"4puntate{date_short}",
        f"5puntate{date_short}",
        f"puntata{date_short}",
        f"puntate{date_short}",
        f"1puntataFB{date_short}",
        f"1puntataIG{date_short}",
        f"1puntataYT{date_short}",
        f"Fb{date_short}",
        f"Ig{date_short}",
        f"Yt{date_short}",
        f"Tg{date_short}",
    ])
    
    promocodes.add(f"6Dom{day_no_zero}{month_name_str}{date.strftime('%Y')}man")
    
    for n in numbers:
        promocodes.update([
            f"{n}nott{day_no_zero}{month_name_str}{year_short}",
            f"{n}bids{day_no_zero}{month_name_str}mat{year_short}",
            f"{n}bids{day_no_zero}{month_name_str}{year_short}",
            f"{n}bidsnott{day_no_zero}{month_name_str}{year_short}",
            f"{n}bidnott{day_no_zero}{month_name_str}{year_short}",
            f"{n}bidsnot{day_no_zero}{month_name_str}{year_short}",
            f"3bidsera{day_no_zero}{month_name_str}{year_short}",
            # Nuovi pattern
            f"{n}bids{date_short}matt",
            f"{n}bidsmatt{date_short}",
            f"{n}bidspom{date_short}",
            f"{n}bids{date_short}mat",
            f"{n}bids{day}{month}{year_short}mat",
            f"{n}bidsera{day_no_zero}{month_name_str}{year_short}",
        ])
    
    for n in numbers:
        for amount in ["100", "150", "200", "250", "300", "400", "500", "600"]:
            promocodes.update([
                f"{n}bids{amount}man{day}{month}{year_short}",
                f"{n}bids{amount}man{day_no_zero}{month_name_str}{year_short}",
                f"{n}bids{day_no_zero}{month_name_str}{year_short}{amount}man",
            ])
            
    time_periods = ['matt', 'pom', 'sera']
    for n in numbers:
        for period in time_periods:
            promocodes.add(f"{n}b{period}{day}{month}{year_short}")
            promocodes.add(f"{n}b{period}{day_no_zero}{month}{year_short}")
            promocodes.add(f"{n}b{period}{day_no_zero}{month_no_zero}{year_short}")              
    
    return promocodes    

async def check_promocode(session: aiohttp.ClientSession, domain_url: str, dess: str, promocode: str) -> Tuple[str, str, str]:
    try:
        async with session.get(
            f"{domain_url}/push_promotions.php?code={promocode}",
            headers={
                "Cookie": f"dess={dess};",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": domain_url + "/",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest"
            },
            timeout=15
        ) as response:
            if response.status == 200:
                text = await response.text()
                text = text.strip()
                
                if text.startswith("ok-"):
                    saldo = text.split("ok-")[1]
                    return (promocode, "ok", saldo)
                elif text.startswith("expired-"):
                    expired = text.split("expired-")[1]
                    return (promocode, "expired", expired)
                elif text == "clicked":
                    return (promocode, "clicked", "")
                elif text == "no":
                    return (promocode, "no", "")
                elif text == "showVerify":
                    return (promocode, "showVerify", "")
                else:
                    return (promocode, "unknown", text)
            else:
                return (promocode, f"http_{response.status}", "")
    except asyncio.TimeoutError:
        return (promocode, "timeout", "")
    except Exception as e:
        return (promocode, f"error", "")

async def redeem_and_show_only_ok(user: Dict, session: aiohttp.ClientSession) -> List[str]:
    today = datetime.now()
    promocodes = generate_promocodes(today)
    
    print(f"🔍 Verifica {len(promocodes)} promocode per {today.strftime('%d/%m/%Y')}")
    print(f"👤 Utente: {user.get('domain', 'unknown')}")
    print(f"🍪 Dess: {user['dess'][:10]}...{user['dess'][-5:] if len(user['dess']) > 15 else user['dess']}")
    print("-" * 80)
    
    domain_url = f"https://{user['domain']}.bidoo.com"
    dess = user['dess']
    
    results = {
        "ok": [],
        "expired": 0,
        "clicked": 0,
        "no": 0,
        "showVerify": 0,
        "other": 0
    }
    
    batch_size = 30
    promocodes_list = list(promocodes)
    
    for i in range(0, len(promocodes_list), batch_size):
        batch = promocodes_list[i:i+batch_size]
        tasks = [check_promocode(session, domain_url, dess, code) for code in batch]
        batch_results = await asyncio.gather(*tasks)
        
        for code, status, data in batch_results:
            if status == "ok":
                results["ok"].append((code, data))
                link = f"{domain_url}/push_promotions.php?code={code}"
                print(f"✅ OK - {code}")
                print(f"   📎 {link}")
                print(f"   💰 Saldo: {data}\n")
            elif status == "expired":
                results["expired"] += 1
            elif status == "clicked":
                results["clicked"] += 1
            elif status == "no":
                results["no"] += 1
            elif status == "showVerify":
                results["showVerify"] += 1
                print(f"🔐 VERIFY - {code}")
                print(f"   📎 {domain_url}/push_promotions.php?code={code}\n")
            else:
                results["other"] += 1
        
        await asyncio.sleep(0.6)
    
    print("\n" + "=" * 80)
    print(f"📊 REPORT FINALE - {today.strftime('%d/%m/%Y')}")
    print("=" * 80)
    print(f"✅ PROMOCODE VALIDI (OK): {len(results['ok'])}")
    
    if results["ok"]:
        print("\n🏆 ELENCO PROMOCODE FUNZIONANTI:")
        for i, (code, saldo) in enumerate(results["ok"], 1):
            link = f"{domain_url}/push_promotions.php?code={code}"
            print(f"   {i:2d}. {code}")
            print(f"       📎 {link}")
            print(f"       💰 Saldo: {saldo}\n")
    
    print(f"\n⏰ Scaduti: {results['expired']}")
    print(f"🔄 Già riscattati oggi: {results['clicked']}")
    print(f"🔐 Richiedono verifica: {results['showVerify']}")
    print(f"❌ Non esistenti/invalidi: {results['no']}")
    print(f"⚠️ Altri errori: {results['other']}")
    
    return [code for code, _ in results["ok"]]

async def main():
    user = {
        "domain": "it",  # o en, es, ecc.
        "dess": ""  # ← INSERISCI IL TUO COOKIE DESS QUI
    }
    
    async with aiohttp.ClientSession() as session:
        codici_validi = await redeem_and_show_only_ok(user, session)
        
        if codici_validi:
            print(f"\n🎯 TOTALE CODICI VALIDI: {len(codici_validi)}")
            print("\n📋 COPIA QUESTI CODICI:")
            for codice in codici_validi:
                print(f"{codice}")
        else:
            print("\n😞 Nessun codice valido trovato oggi")

if __name__ == "__main__":
    asyncio.run(main())
