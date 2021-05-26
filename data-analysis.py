#!/usr/bin/python3
"""
Analyse the data from the interrupt logger

Just to record the fact somewhere: when re-adjusting the COARSE adjustment
(the nut at the foot of the pendulum bob), one tick on the index seems to make about
2 seconds per day difference to the timing of the clock.
I had to adjust it down (slower) by 10 ticks to compensate for the fine adjust mechanism.
"""
import argparse # allow command line optioni to specify discarded outliers %
parser=argparse.ArgumentParser()
parser.add_argument("-d", "--discard", help="percent of outliers to discard (top and bottom)", type=int, default=0)
parser.add_argument("-f", "--full", help="output full data, including extra information", action="store_true")
args=parser.parse_args()

import sys # for stdin
import datetime
half_minute = datetime.timedelta(seconds=30)
dt_nearest_min_prev = None
prev_err = 0
err_data=[]
# Go through input a line at a time
report_first=True
for inline in sys.stdin:
    s = inline.split()
    fine_adjust = float(s[0])
    dt_actual = datetime.datetime.strptime(s[1]+" "+s[2], "%Y-%m-%d %H:%M:%S.%f")
    dt_nearest_min = (dt_actual + half_minute).replace(second=0, microsecond=0)
    # Only process if it's a different time and it's on the hour (also half hour if ACCEPT_HALF is True)
    if dt_nearest_min != dt_nearest_min_prev and dt_nearest_min.minute == 0:
        if dt_actual < dt_nearest_min:
            dt_diff = dt_nearest_min - dt_actual
            err_neg = True
        else:
            dt_diff = dt_actual - dt_nearest_min
            err_neg = False
        err = dt_diff.seconds + (dt_diff.microseconds / 1000000)
        if err_neg: err = -err
        dt_secs = dt_nearest_min.timestamp()
        if report_first:
            print("First data point:", dt_nearest_min)
            report_first = False
        # ~ print("actual:", dt_actual, "nearest:", dt_nearest_min, "err:", err) # DEBUG
        cur_temp = float(s[3]) if len(s) >= 4 else -99
        err_data.append([dt_secs, dt_nearest_min, err, fine_adjust, cur_temp])
        dt_nearest_min_prev = dt_nearest_min
        prev_err = err
# ~ print(err_data) # DEBUG
"""
This part divides the data into two series, one for the chime-on-tick
and the other for chime-on-tock.
It does this by comparing the error for this datum with the previous point in each series,
if there's a big change in the error then it assumes the datum belongs in the other series.
Transients with a big error are discarded.
"""
margin_of_error = 0.7 # Anything outside this margin is considered likely to be in the other series
def calc_d(err_d, curr_e):
	if len(curr_e) > 0: # have previous data to compare with
		return(abs(err_d[2]-curr_e[-1][2]))
	else: # first point in this series so any point is on the margin
		global margin_of_error
		return margin_of_error
series=[{'err_data':[],'avg_err':0}, {'err_data':[],'avg_err':0}]
for err_d in err_data:
	# Compare this error with the previous one in each series
	d0=calc_d(err_d, series[0]['err_data'])
	d1=calc_d(err_d, series[1]['err_data'])
	# put it into the series which matches closer
	s,d = (0,d0) if d0<=d1 else (1,d1)
	if args.full: print("  ",err_d[1],"Error:","{:.2f}".format(err_d[2]),"d0:","{:.2f}".format(d0),"d1:","{:.2f}".format(d1),"Series:",s)
	# discard if it's a rogue point outside the margin of error for both series
	if min(d0,d1) > margin_of_error:
		if args.full: print("   **DISCARDED")
		# If the sereis has just one entry THAT may be the rogue, so clear just in case
		for s in (0,1):
			if len(series[s]['err_data'])==1:
				if args.full: print("   **Series",s,"cleared")
				series[s]['err_data']=[]
	else: # OK, add to the selected series
		series[s]['err_data'].append(err_d+[d0 if s==0 else d1])
	
"""
This part goes through working out how far out of line each point is by
calculating the average of d(prev) and d(next)
"""
for sn in 0,1:
	ed = series[sn]['err_data']
	for i in range(0, len(ed)-1):
		ed[i][5] = (ed[i][5] + ed[i+1][5]) / 2
	# Calculate average, omitting the values most-different-from-neighbours-either-side as outliers
	outlier_percent=args.discard
	n_outliers = int(len(ed)*outlier_percent/100)
	# ~ print("n_outliers", n_outliers)
	out_end = len(ed)-n_outliers
	series[sn]['sorted_ed']=sorted(ed, key=lambda ed: ed[5])[0:out_end]
	# Now work out the average error for the trimmed series
	sed = series[sn]['sorted_ed']
	tot_err=0
	for e in sed:
		tot_err += e[2]
	series[sn]['avg_err'] = tot_err/len(sed) if len(sed)>0 else 0
