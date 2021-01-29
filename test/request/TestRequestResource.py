import unittest, requests

class TestRequestResource(unittest.TestCase):
    def test_baidu(self):
        response = requests.get('http://www.baidu.com')
        if response.status_code == 200:
            print(response.content.decode('utf-8'))
            return response.content

    def test_google(self):
        response = requests.get('http://www.google.com')
        if response.status_code == 200:
            print(response.content.decode('utf-8'))
            return response.content

    def test_request_CHANGELOG(self):
        response = requests.get(
            'https://raw.githubusercontent.com/NWYLZW/right-click-helper/master/CHANGELOG.zh-CN.md'
        )
        if response.status_code == 200:
            print(response.content.decode('utf-8'))
            return response.content


if __name__ == '__main__':
    unittest.main()
