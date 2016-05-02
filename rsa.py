from functools import partial
import random
import timeit

BIT_COUNT = 256
BLOCK_SIZE = (BIT_COUNT + BIT_COUNT) // 8

ENC_PATH = 'encrypt.bin'
DEC_PATH = 'dec_text.txt'

def milli_rabbin_test(n):
	if not(n & 1) or n % 3 == 0 or n % 5 == 0 or n % 7 == 0 or n % 11 == 0: return False
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
			if(x == 1):
				return False
			if(x == n - 1):
				break
		else:
			return False

	return True

def rand_prime(bit_count, not_allowed=[]):
	bit_count -= 1
	rand_num = random.getrandbits(bit_count) | (1 << bit_count)
	while not(milli_rabbin_test(rand_num)) or rand_num in not_allowed:
		rand_num += 1

	return rand_num

def randint_prime(min, max):
	rand_num = random.randint(min, max)
	while not(milli_rabbin_test(rand_num)):
		rand_num = random.randint(min, max)
	return rand_num

def gcd(x, y):
	if x == 0:
		return y
	return gcd( y % x, x)

def mmi(a, m):
	'''modular multiplicative inverse
			a*x = 1 (mod m)
			return x
	'''
	t, newt = 0, 1
	r, newr = m, a
	while newr != 0:
		quotient = r // newr
		r, newr = newr, r - quotient * newr
		t, newt = newt, t - quotient * newt
	if r > 1:
		return('a is not invertible')
	if t < 0:
		t += m
	return t

def encrypt(text_path, e, n):
	text = ''
	with open(text_path, 'r') as handle:
		for block in iter(partial(handle.read, BLOCK_SIZE), ""):
			text += block
	with open(ENC_PATH, 'wb+') as handle:
		for i in range(0, len(text), BLOCK_SIZE-1):
			sliced = text[i:i + min(len(text), BLOCK_SIZE-1)].encode()
			enc_block = pow(int.from_bytes(sliced, byteorder='big', signed=False), e, n)
			print(enc_block.to_bytes(BLOCK_SIZE, byteorder='big'))
			handle.write(enc_block.to_bytes(BLOCK_SIZE, byteorder='big'))

def decrypt(dec_path, dp, dq, p, q, qinv):
	dec = ''
	with open(ENC_PATH, 'rb') as handle:
		while True:
			read_block = handle.read(BLOCK_SIZE)
			if len(read_block) == 0: break
			enc_block = int.from_bytes(read_block, byteorder='big', signed=False)
			m1 = pow(enc_block, dp, p)
			m2 = pow(enc_block, dq, q)
			h = (qinv * (m1 - m2)) % p
			m = m2 + h * q
			dec_block = m.to_bytes((m.bit_length() // 8) + 1, byteorder='big').decode()
			dec += dec_block
	with open(dec_path, 'w') as handle:
		handle.write(dec)
	return dec

if __name__ == '__main__':
	p = rand_prime(BIT_COUNT)
	q = rand_prime(BIT_COUNT, not_allowed=[p])
	n = p * q
	t = (p - 1) * (q - 1)

	e = randint_prime(1, t)
	while gcd(t, e) != 1:
		e = randint_prime(1, t)

	d = mmi(e, t)
	dp = d % (p - 1)
	dq = d % (q - 1)
	qinv = mmi(q, p)

	encrypt('text.txt', e, n)
	dec = decrypt(DEC_PATH, dp, dq, p, q, qinv)
	print(dec)
