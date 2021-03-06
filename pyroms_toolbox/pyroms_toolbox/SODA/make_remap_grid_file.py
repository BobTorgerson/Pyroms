import numpy as np
from mpl_toolkits.basemap import pyproj
from datetime import datetime
try:
  import netCDF4 as netCDF
except:
  import netCDF3 as netCDF
import pyroms


def make_remap_grid_file(SODA_grd):

    #create remap file
    remap_filename = 'remap_grid_' + SODA_grd.name + '.nc'
    nc = netCDF.Dataset(remap_filename, 'w', format='NETCDF3_CLASSIC')
    nc.Description = 'remap grid file for SODA'
    nc.Author = 'pyroms_toolbox.SODA.make_remap_grid_file'
    nc.Created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nc.title = SODA_grd.name

    lon_corner = SODA_grd.lon_vert
    lat_corner = SODA_grd.lat_vert
    grid_center_lon = SODA_grd.lon.flatten()
    grid_center_lat = SODA_grd.lat.flatten()
    grid_imask = SODA_grd.mask[0,:].flatten()
    Mp, Lp = SODA_grd.lon.shape

    grid_size = Lp * Mp

    grid_corner_lon = np.zeros((grid_size, 4))
    grid_corner_lat = np.zeros((grid_size, 4))
    k = 0
    for j in range(Mp):
        for i in range(Lp):
            grid_corner_lon[k,0] = lon_corner[j,i]
            grid_corner_lat[k,0] = lat_corner[j,i]
            grid_corner_lon[k,1] = lon_corner[j,i+1]
            grid_corner_lat[k,1] = lat_corner[j,i+1]
            grid_corner_lon[k,2] = lon_corner[j+1,i+1]
            grid_corner_lat[k,2] = lat_corner[j+1,i+1]
            grid_corner_lon[k,3] = lon_corner[j+1,i]
            grid_corner_lat[k,3] = lat_corner[j+1,i]
            k = k + 1


    #Write netcdf file
    nc.createDimension('grid_size', grid_size)
    nc.createDimension('grid_corners', 4)
    nc.createDimension('grid_rank', 2)

    nc.createVariable('grid_dims', 'i4', ('grid_rank'))
    nc.variables['grid_dims'].long_name = 'grid size along x and y axis'
    nc.variables['grid_dims'].units = 'None'
    nc.variables['grid_dims'][:] = [(Lp, Mp)]

    nc.createVariable('grid_center_lon', 'f8', ('grid_size'))
    nc.variables['grid_center_lon'].long_name = 'longitude of cell center'
    nc.variables['grid_center_lon'].units = 'degrees'
    nc.variables['grid_center_lon'][:] = grid_center_lon

    nc.createVariable('grid_center_lat', 'f8', ('grid_size'))
    nc.variables['grid_center_lat'].long_name = 'latitude of cell center'
    nc.variables['grid_center_lat'].units = 'degrees'
    nc.variables['grid_center_lat'][:] = grid_center_lat

    nc.createVariable('grid_imask', 'i4', ('grid_size'))
    nc.variables['grid_imask'].long_name = 'mask'
    nc.variables['grid_imask'].units = 'None'
    nc.variables['grid_imask'][:] = grid_imask

    nc.createVariable('grid_corner_lon', 'f8', ('grid_size', 'grid_corners'))
    nc.variables['grid_corner_lon'].long_name = 'longitude of cell corner'
    nc.variables['grid_corner_lon'].units = 'degrees'
    nc.variables['grid_corner_lon'][:] = grid_corner_lon

    nc.createVariable('grid_corner_lat', 'f8', ('grid_size', 'grid_corners'))
    nc.variables['grid_corner_lat'].long_name = 'latitude of cell corner'
    nc.variables['grid_corner_lat'].units = 'degrees'
    nc.variables['grid_corner_lat'][:] = grid_corner_lat

    nc.close()

