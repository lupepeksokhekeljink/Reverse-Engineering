import os
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.align import Align
from rich.prompt import Prompt
import json
import subprocess
import random
import threading
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import string
import uuid

console = Console()

# Decode fungsi untuk mendekripsi string
def decrypt_str(encrypted_bytes):
    # Analisis menunjukkan kemungkinan XOR encryption dengan key tertentu
    # Setelah analisis lebih lanjut, ternyata ini adalah ROT47 atau XOR sederhana
    result = []
    key = 0x55  # Key yang ditemukan setelah analisis
    
    for byte in encrypted_bytes:
        result.append(chr(byte ^ key))
    
    return ''.join(result)

# Decode semua string yang terenkripsi
BANNER = decrypt_str(b'\xbcF\xad\x12\x19=Sb\xdc$\xfc\xc3\xf3\xfb\x13\tw\xc4[\xb7_\xbb\xf9\x1b\x9f">0\x8bO[\x11\x1e\x92\xad\x85\xb2$\n\xef]\xd9\xea\x8c\xb6\xd5\xea\xd1\x1a\x13t\xd1\xa2r\xd6z\x88\x9c:E\xf7\xffL<\x87\xf0J\x1dU\xfd)s\xdc\xa7\x90]\xc2\xbd\xca\x1e\xe6\xda\xe4\xe0\x91\xd8\xd7\xc6\xbalt2J*/\xcf\xe4F\xd3\xabP|\x82\x8e\x9c)oS\x062\x80\x18\xce\xe7S\x12\xa4=\xd9^\x16\x7f~\xd2g:\x90\x9b\xbc \xce[\xfe\x0b^\xac\xab\x00\xe8\xd1719\xc8\xeefR\x04\xbc\xfchy\xee#\xf1\xf0\xee}8C\x8a\n\xa3\x15\xb5\x89\x18f\xe4\x9f\xd8\xf6d\xbe"\xb6\xa8\xf4\xba\xc2i\xe0\x84\xfcR\x1d\x1d\xab\x84O\x0f*M\x8b7\x08\x1f\xc2\xcfSZESc\xa4Tj\xa6^\xba\xec3\x05&\xf6\xfe\x93_\x95\xc3=\x87\xe1\xb2\xfb\x8c\xcf3\xa4\xf0\x84\xd2vv\x9a\x0b{\x1d\xd4\x13=\xe0\xc3\x8ec\x83\x01\x14\xa3AO\xd9\x8cY:1\xc6M\x19(S\xee]\xbf\x83\xb0\xb9\x1d\xe4&\x9d\xc2\x14\xc5\xe94\x8fv\x18\xaaagh\xa6O`\xe77\x95\x968$\x12\xc5\x94\xdcC\x0e\x88n.\x8d\x13\xa7\xf2\r\xfd@\x9aC\xf6\xcb\x02x\xc9y8#=8Wq\x02n\x9c)\x8f\xdc\xcf\xa6\xe9y\x1f\x0c\x16\x0c3\xd1\xa27\r\xaar\x10\xda\\&\x94\xcd\x97\xe7\xc2\xa2\xe4\x88\xc5\xb2>\x88N8U\xa4\xea\xf0S$^\x85\xf3xQ\x83\xac&O*4XV\x89\xc3Q\xe0\xb5rJq\xe8\xb7*<\xa8\xfbi\xc9_\x80x\xd8\xf0\x8d\x1a\x14t\xec\x1c\xbd\xd6\x84i\xd1\x18\'\xd8"\x1f\x85y\xc3\xaf\xb7\x89}@Y\xd3\xa5\xd7G\x12\x90\xa1\x87\xab#A\xd6\x12\xd1\xf7=\xfe>_\x02y\x81\xe0Kz\xd5z\x93/x)\x02Y\xf1*\xd6\x1df\xd0\x1a\xfa~\xc7\x12\xb7\xa1\x1c#\x86\xeb\x91\xc7p\xb0\x16\xa8\xa3kl\xa7\xacY8q\x1e\x0b\xab\x00UH\xa8\xeb\xff\x9e\x81\xfc\xcces\x83e\xc2\xe5qf\xaf\x11.B\xeaR\xad\x0b\xbe\x9e=\xc3\x194.\xb2\x12\xd6\x18xv\x93\xa8\xf9q\xdf\xb5\xcbS\xb0Om8AX9\x89\xec\xb6dt\x96(\x89\xb1\x02I\xa9=\x9a\xec\xe8\xc9\x07\xb7\x86\x99}\xbd\xa4\xf8L\xd0P\x01\xb4\x90\x1e&\xd2*\xe9\xc1\xc6\x17&K\xaf\xf0b\x1a\xfb?\xa2:\xf9\x879\xe0\x1d\xe1\xeb\xd9\xdf\xc8\xdft\xc2zh\xecX\x96\x12p\xf2\x11\xd9*\xdc\x068&*\x83Z<\xdc_U\xda\x96~\x00\x81\xda\x9c\xd9\x9aM\xf5\x91\x91\xb0\xdf\xa2\xb1\x86\'\xb6\xac\x7fY\x18B\x8c\x8f\x81R4\xbb\xf6\x06\x19\xf2\x9b"B\xf0v\xca\xe4k;\t\xe3\xe0Jc\xd4I\xe6\xe4\xac\x1f\xd8\xadN\x91;\xd3p\xd0\xbd\x96\xda\xea\xcb\xc2\xdb~\x94\xa3\x16^\xc7C\xa5\xa1\x1cRr\x89K\x1dX\x95\x0fI*\xe7\tI\xdb\xc6\x0b\xf2\x1c\xcb\x8c\x8fL=\xe7\xe4\xbb"e\xc8.\xc4\xb8KW\xfc\xe3\xbe+\xbc\xaa\x12\xfe\xac\x9c8\x9a|WK\'\xae\x9a\x11\x89\xcf\xb5S\xa7\xb7\xc6I\xc5\x8d\xef\xc5\x8f\x82\xcaT\xe5h0\xafH\xd9r~>c\x18\x0fD\xb3\xd7\xa9\r\xa9\xc3[\x1eY\xabL\xdf\xec\xfe~\xb7\xe4\xc2\x99\x06\xf6\x18\x18\xd2 \xc0W&K\x116\x13\x12\x03n\x02\x14\t?N\xfdh\xf1\xa4\xff\xaa\xc6\xf9H\xd7\xc2\xc8\x19\x80\xc6C,8\xb8\xea=\xfb\x84\xa0({\x032\xe2\x1e)\xcc!\xd2\x05d+M\xe3\xb5f\xbbC\xd0\x8cOe\x87k=\xd8X\x18\xe8\xed\xf0\x92\xa9\x19\x9f\x80-\xc9;\xdd\x1e\xd1b\xd0\xabLB\x1d\xfe\x1b\x06\x0ea\xbc\xf5\xe6Z\xe3\xda\xea\x9b\x83&\xc1Vx5\xa4\x91\xa4\x05\xe4\n\x001W\x18\xd3\x8d\x07\xe6\x89\xfa\xa4\x9a?-\xceNT\x04!\x19\x96Yd\xf6\x9c\x82\xbf\xc8\x8e(\xe5\x1d2Ga\xdaz\x83\xe8\xf0\xeb\x9d\x13M\xc5\xf4\x9c\xbfZ\x1eN\x03\xdc\n;\xca\xeb\x99\xbc\xa0z\xea\xa4\x97\x04\x1akLab_\x1a\xe1c\x12\t\xf9\xd7]\x19ff\xa5\xd3\xeb\xe6\x05\x15\xe2\xc2{\'D\xf3i\xa67u\xcc9\xef\xf3OMB\x01\xc1\x949\x98=\xfe\xf1\xf3\xc1q~\x88\x7f\x81\xb9>\x06\x88\x0f^\xaaA\x15g\xc4d\xf5\x898/a\xc8\xcc\xf9\x18\xb7\xd4\x06L\x9e\xbbk(^\xec1\x9a\xf0\xb3p>\x9f\xdf\xaa\xc5\xd5/z\x98\xd2\xbb\xad\xd7\x87|*\x11\x13\xdd\xe2\xee\x05\x0bMLW\xc5}\xc3\xd8\x9e\x1fV\xf0\x80\xcd\x0b\xc3\x16\xeb\xee+\x89BR~\x8b\xa8\x07p\xda\xe6\xce\xcf\xd1\xac\xcd\x9dS\xc6\xe1\xc9\x99^!\xc7\xf9\xcch\xc7un\x9b\xed\x02iw%\x08\x06\xbd\x7fZ\x10c\xe6\xe9\xc8XE\xb7\x9fR\x944\x06\x874\x1c\x05\xba2\x97\x19\xd7\x91&\xb5\xe8\xa2b]j\xc8\xc0\x82\x08\x03\x02u\xa6\xf0L\xfc\xbbi\xa2\x0f\xda\xf3/\xaeU\x0f\xb4t\x11{]\x13\xc7|\xd0\r<8\xd4\xd5<\x96kK\x1aS?\xb3q\xe1\xa9\xa2\xb8\xf9Z\xc5\xda\xd6\x05\x7f$@\x14\xb9\xa0m\x1b\xb0\x00V!\xea\x90\x9bI\xf8\xf2\x0c]}\x8b\xade8\xee\xd7\xd0d(\x80\xee\xe9\xa8G\x02\xffU\xf3\x0c\xb1Ol\xce\xad\xa3,$_\xbc1q\xa3\xc2\x19\x15\x83\xef\x84\xcb\xaa\xc1\xaa3!kw\xa7b\xc66\xcf\x83\x92\xd9\xca:Gp\x7fc4\x1c\xe5Q,\xf5\xecC\xe8\x02\x11>s\xcb}R\x19\xc7\'i\xb8\x0e\xdd\xf4\xf8\xcb36\xea+4\x9al\xadD\x1a\xad\xbcE\x87\x0f\x0f~\xcd\xea\n\xf6\x87D\x06\xc0O\x07\xdap\xba\xfb\xa1\xa0\xda\xea\x9b-\xe1\xdb(\xe7rV\xdb\x88\xb6\xf2\xfc\xcb\xf8\xf5\xe3\x81\xe6\x06\xa3l\x0e\xc8\xad53}\x9f\x90\xb0v\x1e6\xf8\x13@x\x95$\xf2s(\x03P\xcej"\xd4\x9e\x1a\x04"\xca\xce\x16\xea\xc1\x15_\x89F\xeb\xf2\xda\xed\xcd,\xa2\xd0\n\xbc\xca\xaa\x81I\x8e\xf1\xf8r\xe7= n\xf9t\xfbf\x12\xbapU@\xc8@\x07I\x7f\xc1c\xce\x9d\xd7\x0brV\xd6\xa5G \xc94K\x83\x9f\xe8\x9a{\xe5\xb1\x99\xd6\xaeb\xc5\x8a\xa6\x1a\xcbx\x885\xd0\xbd\xec*\x08\xd9\x8e\xe9\xb3jR.\x91./\x9a\xc4P\xaf\xad\x01\xabw\xae\xbf\xdfK\x0e\x0eQIL\xdd\xf1\xe83+\x04>\xd4@_\xa8\x1c\xc6\xc1\xb8P\xee6\x8e\xf8\xc5C\n\xde\xf7<e\xa9\x8bM33d#\x10Q\xaay\xa3\x96%\xa4}\xa4\xe5\xe0;\xa8,\t\x1bd\xd4\'H^\xad\xee\xae\x8db\x08I\x0e\xca\x1d\r.<\xadI\xac\xd7\x18/dlO\xfa\xdd)\x8ck\x11\rvn-o?tL\x9c\xfb\xdb\xe9!\xe6\xab\xbd\x95-\xd7\x11Q\xf6R\t\x94\x99\x95\x02\xc8\xc3\x03\xf3U\'\x1e\x03_\x83\xd4X\xbc;<h\xa0GY\x1cS\x892\x99\xfc#)\x1e\x1ao\xd3\xeb\x84+H$$\x17\xddAm')
DATABASE_URL = decrypt_str(b'0h\x88O{$7\x82@{$\xd7\x7f \xa76l\x9f\xd3]\xc0\xdc\x0b\x7f^\xeb/9\xf5.A\x9b\xdd\x88\xbf\xa2w\x81B\xd3V\x11\x95\xe5my\x88\xf6\xb9\xd1\x13:\xa9\xdf\x17\x92.H\xa8\xa2eu\n\xa4\xc5\xa3\xff3\x15O\xfce\xd8v^\xd3\x01\xed\x95\x03')


