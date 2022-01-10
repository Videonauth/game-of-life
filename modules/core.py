#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# core.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 02.12.18 - 02:54
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

"""
Set of core functions.

Just a set of small helper functions collected and made over the years.
"""
import datetime
import json
import logging
import os
import subprocess
import time
from contextlib import suppress
from typing import Any, List, Optional

__version__ = '0.0.19'


def bash_command(command: list) -> Optional[str]:
    """
    Run external commands.

    :param command: A list object containing the command.
    :return str or None: A string containing stdout or None.
    """
    _new_env = dict(os.environ)
    _new_env['LC_ALL'] = 'C'
    try:
        _stdout = subprocess.check_output(command, env=_new_env).decode('utf8')
    except subprocess.CalledProcessError:
        return None
    else:
        if _stdout:
            return _stdout
        else:
            return None


def list_strip_all_newline(list_item: list) -> list:
    """
    Strip all newline characters from all list_items in list object.

    :param list_item: A list object to be cleaned from newline characters.
    :return list: A list object which has been cleaned.
    """
    return list(map(lambda x: x.strip('\n'), list_item))


def list_append_all_newline(list_item: list) -> list:
    """
    Append a newline character to every list_item in list object.

    :param list_item: A list object to append newlines to.
    :return list: A list object with newlines appended.
    """
    return list(map(lambda x: f'{x}\n', list_item))


def dict_strip_quotes(dict_item: dict) -> dict:
    """
    Strip quote characters from dict values.

    :param dict_item: A dictionary to work with.
    :return dict: A dictionary with quotes stripped.
    """
    _output = {}
    delimiter = '\"'
    for _key, _value in dict_item.items():
        _output.update({_key: _value.strip(delimiter)})
    _tmp = _output
    _output = {}
    delimiter = "'"
    for _key, _value in _tmp.items():
        _output.update({_key: _value.strip(delimiter)})
    return _output


def dict_to_list(dict_item: dict, delimiter: str = '=') -> list:
    """
    Convert a dict object into a list object using delimiter as separator.

    :param dict_item: A dictionary to be converted.
    :param delimiter: A separating delimiter to use. Default is '='.
    :return list: A list object containing dict_item joined by delimiter.
    """
    _output = []
    for _key, _value in dict_item.items():
        _output.append(f'{_key}{delimiter}{_value}')
    return _output


def dict_get_key_by_value(dict_item: dict, value) -> Optional[str]:
    """
    Find a key associated to a value if present, returns key or None otherwise.

    :param dict_item: A dictionary object to be searched in.
    :param value: The value to compare.
    :return str or None: A key as a string or None if not found.
    """
    for _key, _value in dict_item.items():
        if _value == value:
            return _key
    return None


def dict_get_value_by_key(dict_item: dict, key: str) -> Optional[Any[bool, int, float, str, list[Any], dict]]:
    """
    Find a value to a key if present, returns key or None otherwise.

    :param dict_item: A dictionary item to be searched in.
    :param key: The key to search for
    :return any: The value from key or None.
    """
    for _key, _value in dict_item.items():
        if _key == key:
            return _value
    return None


def dict_is_all_none(dict_item: dict) -> bool:
    """
    Test if all dictionary items are None.

    :param dict_item: A dictionary object to be testes.
    :return bool: True if all keys have None as value, False otherwise
    """
    for _key, _value in dict_item.items():
        if _value is not None:
            return False
    return True


def end_program(start_time: float, reason: int):
    """
    End the program and output the time the program has run.

    :param start_time: Delta time from 'time' library taken when the program was started.
    :param reason: Return code to exit on.
    """
    print(f'\nProcess finished after {time.time() - start_time} seconds.')
    print(f'Process finished with exit code {reason}.')
    with suppress(SystemExit):
        exit(reason)


def json_to_dict(filename: str) -> dict:
    """
    Load a .json file and return a dictionary on success.

    :param filename: File name as a string (can include a path).
    :return dict: containing the json data on success.
    """
    try:
        with open(filename, mode='r') as _file:
            _dict_item = json.load(_file)
    except FileNotFoundError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return _dict_item


def dict_to_json(dict_item: dict, filename: str) -> bool:
    """
    Save a dictionary into a json file.

    :param dict_item: Dictionary containing the data.
    :param filename: File name for the json file (can contain a path).
    :return bool: Returns True on success.
    """
    try:
        with open(filename, mode='x') as _file:
            json.dump(dict_item, _file, indent=2, sort_keys=True)
    except FileExistsError:
        try:
            os.remove(filename)
            with open(filename, mode='w') as _file:
                json.dump(dict_item, _file, indent=2, sort_keys=True)
        except PermissionError as _error:
            print(f'{datetime.datetime.today()} {_error}')
            exit(1)
        else:
            return True
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return True


def asc_to_list(filename: str) -> list:
    """
    Load a text file and return a list, each line a single item stripped clean of newline on success.

    :param filename: File name as a string (can include a path).
    :return list: containing the text file data on success.
    """
    try:
        with open(filename, mode='r') as _file:
            _list_item = _file.readlines()
    except FileNotFoundError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return list_strip_all_newline(_list_item)


def list_strip_comments(list_item: list, comment_denominator: str = '#') -> list:
    """
    Strip all items which are comments from a list.

    :param list_item: The list object to be stripped of comments.
    :param comment_denominator: The character with which comment lines start with.
    :return list: A cleaned list object.
    """
    _output = []
    for _item in list_item:
        if not _item[0] == comment_denominator:
            _output.append(_item)
    return _output


