#!/usr/bin/env python3

import random
import sys


def intw(num):
    print(EnglishInteger(num))


class EnglishInteger:

	def __init__(self, newVal=0):
		self.setValue(newVal)
		self.translation = ["", "one", "two", "three", "four", "five", 
			"six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
			"fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

		self.translation_tens = ["error", "error", "twenty", "thirty", "fourty", "fifty",
		"sixty", "seventy", "eighty", "ninety"]

		self.big_translation = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion"]


	def setValue(self, newValue):
		if(isinstance(newValue, int)):
			self.val = newValue
		else:
			raise TypeError("Not an integer: " + str(newValue))


	def getValue():
		return self.val


	def __str__(self):

		if self.val == 0:
			return "zero"

		ans = ""
		v = self.val
		idx = 0
		while(v != 0):
			chunk = v % 1000
			if(chunk != 0):
				ans = self.comma_separated_chunk(chunk) + " " + self.big_translation[idx] + " " + ans
			idx = idx + 1
			v = v // 1000


		# hack to get rid of extra / erroneous spaces
		ans = ans.replace("  ", " ")
		return ans


	def comma_separated_chunk(self, i_chunk):
		s_chunk = str(i_chunk)
		if(len(s_chunk) > 3):
			raise ValueError("Must be at most a three digit chunk: " + s_chunk)

		elif(len(s_chunk) == 3):
			first_digit = int(s_chunk[0])
			ans = self.translation[first_digit] + " hundred " 
			ans = ans + self.comma_separated_chunk(int(s_chunk[1:]))
			return ans

		elif(len(s_chunk) == 2):
			#print("code block 2")
			if(i_chunk < len(self.translation)):
				#print("in translation: " + str(i_chunk))
				ans = self.translation[i_chunk] + " "
				return ans
			else:
				first_digit = int(s_chunk[0])
				ans = self.translation_tens[first_digit] + " "
				ans = ans + self.comma_separated_chunk(int(s_chunk[1:]))
				return ans

		elif(len(s_chunk) == 1):
			return self.translation[i_chunk]
	






# TODO: Move to proper unit-tests in tests/
def debug_tests():

	for i in range(100000):
		ei = EnglishInteger(i)
		#print("\n\n")
		print(str(i) + ": " + str(ei))


	print("-" * 20)
	for i in range(40):
		v = random.randint(0, 18446744073709551615)
		ei = EnglishInteger(v)
		print(str(v) + ": " + str(ei))


def main():
	#debug_tests()
	if(len(sys.argv) != 2):
		print("Improper Usage")
		sys.exit(1)

	user_input = sys.argv[1]
	user_input = user_input.replace(",", "")
	num = int(user_input)
	intw(num)


if __name__ == "__main__":
	main()



