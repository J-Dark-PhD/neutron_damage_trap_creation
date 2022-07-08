# Neutron damage trap creation

A repository for modelling neutron damage effects on hydrogen isotope transport

Inital model:

$\frac{dn_{t}}{dt} = \phi \cdot K \left[1-\frac{n_{t}}{n_{max,\phi}}\right]-A_{0}\cdot \exp\left(\frac{-E_{A}}{k_{B}T}\right)\cdot n_{t}$


To run FESTIM:
## Run FESTIM

Run a FEniCS container:

```
docker run -ti -v ${PWD}:/home/fenics/shared quay.io/fenicsproject/stable:latest
```

Install FESTIM v0.10.0:

```
pip install git+https://github.com/RemDelaporteMathurin/FESTIM@v0.10.0
```

To run the FESTIM simulation:

```
python main.py
```

This will produce several .xdmf files