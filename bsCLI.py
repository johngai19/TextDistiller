from preprocess import *
import argparse
import os
from shutil import copyfile


def dir_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter path of PDF file to summarize')
    parser.add_argument('--path', type=dir_path, help='path of PDF file to summarize')

    args = parser.parse_args()
    copyfile(args.path, app.config['PDF_UPLOADS'] + '/pdf_file.pdf')
    pdfParser(app.config['PDF_UPLOADS'] + '/pdf_file.pdf')
