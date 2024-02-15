"""This module holds generic functions to support the application"""

import datetime
import io
import json
import os
import time


def get_settings(json_file: str) -> dict:
    """Loads the specified settings file into a dictionary.

    Args:
        json_file (str): _description_

    Returns:
        dict: _description_
    """

    with open(json_file, encoding="UTF-8") as settings_file:
        file_contents = settings_file.read()

    return json.loads(file_contents)


def follow(thefile: io.TextIOWrapper, seek_to_end: bool, current_date: str):
    """Generator function that yields new lines in a file.

    Args:
        thefile (io.TextIOWrapper): _description_
        seek_to_end (bool): _description_
        current_date (str): _description_

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
        str: _description_
    """

    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")


def wait_for_todays_file(filename: str, current_date: str) -> bool:
    """This is essentially a wrapper around os.path.exists,
    but rather than returning a value immediately, it sits
    and waits until the file eventually arrives.

    If it spills over to the next day, the function returns False.

    Args:
        filename (str): _description_
        current_date (str): _description_

    Returns:
        bool: _description_
    """

    file_exists = False
    check_current_date = get_current_date()

    while check_current_date == current_date and not file_exists:

        file_exists = os.path.exists(filename)
        time.sleep(1)
        check_current_date = get_current_date()

    return file_exists
