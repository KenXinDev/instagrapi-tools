import instagrapi.exceptions
import os, re, json, time, sys, instagrapi, random, rich, requests, datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from rich import print as KenXinDev
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
import assets.config as config

cl = Client()
loop, success, failed = 0, [], []
file_session = "session/session.json"
dayNow = datetime.now().strftime("%d-%B-%Y")

random_sleep = []

def generate_randomSleep(count: int=8, min_val: int=1, max_val: int=20):
    global random_sleep
    random_sleep = [random.randint(min_val, max_val) for _ in range(count)]

def create_folder():
    os.makedirs("session", exist_ok=True)
    os.makedirs("temporary", exist_ok=True)

def error(message: str):
    KenXinDev(f"[bold white]Error : [bold red]{message}[/]")

def KenXinInput():
    return Console().input("[bold bright_black]   ╰─> ")

class InstagramManager:
    def __init__(self):
        self.cl = cl
    
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
    
    def banners(self):
        self.clear()
        KenXinDev(Panel(config.BANNER, width=80, style='bold bright_black'))
    
    def safe_delay(self, seconds: int = 1):
        time.sleep(seconds)
    
    def login(self):
        try:
            payloads = {
                "username": config.USERNAME,
                "password": config.PASSWORD,
                "relogin": True
            }
            self.cl.login(**payloads)
            self.cl.dump_settings(file_session)
            return True
        except (instagrapi.exceptions, Exception) as e:
            error(str(e).title())
            time.sleep(3)
            return False
    
    def load_sesi(self):
        try:
            if os.path.exists(file_session):
                with open(file_session, 'r') as f:
                    settings = json.load(f)
                self.cl.set_settings(settings)
                try:
                    self.cl.get_timeline_feed()
                    return True
                except LoginRequired:
                    return self.login()
            else:
                return self.login()
        except (instagrapi.exceptions.ClientBadRequestError, Exception) as e:
            error(str(e).title())
            time.sleep(3)
            return False
        
    def logo(self):
        self.account_info = self.cl.account_info().model_dump()
        info = f"[bold white][+] Username : [bold red]{self.account_info.get('pk')}@{self.account_info.get('username')}[/bold red]\n[+] Phone : [bold red]{(self.account_info.get('phone_number') if self.account_info.get('phone_number') else 'Tidak ada')}[/bold red]\n[+] Email : [bold red]{(self.account_info.get('email') if self.account_info.get('email') else 'Tidak ada')}[/bold red]"
        KenXinDev(Panel(info,width=80, style='bold bright_black', title='[bold bright_black] >> [Account Info] << [/]'))
        KenXinDev(Panel("""[bold white][01] Auto Upload Postingan (Album, Single)
[02] Auto Upload Reels (Masih dalam tahap maintance library)
[03] Scrapper Username Tertarget
[04] Scrapper Information Reels Target (tunggal, massal)
[05] Auto Add Follow Request
[06] Auto Unfollow (all, non follback)
[00] Exit Tools[/]""",style='bold bright_black', width=80, title='[bold bright_black]>> [Menu Utama] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
    def menu_utama(self):
        if not self.load_sesi():
            self.banners()
            error("Tidak dapat melanjutkan keluar....")
            time.sleep(3)
            return
        while True:
            self.banners()
            self.logo()
            c = KenXinInput()
            if c in('1', '01'):
                self.uploadPostinganHandler()
            elif c in('2', '02'):
                # self.uploadReelsHandler()
                error("Maintance Library!!!")
                time.sleep(3)
            elif c in('3', '03'):
                self.dumpUserHandler()
            elif c in('4', '04'):
                self.reelsInfoHandler()
            elif c in('5', '05'):
                self.followHandler()
            elif c in('6', '06'):
                self.unfollowHandler()
            else:
                error("Wrong Input!!")
                time.sleep(3)

    def reelsInfoHandler(self):
        KenXinDev(Panel("[bold white][01] Scrapper Reels Tunggal\n[02] Scrapper Reels Massal\n[00] Kembali ke menu[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Reels Info Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        opsi = KenXinInput()
        if opsi in('1', '01'):
            self.reelsInfoTunggal()
        elif opsi in('2', '02'):
            self.reelsInfoMassal()
        elif opsi in('0', '00'):
            return
        else:
            error("Wrong input")
            time.sleep(3)
            return
        
    def reelsInfoMassal(self):
        filename = f"temporary/reels-{dayNow}.txt"
        KenXinDev(Panel("[bold white]Masukan path file reels url target, pastikan target bersifat publik untuk bisa memuat informasi reels[/]",
                        style='bold bright_black', width=80, title='[bold bright_black]>> [Reels Massal Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        file_path = KenXinInput()
        if not os.path.exists(file_path):
            error(f"{file_path} Tidak ditemukan!!")
            time.sleep(3)
            return

        KenXinDev(Panel("[bold white]Apakah anda ingin menyimpan log, ketik ya atau tidak di keyboardmu[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Simpan Log Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        valid_cmd = ('ya', 'tidak')
        log_simpan = KenXinInput().lower()
        if log_simpan not in valid_cmd:
            error("Input tidak valid! Masukkan hanya 'ya' atau 'tidak'")
            time.sleep(3)
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            links = f.read().splitlines()

        for link in links:
            data = self.scrapperReels(link)
            if not data:
                continue
            KenXinDev(f"""
[bold white][+] Reels Information:
[+] Author : [bold green]{data.get('author')}[/bold green]
[+] Media Code : [bold green]{data.get('code')}[/bold green]
[+] Link Reels : [bold green]{data.get('link')}[/bold green]
[+] Video Url : [bold green]{data.get('video_url')}[/bold green]
[+] Caption : [bold green]{data.get('caption')}[/bold green][/]""")

            if log_simpan == 'ya':
                with open(filename, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"""[+] Reels Information:
[+] Author : {data.get('author')}
[+] Media Code : {data.get('code')}
[+] Link Reels : {data.get('link')}
[+] Video Url : {data.get('video_url')}
[+] Caption : {data.get('caption')}
==========================================\n""")

            time.sleep(random.uniform(2, 5))  # delay acak agar tidak dianggap bot

        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

    def reelsInfoTunggal(self):
        filename = f"temporary/reels-{dayNow}.txt"
        KenXinDev(Panel("[bold white]Masukan link reels url target, pastikan target bersifat publik untuk bisa memuat informasi reels[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Reels Tunggal Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        link_target = KenXinInput()
        data = self.scrapperReels(link_target)
        KenXinDev(f"""
[bold white][+] Reels Information:
[+] Author : [bold green]{data.get('author')}[/bold green]
[+] Media Code : [bold green]{data.get('code')}[/bold green]
[+] Link Reels : [bold green]{data.get('link')}[/bold green]
[+] Video Url : [bold green]{data.get('video_url')}[/bold green]
[+] Caption : [bold green]{data.get('caption')}[/bold green][/]""")
        KenXinDev(Panel("[bold white]Apakah anda ingin menyimpan log, ketik ya atau tidak di keyboardmu[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Simpan Log Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        valid_cmd = ('ya', 'tidak')
        log_simpan = KenXinInput().lower()
        if log_simpan not in valid_cmd:
            error("Input tidak valid! Masukkan hanya 'ya' atau 'tidak'")
            time.sleep(3)
        else:
            if log_simpan == 'ya':
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(f"""[+] Reels Information:
[+] Author : {data.get('author')}
[+] Media Code : {data.get('code')}
[+] Link Reels : {data.get('link')}
[+] Video Url : {data.get('video_url')}
[+] Caption : {data.get('caption')}
==========================================\n""")
                KenXinDev(Panel(f"[bold white]Log berhasil tersimpan : [bold green]{filename}[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Simpan Log Success] <<'))
        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

    def scrapperReels(self, url: str):
        try:
            media_id = self.cl.media_pk_from_url(url)
            if not media_id:
                error("Media id tidak ditemukan!!")
                time.sleep(3)
                return
            response = self.cl.media_info(media_id).model_dump()
            media_code = response.get('code')
            video_url = response.get('video_url')
            caption_text = response.get('caption_text')
            author_media = response.get('user', {}).get('username')
            return {
                'author': author_media,
                'code': media_code,
                'link': url,
                'video_url': video_url,
                'caption': caption_text
            }
        except Exception as e:
            error(str(e).title())
            time.sleep(3)
            return

    def unfollowHandler(self):
        KenXinDev(Panel("[bold white][01] Unfollow all\n[02] Unfollow non follback\n[00] Kembali ke menu[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Unfollow Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        opsi = KenXinInput()
        if opsi in('1', '01'):
            self.unfollowAll()
        elif opsi in('2', '02'):
            self.unfollowNonFoll()
        elif opsi in('0', '00'):
            return
        else:
            error("Wrong input")
            time.sleep(3)
            return
        
    def unfollowAll(self):
        KenXinDev(Panel(
            "[bold white]Proses Unfollow all sedang berjalan, tolong tunggu sampai proses selesai[/]", 
            style='bold bright_black', 
            width=80, 
            title='[bold bright_black]>> [Unfollow All] <<')
        )

        following = self.cl.user_following(self.cl.user_id)
        KenXinDev(f"\n[bold white][+] Total following : [bold red]{len(following)}[/]")
        for userid in following:
            try:
                username = following[userid].username
                response = self.cl.user_unfollow(userid)
                if response is True:
                    KenXinDev(f"[bold green][✓] Berhasil unfollow: [bold white]{username}[/]")
                else:
                    KenXinDev(f"[bold yellow][!] Gagal unfollow: [bold white]{username}[/]")
            except Exception as e:
                KenXinDev(f"[bold red][x] Error unfollow user ID {userid}: {e}")
            time.sleep(random.choice(random_sleep))
        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()
    
    def unfollowNonFoll(self):
        KenXinDev(Panel(
            "[bold white]Proses Unfollow non follback sedang berjalan, tolong tunggu sampai proses selesai[/]", 
            style='bold bright_black', 
            width=80, 
            title='[bold bright_black]>> [Unfollow Non Follback] <<')
        )

        try:
            user_id = self.cl.user_id
            following = self.cl.user_following(user_id)
            followers = self.cl.user_followers(user_id)
            
            KenXinDev(f"\n[bold white][+] Total following : [bold red]{len(following)}[/]")
            KenXinDev(f"[bold white][+] Total followers : [bold green]{len(followers)}[/]\n")
            
            non_follback = [uid for uid in following if uid not in followers]

            for uid in non_follback:
                try:
                    username = following[uid].username
                    response = self.cl.user_unfollow(uid)
                    if response:
                        KenXinDev(f"[bold green][✓] Berhasil unfollow (non-follback): [bold white]{username}[/]")
                    else:
                        KenXinDev(f"[bold yellow][!] Gagal unfollow: [bold white]{username}[/]")
                except Exception as e:
                    KenXinDev(f"[bold red][x] Error unfollow user ID {uid}: {e}")
                time.sleep(random.uniform(3, 7))  # delay random biar aman
        except Exception as e:
            KenXinDev(f"[bold red][x] Gagal mengambil data followers/following: {e}")

        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

    def followHandler(self):
        KenXinDev(Panel("[bold white]Masukan file path username dan userid yang sudah di scrap[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Follow Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        try:
            file_path = KenXinInput()
            if not os.path.exists(file_path):
                error(f"{file_path} Tidak ditemukan!!")
                time.sleep(3)
                return
            with open(file_path, 'r') as r:
                data = r.read().splitlines()
            for i in data:
                userid = i.split("<=>")[0]
                username = i.split("<=>")[1]
                self.gasFollow(userid, username, len(data))
        except Exception as e:
            error(str(e).title())
            time.sleep(3)
            return

    def gasFollow(self, userid: int, username: str, total: int, max_retrys: int = 3):
        global loop, success, failed
        KenXinDev(f"[bold white]# Follow {loop}/{total} success: [bold green]{len(success)}[/bold green] failed: [bold red]{len(failed)}[/bold red][/]", end="\r")
        retrys = 0
        while retrys < max_retrys:
            try:
                response = self.cl.user_follow(userid)
                if response is True:
                    success.append(userid)
                    KenXinDev(Panel(Panel(f"[bold white][+] Berhasil follow ke userid\n[+] Username : [bold green]{username}[/bold green]\n[+] Userid : [bold green]{userid}[/bold green]\n[+] Response : [bold green]{response}[/]", style='bold green'), width=80, style='bold bright_black', title='[bold green]Success[/bold green]'))
                    time.sleep(random.choice(random_sleep))
                    break
                else:
                    retrys += 1
            except Exception as e:
                retrys += 1
                error(f"Gagal follow {username} - Percobaan ke-{retrys}: {e}")
                time.sleep(random.choice(random_sleep))
        if retrys >= max_retrys:
            failed.append(userid)
        loop +=1

    
    def dumpUserHandler(self):
        KenXinDev(Panel("[bold white]Masukan cookies instagram anda, gunakan akun tumbal untuk menghindari resiko banned[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Login Cookie] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        dumpHandler = DumperHelper()
        try:
            cookie = KenXinInput()
            username = dumpHandler.check_cookies(cookie)
            if not username:
                error("Invalid Cookie!!")
                time.sleep(3)
                return
            KenXinDev(f"\n[bold white]Berhasil login sebagai : {username}")
            # config.COOKIES.update({"cookie": cookie})
            KenXinDev(Panel("[bold white]Masukan username target yang akan di dump, pastikan target besifat publik dan tidak centang biru[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Dump Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            target_username = KenXinInput()
            userid_scr = dumpHandler.convertId(target_username)
            if not userid_scr:
                error("Username tidak ditemukan!!")
                time.sleep(3)
                return
            typeDump_valid = ('followers', 'following')
            KenXinDev(Panel("[bold white]Masukan type dump ketik di keyboarmu [bold red]followers[/bold red]/[bold red]following[/bold red][/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Type Dump] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            dumpType = KenXinInput().strip().lower()
            if dumpType not in typeDump_valid:
                error("Type dump tidak valid!!")
                time.sleep(3)
            filename = dumpHandler.dump_unlimited(userid_scr, cookie, dumpType, '')
            KenXinDev(Panel(f"[bold white]Dump telah selesai dan user tersimpan di : [bold red]{filename}[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Success Dump] <<'))
        except (Exception) as e:
            error(str(e).title())
            time.sleep(3)
        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

    def uploadReelsHandler(self):
        KenXinDev(Panel("[bold white]Masukan path video reels yang akan di upload\nFormat yang didukung:\n- Video: MP4/MOV[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Reels Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        try:
            video_path = KenXinInput()
            if not os.path.isfile(video_path):
                error(f"{video_path} tidak ditemukan!!")
                time.sleep(3)
                return
            valid_ext = (".mp4", ".mov")
            if not video_path.lower().endswith(valid_ext):
                error("Video harus berformat MP4 atau MOV!!")
                time.sleep(3)
                return
            KenXinDev(Panel("[bold white]Masukan caption untuk reels[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Caption Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            caption = KenXinInput().strip()
            KenXinDev(Panel("[bold white]Masukan hashtags gunakan tanda koma sebagai pemisah[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Hashtags Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            hashtags_input = KenXinInput().strip()
            hashtags = []
            if hashtags_input:
                hashtags = [
                    f"#{tag.strip().replace('#', '')}" 
                    for tag in hashtags_input.split(',') 
                    if tag.strip()
                ]
                # Remove duplicates
                hashtags = list(dict.fromkeys(hashtags))
                # Limit to 30 hashtags
                hashtags = hashtags[:30]
            
            # Combine caption and hashtags
            final_caption = caption
            if hashtags:
                final_caption += "\n\n" + " ".join(hashtags)
            media = self.cl.video_upload(path=video_path, caption=caption)
            link_reels = "https://www.instagram.com/reel/"+media.code
            KenXinDev(Panel(f"[bold white]Berhasil mengupload media : [bold green]{link_reels}[/bold green] Link Postingan[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Reels Info] <<'))
        except Exception as e:
            error(str(e).title())
        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

    def uploadPostinganHandler(self):
        KenXinDev(Panel("[bold white]Masukan path folder untuk upload ke postingan single atau album\nFormat yang didukung:\n- Foto: JPG/JPEG/PNG\n- Video: MP4/MOV\n- Maksimal 10 media per postingan[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Postingan Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
        try:
            folder_path = KenXinInput()
            # Jika folder tidak ada
            if not os.path.isdir(folder_path):
                error(f"{folder_path} tidak ditemukan!!")
                time.sleep(3)
                return
            # Get valid media ekstension
            valid_ext = ('.jpeg', '.jpg', '.png', '.mp4', '.mov')
            media_files = []
            for f in os.listdir(folder_path):
                if f.lower().endswith(valid_ext):
                    media_files.append(os.path.join(folder_path, f))
            # Jika tidak ada media
            if not media_files:
                error("Media files tidak ditemukan!!")
                time.sleep(3)
                return
            media_files = sorted(media_files)
            KenXinDev(f"\n[bold white] Media file ditemukan : [bold green]{len(media_files)}[/bold green] Media[/]")
            KenXinDev(Panel(f"[bold green]{media_files[:10]}[/bold green]", width=80, style='bold bright_black', title='[bold bright_black]>> [Media Info] <<'))
            KenXinDev(Panel("[bold white]Masukan caption untuk postingan[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Caption Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            caption = KenXinInput().strip()
            KenXinDev(Panel("[bold white]Masukan hashtags gunakan tanda koma sebagai pemisah[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Hashtags Handler] <<', subtitle='[bold bright_black]╭──────', subtitle_align='left'))
            hashtags_input = KenXinInput().strip()
            hashtags = []
            if hashtags_input:
                hashtags = [
                    f"#{tag.strip().replace('#', '')}" 
                    for tag in hashtags_input.split(',') 
                    if tag.strip()
                ]
                # Remove duplicates
                hashtags = list(dict.fromkeys(hashtags))
                # Limit to 30 hashtags
                hashtags = hashtags[:30]
            
            # Combine caption and hashtags
            final_caption = caption
            if hashtags:
                final_caption += "\n\n" + " ".join(hashtags)
            paths = media_files[:10]
            # Check media type
            is_video = [f.lower().endswith(('.mp4', '.mov')) for f in paths]
            if sum(is_video) > 0 and len(paths) > 1:
                error("Tidak bisa mix video dengan foto dalam 1 postingan!")
                time.sleep(3)
                return
            if all(is_video):
                if len(paths) > 1:
                    error("Instagram hanya mengizinkan 1 video per postingan!")
                    time.sleep(3)
                    return
                # Upload single video
                media = self.cl.video_upload(paths[0], caption=final_caption)
            else:
                # Upload album
                media = self.cl.album_upload(
                    paths=paths,
                    caption=final_caption
                )
            KenXinDev(Panel(f"[bold white]Berhasil mengupload media : [bold green]https://www.instagram.com/p/{media.code}[/bold green] Link Postingan[/]",style='bold bright_black', width=80, title='[bold bright_black]>> [Postingan Info] <<'))
        except Exception as e:
            error(str(e).title())
        KenXinDev("\n[bold white]Tekan enter untuk kembali[/]")
        input()

class DumperHelper:
    def __init__(self):
        self.useragent = "Mozilla/5.0 (Linux; Android 6.0; E5633 Build/30.2.B.1.21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36 Instagram 37.0.0.21.97 Android (23/6.0; 480dpi; 1080x1776; Sony; E5633; E5633; mt6795; uk_UA; 98288242)"
    
    def convertId(self, username: str):
        try:
            with requests.Session() as r:
                r.headers.update({
                    'user-agent': self.useragent
                })
                self.response = r.get("https://i.instagram.com/api/v1/users/web_profile_info/?username={}".format(username)).json()
                return self.response['data']['user']['id']
        except (requests.exceptions.JSONDecodeError, Exception) as e:
            error(str(e).title())
            time.sleep(3)
            return None
    
    def dump_unlimited(self, uid: int, cookies: str, type: str, cursor: str = ''):
        while True:
            try:
                with requests.Session() as curl:
                    filename = f'temporary/{uid}_{type}.txt'
                    curl.headers.update({
                        'user-agent': self.useragent,
                        'x-csrftoken': re.search('csrftoken=(.*?);', str(cookies)).group(1)
                    })
                    params = {
                        'count': 100,
                        'max_id': cursor
                    }
                    url = 'https://i.instagram.com/api/v1/friendships/{}/{}/'.format(uid, type)
                    response = curl.get(url, params=params, cookies={'cookie': cookies}).json()
                    if 'users' not in response:
                        error("Gagal mengambil data, mungkin cookies kadaluarsa atau akun dibatasi.")
                        break
                    with open(filename, 'a', encoding='utf-8') as f:
                        for i in response['users']:
                            f.write("{}<=>{}\n".format(i["id"], i["username"]))
                    KenXinDev(f"[bold white]# Berhasil mengumpulkan username : [bold green]{len(open(filename, 'r').read().splitlines())}[/]", end="\r")
                    if 'next_max_id' in str(response):
                        cursor = response['next_max_id']
                    else:
                        break
            except KeyboardInterrupt:
                error("KeyboardInterrupt!!")
                time.sleep(3)
                break
            except (requests.exceptions.JSONDecodeError, Exception) as e:
                error(str(e).title())
                time.sleep(3)
                break
        return filename
    
    def check_cookies(self, cookie: str):
        try:
            with requests.Session() as curl:
                curl.headers.update({
                    'user-agent': self.useragent,
                    'x-csrftoken': re.search('csrftoken=(.*?);', str(cookie)).group(1)
                })
                userid = re.search('ds_user_id=(.*?);', str(cookie)).group(1)
                response = curl.get("https://i.instagram.com/api/v1/users/{}/info/".format(userid), cookies={'cookie': cookie}).json()
                return response['user']['username']
        except (requests.exceptions.JSONDecodeError, Exception) as e:
            error(str(e).title())
            time.sleep(3)
            return None

if __name__ == "__main__":
    insta = InstagramManager()
    generate_randomSleep()
    create_folder()
    insta.menu_utama()
