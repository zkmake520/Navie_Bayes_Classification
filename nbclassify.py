import sys
# from math import log
import math
def main():
	argv = sys.argv
	try:
		modelFile = open(argv[1],'r')
	except Exception:
		print("Open file "+argv[1]+" failed")
		sys.exit(0)
	try:
		testFile = open(argv[2],'r')
	except Exception:
		print("Open file "+argv[2]+" failed")
		sys.exit(0)

	positiveReviewProba = 0
	negativeReviewProba = 0
	positiveWordDis = {}
	negativeWordDis = {}
	positiveWordCount = 0 #in case some word didn't exist in modelFile
	negativeWordCount = 0
	totalDocType = ""
	for idx,line in enumerate(modelFile):
		if idx == 0:
			tokens = line.rstrip("\n").rstrip('\r').split(":")

			positiveReviewProba = (float)(tokens[0])
			positiveWordCount = (int)(tokens[1])
			negativeWordCount = int(tokens[2])
			totalDocType = tokens[3]
			negativeReviewProba = 1 - positiveReviewProba
		else:
			tokens = line.rstrip("\n").rstrip('\r').split(" ")
			tokens = list(filter(None,tokens))
			iden = int(tokens[0])
			positiveWordDis[iden] = (float)(tokens[1])
			negativeWordDis[iden] = (float)(tokens[2])
	accuracy = 0
	rightCount = 0
	wrongCount = 0
	#compute precision
	positiveCorrectClassify = 0
	positiveTotalClassify = 0
	negativeCorrectClassify = 0
	negativeTotalClassify = 0

	#recall
	positiveActuallyClassify =0
	negativeActuallyClassify = 0

	docType = ""
	
	for line in testFile:
		tokens = line.rstrip("\n").rstrip('\r').split(" ")
		tokens = list(filter(None,tokens))
		prediction = 0
		positiveProba = math.log(positiveReviewProba) 
		negativeProba = math.log(negativeReviewProba)
		attitude = 0;	
		for idx,token in enumerate(tokens):
			# if idx == 0 and ":" not in token:
			# 	if token == 'HAM':
			# 		attitude = 1
			# 		docType = "EMAIL"
			# 	elif token == 'SPAM':
			# 		attitude = -1	
			# 		docType = "EMAIL"
			# 	elif token == 'POSITIVE':
			# 		attitude = 1
			# 		docType = "IMDB"
			# 	elif token == 'NEGATIVE':
			# 		attitude = -1	
			# 		docType = "IMDB"
			# 	else:
			# 		score = (int)(token)
			# 		if score >= 7:
			# 			attitude = 1
			# 			docType = "IMDB"
			# 		elif score <= 4:
			# 			attitude = -1
			# 			docType = "IMDB"
			if idx != 0 or (idx == 0 and ":" in token): 
				wordAndCount = token.split(":")
				word = (int)(wordAndCount[0])
				appearTimes = (int)(wordAndCount[1])
				p1 = positiveWordDis.get(word,1.0/positiveWordCount)
				p2 = negativeWordDis.get(word,1.0/negativeWordCount)
				positiveProba += math.log(p1)*appearTimes
				negativeProba += math.log(p2)*appearTimes
		if positiveProba > negativeProba:
			# positiveTotalClassify += 1
			# if(attitude == 1):
			# 	positiveCorrectClassify += 1
			# 	positiveActuallyClassify += 1
			# 	rightCount += 1
			# else:
			# 	negativeActuallyClassify += 1
			# 	wrongCount += 1
			if totalDocType == "imdb":
				print("POSITIVE")
			else:
				print("HAM")
		else:
			negativeTotalClassify += 1
			# if(attitude == -1):
			# 	negativeCorrectClassify += 1
			# 	negativeActuallyClassify += 1
			# 	rightCount += 1
			# else:
			# 	positiveActuallyClassify += 1
			# 	wrongCount += 1
			if totalDocType == "imdb":
				print("NEGATIVE") 
			else:
				print("SPAM")
	# precisionP = 1.0*positiveCorrectClassify/(positiveTotalClassify)
	# precisionN = 1.0*negativeCorrectClassify/(negativeTotalClassify)
	# recallP = 1.0*positiveCorrectClassify/positiveActuallyClassify
	# recallN = 1.0*negativeCorrectClassify/negativeActuallyClassify 
	# res.write("Precision Positive:" + str(precisionP) + "\n")
	# res.write("Precision Negative:" + str(precisionN)+"\n")
	# res.write("Recall Positive:" + str(recallP) +"\n")
	# res.write("Recall negative:" + str(recallN) +"\n")
	# res.write("F1 Positive:"+str(2*precisionP*recallP/(precisionP+recallP)) +"\n")
	# res.write("F1 Negative:"+str(2*precisionN*recallN/(precisionN+recallN)) +"\n")

if __name__ == "__main__":
	main()
