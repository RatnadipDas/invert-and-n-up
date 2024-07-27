import os, re


class Directory:
    def __init__(self, dir_path=""):
        assert os.path.isdir(dir_path), f"'{dir_path}' is NOT a valid directory path"

        self._dir_path = dir_path
        self._files = [
            _f
            for _f in os.listdir(self._dir_path)
            if os.path.isfile(os.path.join(self._dir_path, _f))
        ]

    def filter_pdfs(self):
        self._pdf_files = [_f for _f in self._files if re.match(r"^.+\.pdf$", _f)]
        self._pdf_file_names = [
            _m.group(1)
            for _m in map(lambda f: re.search(r"^(.+)\.pdf$", f), self._pdf_files)
        ]

        print(
            f"FILTERED PDF files from the directory '{self._dir_path}'...", end="\n\n"
        )

    def get_directory_path(self):
        return self._dir_path

    def get_pdf_files(self):
        return self._pdf_files

    def get_pdf_file_names(self):
        return self._pdf_file_names
