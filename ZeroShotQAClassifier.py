import os
import pickle
import re

import transformers
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
from transformers import AutoTokenizer

import HandleLowContext
import Logger
from YAMLTools import YamlTools
from ZeroShotClassification import Classifier


class ZeroQA:
    def __init__(self, PredectedClass):
        transformers.logging.set_verbosity_error()
        self.logger = Logger.StartLogging("Question Answering")
        self.PredectedClass = PredectedClass
        self.yamlTools = YamlTools()

    def Classifier(self, ProcessedQuestion: str, model="deepset/roberta-base-squad2"):
        self.logger.info(f"Using {model}")
        tokenizer = AutoTokenizer.from_pretrained(model, do_lower_case=True)
        pipline = transformers.pipeline(
            task="question-answering",
            tokenizer=tokenizer,
            model="deepset/roberta-base-squad2",
        )

        answer = pipline(
            context=ProcessedQuestion.replace("  ", " ")
            .replace("=", "to")
            .replace(",", ""),
            question="change to",
            # question="",
        )
        options = []
        # "collector", "credential", "target"
        if self.PredectedClass == "credential":
            with open(
                os.getcwd() + "\\CurrentConfig\\SampleCredentialKeyList.pickle", "rb"
            ) as optfile:
                options = pickle.load(optfile)
        elif self.PredectedClass == "collector":
            with open(
                os.getcwd() + "\\CurrentConfig\\SampleCollectionKeyList.pickle", "rb"
            ) as optfile:
                options = pickle.load(optfile)
                print("Processing all possible options: \n", *options)
        elif self.PredectedClass == "target":
            with open(
                os.getcwd() + "\\CurrentConfig\\SampleTargetKeyList.pickle", "rb"
            ) as optfile:
                options = pickle.load(optfile)
        cla = Classifier(
            ProcessedQuestion.replace("  ", " ").replace("=", "to").replace(",", ""),
            options,
        )
        KeyClass = cla.Classifier()

        self.logger.debug(answer)
        score = round(answer["score"], 6)
        self.logger.debug(score)
        self.logger.info(answer["answer"])
        self.CheckAnswerStyle(
            self.PredectedClass,
            ProcessedQuestion.replace("  ", " ").replace("=", "to").replace(",", ""),
            KeyClass,
            options,
            answer["answer"],
        )

    def CheckAnswerStyle(
        self, PredectedClass, questionAsked, KeyPredicted, opts, answerReciever: str
    ):
        self.logger.info("$" * 25 + "  " + answerReciever.replace("as", "to"))
        searchResult = re.match(r"(\w*) to (.*)", answerReciever)
        if searchResult != None:
            self.logger.debug(searchResult.group(0))
            self.logger.debug(searchResult.group(1))
        else:
            ansLength = len(answerReciever.split(" "))
            if ansLength == 1:
                self.logger.debug(answerReciever + " will be selected....")
                print(f"Setting {KeyPredicted} as {answerReciever}")
                self.yamlTools.ChangeYaml(
                    self.PredectedClass, KeyPredicted, answerReciever
                )
            else:
                self.logger.info("Very less context")
                print("Very less context to predict the right answer")
                # TODO What happens when less context is given -- We did'nt get that
                # We are able to get the following....
                # Create new window to parse error
                HandleLowContext.HandleError(
                    questionAsked=questionAsked,
                    PredictedClass=PredectedClass,
                    PredectedKey=KeyPredicted,
                )
                lemmatizer = WordNetLemmatizer()
                questionAskedLower = questionAsked.lower()
                words = word_tokenize(questionAskedLower)
                lemm = []
                SW = stopwords.words("english")
                SW.extend(
                    [
                        "cred",
                        "collector",
                        "credential",
                        "target",
                        "tgt",
                        "coll",
                        "as",
                        "in",
                        "put",
                        "set",
                        ",",
                        "and",
                        "or",
                        "initilize",
                        "fix",
                    ]
                )
                SW.extend(opts)
                for word in words:
                    if word in SW:
                        continue
                    else:
                        lemm.append(lemmatizer.lemmatize(word))
                print(lemm)
