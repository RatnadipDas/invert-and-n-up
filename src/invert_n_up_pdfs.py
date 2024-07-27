from .directory import Directory
from .pdf_file import PDFFile
from .n_up_pdf_files import NUpPDFFiles


class InvertNUpPDFs:
    def __init__(self, dir_path=""):
        self._directory = Directory(dir_path)
        self._pdf_files = []
        self._dest_dir = ""

    def gather_pdf_files(self):
        self._directory.filter_pdfs()

        if len(self._directory.get_pdf_files()) == 0:
            print(
                f"NO PDF files found in the directory '{self._directory.get_directory_path()}'...",
                end="\n\n",
            )
            return False

        self._pdf_files = list(
            map(
                lambda f: PDFFile(self._directory.get_directory_path(), f),
                self._directory.get_pdf_file_names(),
            )
        )

        print(
            f"GATHERED PDF files from the directory '{self._directory.get_directory_path()}'...",
            end="\n\n",
        )

        return True

    def invert_pdf_files(self):
        assert (
            len(self._pdf_files) != 0
        ), f"NO PDF files gathered from directory {self._directory.get_directory_path()}"

        for _pdf_file in self._pdf_files:
            _pdf_file.to_jpgs()
            _pdf_file.invert_jpgs()
            self._dest_dir = _pdf_file.to_pdf()

        print(
            f"GENERATED color inverted PDF files from the directory '{self._directory.get_directory_path()}'...\n"
        )

    def n_up_pdf_files(self, ncols=1, nrows=1):
        n_up_pdf_files = NUpPDFFiles(self._dest_dir, ncols, nrows)
        n_up_pdf_files.do_n_up()
        print(
            f"GENERATED N Up PDF files for the directory '{self._directory.get_directory_path()}'...\n"
        )
