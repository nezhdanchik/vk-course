class FileManager:
    def __init__(self, file):
        self.file = file
        self.opened_file = None

    def __enter__(self):
        # передан путь к файлу
        if isinstance(self.file, str):
            self.opened_file = open(self.file, encoding='utf-8')
            return self.opened_file
        # передан файловый объект
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.opened_file:
            self.opened_file.close()


def file_filter(file, find_list, stop_list):
    find_list = {i.lower() for i in find_list}
    stop_list = {i.lower() for i in stop_list}

    with FileManager(file) as f:
        for line in f:
            words = set(line.strip().lower().split())

            if words & stop_list:
                continue

            if words & find_list:
                yield line.strip()
