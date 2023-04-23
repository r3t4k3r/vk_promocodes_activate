import requests
import argparse
from datetime import datetime
import vk_captchasolver as vc
import time

def unixtime_to_pytime(unix_time: int):
    return datetime.fromtimestamp(unix_time)


def activate_promocode(cookie:str, hash:str, promocode:str, delay:int):
    headers = {
        'authority': 'vk.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://vk.com',
        'referer': 'https://vk.com/settings?act=payments&w=promocode',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'act': 'activate',
    }

    data = {
        'act': 'activate',
        'al': '1',
        'hash': hash,
        'promo_code': promocode,
    }

    while True:
        time.sleep(3)
        response = requests.post('https://vk.com/promo_codes.php', params=params, headers=headers, data=data)
        try:
            json = response.json()
            if json['payload'][0] == '2':
                # if captcha
                print('captcha detected!')
                data['captcha_sid'] = json['payload'][1][0][1:-1]
                data['captcha_key'] = vc.solve(sid=int(data['captcha_sid']), s=1)
                continue

            status = json['payload'][1][0]['status']
            if status == 'success':
                balance = json['payload'][1][0]['data']['balance']
                print(f'[STATUS={status}] {promocode} [BALANCE={balance}]')
                break
            else:
                error_text = json['payload'][1][0]['error_message']
                print(f'[STATUS={status}] {promocode} [ERR={error_text}]')
                break
        except:
            print('status', response.status_code)
            print('response', response.text)

def main():
    parser = argparse.ArgumentParser(
        prog='VkPromoActivation',
        description='Activates VKPromo by hash and cookie'
    )
    parser.add_argument('-p', '--promocode')
    parser.add_argument('-c', '--cookie', required=True)
    parser.add_argument('-f', '--file', help='file with promocodes')
    parser.add_argument('-d', '--delay', help='delay between requests', default=3, type=int)
    parser.add_argument('-s', '--hash', required=True, help='hash from https://vk.com/promo_codes.php?act=search request')
    args = parser.parse_args()

    if not args.promocode and not args.file:
        return print('set --promocode or --file to use this script')

    if args.promocode:
        activate_promocode(args.cookie, args.hash, args.promocode, args.delay)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = [x.strip() for x in f.readlines()]

        for line in lines:
            activate_promocode(args.cookie, args.hash, line, args.delay)

if __name__ == '__main__':
    main()