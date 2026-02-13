import re
from datetime import datetime
from typing import List, Set, Dict, Tuple
import asyncio
import aiohttp

# ==================== PREFISSI SOCIAL ====================
SOCIAL_PREFIXES = ['fb', 'ig', 'yt', 'tg']

# ==================== TUTTI I PRODOTTI/MODELLI ====================
PRODUCT_CODES = [
    # Base
    'pol', 'ppp1', 'pp1', 'ep2', 'ep3', 'ep4', 'ep5', 
    'es2', 'es3', 'em3', 'em5', 'em10', 'em2', 'em4', 'em8', 'em14',
    'emmm2', 'emmm3', 'emmm4', 'emmm5', 'smartp1', 'ultrat1', 'andro1', 
    'iph1', 'iphon1', 'iphone1', 'regal1', 'tripc1', 'frigg1', 'frig1', 
    'disp1', 'dispens1', 'videog1', 'bell1', 'belle1', 'bbb1', 'bb1',
    'machef1', 'mache1', 'machef2', 'prof1', 'casa1', 'pizz1',
    'natal1', 'manu1', 'lux1', 'tripl1', 'benz1', 'faida1',
    'master1', 'turb1', 'mbell1', 'leg1', 'lego1',
    'play1', 'plays1', 'break1', 'apple1', 'cuff1',
    'motor1', 'pctab1', 'bidoo1', 'sams1', 'orol1',
    'audio1', 'dopcha1', 'megab1', 'mach1', 'bid1',
    'prop1', 'elet1', 'ipho1', 'epp2', 'ess2', 'fri1',
    'andr1', 'topele1', 'faid1', 'ele1', 'vid1',
    'fai1', 'trip1', 'man', 'ox', 'hbn',
    'hhj', 'szs', 'bu', 'zz', 'lll', 'nn', 'sd', 'iio',
    'hj', 'dj', 'lo', 'asd', 'aw', 'aaa', 'lok', 'ko',
    'hg', 'll', 'ace', 'ppp', 'asw', 'rty', 'yui',
    'qq', 'pi', 'luf', 'ffy', 'sabo', 'ok', 'rub', 'guj',
    'ef', 'awe', 'nh', 'oi', 'wewe', 'huj', 'qwe', 'df',
    'oki', 'fj', 'fd', 'rt', 'er', 'qz', 'we', 'as',
    'zd', 'mh', 'dfg', 'fo', 'ft', 'iij', 'erw', 'po',
    'llo', 'rty', 'uy', 'oiu', 'hfd', 'kpa', 'op', 'xx',
    'nqs', 'qma', 'vy', 'zpt', 'xmd', 'xxd', 'vyf', 'lke',
    'tlu', 'xs', 'vyfie', 'rba', 'xxx', 'rws', 'fzc', 'cf',
    'wewe', 'xnu', 'meme', 'yke', 'boc', 'uj', 'eee', 'jj',
    'tja', 'wop', 'hsa', 'sd', 'mye', 'zs', 'sdg', 'kdr',
    'cmt', 'vuh', 'jrn', 'qfa', 'pgh', 'hhn', 'nu',
    'muot', 'fwu', 'vb', 'zle', 'vbn', 'nrx', 'pdk', 'mjuj',
    'aw', 'ngf', 'jcl', 'vwm', 'az', 'hf', 'ju',
    'lra', 'mzt', 'zcv', 'sxe', 'nm', 'vyu', 'hkv',
    'mqp', 'bh', 'ntd', 'ypr', 'a', 'p', 'hgy', 'cfx',
    'afk', 'uoz', 'wmd', 're', 'hfj', 'rw',
    'xn', 'bo', 'tj', 'kd', 'vs', 'pg', 'nr', 'vsa',
    'back1', 'backto1', 'estate1', 'infan1', 'fuorit1', 'spesa1', 'giard1', 'pet1', 'hobby1',
    'xiao1', 'xiaom1', 'nik1', 'samss1', 'ipand1', 'dron1', 'octab1', 'shop1', 'appand1',
    'golo1', 'fredd1', 'fred1', 'black1', 'hallo2', 'mmanu1', 'andr1', 'aapl1', 'b1',
    'cuuf1', 'tric1', 'triplac1', 'tturbo1', 'turbo1', 'smartph1', 'cuffsmartw1', 'tripcha1',
    'pizza1', 'aste1', 'pul1', 'fold1', 'infa1', 'elelt1', 'bshop1',
    'bbbb1', 'bbbbbb1', 'bbbbbbbbb1', 'pppp1', 'ppppp1',
    'eeeees2', 'eeem3', 'eemm3', 'eeeemm5', 'eeep2', 'eees2', 'eem3', 'eep3',
    'emmmm3', 'emmmm4', 'eppp2', 'eppp3', 'esss2', 'esss3', 'emm8',
    'tardmmm', 'nochhmkj', 'mmanna', 'enoch234', 'jh', 'bhu',
    'complbidoo', '1stAuctbids', 'bid', 'bids',
    'nat1', 'addobb1', 'cuf1', 'cuf', 'e2', 'ip1', 'ea1', 'man1',
]

