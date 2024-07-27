# poppler should be installed
# if not install install it using conda
# conda install poppler


import os

from src.invert_n_up_pdfs import InvertNUpPDFs

invert_n_up_pdfs = InvertNUpPDFs(os.path.join(os.getcwd(), "pdfs/"))
if invert_n_up_pdfs.gather_pdf_files():
    invert_n_up_pdfs.invert_pdf_files()
    invert_n_up_pdfs.n_up_pdf_files(2, 3)
