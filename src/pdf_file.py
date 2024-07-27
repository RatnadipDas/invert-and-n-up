import os, shutil, re

import PIL, img2pdf, pdf2image


class PDFFile:
    def __init__(self, enclosing_dir_path="", file_name=""):
        assert os.path.isdir(
            enclosing_dir_path
        ), f"'{enclosing_dir_path}' is NOT a valid directory path"
        assert os.path.isfile(
            os.path.join(enclosing_dir_path, file_name + ".pdf")
        ), f"'{enclosing_dir_path}' is NOT a file"
        assert re.match(
            r"^.+\.pdf$", os.path.join(enclosing_dir_path, file_name + ".pdf")
        ), f"'{enclosing_dir_path}' is NOT a PDF file"

        self._enclosing_dir_path = enclosing_dir_path
        self._build_dir = os.path.join(os.getcwd(), "build/")
        self._file_name = file_name
        self._file_absolute_path = os.path.join(
            self._enclosing_dir_path, self._file_name + ".pdf"
        )
        self._tmp_dir = os.path.join(os.getcwd(), "tmp/")
        self._jpgs = []
        self._idx_counter = []

        self._generate_build_dir()

    def _generate_build_dir(self):
        if os.path.isdir(self._build_dir):
            shutil.rmtree(self._build_dir)
        os.mkdir(self._build_dir)

    def to_jpgs(self):
        self._jpgs = pdf2image.convert_from_path(self._file_absolute_path)

        print(f"CREATED JPG files for the PDF file '{self._file_name}.pdf'...")

    def invert_jpgs(self):
        assert (
            len(self._jpgs) != 0
        ), f"JPG files NOT generated for the PDF file {self._file_name}.pdf"

        if os.path.isdir(self._tmp_dir):
            shutil.rmtree(self._tmp_dir)

        os.mkdir(self._tmp_dir)

        for _idx, _image in enumerate(self._jpgs):
            self._idx_counter.append(f"{self._tmp_dir}/{self._file_name}_{_idx}.jpg")
            _image = PIL.ImageOps.invert(_image)
            _image.save(self._idx_counter[_idx])

        print(
            f"INVERTED color of the JPG files for the PDF file '{self._file_name}.pdf'..."
        )

    def to_pdf(self):
        assert (
            len(self._idx_counter) != 0
        ), f"Inverted JPG files NOT generated for the PDF file {self._file_name}.pdf"

        with open(
            os.path.join(self._build_dir, f"{self._file_name}-inverted.pdf"), "wb"
        ) as _f:
            _f.write(img2pdf.convert(self._idx_counter))

        shutil.rmtree(self._tmp_dir)

        print(
            f"GENERATED color inverted PDF file for the PDF file '{self._file_name}.pdf'...",
            end="\n\n",
        )

        return self._build_dir
