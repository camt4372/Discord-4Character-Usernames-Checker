import requests
import random
import string
import time
import threading
from datetime import datetime
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== 프록시 설정 ==========
PROXY_USERNAME = "프록시 이름 넣는곳"  # ← ThorData 사용자명 입력
PROXY_PASSWORD = "프록시 비번 넣는곳"  # ← ThorData 비밀번호 입력
PROXY_SERVER = "프록시 서버:포트 넣는곳" # ← ThorData 서버:포트 입력

def get_thordata_proxy():
    session_id = random.randint(100000, 999999)
    proxy_url = (
        f"http://{urllib.parse.quote(PROXY_USERNAME)}:"
        f"{urllib.parse.quote(PROXY_PASSWORD)}@"
        f"{PROXY_SERVER}?session_id={session_id}"
    )
    return {
        "http": proxy_url,
        "https": proxy_url
    }

API_URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
ALLOWED_CHARS = string.ascii_lowercase + string.digits + "_."

total_checked = 0
available_count = 0
taken_count = 0
error_count = 0

lock = threading.Lock()
tried_lock = threading.Lock()
running = True

# 이미 확인한 사용자명 저장 (중복 확인 방지)
tried_usernames = set()

def load_tried_usernames():
    global tried_usernames
    for filename in ("available.txt", "taken.txt"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    # 형식: [타임스탬프] 사용자명
                    parts = line.strip().split("] ")
                    if len(parts) == 2:
                        tried_usernames.add(parts[1])
        except FileNotFoundError:
            continue
    if tried_usernames:
        print(
            f"📂 이전에 확인한 사용자명 "
            f"{len(tried_usernames)}개 불러옴 (중복 확인 제외)"
        )

def generate_username(length=4):
    while True:
        username = ''.join(
            random.choice(ALLOWED_CHARS)
            for _ in range(length)
        )
        if ".." in username:
            continue
        # 이미 확인한 사용자명이면 다시 생성
        with tried_lock:
            if username in tried_usernames:
                continue
            tried_usernames.add(username)
        return username

def save_available(username):
    with open("available.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {username}\n")

def save_taken(username):
    with open("taken.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {username}\n")

def check_username(username, proxy_dict):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 15; Pixel 9) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Mobile Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/register",
        "X-Discord-Locale": "ko",
        "X-Discord-Timezone": "Asia/Seoul"
    }

    payload = {
        "username": username
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            proxies=proxy_dict,
            timeout=10,
            verify=False
        )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return False, "error"

            if "taken" not in data:
                return False, "error"

            if data["taken"] is True:
                return False, "taken"

            if data["taken"] is False:
                return True, "available"

            return False, "error"

        elif response.status_code == 429:
            return False, "rate_limit"

        else:
            return False, "error"

    except requests.exceptions.Timeout:
        return False, "timeout"

    except requests.exceptions.ProxyError:
        return False, "proxy_error"

    except requests.exceptions.RequestException:
        return False, "exception"

    except Exception:
        return False, "exception"

def worker(thread_id):
    global total_checked
    global available_count
    global taken_count
    global error_count
    global running

    current_proxy = get_thordata_proxy()
    request_count = 0

    while running:
        try:
            username = generate_username(4)

            request_count += 1

            if request_count % 3 == 0:
                current_proxy = get_thordata_proxy()

            is_available, result = check_username(
                username,
                current_proxy
            )

            retry_count = 0

            while result in (
                "exception",
                "timeout",
                "proxy_error"
            ) and retry_count < 3:
                retry_count += 1
                current_proxy = get_thordata_proxy()
                time.sleep(0.3)

                is_available, result = check_username(
                    username,
                    current_proxy
                )

            if result == "rate_limit":
                current_proxy = get_thordata_proxy()
                time.sleep(1)
                continue

            with lock:
                total_checked += 1
                current_num = total_checked

                if result == "available":
                    available_count += 1
                    save_available(username)
                    print(
                        f"[{current_num:5d}] "
                        f"✅ 사용가능 {username}"
                    )

                elif result == "taken":
                    taken_count += 1
                    save_taken(username)
                    print(
                        f"[{current_num:5d}] "
                        f"❌ 사용중 {username}"
                    )

                else:
                    error_count += 1
                    print(
                        f"[{current_num:5d}] "
                        f"⚠️ 오류 {username} ({result})"
                    )

        except Exception as e:
            with lock:
                error_count += 1

            print(
                f"\n⚠️ Worker {thread_id} 오류: {repr(e)}"
            )

def monitor():
    global running

    while running:
        time.sleep(2)

        with lock:
            if total_checked > 0:
                print(
                    "\n"
                    f"📊 확인: {total_checked}개 | "
                    f"✅ 사용가능: {available_count}개 | "
                    f"❌ 사용중: {taken_count}개 | "
                    f"⚠️ 오류: {error_count}개"
                )

def scan_multi_thread(num_threads=3):
    global running

    print("=" * 60)
    print("디스코드 4자 사용자명 체커기 | 코다 제작")
    print("=" * 60)
    print(f"스레드 : {num_threads}개")
    print("길이   : 4자리")
    print("결과   : available.txt / taken.txt")
    print("=" * 60)

    load_tried_usernames()

    print("=" * 60)
    print()

    threads = []

    for i in range(num_threads):
        t = threading.Thread(
            target=worker,
            args=(i + 1,),
            daemon=True
        )
        t.start()
        threads.append(t)

    monitor_thread = threading.Thread(
        target=monitor,
        daemon=True
    )
    monitor_thread.start()

    try:
        while running:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\n⏹️ 중지 중...")
        running = False

    for t in threads:
        t.join(timeout=2)

    print()
    print("=" * 60)
    print("최종 결과")
    print("=" * 60)
    print(f"총 확인       : {total_checked}")
    print(f"✅ 사용 가능   : {available_count}")
    print(f"❌ 사용 중     : {taken_count}")
    print(f"⚠️ 오류        : {error_count}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        num_threads = int(
            input("스레드 개수 (권장: 3~5): ")
        )

        if num_threads < 1:
            num_threads = 3

    except ValueError:
        num_threads = 3

    scan_multi_thread(num_threads)