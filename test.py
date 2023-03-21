import requests
from urllib.parse import urlparse, parse_qs
import time

# URL 정의
url = "https://map.naver.com/v5/search/%EB%AA%A8%EB%94%94%EC%97%A0"

# requests 모듈을 사용하여 URL 접속
response = requests.get(url)
time.sleep(3)
# response 객체에서 리디렉션된 URL 정보 추출
redirect_url = response.url
print(redirect_url)

# urlparse 함수를 사용하여 URL 파싱
parsed_url = urlparse(redirect_url)

# parse_qs 함수를 사용하여 쿼리 파라미터 추출
query_params = parse_qs(parsed_url.query)

# isCorrectAnswer 파라미터 추출
is_correct_answer = query_params.get('isCorrectAnswer', [''])[0]

# 출력
print(is_correct_answer)
