import sys
def main():
	argv = sys.argv
	try:
		readin = open(argv[1],'r')
	except Exception:
		print("Open file "+argv[1]+" failed")
		sys.exit(0)
	try:
		output = open(argv[2],'w')
	except Exception:
		print("Open file "+argv[2]+" failed")
		sys.exit(0)
	res = []
	totalWordCount = 0
	positiveReviewCount = 0
	negativeReviewCount = 0

	positiveProbability = 0.0

	positiveWordCount = 0
	negativeWordCount = 0
	positiveWordDistribution = {} 
	negativeWordDistribution = {}
	docType = ""
	for line in readin:
		tokens = line.rstrip("\n").rstrip('\r').split(" ")
		tokens = list(filter(None,tokens))
		i = 0
		attitude = 0;
		for token in tokens:
			if i == 0:
				if token == 'HAM':	#email type
					attitude = 1
					positiveReviewCount += 1
					docType = "email"
				elif token == 'SPAM':
					attitude = -1
					negativeReviewCount += 1
					docType = "email"
				elif token == "POSITIVE":
					attitude = 1
					positiveReviewCount += 1
					docType = "imdb"
				elif token == "NEGATIVE":
					attitude = -1
					negativeReviewCount += 1
					docType = "imdb"
				else:
					docType = "imdb"
					score = (int)(token)
					if score >= 7:
						attitude = 1
						positiveReviewCount += 1
					elif score <= 4:
						attitude = -1
						negativeReviewCount += 1
					else:
						print(line+str(score))
						sys.exit(0)
			else:
				wordAndNum = token.split(":")
				identifier = (int)(wordAndNum[0])
				num = (int)(wordAndNum[1])
				if attitude == 1:
					positiveWordDistribution[identifier] = positiveWordDistribution.get(identifier,0) + num 
					positiveWordCount += num
				else:
					negativeWordDistribution[identifier] = negativeWordDistribution.get(identifier,0) + num 
					negativeWordCount += num
			i += 1
	positiveProbability = 1.0*positiveReviewCount/(positiveReviewCount+negativeReviewCount)				
	output.write(str(positiveProbability)+":"+str(positiveWordCount)+":"+str(negativeWordCount)+":"+docType+"\n");
	positiveKeys = set(positiveWordDistribution.keys())
	negativeKeys = set(negativeWordDistribution.keys())
	inNegativeNotInPositive = negativeKeys - positiveKeys
	totalKeys = list(positiveKeys) + list(inNegativeNotInPositive)
	for i in totalKeys:
		pProba = 1.0*(positiveWordDistribution.get(i,0)+1)/(positiveWordCount)
		nProba = 1.0*(negativeWordDistribution.get(i,0) +1)/(negativeWordCount)
		output.write(str(i) +" "+str(pProba)+" "+str(nProba)+"\n")

if __name__ == "__main__":
	main()