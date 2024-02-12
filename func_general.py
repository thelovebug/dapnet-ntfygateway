import datetime
import json
import os
import time


def get_settings(json_file):
    """
    Loads the specified settings file into a dictionary
    """

    with open(json_file, encoding="UTF-8") as settings_file:
        file_contents = settings_file.read()

    return json.loads(file_contents)


def follow(thefile: str, seek_to_end, current_date: str):
    """
    Generator function that yields new lines in a file
    """
    # seek the end of the file

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


def get_current_date() -> None:
    """
    Very simply, gets the current (UTC) date in ISO8601 format
    """
    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")


def wait_for_todays_file(filename: str, current_date: str) -> None:
    """
    This is essentially a wrapper around os.path.exists,
    but rather than returning a value immediately, it sits
    and waits until the file eventually arrives.

    If it spills over to the next day, the function returns False.u
    """

    file_exists = False
    check_current_date = get_current_date()

    while check_current_date == current_date and not file_exists:

        file_exists = os.path.exists(filename)
        time.sleep(1)
        check_current_date = get_current_date()

    return file_exists
