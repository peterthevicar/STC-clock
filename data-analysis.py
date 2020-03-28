#!/usr/bin/python3
"""
Analyse the data from the interrupt logger
"""
import sys # for stdin
import datetime
half_minute = datetime.timedelta(seconds=30)
dt_nearest_min_prev = None
err_data=[]
# Go through input a line at a time
for inline in sys.stdin:
    s = inline.split()
    fine_adjust = s[0]
    dt_actual = datetime.datetime.strptime(s[1]+" "+s[2], "%Y-%m-%d %H:%M:%S.%f")
    dt_nearest_min = (dt_actual + half_minute).replace(second=0, microsecond=0)
    # Only process if it's a different time and it's on the hour
    if dt_nearest_min != dt_nearest_min_prev and (dt_nearest_min.minute == 0):
        if dt_actual < dt_nearest_min:
            dt_diff = dt_nearest_min - dt_actual
            err_neg = True
        else:
            dt_diff = dt_actual - dt_nearest_min
            err_neg = False
        err = dt_diff.seconds + (dt_diff.microseconds / 1000000)
        if err_neg: err = -err
        # ~ print("actual:", dt_actual, "nearest:", dt_nearest_min, "err:", err)
        err_data.append([dt_nearest_min.time(), err])
        dt_nearest_min_prev = dt_nearest_min
# ~ print(err_data)
# Calculate average, omitting top and bottom extreme values as outliers
outlier_percent=5
out_start = int(len(err_data)*outlier_percent/100)
out_end = -out_start if out_start > 0 else None
sum_err = 0; n_err = 0; max_err = -100; min_err = 100
for dt_time, err in sorted(err_data, key=lambda err_data: err_data[1])[out_start:out_end]:
    if err > max_err: max_err=err
    if err < min_err: min_err=err
    sum_err += err
    n_err += 1
    print(dt_time, err)
avg_err = sum_err/n_err
print("\n\nn:",n_err, "out:",out_start)
print("avg:",avg_err)  
print("max:",max_err,"= avg +",max_err-avg_err) 
print("min:",min_err,"= avg -",avg_err-min_err)
print("max-min:", max_err - min_err)
    

