#!/bin/bash
#Log today's and tomorrow's weather forecast for correlation analysis
JQFILTER="
.weather[0,1] |
.date, 
\",TMax,\", .maxtempC, 
\",TMin,\", .mintempC, 
\",TAvg,\", ((.maxtempC | tonumber)+(.mintempC | tonumber))/2,
\",SunH,\", .sunHour,
\"\n\""
curl -s wttr.in/Lymington?format=j1 | 
  jq -j "$JQFILTER" >>Data/weather.txt

