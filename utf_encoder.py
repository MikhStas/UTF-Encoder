#! /usr/bin/python3

import chardet
import os
import argparse
import sys


def sub_add_label_to_filename(path: str, label: str) -> str:
    '''
    Insert label between filename and extension
    '''

    root, ext = os.path.splitext(path)
    root += label
    result = root + ext

    return result

def sub_convert_to_absolute_path(path: str) -> str:
    ''' 
    Convert relative path to absolute path. Convertation is 
    performed relative to the calling script path
    ''' 

    script_dir_path = os.path.dirname(__file__)
    dirty_path = os.path.join(script_dir_path, path)
    real_path = os.path.realpath(dirty_path)

    return real_path

def sub_check_file(file_path: str) -> None:
    '''
    Check file existence and exit programm if file was not found
    '''

    file_path = sub_convert_to_absolute_path(file_path)

    if os.path.isfile(file_path):
        print(f"==> File {file_path} found")
    else:
        print(f"!!! File {file_path} not found !!!")
        raise SystemExit

def sub_get_file_encoding(content: str) -> str:
    '''
    Return file encoding
    '''

    encoding = ''
    enc = chardet.detect(content)
    encoding = enc['encoding']

    return encoding

def sub_convert_to_utf(content: str, encoding: str) -> str:
    '''
    Convert file encoding to utf-8
    '''

    content = content.decode(encoding)
    content = content.encode("utf-8")

    return content

def sub_get_file_content(file_path: str) -> str:
    '''
    Just return binary content of file
    '''

    content = ''

    with open(file_path, 'rb') as inf:
        content = inf.read()

    return content

def show(args) -> None:
    '''
    Return file encoding. Use this function with 'show' command
    '''

    args.file = sub_convert_to_absolute_path(args.file)

    sub_check_file(args.file)
    file_content = sub_get_file_content(args.file)
    encoding = sub_get_file_encoding(file_content)

    print(f'File encoding: {encoding}')

def encode(args) -> None:
    '''
    Check file encoding and encode it to utf-8 if nessesary
    '''
    
    args.file = sub_convert_to_absolute_path(args.file)

    sub_check_file(args.file)
    file_content = sub_get_file_content(args.file)
    encoding = sub_get_file_encoding(file_content)
    if encoding == 'utf-8':
        print(f'File {args.file} already has utf-8 encoding!')
    else:
        file_path = ''
        if args.replace:
            file_path = args.file
        else:
            file_path = sub_add_label_to_filename(args.file, '_(utf)')

        content_utf = sub_convert_to_utf(file_content, encoding)

        with open(file_path, 'wb') as ouf:
            try:
                ouf.write(content_utf)
                print(f"==> File {file_path} successfully created")
            except:
                print("!!! There was an error while encoding !!!")

        print('Encoding complete!')

def create_menu(parser_obj):
    subparsers = parser_obj.add_subparsers(
                title='Commands',
                description='Valid commands',
                help='Description'
            )

    show_cmd_parser = subparsers.add_parser('show', help='Show file encoding')
    show_cmd_parser.add_argument('file', help='Path to file')
    show_cmd_parser.set_defaults(func=show)

    encode_cmd_parser = subparsers.add_parser('encode', help='Encode file to utf-8')
    encode_cmd_parser.add_argument('file', help='Path to file')
    encode_cmd_parser.add_argument('--replace', help='Replace existing file', 
            action='store_true')
    encode_cmd_parser.set_defaults(func=encode)

def main_func():
    print('UTF-8 encoder...')

    parser = argparse.ArgumentParser(description='utf encoder')
    create_menu(parser)
    args = parser.parse_args()

    if not vars(args):
        parser.print_usage()

    else:
        args.func(args)


if __name__ == '__main__':
    main_func()