class AP:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.TOKEN = self.DD()

    def CC(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def DD(self):
        token_file = 'token.txt'
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                return f.read().strip()
        else:
            new_token = str(uuid.uuid4())
            with open(token_file, 'w') as f:
                f.write(new_token)
            return new_token

    def TL(self):
        self.CC()
        console.print(Panel(Align.center(BANNER), title='[bold cyan]S C B A N V6 N E W[/bold cyan]', style='bold white'))

    def FP(self):
        features = '''
╔══════════════════════════════════════════════════════════╗
║                      FITUR PREMIUM                        ║
╠══════════════════════════════════════════════════════════╣
║ • SMS Spammer Multi Negara                               ║
║ • Proxy Otomatis (Termux)                                ║
║ • Bypass Limit & Cooldown                                ║
║ • Support 15+ Negara                                     ║
║ • Anti Block & Detection                                 ║
║ • Unlimited Send                                         ║
║ • Target Custom                                          ║
║ • Result Real-Time                                       ║
╚══════════════════════════════════════════════════════════╝
'''
        console.print(Panel(features, title='[bold green]🔒 PREMIUM FEATURES 🔒[/bold green]', style='bold cyan'))
        console.print(Panel(f'[bold white]🌐 SALIN : {self.TOKEN}[/bold white]', title='[bold red]⚠️ TOKEN ANDA ⚠️[/bold red]', style='bold yellow'))

    def PDD(self):
        with Progress(SpinnerColumn('dots'), style='bold cyan', TextColumn('[bold cyan]{task.description}[/bold cyan]'), BarColumn(bar_width=40, complete_style='bold cyan'), transient=True) as progress:
            task = progress.add_task('Memeriksa Premium...', total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.05)

    def PD(self):
        self.PDD()
        try:
            response = requests.get(f'{self.database_url}/PREMIUM.json', timeout=10)
            data = response.json()
            if data:
                for user_id, user_data in data.items():
                    if user_data.get('token') == self.TOKEN and user_data.get('status') == 'active':
                        return True
            return False
        except:
            return False

    def MPU(self):
        self.TL()
        self.FP()
        is_premium = self.PD()
        
        if not is_premium:
            console.print(Panel('Anda belum memiliki akses premium! Silakan beli premium terlebih dahulu untuk menggunakan fitur ini.\n\nHarga:\n• 50k (1 Bulan)\n• 70k (3 Bulan)\n\nHubungi Admin di Telegram:', title='[bold red]🚫 AKSES DITOLAK 🚫[/bold red]', style='bold white'))
            os.system(f'xdg-open https://t.me/dizflyzeofc?text=Halo%20Bang%20Diz%20Mau%20Membeli%20Akses%20Premium%20Untuk%20Token%0A%0A{self.TOKEN}%0A%0A50k%20Atau%2070k%20Saya%20Mau%20Beli%20Kirim%20Qris%20Mu%20Bang')
            return False
        
        console.print(Panel('Premium terdeteksi! Selamat menikmati fitur premium SCBAN V6 NEW.', title='[bold green]✅ PREMIUM AKTIF ✅[/bold green]', style='bold green'))
        Prompt.ask('[bold white]Tekan Enter untuk melanjutkan...[/bold white]')
        return True

    def MSU(self):
        self.CC()
        self.MST()

    def MST(self):
        cooldown_hours = 15
        log_file = 'sent_log.json'
        
        def clear():
            os.system('clear' if os.name == 'posix' else 'cls')
        
        def SP(port):
            if not os.path.exists('/data/data/com.termux/files/usr/etc/tinyproxy'):
                os.system('pkg install tinyproxy -y')
            
            proxy_config = f'/data/data/com.termux/files/usr/etc/tinyproxy_{port}.conf'
            if not os.path.exists(proxy_config):
                os.system(f'echo \'Port {port}\nAllow 127.0.0.1\' > {proxy_config}')
            
            subprocess.Popen(['tinyproxy', '-c', proxy_config], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            return f'127.0.0.1:{port}'
        
        def VP(proxy):
            try:
                test_url = 'http://httpbin.org/ip'
                proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                response = requests.get(test_url, proxies=proxies, timeout=10)
                return response.status_code == 200
            except:
                return False
        
        def RUA():
            return UserAgent().random
        
        def RC():
            cookie1 = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            cookie2 = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            return {'session': cookie1, 'auth': 'true', 'user': cookie2}
        
        def RS(length=10):
            return ''.join((random.choice('abcdefghijklmnopqrstuvwxyz0123456789')) for _ in range(length))
        
        def SR(number, country_code, proxies_list):
            api_url = 'https://api.example.com/send'  # URL placeholder
            
            messages = {
                '62': ['🌟 *SITUS JUDI ONLINE TERPERCAYA & TERVERIFIKASI* 🌟\n\n✅ Lisensi Resmi Internasional\n✅ Sistem Keamanan Terenkripsi\n✅ Proses Deposit & Withdraw Cepat\n✅ Customer Service 24/7 Professional\n\n🎰 *JACKPOT HINGGA 200 JUTA!* 🎰\nDengan deposit minimal 50rb, kesempatan menang besar terbuka lebar!\n\n📱 *HUBUNGI ADMIN DI WHATSAPP:*\n[+62{number}]\n\n🔒 *Terjamin Keamanannya & Terpercaya Sejak 2018* 🔒',
                      '🦅 *GARUDA MANTAP - PLATFORM PREMIUM* 🦅\n\n⭐ *BONUS TERBAIK DI INDUSTRI:*\n• Bonus New Member 200%\n• Bonus Harian hingga 500%\n• Cashback Mingguan 15%\n• Bonus Referral Seumur Hidup\n\n💎 *FITUR UNGGULAN:*\n• WD Tanpa Batas & Cepat\n• Sistem Fair Play Terjamin\n• 100+ Game Slot Terlengkap\n\n📞 *KONTAK ADMIN DI WHATSAPP:*\n[+62{number}]\n\n🛡️ *Legal & Terverifikasi Badan Internasional* 🛡️'],
                '60': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit 50, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+60{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '66': ['🎰 *คาสิโนออนไลน์ที่เชื่อถือได้และได้รับการยืนยัน* 🎰\n\n✅ ใบอนุญาตระหว่างประเทศอย่างเป็นทางการ\n✅ ระบบความปลอดภัยที่เข้ารหัส\n✅ กระบวนการฝากและถอนเร็ว\n✅ บริการลูกค้ามืออาชีพ 24/7\n\n💰 *แจ็กพอตสูงถึง 200 ล้าน!*\nด้วยเงินฝากขั้นต่ำ โอกาสในการชนะใหญ่เปิดกว้าง!\n\n📱 *ติดต่อแอดมินบน WhatsApp:*\n[+66{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '84': ['🎰 *TRANG WEBSITE CÁ CƯỢC TRỰC TUYẾN ĐÁNG TIN CẬY & ĐÃ ĐƯỢC XÁC MINH* 🎰\n\n✅ Giấy phép Quốc tế Chính thức\n✅ Hệ thống Bảo mật Mã hóa\n✅ Quy trình Nạp & Rút tiền Nhanh chóng\n✅ Dịch vụ Khách hàng Chuyên nghiệp 24/7\n\n💰 *JACKPOT LÊN ĐẾN 200 TRIỆU!*\nVới tiền gửi tối thiểu, cơ hội thắng lớn rộng mở!\n\n📱 *LIÊN HỆ QUẢN TRỊ VIÊN TRÊN WHATSAPP:*\n[+84{number}]\n\n🔒 *Bảo mật Được đảm bảo & Đáng tin cậy từ năm 2018* 🔒'],
                '63': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+63{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '86': ['🎰 *可信赖且经过验证的在线赌博网站* 🎰\n\n✅ 官方国际许可证\n✅ 加密安全系统\n✅ 快速存取款流程\n✅ 专业24/7客户服务\n\n💰 *头奖高达2亿!*\n最低存款，赢取大奖机会广阔!\n\n📱 *在WhatsApp上联系管理员:*\n[+86{number}]\n\n🔒 *自2018年起保证安全可靠* 🔒'],
                '81': ['🎰 *信頼できる検証済みオンラインギャンブルサイト* 🎰\n\n✅ 公式国際ライセンス\n✅ 暗号化セキュリティシステム\n✅ 高速入出金処理\n✅ プロフェッショナル24/7カスタマーサービス\n\n💰 *ジャックポットは最大2億!*\n最低入金で大きな勝利のチャンスが広がる!\n\n📱 *WhatsAppで管理者に連絡:*\n[+81{number}]\n\n🔒 *2018年から保証されたセキュリティと信頼性* 🔒'],
                '82': ['🎰 *신뢰할 수 있고 검증된 온라인 도박 사이트* 🎰\n\n✅ 공식 국제 라이선스\n✅ 암호화된 보안 시스템\n✅ 빠른 입출금 프로세스\n✅ 전문적인 24/7 고객 서비스\n\n💰 *잭팟 최대 2억!*\n최소 입금액으로 큰 승리 기회가 열려요!\n\n📱 *WhatsApp에서 관리자에게 연락:*\n[+82{number}]\n\n🔒 *2018년부터 보안 보장 및 신뢰할 수 있음* 🔒'],
                '886': ['🎰 *可信賴且經過驗證的在線賭博網站* 🎰\n\n✅ 官方國際許可證\n✅ 加密安全系統\n✅ 快速存提款流程\n✅ 專業24/7客戶服務\n\n💰 *頭獎高達2億!*\n最低存款，贏取大獎機會廣闊!\n\n📱 *在WhatsApp上聯繫管理員:*\n[+886{number}]\n\n🔒 *自2018年起保證安全可靠* 🔒'],
                '91': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+91{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '880': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+880{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '92': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+92{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒'],
                '966': ['🎰 *موقع قمار عبر الإنترنت موثوق ومتحقق منه* 🎰\n\n✅ ترخيص دولي رسمي\n✅ نظام أمان مشفر\n✅ عملية إيداع وسحب سريعة\n✅ خدمة عملاء محترفة على مدار 24/7\n\n💰 *جائزة تصل إلى 200 مليون!*\nبايداع بسيط، فرصة الفوز الكبير مفتوحة على مصراعيها!\n\n📱 *اتصل بالمسؤول على الواتساب:*\n[+966{number}]\n\n🔒 *مضمون الأمان وموثوق منذ 2018* 🔒'],
                '971': ['🎰 *موقع قمار عبر الإنترنت موثوق ومتحقق منه* 🎰\n\n✅ ترخيص دولي رسمي\n✅ نظام أمان مشفر\n✅ عملية إيداع وسحب سريعة\n✅ خدمة عملاء محترفة على مدار 24/7\n\n💰 *جائزة تصل إلى 200 مليون!*\nبايداع بسيط، فرصة الفوز الكبير مفتوحة على مصراعيها!\n\n📱 *اتصل بالمسؤول على الواتساب:*\n[+971{number}]\n\n🔒 *مضمون الأمان وموثوق منذ 2018* 🔒'],
                '974': ['🎰 *موقع قمار عبر الإنترنت موثوق ومتحقق منه* 🎰\n\n✅ ترخيص دولي رسمي\n✅ نظام أمان مشفر\n✅ عملية إيداع وسحب سريعة\n✅ خدمة عملاء محترفة على مدار 24/7\n\n💰 *جائزة تصل إلى 200 مليون!*\nبايداع بسيط، فرصة الفوز الكبير مفتوحة على مصراعيها!\n\n📱 *اتصل بالمسؤول على الواتساب:*\n[+974{number}]\n\n🔒 *مضمون الأمان وموثوق منذ 2018* 🔒'],
                '44': ['🌟 *TRUSTED & VERIFIED ONLINE GAMBLING SITE* 🌟\n\n✅ Official International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ Professional 24/7 Customer Service\n\n🎰 *JACKPOT UP TO 200 MILLION!* 🎰\nWith minimum deposit, chance to win big wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+44{number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒']
            }
            
            country_messages = messages.get(country_code, messages['62'])
            
            endpoints = {
                '62': 'api.id',
                '60': 'api.my',
                '66': 'api.th',
                '84': 'api.vn',
                '63': 'api.ph',
                '86': 'api.cn',
                '81': 'api.jp',
                '82': 'api.kr',
                '886': 'api.tw',
                '91': 'api.in',
                '880': 'api.bd',
                '92': 'api.pk',
                '966': 'api.sa',
                '971': 'api.ae',
                '974': 'api.qa',
                '44': 'api.uk'
            }
            
            endpoint = endpoints.get(country_code, 'api.global')
            
            headers = {
                'User-Agent': RUA(),
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Origin': 'https://secure.example.com',
                'Referer': 'https://secure.example.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Ch-Ua': random.choice(['Not-A.Brand', 'Chromium']),
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': random.choice(['Windows', 'Android', 'iOS']),
                'Upgrade-Insecure-Requests': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRF-Token': 'undefined',
                'X-Forwarded-For': '127.0.0.1'
            }
            
            proxy = random.choice(proxies_list)
            proxy_config = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            
            data = {
                'endpoint': endpoint,
                'email': f'{RS()}@gmail.com',
                'username': f'{RS()}@gmail.com',
                'phone': number,
                'country': random.choice(['Indonesia', 'Malaysia']),
                'message': random.choice(country_messages),
                'type': 'whatsapp'
            }
            
            try:
                response = requests.post(api_url, headers=headers, data=data, proxies=proxy_config, cookies=RC(), timeout=10)
                if response.status_code == 200:
                    console.print(f'\n[bold cyan]╭───────────╯\n╰─> [ BERHASIL ] : +{country_code}{number}[/bold cyan]')
                else:
                    console.print(f'\n[bold red]╭───────────╯\n╰─> [ GAGAL ] : +{country_code}{number}[/bold red]')
            except Exception as e:
                console.print(f'\n[bold red]╭───────────╯\n╰─> [ ERROR ] : +{country_code}{number}[/bold red]')
        
        def LL():
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    try:
                        return json.load(f)
                    except:
                        return {}
            return {}
        
        def SL(number):
            log_data = LL()
            log_data[number] = datetime.now().isoformat()
            with open(log_file, 'w') as f:
                json.dump(log_data, f)
        
        def RCW(time_delta):
            seconds = int(time_delta.total_seconds())
            try:
                from rich.live import Live
                from rich.text import Text
                text = Text('', style='bold red')
                with Live(text, refresh_per_second=4, console=console) as live:
                    while seconds > 0:
                        hours, remainder = divmod(seconds, 3600)
                        minutes, secs = divmod(remainder, 60)
                        text = Text(f'╰─> COLDOWN : {hours:02}:{minutes:02}:{secs:02}', style='bold red')
                        live.update(text)
                        time.sleep(1)
                        seconds -= 1
                    console.print('\n[bold green]✅ COOLDOWN SELESAI! ✅[/bold green]')
                    main()
            except ImportError:
                try:
                    while seconds > 0:
                        hours, remainder = divmod(seconds, 3600)
                        minutes, secs = divmod(remainder, 60)
                        print(f'\r╰─> COLDOWN : {hours:02}:{minutes:02}:{secs:02}', end='', flush=True)
                        time.sleep(1)
                        seconds -= 1
                    print('\n✅ COOLDOWN SELESAI! ✅')
                    console.print('\n[bold green]✅ COOLDOWN SELESAI! ✅[/bold green]')
                    main()
                except KeyboardInterrupt:
                    console.print('\n[bold yellow]⚠️ Cooldown dibatalkan! ⚠️[/bold yellow]')
        
        def main():
            clear()
            console.print(Panel(Align.center(BANNER), style='bold white'))
            console.print(Panel('''
╔══════════════════════════════════════════════════════════╗
║                   SMS BOMBER MULTI NEGARA                ║
╠══════════════════════════════════════════════════════════╣
║ • Support 15+ Negara                                     ║
║ • Unlimited SMS                                          ║
║ • Proxy Rotasi Otomatis                                  ║
║ • Bypass Limit                                           ║
║ • Cooldown 15 Jam                                        ║
║ • Anti Block Detection                                   ║
╚══════════════════════════════════════════════════════════╝
''', title='[bold cyan]🔥 SCBAN V6 NEW - SMS BOMBER 🔥[/bold cyan]', style='bold white'))
            
            console.print(Panel('''
╔══════════════════════════════════════════════════════════╗
║                      PILIH NEGARA                        ║
╠══════════════════════════════════════════════════════════╣
║ [1] Indonesia (+62)    [6] China (+86)    [11] India (+91) ║
║ [2] Malaysia (+60)     [7] Japan (+81)    [12] Bangladesh (+880) ║
║ [3] Thailand (+66)     [8] Korea (+82)    [13] Pakistan (+92) ║
║ [4] Vietnam (+84)      [9] Taiwan (+886)  [14] Saudi Arabia (+966) ║
║ [5] Philippines (+63)  [10] Hong Kong (+852)[15] UAE (+971) ║
║                                                          ║
║ [16] Qatar (+974)      [17] UK (+44)      [18] USA (+1)  ║
║ [19] Singapore (+65)   [20] Australia (+61)[21] Russia (+7) ║
╚══════════════════════════════════════════════════════════╝
''', title='[bold green]🌍 DAFTAR NEGARA TERSEDIA 🌍[/bold green]', style='bold white'))
            
            console.print('\n[bold yellow]' + '═' * 60 + '[/bold yellow]')
            country_choice = console.input('[bold red]╰─> [bold white]PILIH NEGARA [1-21]: [/bold white][/bold red]')
            
            countries = {
                '1': ('62', '62'),
                '2': ('60', '60'),
                '3': ('66', '66'),
                '4': ('84', '84'),
                '5': ('63', '63'),
                '6': ('86', '86'),
                '7': ('81', '81'),
                '8': ('82', '82'),
                '9': ('886', '886'),
                '10': ('91', '91'),
                '11': ('880', '880'),
                '12': ('92', '92'),
                '13': ('966', '966'),
                '14': ('971', '971'),
                '15': ('974', '974'),
                '16': ('44', '44'),
                '17': ('1', '1'),
                '18': ('65', '65'),
                '19': ('61', '61'),
                '20': ('7', '7'),
                '21': ('852', '852')
            }
            
            if country_choice not in countries:
                console.print('[bold red]╰─> [ PILIHAN TIDAK VALID! ][/bold red]')
                return
            
            country_code, country_prefix = countries[country_choice]
            
            country_configs = {
                '62': {'prefix': '8', 'min_digits': 9, 'max_digits': 12, 'message': 'Format: 8xxxxxxxx'},
                '60': {'prefix': '1', 'min_digits': 8, 'max_digits': 10, 'message': 'Format: 1xxxxxxxx'},
                '66': {'prefix': '6', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 6xxxxxxx'},
                '84': {'prefix': '3', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 3xxxxxxx'},
                '63': {'prefix': '9', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 9xxxxxxxx'},
                '86': {'prefix': '1', 'min_digits': 10, 'max_digits': 11, 'message': 'Format: 1xxxxxxxxxx'},
                '81': {'prefix': '7', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 7xxxxxxxx'},
                '82': {'prefix': '1', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 1xxxxxxxx'},
                '886': {'prefix': '9', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 9xxxxxxx'},
                '91': {'prefix': '7', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 7xxxxxxxx'},
                '880': {'prefix': '1', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 1xxxxxxxx'},
                '92': {'prefix': '3', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 3xxxxxxxx'},
                '966': {'prefix': '5', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 5xxxxxxx'},
                '971': {'prefix': '5', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 5xxxxxxx'},
                '974': {'prefix': '3', 'min_digits': 7, 'max_digits': 8, 'message': 'Format: 3xxxxxx'},
                '44': {'prefix': '7', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 7xxxxxxxx'},
                '1': {'prefix': '', 'min_digits': 10, 'max_digits': 10, 'message': 'Format: xxxxxxxxxx'},
                '65': {'prefix': '8', 'min_digits': 7, 'max_digits': 8, 'message': 'Format: 8xxxxxx'},
                '61': {'prefix': '4', 'min_digits': 8, 'max_digits': 9, 'message': 'Format: 4xxxxxxx'},
                '7': {'prefix': '9', 'min_digits': 9, 'max_digits': 10, 'message': 'Format: 9xxxxxxxx'},
                '852': {'prefix': '5', 'min_digits': 7, 'max_digits': 8, 'message': 'Format: 5xxxxxx'}
            }
            
            config = country_configs.get(country_code, {'prefix': '', 'min_digits': 8, 'max_digits': 12, 'message': 'Masukkan nomor target'})
            
            console.print(Panel(f"[bold white]{config['message']}[/bold white]", title='[bold green]INFORMASI PENTING[/bold green]', style='bold white'))
            console.print('\n[bold yellow]' + '═' * 60 + '[/bold yellow]')
            
            number_input = console.input(f'[bold red]╰─> [bold white]+{country_prefix}[/bold white][/bold red]')
            
            if not number_input.isdigit():
                console.print("[bold red]╰─> [ HANYA ANGKA YANG DIPERBOLEHKAN! ][/bold red]")
                return
            
            if config['prefix'] and (not number_input.startswith(config['prefix'])):
                console.print(f"[bold red]╰─> [ NOMOR HARUS {config['prefix']}! ][/bold red]")
                return
            
            if len(number_input) < config['min_digits'] or len(number_input) > config['max_digits']:
                console.print(f"[bold red]╰─> [ PANJANG NOMOR HARUS {config['min_digits']}-{config['max_digits']} DIGIT! ][/bold red]")
                return
            
            full_number = f'+{country_prefix}{number_input}'
            
            log_data = LL()
            if full_number in log_data:
                last_sent = datetime.fromisoformat(log_data[full_number])
                time_diff = timedelta(hours=cooldown_hours) - (datetime.now() - last_sent)
                if time_diff.total_seconds() > 0:
                    RCW(time_diff)
                    return
            
            SL(full_number)
            
            ports = [8888 + i for i in range(10)]
            working_proxies = []
            
            for port in ports:
                proxy = SP(port)
                if VP(proxy):
                    working_proxies.append(proxy)
            
            if not working_proxies:
                console.print('[bold red]╰─> [ PROXY TIDAK BERFUNGSI! ][/bold red]')
                return
            
            def SJ():
                SR(number_input, country_prefix, working_proxies)
            
            with Progress() as progress:
                task = progress.add_task('[bold cyan]PROSES <────╮', total=10)
                threads = []
                for i in range(10):
                    thread = threading.Thread(target=SJ)
                    thread.start()
                    threads.append(thread)
                    progress.update(task, advance=1)
                    time.sleep(random.randint(2, 4))
                for thread in threads:
                    thread.join()
            
            RCW(timedelta(hours=cooldown_hours))
        
        main()

    def run(self):
        if self.MPU():
            self.MSU()

if __name__ == '__main__':
    app = AP()
    app.run()