library(ncdf4)
library(maptools)

library(RColorBrewer)
library(lattice)
library(raster)
library(rasterVis)


url='http://opendap.renci.org:1935/thredds/dodsC/oedata/SSH.1440x720.20140917.nc'
url='http://mrtee.europa.renci.org:8080/thredds/dodsC/DataLayers/JPL.ECCO2.SSH.1440x720.20140917.nc'
#url='http://localhost:8080/thredds/dodsC/DBTest/netCDF/SSH.1440x720.20140917.nc'


nc=open.ncdf(url)

lon=ncvar_get(nc,"LONGITUDE_T")
# lon <- lon-180
lat=ncvar_get(nc,"LATITUDE_T")


ssh=ncvar_get(nc, "SSH") 

temp11 <- ssh[ , ] 

# plot as image
#image(lon,lat,temp11) 
#data(wrld_simpl)
#plot(wrld_simpl,add=TRUE)

# grid <- expand.grid(xlon=lon, ylat=lat)
# xyz <- cbind(grid, temp11)
# pj <- "+proj=lcc +lat_1=25.00 +lat_2=60.00 +lat_0=42.5 +lon_0=-100.00 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"

# rast.ssh <- rasterFromXYZ(xyz, crs=pj) 

f <- '/Users/bblanton/Desktop/Dropbox/bb/SSH.1440x720.20140917.nc'
b <- brick(f,package="raster")
library(maps)
library(mapdata)
library(mapproj)
map(database= "world", col="grey80", fill=TRUE, projection="gilbert", ylim=c(-90,90), xlim=c(-180,180), orientation= c(90,0,225))

