import urllib.request
import urllib.error
import ssl
import concurrent.futures

BANNER = r"""
   _____                                    ______ _   _ ________  
██████╗ ███╗   ██╗███████╗    ███████╗███╗   ██╗██║   ██║███╗   ███╗
██╔══██╗████╗  ██║██╔════╝    ██╔════╝████╗  ██║██║   ██║████╗ ████║
██║  ██║██╔██╗ ██║███████╗    █████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
██║  ██║██║╚██╗██║╚════██║    ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
██████╔╝██║ ╚████║███████║    ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝BY rhmanz
              [ ScannerFUZZ v1.0 - Stealth Recon Tool ]
                            [ BY rhmanz ]
           [ Developed for Cybersecurity Practical Lab ]
==============================================================================
"""

print(BANNER)

domain = input("Masukkan URL Domain/IP: ")
file_output = input("Masukkan nama file Output: ")

THREADS = 10

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def check_subdomain(sub):
    sub = sub.strip()
    if not sub:
        return None

    url = f"https://{sub}.{domain}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=4, context=ssl_context)
        return f"[+] LIVE ({response.getcode()}): {url}"
    
    except urllib.error.HTTPError as e:
        # Jika dapat 403, kita catat untuk dianalisis lebih lanjut
        return f"[!] RESPONDED ({e.code}): {url}"
    
    except Exception:
        return None

try:
    with open("subdomains-top1million-5000.txt", "r") as f:
        wordlist = f.readlines()

    print(f"[*] Memproses permintaan (Stealth Mode)...")

    with open(f"{file_output}.txt", "a") as logFile:
        logFile.write(f"==== Hasil Recon subdomain {domain} ====\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
            results = executor.map(check_subdomain, wordlist)

            for result in results:
                if result:
                    print(result)
                    logFile.write(result + "\n")

    print(f"\n[✔] Scan selesai! Cek hasil di {file_output}.txt")

except FileNotFoundError:
    print("[-] Error: File wordlist tidak ditemukan!")