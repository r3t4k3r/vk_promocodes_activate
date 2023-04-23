# vk_promocodes_activate
Activate VkPromo from command line

## How to install:
1. clone this repository `git clone https://github.com/r3t4k3r/vk_promocodes_activate.git`
2. enter in project direcotory `cd vk_promocodes_activate`

### with venv (optional)
1. create venv `python3 -m venv venv`
2. install dependencies `venv/bin/pip install -r requirements.txt`

### without venv
1. install dependencies `pip install -r requirements.txt`

## How to run

### venv
1. `venv/bin/python3 main.py -h`

### without venv
1. `python3 main.py -h`

## args and params
1. `-c` `--cookie` cookie string from request to https://vk.com/promo_codes.php?act=search tested only on chrome based browser
2. `-k` `--cookiefile` file with cookies (https://vk.com/promo_codes.php?act=search tested only on chrome based browser)
3. `-s` `--hash` hash FormData param from request to https://vk.com/promo_codes.php?act=search
4. `-p` `--promocode` activate only one promocode
5. `-f` `--file` activates promocodes from file (every promo from newline)
6. `-d` `--delay` delay between requests

## run example
1. one promo 
```
venv/bin/python3 main.py -c "remixstlid=9070488774126112932_7N31zfOTHks7E1ODLwWOXu8xc0zjqsH9YppxngjBqUD; remixua=157%7C-1%7C195%7...more values here" -p "FL2Y-7CZT-RYHS-MQ0T"
```

2. many promo and cookie from file
```
venv/bin/python3 main.py -k cookies.txt -f promocodes_folder/Petya.txt
```

## thanks to 
- raya
- дыня
