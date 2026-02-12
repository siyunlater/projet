import openmc
import numpy as np
import argparse

# Arguments parser
parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--batch", type=int, required=True)
parser.add_argument("--particle", type=int, required=True)
parser.add_argument("--outdir", type=str, required=True)
args = parser.parse_args()

###############################################################
# Material
###############################################################

uo2 = openmc.Material(1, "uo2")
uo2.add_nuclide('U235', 0.03) #atomic density
uo2.add_nuclide('U238', 0.97)
uo2.add_nuclide('O16', 2.0)
uo2.set_density('g/cm3', 10.0)

zirconium = openmc.Material(name="zirconium")
zirconium.add_element('Zr', 1.0)
zirconium.set_density('g/cm3', 6.6)

water = openmc.Material(name="h2o")
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 1.0)

water.add_s_alpha_beta('c_H_in_H2O')

materials = openmc.Materials([uo2, zirconium, water])

materials.export_to_xml()

###############################################################
# Geometry
###############################################################

fuel_outer_radius = openmc.ZCylinder(r=0.39)
clad_inner_radius = openmc.ZCylinder(r=0.40)
clad_outer_radius = openmc.ZCylinder(r=0.46)

fuel_region = -fuel_outer_radius
gap_region = +fuel_outer_radius & -clad_inner_radius
clad_region = +clad_inner_radius & -clad_outer_radius

fuel = openmc.Cell(name='fuel')
fuel.fill = uo2
fuel.region = fuel_region

gap = openmc.Cell(name='air gap')
gap.region = gap_region

clad = openmc.Cell(name='clad')
clad.fill = zirconium
clad.region = clad_region

pitch = 1.26
left = openmc.XPlane(-pitch/2, boundary_type='reflective')
right = openmc.XPlane(pitch/2, boundary_type='reflective')
bottom = openmc.YPlane(-pitch/2, boundary_type='reflective')
top = openmc.YPlane(pitch/2, boundary_type='reflective')

water_region = +left & -right & +bottom & -top & +clad_outer_radius

moderator = openmc.Cell(name='moderator')
moderator.fill = water
moderator.region = water_region

box = openmc.model.RectangularPrism(width=pitch, height=pitch,
                                    boundary_type='reflective')

water_region = -box & +clad_outer_radius

root_universe = openmc.Universe(cells=(fuel, gap, clad, moderator))
geometry = openmc.Geometry(root_universe)

geometry.export_to_xml()

###############################################################
# Source & Setting
###############################################################

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-0.63, -0.63, -0.63, 0.63, 0.63, 0.63]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
source = openmc.IndependentSource(space=uniform_dist)

settings = openmc.Settings()
settings.source = source
settings.batches = args.batch # batch
settings.particles = args.particle # particle
settings.seed = args.seed # random seed
settings.output = {'path': args.outdir}

settings.export_to_xml()

###############################################################
# Tally
###############################################################

cell_filter = openmc.CellFilter(fuel)

# Create mesh which will be used for tally
mesh = openmc.RegularMesh()
mesh.dimension = [50, 50]
mesh.lower_left = [-0.39, -0.39]
mesh.upper_right = [0.39, 0.39]

# Create mesh filter for tally
mesh_filter = openmc.MeshFilter(mesh)

tallies = openmc.Tallies()

tally_fission = openmc.Tally(name='fission')
tally_fission.filters = [mesh_filter]
tally_fission.scores = ['fission']

tally_heating = openmc.Tally(name='heating')
tally_heating.filters = [mesh_filter]
tally_heating.scores = ['heating']

tally_f_total = openmc.Tally(name='fission_total')
tally_f_total.scores = ['fission']

tally_h_total = openmc.Tally(name='heating_total')
tally_h_total.scores = ['heating']

tallies = openmc.Tallies([tally_fission, tally_heating, tally_f_total, tally_h_total])
tallies.export_to_xml()

###############################################################
# Run
###############################################################
openmc.run()