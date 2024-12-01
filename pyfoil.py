# PyFoil
# XFoil Automation Script
# 
# Developed by Joseph Hobbs
# This code is in the public domain

from cmd import generate_commands

from xfoil import run_xfoil

class PyFoil(object):
    """
    A Python wrapper over XFoil
    """

    def __init__(self, airfoil, xfoil="xfoil", output=".pyfoil"):
        # Save airfoil
        self.airfoil = airfoil

        # Save XFoil location
        self.xfoil = xfoil

        # Save output file name
        self.output = output

        # Save Reynolds number and Mach number
        self.re = None
        self.m = None

        # Save XFoil timeout (seconds)
        self.timeout = 30

        # Save verbosity
        self.verbose = False

    def alfa(self, values):
        """
        Run XFoil with given angles of attack

        Parameters:
        - `values` (`float` or `int` or `list[float]` or `list[int]`): a list of angles of attack
        """
        return self._run("ALFA", values)

    def cl(self, values):
        """
        Run XFoil with given angles of attack

        Parameters:
        - `values` (`float` or `int` or `list[float]` or `list[int]`): a list of angles of attack
        """
        return self._run("CL", values)

    def _run(self, mode, values):
        """
        Run XFoil with given mode and values

        Parameters:
        - `mode` (`str`): PyFoil mode
        - `values` (`float` or `int` or `list[float]` or `list[int]`): list of values
        """
        # Process input
        xfoil_input = None

        if isinstance(values, float) or isinstance(values, int):
            # Wrap single value in a list
            xfoil_input = [values]
        elif isinstance(values, list):
            # This is a list
            xfoil_input = values
        else:
            raise TypeError(f"invalid input to PyFoil {values}")

        # Generate input commands
        commands = generate_commands(
            self.airfoil,
            mode,
            xfoil_input,
            re=self.re,
            m=self.m,
            output=self.output,
        )

        # Send commands to XFoil
        return run_xfoil(
            commands,
            verbose=self.verbose,
            output=self.output,
            xfoil=self.xfoil,
            timeout=self.timeout,
        )