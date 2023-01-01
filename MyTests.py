from emotion_recognition import EmotionRecognizer
from sklearn.svm import SVC

my_model = SVC()

rec = EmotionRecognizer(model=my_model, emotions=['positive', 'negative', 'neutral'], balance=True, verbose=0)

rec.train()

print("Test score:", rec.test_score())

print("Train score:", rec.train_score())

# rec.determine_best_model()
#
# print(rec.model.__class__.__name__, "is the best")
#
# print("Test score:", rec.test_score())