# ==================== PATTERN BIDS ====================
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

# ==================== PATTERN INFLU ====================
INFLU_PATTERNS = [
    "influ{}complbidoo",
]

def get_date_formats(date: datetime) -> List[str]:
    """Genera tutti i formati data possibili dalla data corrente"""
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
    """Genera tutti i possibili promocode validi SOLO per la data specificata"""
    if date is None:
        date = datetime.now()
    
    date_formats = get_date_formats(date)
    date_short = date.strftime('%d%m%y')
    date_long = date.strftime('%d%m%Y')
    
    promocodes = set()
    
    # ============ PATTERN 1: [DATA][PRODOTTO] ============
    for df in date_formats:
        for product in PRODUCT_CODES:
            promocodes.add(f"{df}{product}")
    
    # ============ PATTERN 2: [SOCIAL][DATA][PRODOTTO] ============
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            for product in PRODUCT_CODES:
                promocodes.add(f"{social}{df}{product}")
    
    # ============ PATTERN 3: [DATA][SOCIAL][PRODOTTO] ============
    for df in date_formats:
        for social in SOCIAL_PREFIXES:
            for product in PRODUCT_CODES:
                promocodes.add(f"{df}{social}{product}")
    
    # ============ PATTERN 4: SOLO SOCIAL + DATA ============
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            promocodes.add(f"{social}{df}")
    
    # ============ PATTERN 5: BIDS ============
    promocodes.add(f"5bids{date_short}")
    promocodes.add(f"5bids300man{date_short}")
    promocodes.add(f"6bidsman{date_short}")
    promocodes.add(f"2bids22mastman{date_short}")
    promocodes.add(f"2bidsmasterchef{date_short}")
    promocodes.add(f"3bids250manbids{date_short}")
    promocodes.add(f"3bidstripsmart{date_short}j")
    promocodes.add(f"black7bidsbidoo")
    promocodes.add(f"fast{date_long}bhu")
    
    # ============ PATTERN 6: INFLU ============
    promocodes.add(f"influ{date_short}complbidoo")
    
    # ============ PATTERN 7: SPECIALE 6Dom ============
    day = date.strftime('%d')
    day_no_zero = str(int(day))
    month_names = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
    month_name_str = month_names[int(date.strftime('%m')) - 1]
    promocodes.add(f"6Dom{day_no_zero}{month_name_str}{date.strftime('%Y')}man")
    
    # ============ PATTERN 8: emmm500man ============
    promocodes.add("emmm500man")
    
    # ============ PATTERN 9: 300p + data + jh ============
    promocodes.add(f"300p{date_short}jh")
    
    # ============ PATTERN 10: Data senza prodotto ============
    promocodes.add(f"{date_short}pet1")
    promocodes.add(f"fb{date_short}")
    promocodes.add(f"ig{date_short}")
    promocodes.add(f"yt{date_short}")
    promocodes.add(f"tg{date_short}")
    
    return promocodes

async def check_promocode(session: aiohttp.ClientSession, domain_url: str, dess: str, promocode: str) -> Tuple[str, str, str]:
    """Controlla un singolo promocode e ritorna (promocode, response, saldo)"""
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
            timeout=8
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
    """Riscatta i promocode e mostra SOLO quelli con response 'ok'"""
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
    
    batch_size = 50
    promocodes_list = list(promocodes)
    
    for i in range(0, len(promocodes_list), batch_size):
        batch = promocodes_list[i:i+batch_size]
        tasks = [check_promocode(session, domain_url, dess, code) for code in batch]
        batch_results = await asyncio.gather(*tasks)
        
        for code, status, data in batch_results:
            if status == "ok":
                results["ok"].append((code, data))
                # 🔥 MODIFICA: Mostra anche il link completo
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
        
        await asyncio.sleep(0.3)
    
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
    """ESEGUI QUESTO - già pronto all'uso"""
    user = {
        "domain": "it",  # o en, fr, es, de ecc.
        "dess": "il_tuo_dess_qui"  # ← INSERISCI IL TUO COOKIE DESS QUI
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
