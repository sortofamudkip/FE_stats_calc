from random import randint

def levelup(growths: list) -> int: #returns how many stats were leveled
	sum_ = 0
	for x in growths:
		rand = randint(0,99)
		if rand < x: sum_ += 1
	return sum_

def test(growths: list, n: int):
	hits = [0 for i in range(len(growths)+1)]
	for i in range(n):
		hits[levelup(growths)] += 1
	total = sum(hits)
	return [x*1.0/total for x in hits]

def Q_val(X, Y):
	assert len(X) == len(Y)
	return sum([(X[i]-Y[i])**2/float(Y[i]) for i in range(len(X)) if Y[i] != 0])

def chi_square_test(X, Y): #tests at 95% confidence
	Q = Q_val(X, Y)
	print("Value of Q: {}".format(Q))
	return Q <= 14.07

def passes_monte_carlo(growths, calculated, n, print_result=False):
	actual = test(growths, n)
	if print_result:
		print("Expected:", ["{:.3f}".format(x) for x in calculated])
		print("Actual:  ", ["{:.3f}".format(x) for x in actual])
	return chi_square_test(actual, calculated)


# growths = [70,40,60,60,55,20,30]
# forumla_results = [0.75,5.76,18.07,30.77,27.23,13.58,3.49,0.35]

# if passes_monte_carlo(growths, forumla_results, 14721):
# 	print("Passed Monte Carlo Test with 95% confience rate")
# else:
# 	print("Failed Monte Carlo Test")


# results = test(growths, 14721)
# s = sum(results)
# for i in range(len(results)):
# 	print("{:2d}:  {:6.2f}%".format(i, 100.*results[i]/s))