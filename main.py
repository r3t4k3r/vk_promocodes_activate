import requests
import argparse
from datetime import datetime
import vk_captchasolver as vc
import time


def unixtime_to_pytime(unix_time: int):
    return datetime.fromtimestamp(unix_time)


def get_hash(cookie: str):
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
        'act': 'show',
    }

    data = {
        'act': 'show',
        'al': '1',
        'dmcah': '',
        'is_znav': '1',
        'loc': 'settings',
        'ref': '',
        'w': 'promocode',
    }
    try:
        response = requests.post('https://vk.com/wkview.php', params=params, headers=headers, data=data)
        return response.text.split('hash: \'')[1].split('\'')[0]
    except:
        raise Exception('Cannot get hash, invalid cookie?')

def check_promocode(args):
    headers = {
        'authority': 'vk.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': args.cookie,
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
        'act': 'search',
    }

    data = {
        'act': 'search',
        'al': '1',
        'hash': args.hash,
        'query': args.promocode,
    }

    captcha_tries_count = 0

    while True:
        response = requests.post('https://vk.com/promo_codes.php', params=params, headers=headers, data=data)
        try:
            json = response.json()
            if json['payload'][0] == '2':
                data['captcha_sid'] = json['payload'][1][0][1:-1]
                data['captcha_key'] = vc.solve(sid=int(data['captcha_sid']), s=1)
                captcha_tries_count += 1
                time.sleep(args.captchadelay)
                continue

            status = json['payload'][1][0]['status']
            if status == 'success':
                votes = json['payload'][1][0]['promo_code']['votes']
                expired_at = datetime.fromtimestamp(json['payload'][1][0]['promo_code']['expired_at'])
                print(f'[{status.upper()}] {args.promocode} [CAPTCHA_TRIES_COUNT={captcha_tries_count}] [VOTES={votes}] [EXPIRED_AT={expired_at}]')
                captcha_tries_count = 0
                if args.good:
                    with open(args.good, 'a', encoding='utf-8') as f:
                        f.write(args.promocode + '\n')
                time.sleep(args.delay)
                break
            else:
                error_text = json['payload'][1][0]['error_message']
                print(f'[{status.upper()}] {args.promocode} [CAPTCHA_TRIES_COUNT={captcha_tries_count}] [ERR={error_text}]')
                captcha_tries_count = 0
                if args.bad:
                    with open(args.bad, 'a', encoding='utf-8') as f:
                        f.write(args.promocode + '\n')
                    time.sleep(args.delay)
                break
        except Exception as e:
            print('status', response.status_code)
            print('response', response.text)
            print('exception', e)


def activate_promocode(args):
    headers = {
        'authority': 'vk.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': args.cookie,
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
        'hash': args.hash,
        'promo_code': args.promocode,
    }

    captcha_tries_count = 0

    while True:
        response = requests.post('https://vk.com/promo_codes.php', params=params, headers=headers, data=data)
        try:
            json = response.json()
            if json['payload'][0] == '2':
                data['captcha_sid'] = json['payload'][1][0][1:-1]
                data['captcha_key'] = vc.solve(sid=int(data['captcha_sid']), s=1)
                captcha_tries_count += 1
                time.sleep(args.captchadelay)
                continue

            status = json['payload'][1][0]['status']
            if status == 'success':
                balance = json['payload'][1][0]['data']['balance']
                print(f'[{status.upper()}] {args.promocode} [CAPTCHA_TRIES_COUNT={captcha_tries_count}] [BALANCE={balance}]')
                if args.good:
                    with open(args.good, 'a', encoding='utf-8') as f:
                        f.write(args.promocode + '\n')
                captcha_tries_count = 0
                time.sleep(args.delay)
                break
            else:
                error_text = json['payload'][1][0]['error_message']
                print(f'[{status.upper()}] {args.promocode} [CAPTCHA_TRIES_COUNT={captcha_tries_count}] [ERR={error_text}]')
                if args.bad:
                    with open(args.bad, 'a', encoding='utf-8') as f:
                        f.write(args.promocode + '\n')
                captcha_tries_count = 0
                time.sleep(args.delay)
                break
        except Exception as e:
            print('status', response.status_code)
            print('response', response.text)
            print('exception', e)


def main():
    parser = argparse.ArgumentParser(
        prog='VkPromoActivation',
        description='Activates VKPromo by hash and cookie'
    )
    parser.add_argument('-p', '--promocode')
    parser.add_argument('-c', '--cookie', help='cookie string')
    parser.add_argument('-k', '--cookiefile', help='file with cookies')
    parser.add_argument('-f', '--file', help='file with promocodes')
    parser.add_argument('-d', '--delay', help='delay between requests', default=3, type=int)
    parser.add_argument('-y', '--captchadelay', help='delay before solve captcha, by default captchadelay=delay', default=None, type=int)
    parser.add_argument('-s', '--hash', help='hash from https://vk.com/promo_codes.php?act=search request')
    parser.add_argument('-r', '--check', help='check promocodes, require -g and -b params', action="store_true")
    parser.add_argument('-g', '--good', help='save good promocodes to file')
    parser.add_argument('-b', '--bad', help='save bad promocodes to file')
    args = parser.parse_args()

    if not args.promocode and not args.file:
        return print('set --promocode or --file to use this script')

    if not args.cookie and not args.cookiefile:
        return print('set --cookie or --cookiefile to use this script')

    if args.cookie:
        args.cookie = args.cookie.strip()
    elif args.cookiefile:
        with open(args.cookiefile, 'r', encoding='utf-8') as f:
            args.cookie = f.read().strip()

    if not args.hash:
        print('hash not provided, getting hash ...')
        args.hash = get_hash(args.cookie)
        print('hash received')

    if not args.captchadelay:
        args.captchadelay = args.delay

    # rewrite data if good or bad is enable
    if args.good:
        with open(args.good, 'w') as f:
            f.write('')
    if args.bad:
        with open(args.bad, 'w') as f:
            f.write('')

    # select function
    if args.check:
        activate_func = check_promocode
        print('start checking promocodes...')
    else:
        activate_func = activate_promocode
        print('start activate promocodes...')

    if args.promocode:
        activate_func(args)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = [x.strip() for x in f.readlines()]

        for line in lines:
            args.promocode = line
            activate_func(args)


if __name__ == '__main__':
    main()
