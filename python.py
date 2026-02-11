import re
from datetime import datetime
from typing import List, Set, Dict, Tuple
import asyncio
import aiohttp

# Pattern base identificati
SOCIAL_PREFIXES = ['fb', 'ig', 'yt', 'tg']
PRODUCT_CODES = [
    'pol', 'ppp1', 'pp1', 'ep2', 'ep3', 'ep4', 'ep5', 
    'es2', 'es3', 'em3', 'em5', 'em10', 'emmm2', 'emmm3', 'emmm4', 'emmm5',
    'smartp1', 'ultrat1', 'andro1', 'iph1', 'iphon1', 'iphone1',
    'regal1', 'tripc1', 'frigg1', 'frig1', 'disp1', 'dispens1',
    'videog1', 'bell1', 'belle1', 'bbb1', 'bb1',
    'machef1', 'mache1', 'prof1', 'casa1', 'pizz1',
    'natal1', 'manu1', 'lux1', 'tripl1', 'benz1', 'faida1',
    'master1', 'turb1', 'mbell1', 'leg1', 'lego1',
    'play1', 'plays1', 'break1', 'apple1', 'cuff1',
    'motor1', 'pctab1', 'bidoo1', 'sams1', 'orol1',
    'audio1', 'dopcha1', 'megab1', 'mach1', 'bid1',
    'prop1', 'elet1', 'ipho1', 'epp2', 'ess2', 'fri1',
    'andr1', 'casa1', 'topele1', 'faid1', 'ele1', 'vid1',
    'fai1', 'turb1', 'trip1', 'tricha1', 'prof1', 'cuff1',
    'pctab1', 'bidoo1', 'sams1', 'orol1', 'audio1', 'dopcha1',
    'megab1', 'mach1', 'bid1', 'prop1', 'elet1', 'ipho1',
    'epp2', 'ess2', 'fri1', 'andr1', 'topele1', 'faid1',
    'ele1', 'vid1', 'fai1', 'trip1', 'man', 'ox', 'hbn',
    'hhj', 'szs', 'bu', 'zz', 'lll', 'nn', 'sd', 'iio',
    'hj', 'dj', 'lo', 'asd', 'aw', 'aaa', 'lok', 'ko',
    'hg', 'll', 'lok', 'ace', 'ppp', 'asw', 'rty', 'yui',
    'qq', 'pi', 'luf', 'ffy', 'sabo', 'ok', 'rub', 'guj',
    'ef', 'awe', 'nh', 'oi', 'wewe', 'huj', 'qwe', 'df',
    'oki', 'fj', 'fd', 'rt', 'er', 'qz', 'we', 'as',
    'zd', 'mh', 'dfg', 'fo', 'ft', 'iij', 'erw', 'po',
    'llo', 'rty', 'uy', 'oiu', 'hfd', 'kpa', 'op', 'xx',
    'nqs', 'qma', 'vy', 'zpt', 'xmd', 'xxd', 'vyf', 'lke',
    'tlu', 'xs', 'vyfie', 'rba', 'xxx', 'rws', 'fzc', 'cf',
    'wewe', 'xnu', 'meme', 'yke', 'boc', 'uj', 'eee', 'jj',
    'tja', 'wop', 'hsa', 'sd', 'mye', 'zs', 'sdg', 'kdr',
    'cmt', 'zs', 'vuh', 'jrn', 'qfa', 'pgh', 'hhn', 'nu',
    'muot', 'fwu', 'vb', 'zle', 'vbn', 'nrx', 'pdk', 'mjuj',
    'aw', 'ngf', 'jcl', 'vwm', 'az', 'hf', 'ju', 'lok',
    'lra', 'mzt', 'zcv', 'sxe', 'nm', 'vyu', 'hkv', 'aaa',
    'mqp', 'bh', 'ntd', 'ypr', 'a', 'p', 'hgy', 'cfx',
    'afk', 'qma', 'uoz', 'wmd', 're', 'lke', 'hfj', 'lk',
    'rw', 'zpt', 'rw', 'xn', 'bo', 'tj', 'xnu', 'boc',
    'mye', 'kd', 'boc', 'tja', 'vsa', 'tja', 'vs', 'pgh',
    'pg', 'mye'
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
    promocodes = set()
    
    # Pattern 1: [DATA][PRODOTTO]
    for df in date_formats:
        for product in PRODUCT_CODES:
            promocodes.add(f"{df}{product}")
    
    # Pattern 2: [SOCIAL][DATA][PRODOTTO]
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            for product in PRODUCT_CODES:
                promocodes.add(f"{social}{df}{product}")
    
    # Pattern 3: [DATA][SOCIAL][PRODOTTO]
    for df in date_formats:
        for social in SOCIAL_PREFIXES:
            for product in PRODUCT_CODES:
                promocodes.add(f"{df}{social}{product}")
    
    # Pattern 4: Formati speciali
    day = date.strftime('%d')
    month = date.strftime('%m')
    year_short = date.strftime('%y')
    year_long = date.strftime('%Y')
    day_no_zero = str(int(day))
    
    special_patterns = [
        f"6Dom{day_no_zero}gen{year_long}man",
        f"5bids300man{day}{month}{year_short}",
        f"6bidsman{day}{month}{year_short}",
        f"{day}{month}{year_short}Masterchef5b",
    ]
    promocodes.update(special_patterns)
    
    # Pattern 5: Versione con "em" speciale
    promocodes.add("emmm500man")
    
    # Pattern 6: Solo social + data
    for social in SOCIAL_PREFIXES:
        for df in date_formats:
            promocodes.add(f"{social}{df}")
    
    return promocodes

async def check_promocode(session: aiohttp.ClientSession, domain_url: str, dess: str, promocode: str) -> Tuple[str, str, str]:
    """
    Controlla un singolo promocode e ritorna (promocode, response, saldo)
    Response possibili: 'ok', 'expired', 'clicked', 'no', 'showVerify', 'error'
    """
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
                
                # Analizza la response secondo i pattern specificati
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
        return (promocode, f"error_{str(e)[:30]}", "")

async def redeem_and_show_only_ok(user: Dict, session: aiohttp.ClientSession = None):
    """
    Riscatta i promocode e mostra SOLO quelli con response 'ok'
    """
    # Genera codici per oggi
    today = datetime.now()
    promocodes = generate_promocodes(today)
    
    print(f"🔍 Verifica {len(promocodes)} promocode per {today.strftime('%d/%m/%Y')}")
    print(f"👤 Utente: {user.get('domain', 'unknown')}\n")
    print("-" * 80)
    
    domain_url = f"https://{user['domain']}.bidoo.com"
    dess = user['dess']
    
    # Stats
    results = {
        "ok": [],
        "expired": 0,
        "clicked": 0,
        "no": 0,
        "showVerify": 0,
        "other": 0
    }
    
    # Processa in batch per non sovraccaricare
    batch_size = 50
    promocodes_list = list(promocodes)
    
    for i in range(0, len(promocodes_list), batch_size):
        batch = promocodes_list[i:i+batch_size]
        tasks = [check_promocode(session, domain_url, dess, code) for code in batch]
        batch_results = await asyncio.gather(*tasks)
        
        for code, status, data in batch_results:
            if status == "ok":
                results["ok"].append((code, data))
                print(f"✅ OK - {code} - Saldo: {data}")
            elif status == "expired":
                results["expired"] += 1
                print(f"⏰ EXPIRED - {code} - Scaduto: {data}")
            elif status == "clicked":
                results["clicked"] += 1
                print(f"🔄 CLICKED - {code} - Già riscattato oggi")
            elif status == "no":
                results["no"] += 1
                # Non mostriamo questi per non sporcare l'output
                pass
            elif status == "showVerify":
                results["showVerify"] += 1
                print(f"🔐 VERIFY - {code} - Richiede verifica")
            else:
                results["other"] += 1
                print(f"❌ {status.upper()} - {code}")
        
        # Piccola pausa tra batch
        await asyncio.sleep(0.5)
    
    # Report finale
    print("\n" + "=" * 80)
    print(f"📊 REPORT FINALE - {today.strftime('%d/%m/%Y')}")
    print("=" * 80)
    print(f"✅ PROMOCODE VALIDI (OK): {len(results['ok'])}")
    
    if results["ok"]:
        print("\n🏆 ELENCO PROMOCODE FUNZIONANTI:")
        for i, (code, saldo) in enumerate(results["ok"], 1):
            print(f"   {i:2d}. {code} -> Saldo: {saldo}")
    
    print(f"\n⏰ Scaduti: {results['expired']}")
    print(f"🔄 Già riscattati oggi: {results['clicked']}")
    print(f"🔐 Richiedono verifica: {results['showVerify']}")
    print(f"❌ Non esistenti/invalidi: {results['no']}")
    print(f"⚠️ Altri errori: {results['other']}")
    
    # Ritorna solo i promocode validi
    return [code for code, _ in results["ok"]]

async def main():
    """Esempio di utilizzo"""
    # Configurazione utente
    user = {
        "domain": "it",  # o altro dominio
        "dess": "inserisci qui il tuo dess :)"  # Sostituisci con il cookie dess reale
    }
    
    async with aiohttp.ClientSession() as session:
        valid_codes = await redeem_and_show_only_ok(user, session)
        
        if valid_codes:
            print(f"\n💎 TOTALE PROMOCODE VALIDI: {len(valid_codes)}")
            print("\n📋 Copia questi codici:")
            for code in valid_codes:
                print(code)
        else:
            print("\n😞 Nessun promocode valido trovato oggi")

if __name__ == "__main__":
    asyncio.run(main())
