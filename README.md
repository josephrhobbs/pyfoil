# PyFoil

A Python wrapper for XFoil, an airfoil analysis program developed by MIT Professor Mark Drela.

# Requirements

PyFoil requires a working XFoil installation.  You can learn more about XFoil and download it [here](https://web.mit.edu/drela/Public/web/xfoil/).

# Usage

## Initializing PyFoil

Initialize PyFoil by creating an instance of the `PyFoil` class.

The PyFoil initializer takes a string indicating the airfoil to be analyzed.  If the string is of
the form `"nacaXXXX"`, then PyFoil will use NACA airfoil `XXXX`.  Otherwise, PyFoil will look for
a file with the given name.

```python
from pyfoil import PyFoil

pf = PyFoil("naca0012")
```

__Note__: PyFoil assumes that you have XFoil installed and can run it from the command line as `xfoil`.
If this is not the case, you must pass a second argument to the initializer specifying the XFoil binary's
location as follows.

```python
pf = PyFoil("naca0012", xfoil="/path/to/xfoil")
```

## Setting Reynolds and Mach Numbers (optional)

If you desire to set a Reynolds and Mach number, you can do so as follows.

```python
pf.re = 1e6 # Reynolds number = 1e6
pf.m  = 0.2 # Mach number     = 0.2
```

Skipping this step or setting `Pyfoil.re` to `None` will put PyFoil in inviscid mode.  Similarly,
setting `Pyfoil.m` to `None`, or not setting `Pyfoil.m`, will put PyFoil in incompressible mode.

## Setting Angles of Attack

You can provide PyFoil with one or more angles of attack like so.  Angles of attack are in _degrees_.

```python
# One angle of attack
output = pf.alfa(0)

# Multiple angles of attack
output = pf.alfa([0, 1, 2, 3])
```

## Setting Coefficient of Lift

Alternatively, you can provide PyFoil with one or more coefficients of lift as follows.

```python
# One coefficient of lift
output = pf.cl(0.3)

# Multiple coefficients of lift
output = pf.cl([0.1, 0.2, 0.3])
```

# Output

PyFoil outputs are in the form of Python dictionaries like so.

```python
{
    "alfa": [ 0.0,   0.1,   0.2 ],
    "CL":   [ 0.20,  0.25,  0.30],
    "CD":   [ 0.01,  0.02,  0.03],
    "CDp":  [-0.01, -0.02, -0.03],
    "CDf":  [ 0.02,  0.04,  0.06],
    "CM":   [ 0.01,  0.01,  0.02],
}
```

The keys are as follows.

- `alfa`: Angle of attack (degrees)
- `CL`: Coefficient of lift
- `CD`: Coefficient of drag, equal to `CDp` + `CDf`
- `CDp`: Coefficient of pressure drag, due to inviscid effects
- `CDf`: Coefficient of skin friction drag, due to viscous effects
- `CM`: Coefficient of moment around the quarter-chord (point with coordinates `(0.25, 0.0)`)