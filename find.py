'''
Find optimum combinations of components from a given 
selection.
'''
import e_series as _es

def find_res_parallel(r_target, series=_es.e24(1E-1, 10E6), n_min=2, n_max=2):
	'''
	Search for parallel combinations of resistors close 
	to the target resistance.
	
	r_target = target resistance.
	[series] = series to search.
	'''
	from basic import sum_inv
	return _finder(r_target, sum_inv, series, n_min, n_max)

def find_res_series(r_target, series=_es.e24(1E-1, 10E6), n_min=2, n_max=2):
	'''
	Search for series combinations of resistors close 
	to the target resistance.
	
	r_target = target resistance.
	[series] = series to search.
	'''
	from basic import sum
	return _finder(r_target, sum, series, n_min, n_max)
		
def find_cap_parallel(c_target, series=_es.e12(10E-12, 10E-6), n_min=2, n_max=2):
	'''
	Search for parallel combinations of capacitors close
	to the target capacitance.
	
	c_target = target capacitance.
	[series] = series to search.
	'''
	from basic import sum
	return _finder(c_target, sum, series, n_min, n_max)

def find_cap_series(c_target, series=_es.e12(10E-12, 10E-6), n_min=2, n_max=2):
	'''
	Search for series combinations of capacitors close
	to the target capacitance.
	
	c_target = target capacitance.
	[series] = series to search.
	'''
	from basic import sum_inv
	return _finder(c_target, sum_inv, series, n_min, n_max)

def find_pot_div(r_target, series=_es.e24(100, 100E3)):
	'''
	Search for a potential divider combination.
	
	r_target = target ratio.
	[series] = series to search.
	'''
	from basic import pot_div_ratio
	return _finder(r_target, pot_div_ratio, series, n_min=2, n_max=2)

def _finder(target, function, series, n_min=2, n_max=2, quiet=0):
	'''
	Combines the values listed in series using the function defined 
	by function and rates them by how close the combined value is 
	to the target value.
	
	target = target value.
	function = function with which to combine values.
	series = series to search.
	[n_min] = minimum number of combined values.
	[m_max] = maximum number of combined values.
	[quiet] = enables of disables printing.
	'''
	from si_prefix import si
	def _calc(*x):
		calc = function(*x)
		within = ((calc*100.0)/target)-100.0
		return (calc, within)
	if quiet == 0:
		print 'TARGET = ', si(target)
	x = []
	l = len(series)
	for n in range(n_min, n_max+1):
		for i in range(l**n):   
			xi = []
			for j in range(n):
				xi.append((i/(l**j))%l)
				if len(xi) > 1:
					if xi[-1] < xi[-2]:
						break
			else:
				x.append(tuple([series[xii] for xii in xi]))
	results = [_calc(*xi) + xi for xi in x]
	# result of line above leaves the within variable in column 1 of each tuple.
	within_index = 1
	results.sort(key=lambda x: abs(x[within_index]))
	if quiet == 0:
		for x in results[:min(15,len(results))]:
			print si(x[0]), '{0:.3f}% | '.format(x[1]).rjust(12),
			for y in x[2:]:
				print si(y),
			print ''
	return [x[2:] for x in results[:min(15,len(results))]]
