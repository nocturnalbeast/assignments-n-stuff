def best_hands(hands):
	smp_hand = [sorted(i.split(" ")) for i in hands]
	for i in smp_hand:
		for j in i:
			print j[-1],j[:-1]


best_hands([
			"2S 2H 2C 8D JH",
			"4S AH AS 8C AD",
		])