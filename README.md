# Discord 4자리 사용자명 체커

Discord의 **4자리 사용자명(Username)**을 무작위로 생성하고 사용 가능 여부를 확인하는 Python 기반 **사용자명 체커**입니다.

생성된 사용자명을 Discord Username 관련 API에 요청하여 결과를 확인하고, 사용 가능한 사용자명과 이미 사용 중인 사용자명을 각각 파일에 저장합니다.

> ⚠️ **본 프로그램은 ThorData에서 구매한 프록시를 사용하는 것을 기준으로 제작되었습니다.**
>
> 다른 프록시 제공업체의 프록시는 지원하지 않으며, 정상적인 동작을 보장하지 않습니다.

---

## ✨ 주요 기능

* Discord 4자리 사용자명 자동 생성
* 영문 소문자, 숫자, `_`, `.` 조합 지원
* 잘못된 형식의 일부 사용자명 자동 제외
* 사용자명 사용 가능 여부 체커
* **ThorData 프록시 사용**
* Proxy Session ID 자동 생성
* 멀티스레딩 지원
* Rate Limit 감지
* 네트워크 오류 발생 시 프록시 변경 및 재시도
* 사용 가능한 사용자명 자동 저장
* 이미 사용 중인 사용자명 자동 저장
* 실시간 체커 통계 출력
* 체커 종료 후 최종 결과 출력

---

## 🖥️ 필수 환경

다음 환경이 필요합니다.

* Python **3.8 이상**
* 인터넷 연결
* **ThorData에서 구매한 프록시**
* ThorData 프록시 사용자명
* ThorData 프록시 비밀번호
* ThorData 프록시 서버 및 포트

### 필요한 Python 라이브러리

```bash
pip install requests urllib3
```

---

## 📁 프로젝트 구조

```text
Discord-4Character-Usernames-Checker/
│
├── main.py
├── available.txt
├── taken.txt
└── README.md
```

| 파일              | 설명                  |
| --------------- | ------------------- |
| `main.py`       | Discord 4자리 사용자명 체커 |
| `available.txt` | 사용 가능한 사용자명 저장      |
| `taken.txt`     | 이미 사용 중인 사용자명 저장    |
| `README.md`     | 프로젝트 설명 및 사용 방법     |

`available.txt`와 `taken.txt`는 프로그램 실행 후 자동으로 생성됩니다.

---

## 🌐 ThorData 프록시 설정

본 프로그램은 **ThorData에서 구매한 프록시를 기준으로 제작되었습니다.**

