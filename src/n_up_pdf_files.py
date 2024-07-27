import os, shutil

import pymupdf

from .directory import Directory


class NUpPDFFiles:
    def __init__(self, src_dir="", ncols=1, nrows=1):
        self._src_dir = Directory(src_dir)
        self._dist_dir = os.path.join(os.getcwd(), "dist/")
        self._ncols = ncols
        self._nrows = nrows
        self._grid_size = self._ncols * self._nrows
        self._width = 0.0
        self._height = 0.0
        self._base_x = 0.0
        self._base_y = 0.0
        self._rectangles = []

        self._initialize_bases()
        self._generate_rectangles()
        self._generate_out_dir()

    def _generate_out_dir(self):
        if os.path.isdir(self._dist_dir):
            shutil.rmtree(self._dist_dir)
        os.mkdir(self._dist_dir)

    def _initialize_bases(self):
        self._width, self._height = pymupdf.paper_size(
            "A4"
        )  # A4 portrait output page format
        _r = pymupdf.Rect(0, 0, self._width, self._height)

        _cal_x1_r = _r / self._ncols
        self._base_x = _cal_x1_r.x1

        _cal_y1_r = _r / self._nrows
        self._base_y = _cal_y1_r.y1

    def _generate_rectangles(self):
        for _nrow in range(self._nrows):
            for _ncol in range(self._ncols):
                _r = pymupdf.Rect(
                    _ncol * self._base_x,
                    _nrow * self._base_y,
                    (_ncol + 1) * self._base_x,
                    (_nrow + 1) * self._base_y,
                )
                self._rectangles.append(_r)

    def _pdf_n_up(self, enclosing_dir="", file_name=""):
        _src_file = pymupdf.open(os.path.join(enclosing_dir, file_name + ".pdf"))
        _dist_file = pymupdf.open()
        _dist_page = None

        for _src_page in _src_file:
            if _src_page.number % self._grid_size == 0:  # create new output page
                # if previous page exist give border to the previously inserted pages
                if _dist_page:
                    self._set_border_to_n_ups(_dist_page)

                # setup a new page
                # pno(int): page number in front of which the new page should be inserted. Must be in 1 < pno <= page_count.
                # pno(int): special values -1 and doc.page_count insert after the last page.
                _dist_page = _dist_file.new_page(
                    -1, width=self._width, height=self._height
                )

            # insert input page into the correct rectangle
            _dist_page.show_pdf_page(
                self._rectangles[_src_page.number % self._grid_size],
                _src_file,
                _src_page.number,
            )

            # give border to the inserted pages for the last page
            if _dist_page:
                self._set_border_to_n_ups(_dist_page)

        # by all means, save new file using garbage collection and compression
        _dist_file.save(
            os.path.join(self._dist_dir, f"{file_name}-n-uped.pdf"),
            garbage=3,
            deflate=True,
        )

        print(
            f"GENERATED N Up PDF file for the PDF file {file_name}.pdf...", end="\n\n"
        )

    def _set_border_to_n_ups(self, page):
        _inserted_pages_info = page.get_image_info()
        for _inserted_page_info in _inserted_pages_info:
            _shape = page.new_shape()
            _shape.draw_rect(_inserted_page_info["bbox"])
            _shape.finish(width=0.5, color=(0, 0, 0))
            _shape.commit()

    def do_n_up(self):
        self._src_dir.filter_pdfs()
        if len(self._src_dir.get_pdf_files()) == 0:
            print(
                f"NO PDF files found in the directory '{self._src_dir.get_directory_path()}'...",
                end="\n\n",
            )

        _pdf_names = self._src_dir.get_pdf_file_names()
        for _pdf_name in _pdf_names:
            self._pdf_n_up(self._src_dir.get_directory_path(), _pdf_name)
