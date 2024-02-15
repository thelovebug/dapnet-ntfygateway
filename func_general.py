"""This module holds generic functions to support the application"""

import datetime
import io
import json
import os
import time


def get_settings(json_file: str) -> dict:
    """Loads the specified settings file into a dictionary.

    Args:
        json_file (str): _the name of the JSON settings file that needs to be loaded_

    Returns:
        dict: _a dictionary containing the JSON settings file_
    """

    with open(json_file, encoding="UTF-8") as settings_file:
        file_contents = settings_file.read()

    return json.loads(file_contents)


def follow(thefile: io.TextIOWrapper, seek_to_end: bool, current_date: str):
    """Generator function that yields new lines in a file.

    Args:
        thefile (io.TextIOWrapper): _the pointer to the file we just opened_
        seek_to_end (bool): _determines whether we jump to the end of the file once opened_
        current_date (str): _today's date, used to determine whether we need to switch to a new log file or not_

    Yields:
        _type_: _description_
    """
    # Seek to the end of the file. But only on the first file of the run.
    if seek_to_end:
        thefile.seek(0, os.SEEK_END)

    # start infinite loop
    while True:

        # Read the next line of the file
        line = thefile.readline()

        # What if there isn't one?
        if not line:
            # If we've gone into a new day, break out of this loop
            if current_date != get_current_date():
                yield "It's a new day!"
                break

            # Wait for one second and try again in a bit.
            time.sleep(1)
            continue

        # Return the line received from the file
        yield line


def get_current_date() -> str:
    """Very simply, gets the current (UTC) date in ISO8601 format.

    Returns:
        str: _the current UTC date in yyyy-mm-dd format_
    """

    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")


def wait_for_todays_file(filename: str, current_date: str) -> bool:
    """This is essentially a wrapper around os.path.exists,
    but rather than returning a value immediately, it sits
    and waits until the file eventually arrives.

    If it spills over to the next day, the function returns False.

    Args:
        filename (str): _the absolute location of the file we're going to be waiting for_
        current_date (str): _today's date, used to determine whether we need to switch to a new log file or not_

    Returns:
        bool: _True if the file has appeared, False if the file hasn't appeared and it's now the next day_
    """

    file_exists = False
    check_current_date = get_current_date()

    while check_current_date == current_date and not file_exists:

        file_exists = os.path.exists(filename)
        time.sleep(1)
        check_current_date = get_current_date()

    return file_exists
