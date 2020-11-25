grain_filter_script.py: Used to filter grains.out to make file with only grains
above a manually set chi2 threshold

calc_stress.py: Calculates stress data (currently for Ti-7Al) and dumps it as
pickle files. Easily changed to be used for other materials.

read_data.py: Reads in filtered stress and strain data and makes a couple of
histograms for reasonability checks

check_data.py: Used to make histograms to check distribution of strain
components for reasonability

check_strain_spatial.py: Used to plot strain components in 2D to check spatial
distribution of strain components for reasonability

coaxiality.py: Calculates coaxiality angle. Macroscopic stress tensor goes on
line 43.
