import random, math, time

BIT_COUNT = 256

def milli_rabbin_test(n):
	if not(n & 1) or n % 3 == 0 or n % 5 == 0 or n % 7 == 0 or n % 11 == 0:
		return False;
	s = 0
	d = n - 1
	while d % 2 == 0:
		d = d >> 1
		s += 1

	for k in range(n.bit_length()):
		a = random.randint(2, n - 2)
		x = pow(a % (n - 1), int(d), n)

		if(x == 1 or x == n - 1):
			continue

		for j in range(s - 1):
			x = (x * x) % n
			# print(x)
			if(x == 1):
				return False
			if(x == n - 1):
				break
		else:
			return False

	return True


def rand_prime(bit_count=10):
	bit_count -= 1
	rand_num = random.getrandbits(bit_count) | (1 << bit_count)
	while not(milli_rabbin_test(rand_num)):
		rand_num += 1
	return rand_num

def gcd(x, y):
	if x == 0:
		return y
	return gcd( y % x, x)

def mmi(a, m):
	"""modular multiplicative inverse
			a*x = 1 (mod m)
			return x
	"""
	t, newt = 0, 1
	r, newr = m, a
	while newr != 0:
		quotient = r // newr
		r, newr = newr, r - quotient * newr
		t, newt = newt, t - quotient * newt
	if r > 1:
		return("a is not invertible")
	if t < 0:
		t += m
	return t

if __name__ == '__main__':
	p = rand_prime(BIT_COUNT)
	q = rand_prime(BIT_COUNT)
	n = p * q
	t = (p - 1) * (q - 1)

	e = 65537
	while gcd(t, e) != 1:
		e = random.randint(1, t)

	d = mmi(e, t)
	print(d, e, t)
