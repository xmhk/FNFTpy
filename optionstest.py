from FNFTpy import *



o1 = get_kdvv_options()
print_kdvv_options(o1)
o1 = get_kdvv_options(dis=12)
print_kdvv_options(o1)


print ("########")
print_nsep_options()

#o2 = get_nsep_options(loc = 0)
# o2 = get_nsep_options(filt=0)
#o2 = get_nsep_options(bb=[-2,-2,2,2])
# o2 = get_nsep_options(maxev=3)
#o2 = get_nsep_options(nf=0)
#o2 = get_nsep_options(dis=4)
#print_nsep_options(o2)


print_nsev_options()
o3 = get_nsev_options(bsf=1)
o3 = get_nsev_options(bsl=1)
o3 = get_nsev_options(niter=1)
o3 = get_nsev_options(dst=1)
o3 = get_nsev_options(cst=1)
o3 = get_nsev_options(dis=1)
o3 = get_nsev_options(nf=0, dis=2, niter=None)

print_nsev_options(o3)