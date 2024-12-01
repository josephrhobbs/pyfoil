# PyFoil
# Generate XFoil Input Commands
#
# Developed by Joseph Hobbs
# This code is in the public domain

def generate_commands(airfoil, mode, values, re=None, m=None, output=".pyfoil"):
    """
    Generate XFoil input commands

    Parameters:
    - `airfoil` (`str`):s file name of the airfoil OR if input is `nacaXXXX`, a NACA XXXX airfoil
    - `mode` (`str`): generate polars for given angle of attack (`"ALFA"`) or given CL (`"CL"`)
    - `values` (`list[float]`): given angles of attack or CLs, based on `mode`
    - `re` (`float` or `int`): the Reynolds number (optional, assumed inviscid if none provided)
    - `m` (`float`): the Mach number (optional, assumed incompressible if none provided)
    - `output` (`str`): output file name (optional, defaults to `.pyfoil`)
    """
    # Parse mode
    if mode == "ALFA":
        value_command = "alfa"
    elif mode == "CL":
        value_command = "c"
    else:
        raise TypeError(f"invalid PyFoil mode {mode}")

    # Parse airfoil name
    if airfoil[0:3] == "naca":
        airfoil_command = f"naca {airfoil[4:7]}"
    else:
        airfoil_command = f"load {airfoil}"

    # Initialize commands list
    commands = []

    # Load airfoil and enter OPER mode
    commands.extend([
        airfoil_command,
        "",
        "oper",
        "alfa 0",
    ])

    # Apply Re and M if necessary 
    if re is not None:
        commands.append(f"visc {re}")
    
    if m is not None:
        commands.append(f"mach {m}")

    # Add output file and initiate polar accumulation
    commands += [
        "iter 200",
        "pacc",
        output,
        "",
    ]

    # Process values
    for v in values:
        commands.append(f"{value_command} {v}")

    # Quit the program
    commands.extend([
        "pacc",
        "",
        "quit",
    ])

    # Return valuess
    return "\n".join(commands)