from cdms_utils.cdms_compat import *
import cdms_utils.var_utils as vu
import genutil as g

fin = cdms.open("/disks/archive/real/prob_land_cc/grid_box_25km/2060-2089/prob_land_cc_grid_box_25km_may_2060-2089_mslp_dmean_tmean_abs.nc")
v = fin("cdf_mslp_dmean_tmean_abs")

def p(v):
 print v.shape
 print v.getAxisIds()

p(v)

x = vu.cleverSqueeze(v)
p(x)

y = vu.cleverSqueeze(v, ["meaning_period"])
p(y)

print "SAME?"
d = y(squeeze=1) - x
p(d)
print g.minmax(d)
