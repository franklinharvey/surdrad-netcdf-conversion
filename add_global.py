'''
Input: NetCDF file
Output: NetCDF file with Surfrad metadata
'''

import sys
from netCDF4 import Dataset

def main(filesToProcess):
    for input in filesToProcess:
        foo = Dataset(input, "r+", format="NETCDF4")
        foo = add_globals(foo)
        foo = add_var_attrs(foo)

def add_globals(foo):
    foo.Conventions='CF-1.6'
    foo.title = 'NOAA/ESRL/GMD/GRAD Radiation Archive - %s' % testsite
    foo.institution = 'National Oceanic and Atmospheric Administration (NOAA) - David Skaggs Research Center - Boulder, CO'
    foo.comment = "Converted from .dat file in the radiation group's FTP server"
    return foo

def add_var_attrs(foo):
    foo.variables["solar_zenith_angle"].units = "degree"
    foo.variables["surface_downwelling_shortwave_flux"].units = "W/m-2"
    foo.variables["surface_upwelling_shortwave_flux"].units = "W/m-2"
    foo.variables["surface_direct_normal_shortwave_flux"].units = "W/m-2"
    foo.variables["surface_diffuse_downwelling_shortwave_flux_in_air"].units = "W/m-2"
    foo.variables["surface_downwelling_longwave_flux"].units = "W/m-2"
    foo.variables["downwelling_pyrgeometer_case_temp"].units = "K"
    foo.variables["downwelling_pyrgeometer_dome_temp"].units = "K"
    foo.variables["surface_upwelling_longwave_flux"].units = "W/m-2"
    foo.variables["upwelling_pyrgeometer_case_temp"].units = "K"
    foo.variables["upwelling_pyrgeometer_dome_temp"].units = "K"
    foo.variables["downwelling_UVB_flux"].units = "W/m-2"
    foo.variables["surface_downwelling_photosynthetic_radiative_flux_in_air"].units = "W/m-2"
    foo.variables["surface_net_downward_shortwave_flux"].units = "W/m-2"
    foo.variables["surface_net_downward_longwave_flux"].units = "W/m-2"
    foo.variables["surface_net_downward_radiative_flux"].units = "W/m-2"
    foo.variables["surface_temperature"].units = "K"
    foo.variables["relative_humidity"].units = "1"
    foo.variables["wind_speed"].units = "m s-1"
    foo.variables["wind_from_direction"].units = "degree"
    foo.variables["air_pressure"].units = 'Pa'
    return foo

if __name__ == '__main__':
    main(sys.argv[1:])