[ThorData 공식 홈페이지](https://thordata.com/)

`main.py` 상단의 프록시 설정 부분을 자신의 ThorData 프록시 정보로 변경해야 합니다.

```python
PROXY_USERNAME = "프록시 이름 넣는곳"
PROXY_PASSWORD = "프록시 비번 넣는곳"
PROXY_SERVER = "프록시 서버:포트 넣는곳"
```

예시:

```python
PROXY_USERNAME = "your_username"
PROXY_PASSWORD = "your_password"
PROXY_SERVER = "proxy.example.com:12345"
```

### ⚠️ 중요

**ThorData에서 구매한 프록시를 사용하는 것을 전제로 합니다.**

현재 프로그램의 Proxy Session 생성 및 관리 방식은 ThorData 프록시 사용을 기준으로 작성되어 있습니다.

다른 프록시 제공업체의 프록시를 사용하는 경우 정상적인 동작을 보장하지 않습니다.

---

## 🔑 프록시 인증 정보

실제 프록시 계정 정보를 GitHub 등의 공개 저장소에 업로드하지 마십시오.

예를 들어 다음과 같이 실제 인증 정보를 코드에 직접 입력한 상태로 공개 저장소에 업로드하면 프록시 계정 정보가 노출될 수 있습니다.

```python
PROXY_USERNAME = "실제_사용자명"
PROXY_PASSWORD = "실제_비밀번호"
```

GitHub에 소스 코드를 업로드하기 전 실제 인증 정보를 제거하거나 환경변수 등의 별도 방식으로 관리하는 것을 권장합니다.

---

## 🚀 설치 및 실행

### 1. 저장소 다운로드

Git을 사용하는 경우:

```bash
git clone https://github.com/camt4372/Discord-4Character-Usernames-Checker.git
```

프로젝트 폴더로 이동합니다.

```bash
cd Discord-4Character-Usernames-Checker
```

### 2. 필요한 라이브러리 설치

```bash
pip install requests urllib3
```

### 3. ThorData 프록시 정보 입력

`main.py`에서 다음 항목을 자신의 프록시 정보로 변경합니다.

```python
PROXY_USERNAME = "프록시 이름 넣는곳"
PROXY_PASSWORD = "프록시 비번 넣는곳"
PROXY_SERVER = "프록시 서버:포트 넣는곳"
```

### 4. 체커 실행

```bash
python main.py
```

---

## 🧵 스레드 개수 설정

체커를 실행하면 다음과 같은 입력창이 표시됩니다.

```text
스레드 개수 (권장 : 3-5):
```

예:

```text
스레드 개수 (권장 : 3-5): 3
```

입력한 개수만큼 Worker Thread가 생성되어 사용자명 체커를 수행합니다.

### 권장 스레드

```text
3 ~ 5개
```

스레드 개수가 지나치게 많아질 경우 요청량이 증가하여 **Rate Limit 또는 기타 제한이 발생할 가능성이 높아질 수 있습니다.**

따라서 필요한 수준의 스레드 개수를 사용하는 것을 권장합니다.

---

## 🔢 사용자명 생성 방식

체커는 기본적으로 **4자리 사용자명**을 무작위로 생성합니다.

사용되는 문자는 다음과 같습니다.

```text
a-z
0-9
_
.
```

예:

```text
ab12
a1_b
x9.z
zz_1
```

---

## 🚫 생성에서 제외되는 사용자명

체커는 다음 조건에 해당하는 사용자명을 생성하지 않습니다.

### 영문자가 없는 경우

```text
1234
567_
9._2
```

### `..`이 포함된 경우

```text
ab..
a..1
```

### `.`으로 시작하는 경우

```text
.ab1
```

### `.`으로 끝나는 경우

```text
ab1.
```

---

## 📡 사용자명 체커 동작

체커는 Discord의 Username 관련 API에 생성된 사용자명을 전달하여 결과를 확인합니다.

요청 데이터는 다음과 같은 형태입니다.

```json
{
    "username": "abcd"
}
```

HTTP 응답에 따라 결과를 다음과 같이 분류합니다.

| 응답           | 처리                       |
| ------------ | ------------------------ |
| `200`        | 사용자명 사용 가능 여부 확인         |
| `400`        | `already_taken` 포함 여부 확인 |
| `429`        | Rate Limit 처리            |
| 기타 상태 코드     | 오류 처리                    |
| 요청 Exception | 예외 처리 및 재시도              |

> Discord의 API Endpoint, Header, 응답 구조 및 Username 정책은 변경될 수 있습니다. 따라서 향후에도 현재와 동일하게 작동한다고 보장할 수 없습니다.

---

## 🔄 프록시 Session 관리

체커는 ThorData Proxy URL에 랜덤한 `session_id`를 추가합니다.

```python
session_id = random.randint(100000, 999999)
```

생성된 Session ID는 Proxy URL에 포함됩니다.

```text
http://사용자명:비밀번호@서버:포트?session_id=XXXXXX
```

또한 Worker마다 Proxy를 생성하고 일정 횟수의 요청 이후 새로운 Proxy Session을 생성합니다.

현재 코드에서는 **3회 요청마다 Proxy Session을 새로 생성**합니다.

```python
if request_count % 3 == 0:
    current_proxy = get_thordata_proxy()
```

---

## 🔁 오류 발생 시 재시도

네트워크 요청에서 Exception이 발생하면 새로운 Proxy Session을 생성하여 최대 **3회까지 재시도**합니다.

동작 방식:

```text
요청
 │
 ├── 정상 응답
 │
 ├── Rate Limit
 │    └── 새로운 Proxy Session 생성
 │
 └── Exception
      │
      ├── 1회 재시도
      ├── 2회 재시도
      └── 3회 재시도
```

3회 재시도 이후에도 실패하면 해당 요청은 오류로 처리됩니다.

---

## 💾 결과 파일

체커는 검사 결과를 두 개의 파일에 저장합니다.

### ✅ `available.txt`

사용 가능한 것으로 판정된 사용자명이 저장됩니다.

```text
[2026-08-16 14:30:21] ab1_
[2026-08-16 14:30:25] x9_z
```

---

### ❌ `taken.txt`

이미 사용 중인 것으로 판정된 사용자명이 저장됩니다.

```text
[2026-08-16 14:30:22] abc1
[2026-08-16 14:30:23] zzzz
```

각 결과에는 체커가 해당 사용자명을 처리한 날짜와 시간이 함께 저장됩니다.

---

## 📊 실시간 체커 통계

체커는 실행 중 약 2초마다 현재 상태를 출력합니다.

예:

```text
📊 150개 | 사용가능(발견) :2개 | 사용중 :146개 | 오류 :2개
```

| 항목         | 설명                    |
| ---------- | --------------------- |
| `150개`     | 현재까지 체커가 처리한 총 사용자명   |
| `사용가능(발견)` | 사용 가능한 것으로 판정된 사용자명   |
| `사용중`      | 이미 사용 중인 것으로 판정된 사용자명 |
| `오류`       | 오류가 발생한 요청            |

---

## 🛑 체커 중지

프로그램 실행 중 다음 단축키를 사용하여 체커를 중지할 수 있습니다.

```text
Ctrl + C
```

중지하면 최종 결과가 출력됩니다.

```text
⏹️ 중지 중...

📊 최종 결과 :
   총 확인 : 1000개
   ✅ 사용 가능 : 5개 (available.txt)
   ❌ 이미 사용 중 : 990개 (taken.txt)
   ⚠️ 오류: 5개
```

---

## ⚠️ Rate Limit

Discord에서 `429` 응답이 반환되면 체커는 Rate Limit으로 처리합니다.

```text
429 Too Many Requests
```

Rate Limit이 발생하면 새로운 ThorData Proxy Session을 생성합니다.

다만 **Proxy를 사용한다고 해서 Discord의 Rate Limit이나 기타 서비스 제한을 우회할 수 있다고 보장되는 것은 아닙니다.**

과도한 요청을 피하고 적절한 스레드 수를 사용하는 것을 권장합니다.

---

## 🔧 문제 해결

### 프록시 인증 오류

다음 설정을 확인하십시오.

```python
PROXY_USERNAME = "..."
PROXY_PASSWORD = "..."
PROXY_SERVER = "..."
```

ThorData에서 제공받은 정보와 정확하게 일치해야 합니다.

### Proxy 연결 오류

다음 항목을 확인하십시오.

1. ThorData Proxy가 정상적으로 활성화되어 있는지 확인
2. Proxy 서버 주소 확인
3. Proxy 포트 확인
4. Proxy 사용자명 확인
5. Proxy 비밀번호 확인
6. 인터넷 연결 확인

### 모든 요청이 오류로 처리되는 경우

다음 사항을 확인하십시오.

1. ThorData Proxy 연결 상태
2. Discord API Endpoint 변경 여부
3. Discord API 응답 형식 변경 여부
4. Request Header 변경 여부
5. 네트워크 연결 상태
6. 입력한 Proxy 인증 정보

---

## 🔐 SSL 관련 설정

현재 코드에서는 다음과 같이 SSL 인증서 검증을 비활성화하고 있습니다.

```python
verify=False
```

또한 관련 경고를 비활성화합니다.

```python
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)
```

이는 현재 코드의 동작을 설명하기 위한 내용이며, **실제 운영 환경에서는 SSL 인증서 검증을 비활성화하는 것을 권장하지 않습니다.**

---

## 📌 프록시 지원

### 지원 프록시

**ThorData에서 구매한 프록시**

[ThorData 공식 홈페이지](https://thordata.com/)

### 미지원 프록시

다른 프록시 제공업체의 프록시는 공식적으로 지원하지 않습니다.

본 체커의 Proxy Session 처리 방식은 **ThorData 프록시 사용을 기준으로 작성되었습니다.**

---

## 📞 문의

프로그램 관련 문의, 오류 제보 및 기타 질문은 아래 Discord를 이용해 주세요.

### Discord 문의 서버

[Discord 문의 서버 참여하기](https://discord.gg/6c5H5dEEmG)

### 문의 페이지

[zzp.kr/discord](https://zzp.kr/discord)

---

## ⭐ 프로젝트 지원

프로젝트가 도움이 되셨다면 GitHub 저장소에 ⭐ **Star**를 눌러주시면 프로젝트 유지 및 개선에 도움이 됩니다.

[Discord-4Character-Usernames-Checker GitHub 저장소](https://github.com/camt4372/Discord-4Character-Usernames-Checker)

---

# 📚 공부 및 학습 목적

> ⚠️ **본 프로그램은 Python 프로그래밍, HTTP 요청, API 통신, 프록시 처리, 멀티스레딩 등의 기술을 공부하고 학습하기 위한 목적으로만 사용하시기 바랍니다.**
>
> 본 프로그램을 이용하여 Discord 또는 제3자 서비스에 과도한 요청을 보내거나, 서비스의 이용 제한 및 보안 정책을 우회하거나, 기타 부적절한 용도로 사용하는 것을 권장하지 않습니다.
>
> 프로그램을 사용하기 전에 해당 서비스의 이용약관 및 관련 정책을 반드시 확인하시기 바랍니다.
>
> **본 프로젝트는 공부 및 학습용으로만 제공됩니다.**
