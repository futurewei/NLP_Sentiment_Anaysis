import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class voted_classifier:
	def __init__(self, *classifiers):
		self.classifier = classifiers


	def train(self, features):
		random.shuffle(features)
		len(features)
		training_data = features[:1900]
		testing_data = features[1900:]
		machine_addr = ["algorithm/MNB.pickle", "algorithm/Ber.pickle", "algorithm/Logits.pickle", "algorithm/SGD.pickle", "algorithm/LinearSVC.pickle"]
		counter =0
		for machine in self.classifier:
			machine.train(training_data)
			print (nltk.classify.accuracy(machine, testing_data)*100)
			save = open(machine_addr[counter], "wb")
			pickle.dump(machine, save)
			counter=counter+1

	def classify(self, data):
		testing_result= []
		for machine in self.classifier:
			testing_result.append(machine.classify(data))
		return mode(testing_result)

	def confidence(self, data):
		testing_result= []
		for machine in self.classifier:
			testing_result.append(machine.classify(data))
		votes = testing_result.count(mode(testing_result))
		return votes/len(testing_result)



short_pos = open("short_reviews/positive.txt","r", encoding='utf-8', errors='replace').read()
short_neg = open("short_reviews/negative.txt","r", encoding='utf-8', errors='replace').read()

# only keep adj, verb, adv

allowedType =["J", "R", "V"]
positive_set =[]
negative_set =[]
vocabs =[]
sentences =[]

for sentence in short_pos.split("\n"):
	sentences.append((sentence, "pos"))
	words = word_tokenize(sentence)
	form = nltk.pos_tag(words)
	for word in form:
		if word[1][0] in allowedType:
			vocabs.append(word[0].lower())

for sentence in short_neg.split("\n"):
	sentences.append((sentence, "neg"))
	words = word_tokenize(sentence)
	form = nltk.pos_tag(words)
	for word in form:
		if word[1][0] in allowedType:
			vocabs.append(word[0].lower())


statistics = nltk.FreqDist(vocabs)


vocab = list(statistics.keys())[:5000]

training_data=[]
for sentence, classification in sentences:
	words = word_tokenize(sentence)
	features ={}
	for word in words:
		if word in vocab:
			features[word] = True
		else:
			features[word]=False
	training_data.append([features , classification])


print ("haha")
print (len(training_data))


open_file=open("training_data/data.pickle", "wb")
pickle.dump(training_data,open_file)
open_file.close()

MNB = SklearnClassifier(MultinomialNB())
Ber = SklearnClassifier(BernoulliNB())
Logits = SklearnClassifier(LogisticRegression())
SGD = SklearnClassifier(SGDClassifier())
LinearSVC = SklearnClassifier(LinearSVC())

vote_machine = voted_classifier(MNB, Ber, Logits, SGD,LinearSVC)
vote_machine.train(training_data)
open_file = open("algorithm/vote.pickle", "wb")
pickle.dump(vote_machine, open_file)
open_file.close()
