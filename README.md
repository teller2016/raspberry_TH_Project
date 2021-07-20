## 라즈베리파이를 이용한 온습도 모니터링 시스템

## 주요 기술
```sh
* Framework
    - Django
* Frontend
    - HTML
    - CSS
    - Javascript
* DB
    - MySQL
* Hardware
    - Raspberry pi3 B+
    - 온도 습도 센서
```

## Before start
- 상세 내용은 설명문서를 확인해주세요.

온습도 센서 이용을 위해 설정이 필요합니다.
```sh
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssi
sudo pip3 install Adafruit_DHT
```

./static에 다음과 같이 설정이 필요합니다.
```sh
git clone https://github.com/xdan/datetimepicker.git
git clone https://github.com/ericjgagnon/wickedpicker.git
```



