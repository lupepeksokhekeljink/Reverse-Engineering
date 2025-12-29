import os
import sys
import requests
import re
from multiprocessing.dummy import Pool
from colorama import Fore, init
import urllib3
import time
import random

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# Colors
red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
magenta = Fore.MAGENTA
white = Fore.WHITE
reset = Fore.RESET

# User agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'curl/7.85.0',
    'Wget/1.21.3 (linux-gnu)'
]

# Banner
banner = red + '''
     ██████  ██░ ██ ▓█████  ██▓     ██▓      █████▒██▓ ███▄    █ ▓█████▄ ▓█████  ██▀███  
   ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    ▓██   ▒▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
   ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    ▒████ ░▒██▒▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒
     ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    ░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
   ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒░▒█░   ░██░▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒
   ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░ ▒ ░   ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
   ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░ ░      ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
   ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░    ░ ░    ▒ ░   ░   ░ ░  ░ ░  ░    ░     ░░   ░ 
         ░   ░  ░  ░   ░  ░    ░  ░    ░  ░        ░           ░    ░       ░  ░   ░     
           ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
           ┃              𝐓𝐨𝐨𝐥𝐬  𝐖𝐞𝐛𝐬𝐡𝐞𝐥𝐥  𝐒𝐜𝐚𝐧𝐞𝐫  𝐁𝐲  𝐑𝐢𝐝𝐗𝐩𝐥𝐨𝐢𝐭              ┃
           ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
''' + reset + '\n'

def show_banner():
    """Clear screen and show banner"""
    clear_command = 'cls' if os.name == 'nt' else 'clear'
    try:
        os.system(clear_command)
    except Exception:
        pass
    print(banner)

def load_list_from_file(path):
    """Load list from file, skip comments"""
    items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                items.append(line)
    except FileNotFoundError:
        print(red + '[ERROR]' + reset + ' File not found: ' + path)
        sys.exit(1)
    except Exception as e:
        print(red + '[ERROR]' + reset + ' Failed to read ' + path + ': ' + str(e))
        sys.exit(1)
    return items

class EvaiLCode:
    """Main scanner class"""
    
    def __init__(self, keywords, min_delay):
        """Initialize scanner"""
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.user_agents = USER_AGENTS
        self.min_delay = float(min_delay)
        self.last_request = {}
        self.keywords = [k.lower() for k in keywords]
    
    def URLdomain(self, site):
        """Extract domain from URL"""
        site = site.strip()
        site = re.sub(r'^https?://', '', site, flags=re.I)
        site = site.split('/')[0]
        return site
    
    def _print_info(self, full_url, is_vuln=None, note=None):
        """Print scanning info"""
        tag = magenta + '[INFO]' + reset
        url_text = white + full_url + reset
        
        if note and is_vuln is None:
            print(tag + ' ' + url_text + ' ' + cyan + '[' + note + ']' + reset)
            return
        
        if is_vuln:
            status = green + '[Yes Vuln Backdor]' + reset
        else:
            status = red + '[Not Vuln Backdor]' + reset
        
        print(tag + ' ' + url_text + ' ' + status)
    
    def checker(self, site):
        """Check for webshell vulnerabilities"""
        domain = self.URLdomain(site)
        url = 'http://' + domain
        
        for Path in Pathlist:
            full = url + Path
            now = time.time()
            last = self.last_request.get(domain, 0)
            elapsed = now - last
            
            if elapsed < self.min_delay:
                to_sleep = self.min_delay - elapsed
                time.sleep(to_sleep)
            
            headers = self.headers.copy()
            headers['User-Agent'] = random.choice(self.user_agents)
            
            try:
                response = requests.get(full, headers=headers, verify=False, timeout=15)
                self.last_request[domain] = time.time()
                
                if response.status_code == 200:
                    text = response.text.lower()
                    if any(keyword in text for keyword in self.keywords):
                        with open('BackdorResult.txt', 'a', encoding='utf-8') as result_file:
                            result_file.write(full + '\n')
                        self._print_info(full, is_vuln=True)
                        return
                    else:
                        self._print_info(full, is_vuln=False)
                else:
                    self._print_info(full, is_vuln=False)
                    
            except requests.exceptions.RequestException:
                self._print_info(full, note='Request Failed')
            except Exception as e:
                if isinstance(site, str):
                    site_display = site
                else:
                    site_display = str(site)
                print(magenta + '[INFO]' + reset + ' ' + white + site_display + reset + ' ' + red + '[Error]' + reset + ' ' + str(e))

def RedZone(site):
    """Wrapper function for multiprocessing"""
    try:
        control.checker(site)
    except Exception as e:
        print(magenta + '[INFO]' + reset + ' ' + white + site + reset + ' ' + red + '[Error]' + reset + ' ' + str(e))

if __name__ == "__main__":
    try:
        show_banner()
        
        targets_file = input('ENTER LIST SITE (eg targets.txt): ').strip()
        paths_file = 'ShellPath.txt'
        keywords_file = 'ShellKeword.txt'
        
        try:
            threads_input = int(input('ENTER NUMBER OF THREADS (eg 50): ').strip())
            if threads_input <= 0:
                threads_input = 50
        except Exception:
            threads_input = 50
        
        try:
            delay_input = float(input('ENTER MIN DELAY PER HOST IN SECONDS (eg 1.5): ').strip())
            if delay_input < 0:
                delay_input = 1.5
        except Exception:
            delay_input = 1.5
        
        targets = load_list_from_file(targets_file)
        raw_paths = load_list_from_file(paths_file)
        keywords = load_list_from_file(keywords_file)
        
        Pathlist = []
        for p in raw_paths:
            p = p.strip()
            if not p:
                continue
            if not p.startswith('/'):
                p = '/' + p
            Pathlist.append(p)
        
        control = EvaiLCode(keywords, delay_input)
        
        pool_size = min(max(1, threads_input), max(1, len(targets)))
        mp = Pool(pool_size)
        mp.map(RedZone, targets)
        mp.close()
        mp.join()
        
        print(cyan + 'Check Result.txt File for the vulnerabilities' + reset)
        
    except Exception as e:
        print(red + 'An error occurred: ' + str(e) + reset)
