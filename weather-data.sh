#!/bin/bash
# Script to extract the daily forecast data from weather.log
# There are usually two records for each day. The first is the forecast, 
# the second the actual. We want the actual
awk -F, '{if ($1!=prevdate) print prevdata; prevdate=$1; prevdata=$0}' Data/weather.log
