# Auction-Social-Advertising
Code for the WSDM 2020 submission "Truthful Auctions with Budget Constraints for Social Advertising"

Usage:

python Code/auction.py -p [path to input data] -s [file with influence data] -a [file with advertiser data] -i [number of iterations] -o [path for output]

Example:

python Code/auction.py -p Flixster/ -s influence_10_iterations_top.csv -a value=random(0.5,2).csv -i 100 -o Results/results_flixster.csv
