# freitag-telegram-alarm

개인적으로 한번 만들어보고 싶었던 프라이탁 신제품 알람 크롤러  
셀레니움 + 파이썬으로 만들었고 알람은 텔레그램을 사용했다.

20분 간격으로 번갈아가면서 수집한다. 너무 짧은 주기로 돌리면 recaptcha가 올라오는데 해결할 방법이 마땅히 없는 것 같다.
제품은 가장 인기있는 6가지 모델만 추가해놨다. 


# 사용법

1. 텔레그램 봇 생성 후 입력 token 입력 (main.py line:56)
   - 참고: https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0

2. 텔레그램 user_id(chat_id) 확인 후 입력 (main.py line:57)
   - 참고: https://telegram.me/userinfobot

3. 설치형 레디스 download & run (mac)
   - ```
     brew install redis
     brew services start redis
     redis-server
     ```

4. main.py 실행
   - ```
     python main.py
     
     ****
     Choose two 
     example: 1 2 or 2 5 or 3 3
     ****
     0: miami
     1: dragnet
     2: lassie
     3: dexter
     4: leland
     5: bob
     
     >? 0 2
     
     chose item: miami, dragnet
     ```
