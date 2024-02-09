#!/usr/bin/python

import func_messages
import func_general

settings = {}


if __name__ == "__main__":

    # Load the specified config into the settings dictionary
    settings = func_general.get_settings("config.json")

    # Send informational message that the system is active and running
    func_messages.info_message("online", settings)

    # First iteration, so we start from the end of the logfile
    seek_to_end = True

    while True:

        current_date = func_general.get_current_date()

        # Get the actual filename based on the current date
        filename = (
            f'{settings["logfile"]["path"]}{settings["logfile"]["format"]}'.replace(
                "{date}", current_date
            )
        )

        # Send informational message that we're waiting for the logfile
        func_messages.info_message("logfile_waiting", settings, optional=filename)

        # Sit here and wait until the file actually exists
        #     (or the current date changes again)
        file_exists = func_general.wait_for_todays_file(filename, current_date)

        # Send informational message that we're monitoring the logfile
        func_messages.info_message("logfile_monitoring", settings, optional=filename)

        # If the file ever turns up for this day, start to process it
        # otherwise, move on to the next iteration for the new day
        if file_exists:

            # Open the file for reading
            with open(filename, "r") as logfile:

                # Create the generator
                loglines = func_general.follow(logfile, seek_to_end, current_date)

                # Iterate the generator - THIS IS THE PRIMARY WORK LOOP
                for line in loglines:

                    # If it's a new day, break out and look for the new file
                    if func_general.get_current_date() != current_date:
                        break

                    # THIS IS WHERE THE WORK GETS DONE
                    # Force reload of settings, this should prevent the need
                    settings = func_general.get_settings("config.json")
                    # to restart the application after a profile change

                    # Get the message details out of the log line
                    message = func_messages.extract_message(line, settings)
                    # Send the message out (if appropriate)
                    func_messages.send_message(message, settings)

        # Because, at this point, we'd be looking for a new file, we
        # don't want to skip to the end of it so we get everything from the start
        seek_to_end = False