if args.full: print("Series 0:",len(series[0]['sorted_ed']), 
						"points, avg_err:","{:.2f}".format(series[0]['avg_err']),
					"  Series 1:",len(series[1]['sorted_ed']), 
						"points, avg_err:","{:.2f}".format(series[1]['avg_err']),
					"  Diff:","{:.2f}".format(abs(series[0]['avg_err']-series[1]['avg_err'])))
"""
Now we have the two series, we have to choose the one with the most data
to work out the trend, plus whether it's the fast or the slow series.
We're aiming to get the clock centred between the two series so the error
is never too bad (around 1s).
If there's only one series then use that as it is. This will cause a bit 
of 'hunting' when the clock is just switching between two and one series
however this won't happen often and only calls for a 1s per day adjustment.

adjust is added to the computed AVGERR before correcting the clock
so if we're using the slow series (more positive) adjust needs to be -ve,
for the fast series (more negative) +ve, and for a single series 0

"""
if len(series[1]['err_data'])<=2: # Almost all in a single series
	sn=0; adjust=0
else:
	# midway between 2 series. -ve if s0 is the fast series
	midway = 0.5 * (series[0]['avg_err']-series[1]['avg_err'])
	# if using s0 the midway sign will be inverted, if using s1 it will be OK
	sn, adjust = (0, -midway) if len(series[0]['sorted_ed']) > len(series[1]['sorted_ed']) else (1, midway)
if args.full: print("Using series", sn, "with", len(series[sn]['sorted_ed']), "data points and adjust set to", "{:.2f}".format(adjust))

"""
Now do the hard work of calculating the trend etc
"""
sorted_data = series[sn]['sorted_ed']
sum_fa = 0
sum_err = 0; n_err = 0; max_err = -100; min_err = 100
sum_dt = 0
sum_temp = 0; n_temp = 0
for dt_secs, dt_nearest_min, err, fine_adjust, cur_temp, err_diff in sorted_data:
	sum_fa += fine_adjust
	if err > max_err: max_err=err
	if err < min_err: min_err=err
	sum_err += err
	sum_dt += dt_secs
	if cur_temp != -99:
		sum_temp += cur_temp
		n_temp += 1
	n_err += 1
	# ~ print(dt_secs, err)
avg_err = sum_err / n_err
print("AVGER", "{:.3f}".format(avg_err+adjust), "(Average Error, positive means clock is slow.","{:.2f}".format(abs(adjust)), "subtracted" if adjust<0 else "added", "for tick/tock compensation)")
# Now we know the average we can calculate the least-square slope
avg_fa = sum_fa / n_err
avg_dt_secs = sum_dt / n_err
avg_temp = sum_temp / n_temp if n_temp > 0 else -99
# ~ print("avg_dt_secs:", avg_dt_secs)
sum_xy = 0; sum_x_sq = 0
for dt_secs, dt_nearest_min, err, fine_adjust, cur_temp, err_diff in sorted_data:
	sum_xy += (dt_secs - avg_dt_secs)*(err - avg_err)
	sum_x_sq += (dt_secs - avg_dt_secs)**2
slope = sum_xy/sum_x_sq
# convert from seconds per second to seconds per day
slope = slope*60*60*24
print("TREND", "{:.3f}".format(slope), "(Least squares trend, seconds/day, positive means clock getting slower)")
print("FINEA","{:.2f}".format(avg_fa),"(Average fine adjust setting)")
print("AVGTC","{:.2f}".format(avg_temp),"(Average temperature in clock case)")
print("  Maximum error:","{:.3f}".format(max_err),"= average error +","{:.3f}".format(max_err-avg_err))
print("  Minimum error:","{:.3f}".format(min_err),"= average error -","{:.3f}".format(avg_err-min_err))
print("  Spread of values (max-min):", "{:.3f}".format(max_err - min_err))
print("  Data points in series (including outliers): "+str(len(series[sn]['err_data']))+", Outliers "+"("+str(outlier_percent)+"% most different from neighbours) discarded:",str(len(series[sn]['err_data'])-len(series[sn]['sorted_ed'])))
