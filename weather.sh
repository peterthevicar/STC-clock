#!/bin/bash
#Log today's and tomorrow's weather forecast for correlation analysis
JQFILTER="
.weather[0,1] |
.date, 
\",TMax,\", .maxtempC, 
\",TMin,\", .mintempC, 
\",TAvg,\", ([.hourly[].tempC | tonumber] | add/8),
\",SunH,\", .sunHour,
\",HAvg,\", ([.hourly[].humidity | tonumber] | add/8),
\",PAvg,\", ([.hourly[].pressure | tonumber] | add/8),
\"\n\""
curl -s wttr.in/Lymington?format=j1 | 
  jq -j "$JQFILTER"

