#!/usr/bin/python3
"""
Analyse the data from the interrupt logger

Just to record the fact somewhere: when re-adjusting the COARSE adjustment
(the nut at the foot of the pendulum bob), one tick on the index seems to make about
2 seconds per day difference to the timing of the clock.
I had to adjust it down (slower) by 10 ticks to compensate for the fine adjust mechanism.
"""
import sys # for stdin
import datetime
half_minute = datetime.timedelta(seconds=30)
dt_nearest_min_prev = None
err_data=[]
# Go through input a line at a time
for inline in sys.stdin:
    s = inline.split()
    fine_adjust = float(s[0])
    dt_actual = datetime.datetime.strptime(s[1]+" "+s[2], "%Y-%m-%d %H:%M:%S.%f")
    dt_nearest_min = (dt_actual + half_minute).replace(second=0, microsecond=0)
    # Only process if it's a different time and it's on the hour (also half hour if ACCEPT_HALF is True)
    ACCEPT_HALF = False
    if dt_nearest_min != dt_nearest_min_prev and (dt_nearest_min.minute == 0 or (ACCEPT_HALF and dt_nearest_min.minute == 30)):
        if dt_actual < dt_nearest_min:
            dt_diff = dt_nearest_min - dt_actual
            err_neg = True
        else:
            dt_diff = dt_actual - dt_nearest_min
            err_neg = False
        err = dt_diff.seconds + (dt_diff.microseconds / 1000000)
        if err_neg: err = -err
        dt_secs = dt_nearest_min.timestamp()
        # ~ print("actual:", dt_actual, "nearest:", dt_nearest_min, "err:", err)
        err_data.append([fine_adjust, dt_secs, err])
        dt_nearest_min_prev = dt_nearest_min
print(err_data)
# Calculate average, omitting top and bottom extreme values as outliers
outlier_percent=5
out_start = int(len(err_data)*outlier_percent/100)
out_end = -out_start if out_start > 0 else None
sum_fa = 0
sum_err = 0; n_err = 0; max_err = -100; min_err = 100
sum_dt = 0
for fine_adjust, dt_secs, err in sorted(err_data, key=lambda err_data: err_data[1])[out_start:out_end]:
    sum_fa += fine_adjust
    if err > max_err: max_err=err
    if err < min_err: min_err=err
    sum_err += err
    sum_dt += dt_secs
    n_err += 1
    # ~ print(dt_secs, err)
avg_fa = sum_fa / n_err
avg_err = sum_err / n_err
avg_dt_secs = sum_dt / n_err
print("Data points:",n_err, ", Outliers discarded:",out_start)
print("  Average fine adjust:","{:.3f}".format(avg_fa))
print("  Average error:","{:.3f}".format(avg_err))
print("  Maximum error:","{:.3f}".format(max_err),"= average error +","{:.3f}".format(max_err-avg_err))
print("  Minimum error:","{:.3f}".format(min_err),"= average error -","{:.3f}".format(avg_err-min_err))
print("  Spread of values (max-min):", "{:.3f}".format(max_err - min_err))
# Now we know the average we can calculare the least-square slope
# Can't fit the curve with half hours included; the numbers are too jittery
if not ACCEPT_HALF:
    print("Fit line to data points")
    # ~ print("avg_dt_secs:", avg_dt_secs)
    sum_xy = 0; sum_x_sq = 0
    for fine_adjust, dt_secs, err in sorted(err_data, key=lambda err_data: err_data[1])[out_start:out_end]:
        sum_xy += (dt_secs - avg_dt_secs)*(err - avg_err)
        sum_x_sq += (dt_secs - avg_dt_secs)**2
    slope = sum_xy/sum_x_sq
    # convert from seconds per second to seconds per day
    slope = slope*60*60*24
    print("  Best fit error trend (seconds/day, positive means clock getting slower):", "{:.3f}".format(slope))
else:
    print("Not fitting line to data points because half hours are included")
