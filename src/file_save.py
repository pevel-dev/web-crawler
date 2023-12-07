import pathlib
import urllib.parse


class FileSave:
    def __init__(self, base_path):
        self._base_path = base_path

    def html_save(self, url: str, body):
        url = url.replace(':', '_').replace('&',  '_')
        url_parts = url.split('/')[2:]
        path = pathlib.Path(self._base_path + '/' + '/'.join(url_parts[:-1]))
        path.mkdir(parents=True, exist_ok=True)

        name_file = url_parts[-1].split('?')[0]

        file_path = pathlib.Path(str(path) + name_file + '.html')
        file_path = urllib.parse.unquote(str(file_path))

        try:
            with open(str(file_path), 'w', encoding='utf-8') as f:
                f.write(body)
        except Exception as ex:
            print(ex)
