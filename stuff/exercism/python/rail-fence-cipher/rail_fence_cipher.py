from itertools import cycle, chain

def fence_pattern(rail, size):
	zig = cycle(chain(range(rail), range(rail - 2, 0, -1)))
	return zip(zig, range(size))

def encode(message, rails):
	fence_mtr = fence_pattern(rails,len(message))
	return "".join(message[i] for _, i in sorted(fence_mtr))

def decode(encrypt, rails):
	fence = fence_pattern(rails,len(encrypt))
	fence_msg = zip(encrypt, sorted(fence))
	return "".join(char for char, _ in sorted(fence_msg, key=lambda item: item[1][1]))
