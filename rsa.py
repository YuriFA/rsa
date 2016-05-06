from functools import partial
from collections import namedtuple
from gen_prime import rand_prime, randint_prime, mmi, coprime
import sys
import timeit

BIT_COUNT = 256

TEXT_PATH = 'text.txt'
ENC_PATH = 'encrypt.bin'
DEC_PATH = 'dec_text.txt'

class Rsa():
	def __init__(self, bit_count):
		self.p = rand_prime(bit_count)
		self.q = rand_prime(bit_count, not_allowed=[self.p])
		self.block_size = (bit_count + bit_count) // 8
		self.generate_keys()

	def generate_keys(self):
		self.n = self.p * self.q
		t = (self.p - 1) * (self.q - 1)
		self.e = coprime(t)
		d = mmi(self.e, t)
		self.dp = d % (self.p - 1)
		self.dq = d % (self.q - 1)
		self.qinv = mmi(self.q, self.p)

	def encrypt(self, text_path, enc_path):
		text = ''
		with open(text_path, 'r') as handle:
			for block in iter(partial(handle.read, self.block_size), ""):
				text += block
		with open(enc_path, 'wb+') as handle:
			for i in range(0, len(text), self.block_size - 1):
				sliced = text[i:i + min(len(text), self.block_size - 1)].encode()
				enc_block = pow(int.from_bytes(sliced, byteorder='big', signed=False), self.e, self.n)
				print(enc_block.to_bytes(self.block_size, byteorder='big'))
				handle.write(enc_block.to_bytes(self.block_size, byteorder='big'))

	def decrypt(self, enc_path, dec_path):
		dec = ''
		with open(enc_path, 'rb') as handle:
			while True:
				read_block = handle.read(self.block_size)
				if len(read_block) == 0: break
				enc_block = int.from_bytes(read_block, byteorder='big', signed=False)
				m1 = pow(enc_block, self.dp, self.p)
				m2 = pow(enc_block, self.dq, self.q)
				h = (self.qinv * (m1 - m2)) % self.p
				m = m2 + h * self.q
				dec_block = m.to_bytes((m.bit_length() // 8) + 1, byteorder='big').decode()
				dec += dec_block
		with open(dec_path, 'w') as handle:
			handle.write(dec)
		return dec

def main():
	rsa = Rsa(BIT_COUNT)
	rsa.encrypt(TEXT_PATH, ENC_PATH)
	print(rsa.decrypt(ENC_PATH, DEC_PATH))
if __name__ == '__main__':
	sys.exit(main())
