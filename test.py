from pyfoil import PyFoil

foils = [PyFoil(f"orig{i}foilmod.dat") for i in range(15)]

# Reynolds number
RE = 1e6

# Mach number
M  = 0.7

# List of CD values
cds = []

for foil in foils:
    foil.re = RE
    foil.m  = M
    cd = foil.cl(0.2)["CD"]
    cds.append(cd)

print(cds)