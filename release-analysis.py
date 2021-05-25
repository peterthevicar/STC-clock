#!/usr/bin/python3
"""
Compare release data with interrupt data to find how long it takes from release to first strike
"""
import argparse # allow command line optioni to specify discarded outliers %
parser=argparse.ArgumentParser()
parser.add_argument("-s", "--suffix", help="file suffix, e.g. 2021-05-01", type=str, required=True)
args=parser.parse_args()

import sys # for stdin
import datetime
half_minute = datetime.timedelta(seconds=30)
i_nearest_min_prev=1; d_tot=0; d_n=0; d_max=-99; d_min=99
print(args.suffix)
print("Hour\tDelay from release to strike (s)")
with open('Data/interrupts.log.'+args.suffix, 'r') as interrupts:
	with open('Data/release.log.'+args.suffix, 'r') as release:
		i_line=interrupts.readline()
		r_line=release.readline()
		while i_line and r_line:
			# ~ print(i_line, r_line)
			i_s=i_line.split()
			i_actual = datetime.datetime.strptime(i_s[1]+" "+i_s[2], "%Y-%m-%d %H:%M:%S.%f")
			i_nearest_min = (i_actual + half_minute).replace(second=0, microsecond=0)
			r_s=r_line.split()
			r_actual = datetime.datetime.strptime(r_s[0]+" "+r_s[1], "%Y-%m-%d %H:%M:%S.%f")
			r_nearest_min = (r_actual + half_minute).replace(second=0, microsecond=0)
			# ~ print("i:",i_nearest_min,"r:",r_nearest_min)
			if i_nearest_min == r_nearest_min:
				if i_nearest_min != i_nearest_min_prev and i_nearest_min.minute == 0:
					i_nearest_min_prev = i_nearest_min
					diff = i_actual-r_actual
					diff_s = diff.seconds + (diff.microseconds / 1000000)
					print("{:02d}".format(i_nearest_min.hour),"\t"+"{:.3f}".format(diff_s))
					d_n+=1; d_tot+=diff_s
					d_max=max(d_max, diff_s); d_min=min(d_min, diff_s)
				r_line=release.readline()
				i_line=interrupts.readline()
			elif i_nearest_min > r_nearest_min:
				r_line=release.readline()
			else:
				i_line=interrupts.readline()
print("Average delay from release to strike:","{:.2f}".format(d_tot/d_n))
print("Max delay:","{:.2f}".format(d_max),"Min delay:","{:.2f}".format(d_min),"Variation:","{:.2f}".format(d_max-d_min))
