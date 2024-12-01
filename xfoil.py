# PyFoil
# XFoil Interface
#
# Developed by Joseph Hobbs
# This code is in the public domain

import os, subprocess

def run_xfoil(commands, verbose=False, output=".pyfoil", xfoil="xfoil", timeout=30):
    """
    Run XFoil, saving the result to a file

    Parameters:
    - `commands` (`str`): text input to XFoil
    - `verbose` (`bool`): verbosity of the program (defaults to `False`)
    - `output` (`str`): name of the output file (defaults to `.pyfoil`)
    - `xfoil` (`str`): location of XFoil installation (optional, defaults to `"xfoil"`)
    - `timeout` (`int`): timeout of XFoil, in seconds (optional, defaults to 30 seconds)
    """
    # Remove old output file, if it exists
    try:
        os.remove(output)
    except FileNotFoundError:
        # It didn't exist, no problem
        pass

    # Start XFoil
    process = subprocess.Popen(
        xfoil,
        stdin=subprocess.PIPE,
        stdout=None if verbose else subprocess.DEVNULL,
        stderr=None if verbose else subprocess.DEVNULL,
        text=True
    )

    # Send commands
    process.communicate(
        input=commands,
        timeout=timeout,
    )

    # Poll return code
    _return_code = process.poll()

    # Parse XFoil output file
    parsed_output = parse_output(output=output)

    # Remove output file
    os.remove(output)

    # Remove boundary layer file, if it exists
    try:
        os.remove(":00.bl")
    except FileNotFoundError:
        # It didn't exist, no problem
        pass

    return parsed_output

def parse_output(output=".pyfoil"):
    """
    Parse XFoil output file into Python dictionary

    Parameters:
    - `output` (`str`): output file to read (optional, defaults to `".pyfoil"`)
    """
    # Open output file
    with open(output, "r") as f:
        lines = f.read().split("\n")

    # Initialize line index
    line_index = 0

    # Look for output table
    for idx, line in enumerate(lines):
        dash_count = sum([s == "-" for s in line])
        if dash_count > 30:
            line_index = idx

    # Initialize dictionary
    xfoil_values = {
        "alfa": [],
        "CL": [],
        "CD": [],
    }

    # Iterate through output
    for line in lines[line_index+1:]:
        values = [float(val.strip()) for val in line.split(" ") if val.strip()]
        if values:
            xfoil_values["alfa"].append(values[0])
            xfoil_values["CL"].append(values[1])
            xfoil_values["CD"].append(values[2])

    return xfoil_values