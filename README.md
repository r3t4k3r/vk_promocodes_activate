# vk_promocodes_activate
Activate VkPromo from command line

## How to install:
### with venv (optional)
1. create venv `python3 -m venv venv`
2. install dependencies `venv/bin/pip -r requirements.txt`

### without venv
1. install dependencies `pip install -r requirements.txt`

## How to run

### venv
1. `venv/bin/python3 main.py -h`

### without venv
1. `python3 main.py -h`

## args and params
1. `-c` `--cookie` cookie string from request to https://vk.com/promo_codes.php?act=search tested only on chrome based browser
2. `-s` `--hash` hash FormData param from request to https://vk.com/promo_codes.php?act=search
3. `-p` `--promocode` activate only one promocode
4. `-f` `--file` activates promocodes from file (every promo from newline)
5. `-d` `--delay` delay before requests

## run example
1. one promo ```
venv/bin/python3 main.py -s "58afdf97cdf462d331" -c "remixstlid=9070488774126112932_7N31zfOTHks7E1ODLwWOXu8xc0zjqsH9YppxngjBqUD; remixua=157%7C-1%7C195%7...more values here" -p "FL2Y-7CZT-RYHS-MQ0T"
```
2. many promo ```
venv/bin/python3 main.py -s "58afdf97cdf462d331" -c "remixstlid=9070488774126112932_7N31zfOTHks7E1ODLwWOXu8xc0zjqsH9YppxngjBqUD; remixua=157%7C-1%7C195%7...more values here" -f promocodes_folder/Petya.txt
```

## thanks to 
- raya
- дыня