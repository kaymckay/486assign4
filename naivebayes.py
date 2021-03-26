# Kayla McKay (kaymckay)
import sys
import os
import math
from preprocessing import fillStopwords, removeSGML, tokenizeText, removeStopwords, stemWords



def trainNaiveBayes(directory, files, nums):
	# counts
	lies = 0
	trues = 0
	vocab = 0
	indexTrue = {}
	indexLie = {}
	vocab = []
	# preprocess files & tokenize training data
	for filename in files:
		with open(os.path.join(directory, filename), 'r') as f: 
			Lines = f.readlines()
			for line in Lines:
				line = removeSGML(line)
				tokens = tokenizeText(line)
				if tokens:
					# tokens = removeStopwords(tokens)
					# tokens = stemWords(tokens)
					for token in tokens:
						if token:
							if "true" in filename: 			
								if token in indexTrue:
									indexTrue[token] += 1
									trues += 1
								elif not token == '':
									indexTrue[token] = 1
									trues += 1
							else:
								if token in indexLie:
									indexLie[token] += 1
									lies += 1
								elif not token == '':
									indexLie[token] = 1
									lies += 1
							if not token in vocab:
								vocab.append(token)

	# N
	nums["LN"] = lies
	nums["TN"] = trues
	nums["V"] = len(vocab)

	# Probablity of category
	nums["P_L"] = float(nums["lie"]) / nums["total"]
	nums["P_T"] = float(nums["true"]) / nums["total"]

	# If token not in category
	nums["S_L"] = 1 / float(lies + len(vocab))
	nums["S_T"] = 1 / float(trues + len(vocab))

	# Calculate counts
	for word in indexLie:
		indexLie[word] = (indexLie[word] + 1) / float(lies + len(vocab))

	for word in indexTrue:
		indexTrue[word] = (indexTrue[word] + 1) / float(lies + len(vocab))

	return nums, indexTrue, indexLie



def testNaiveBayes(file, nums, indexTrue, indexLie):
	# Function that predicts the class (truth or lie) of a previously unseen document
	lie = math.log(nums["P_L"])			# num lie files / num files
	true = math.log(nums["P_T"])		# num true files / num files

	for word in file:

		# Calculate True
		if word in indexTrue:
			true += math.log(indexTrue[word])
		else:
			true += math.log(nums["S_T"])  	#  1 / float(num words in trues + vocab)

		# Calculate Lie
		if word in indexLie:
			lie += math.log(indexLie[word])
		else:
			lie += math.log(nums["S_L"])	# #  1 / float(num words in lies + vocab)

	if true > lie:
		return "true"
	return "lie"


def main(directory):
	files = []
	nums = {"true":0,"lie":0,"total":0}
	fillStopwords()

	#  open directory 
	for filename in os.listdir(directory):
		if "true" in filename:
			nums["true"] += 1
		else:
			nums["lie"] += 1
		nums["total"] += 1
		files.append(filename)


	count = 0
	nums["total"] -= 1
	outputs = {}
	accuracy = 0
	while count < nums["total"]:
		token = ""

		testfile = files[0]
		if "true" in testfile:
			nums["true"] -= 1
		else:
			nums["lie"] -= 1		

		files = files[1:]

		nums, indexTrue, indexLie = trainNaiveBayes(directory, files, nums)

		file = []
		with open(os.path.join(directory, testfile), 'r') as f:
			Lines = f.readlines()
			for line in Lines:
				line = removeSGML(line)
				tokens = tokenizeText(line)
				if tokens:
					# tokens = removeStopwords(tokens)
					# tokens = stemWords(tokens)
					for token in tokens:
						file.append(token)


		prediction = testNaiveBayes(file, nums, indexTrue, indexLie)
		outputs[testfile] = prediction

		if "true" in testfile and prediction == "true":
			accuracy += 1
		if "lie" in testfile and prediction == "lie":
			accuracy += 1
	
		files.append(testfile)
		if "true" in testfile:
			nums["true"] += 1
		else:
			nums["lie"] += 1
		count += 1

	print(float(accuracy) / nums["total"])	
	sys.stdout = open("naivebayes.output", "w")
	outputs = sorted(outputs.items(), key=lambda x: x[0])


	for out, val in outputs:
		print(out + " " + val)


					



if __name__ == '__main__':
    # run main
    # python naivebayes.py bestfriend.deception/
    main(sys.argv[1])