def list_strip_all_blank(list_item: list) -> list:
    """
    Strip all items from a list which are '' or empty.

    :param list_item: The list object to be stripped of all empty values.
    :return list: A cleaned list object.
    """
    _output = []
    for _item in list_item:
        if _item and _item != '':
            _output.append(_item)
    return _output


def list_to_dict(list_item: list, delimiter: str = '=') -> dict:
    """
    Convert a list containing key, value pairs separated by delimiter to a dict object.

    Note: Will strip all list items which are empty or blank '' or which are assumed to be comments '#'.

    Example:
        Given:
        example_list = ['# example_comment',
                        'example_key1=example_value1',
                        'example_key2=example_value2',
                        '',
                        ]
        Will convert to:
        example_dict = {'example_key1': example_value,
                        'example_key2': example_value}

    :param list_item: The input list object.
    :param delimiter: The separator to use.
    :return dict: The new created dict object.
    """
    _output = {}
    list_item = list_strip_comments(list_item)
    list_item = list_strip_all_blank(list_item)
    for _line in list_item:
        _output.update({_line.split(delimiter)[0]: _line.split(delimiter)[1]})
    return _output


def dict_to_stdout(dict_item: dict) -> bool:
    """
    Print the dict objects contents to screen.

    :param dict_item: A dict object to print out.
    :return bool: True on finish.
    """
    for _key, _value in dict_item.items():
        print(f'{_key}: {_value}')
    return True


def list_to_stdout(list_item: list) -> bool:
    """
    Print the list objects contents to screen, each as own line.

    :param list_item: A dict object to print out.
    :return bool: True on finish.
    """
    for _line in list_item:
        print(f'{_line}')
    return True


def asc_to_dict(filename: str) -> dict:
    """
    Load an asc file into a dict object.

    :param filename: The file to load.
    :return dict: A dict object containing data.
    """
    return list_to_dict(asc_to_list(filename))


def list_to_asc(list_item: list, filename: str) -> bool:
    """
    Save a list into an asc file.

    :param list_item: List containing the data.
    :param filename: File name for the asc file (can contain a path).
    :return bool: Returns True on success.
    """
    list_item = list_append_all_newline(list_item)
    try:
        with open(filename, mode='x') as _file:
            _file.writelines(list_item)
    except FileExistsError:
        try:
            os.remove(filename)
            with open(filename, mode='w') as _file:
                _file.writelines(list_item)
        except PermissionError as _error:
            print(f'{datetime.datetime.today()} {_error}')
            exit(1)
        else:
            return True
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return True


def dict_to_asc(dict_item: dict, filename: str) -> bool:
    """
    Save a dict into an asc file.

    :param dict_item: The dict object to save.
    :param filename: The file path to be saved to.
    :return bool: True on success.
    """
    return list_to_asc(dict_to_list(dict_item), filename)


def setup_logger(logger_name: str, log_file_name: str, level: int = logging.DEBUG):
    """
    Help for setting up different loggers.

    :param logger_name: System intern name for getLogger function
    :param log_file_name: File name for the log file
    :param level: logging object (<class 'int'>) defining the log level (by default it logs all logging.DEBUG)
    """
    _logger = logging.getLogger(logger_name)
    if len(_logger.handlers) == 0:
        _formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        _file_handler = logging.FileHandler(log_file_name, mode='a')
        _file_handler.setFormatter(_formatter)
        _stream_handler = logging.StreamHandler()
        _stream_handler.setFormatter(_formatter)
        _logger.setLevel(level)
        _logger.addHandler(_file_handler)
        _logger.addHandler(_stream_handler)


def raw_to_file(filename: str, raw: str) -> bool:
    """
    Save raw data to file.

    :param filename: the path to be saved to.
    :param raw: The content for the file.
    :return bool: True on success.
    """
    try:
        with open(filename, mode='x') as _file:
            _file.write(raw)
    except FileExistsError:
        try:
            os.remove(filename)
            _file.write(raw)
        except PermissionError as _error:
            print(f'{datetime.datetime.today()} {_error}')
            exit(1)
        else:
            return True
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return True


def file_to_raw(filename: str) -> Optional[Any[bool, int, float, List[Any], dict]]:
    """
    Load a file and returns its raw content.

    :param filename: File name as a string (can include a path).
    :return: containing the raw file data on success.
    """
    try:
        with open(filename, mode='r') as _file:
            _raw = _file.read()
    except FileNotFoundError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    except PermissionError as _error:
        print(f'{datetime.datetime.today()} {_error}')
        exit(1)
    else:
        return _raw


def dir_create(path: str) -> bool:
    """
    Create a directory or if path to directory does not exist create the whole path.

    Note: Equivalent of 'mkdir -p <path>'. Bails out on permission error.

    :param path: The path/directory to create as string.
    :return bool: Returns True on success and False if the directory exists already.
    """
    try:
        os.mkdir(path)
    except FileNotFoundError:
        try:
            os.makedirs(path)
        except PermissionError:
            print('Lacking permissions to create directories.')
            exit(1)
        else:
            return True
    except FileExistsError:
        return False
    except PermissionError:
        print('Lacking permissions to create directories.')
        exit(1)
    else:
        return True


if __name__ == '__main__':
    pass
