import transformers
from transformers import AutoTokenizer

import Logger


class Classifier:
    def __init__(self, quest: str, options: list):
        transformers.logging.set_verbosity_error()
        self.logger = Logger.StartLogging("Zero-Shot-Classification")
        self.quest = quest
        self.options = options

    def Classifier(self, model="facebook/bart-large-mnli"):
        self.logger.info(f"Using {model}")
        tokenizer = AutoTokenizer.from_pretrained(model, do_lower_case=True)
        pipline = transformers.pipeline(
            task="zero-shot-classification",
            tokenizer=tokenizer,
            model="facebook/bart-large-mnli",
        )

        classificationOut = pipline(self.quest, self.options)
        self.logger.debug(classificationOut)
        indexOfHighScore = classificationOut["scores"].index(
            max(classificationOut["scores"])
        )
        selectedClass = classificationOut["labels"][indexOfHighScore]
        self.logger.info(f"Selecting {selectedClass}")
        score = max(classificationOut["scores"])
        print(f"Selecting {selectedClass} with score {round(score*100,2)}%")
        return selectedClass
