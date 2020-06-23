# Note format of Make rule
	# target file : dependencies
	# follow with an indented line that contains command to run in terminal

# Generate summary file
output/zonal_stats.csv : scripts/zonal_stats.py data/raw/boulder_county.shp data/raw/boulder_co_nlcd_2011.tif
	python scripts/zonal_stats.py data/raw/boulder_county.shp data/raw/boulder_co_nlcd_2011.tif > output/zonal_stats.csv

# Start replacing hard coded names 
#output/zonal_stats.csv : data/raw/boulder_county.shp data/raw/boulder_co_nlcd_2011.tif
	#python scripts/zonal_stats.py $^ > $@

# Download polygon file (note no dependency)
data/raw/boulder_county.shp :
	wget -q -nc https://ndownloader.figshare.com/files/14535518 -O data/raw/polygon.zip
	unzip data/raw/polygon.zip -d data/raw
	rm data/raw/polygon.zip

# Download raster file (note no dependency)
data/raw/boulder_co_nlcd_2011.tif :
	wget -q -nc https://ndownloader.figshare.com/files/14535515 -O data/raw/boulder_co_nlcd_2011.tif

# PHONY tells Make that this line does not build anything
# This line can be run as `make clean` to remove all files included below
# Recall that rm is the bash command to delete files (-f) or directories (-r) 
.PHONY : clean
clean :
	rm -r data/raw/*
	rm -f output/zonal_stats.csv
