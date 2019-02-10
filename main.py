import requests
import os
import argparse
from dotenv import load_dotenv


TOKEN = os.getenv("TOKEN")


def shorten_url(long_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }
    data = {
        'long_url': long_url
    }
    response = requests.post(url, headers=headers, json=data)
    response_dict = response.json()
    if response.ok:
        return response_dict['link']
    else:
        return None


def get_clicks_count(short_url):
    url = 'https://api-ssl.bitly.com/v4//bitlinks/{}/clicks/summary'.\
        format(short_url)
    headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }
    data = {
        'bitlink': short_url,
        'units': -1,
        'unit': 'month'
    }
    response = requests.get(url, headers=headers, json=data)
    response_dict = response.json()
    if response.ok:
        return response_dict['total_clicks']
    else:
        return None


def is_bitlink(url):
    # at first we have to get rid of http/https in the beginning of string,
    # otherwise API answer will be invalid
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]

    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url)
    headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }
    data = {
        'bitlink': url
    }
    response = requests.get(url, headers=headers, json=data)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='This is a URL shortener \
                                                  and stats viewer.')
    parser.add_argument('url', help='If you want to make your url short, just \
                                     type it down. If you already have \
                                     shortened url, type it down to see the \
                                     stats.')
    args = parser.parse_args()

    url = args.url

    if is_bitlink(url):
        bitlink_clicks_count = get_clicks_count(url)
        if bitlink_clicks_count is None:
            print('Some error happened (bitlink)')
        else:
            print('Link has been clicked {} times'.
                                        format(bitlink_clicks_count))
    else:
        short_url = shorten_url(url)
        if short_url is None:
            print('Some error happened')
        else:
            print('Short link: {}'.format(short_url))
