import quopri
from urllib.parse import unquote


class GetRequest:

    def split_params(self, param: str):
        data = {}
        split_1 = param.split('&')
        for i in split_1:
            split_2 = i.split('=')
            data[split_2[0]] = split_2[1]
        return data


class PostRequest:

    def get_bytes(self, env: dict):
        data = {}
        length_data = env.get('CONTENT_LENGTH')
        data_for_bytes = env['wsgi.input'].read(int(length_data))
        data_for_string = unquote(data_for_bytes.decode("utf8"))
        split_1 = data_for_string.split('&')
        for i in split_1:
            split_2 = i.split('=')
            data[split_2[0]] = split_2[1]
        return data


if __name__ == '__main__':
    GetRequest().split_params("utm_sorce=yandex&utm_medium=cpc")
