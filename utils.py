import os

import Logger
from YAMLTools import YamlTools
from ZeroShotClassification import Classifier
from ZeroShotQAClassifier import ZeroQA

logger = Logger.StartLogging("LLMDemo")


class utilsLLM:
    def __init__(self):
        self.YT = YamlTools()
        # self.YT.CheckCollectionCogency()
        self.PreparePickle()

    def AskQuestionAndProcess(self, question: str):
        # question = input(
        #     "Ask me anything\nLike: In credential, set access_key_id as sumukhaS and set secret_access_key as AKIAIOSFODNN7EXAMPLE and post a collection\n"
        # )
        # for i in ["collector", "credential", "target"]:
        #     if i in question.split(",")[0].lower():
        #         break

        cla = Classifier(question.split(",")[0], ["collector", "credential", "target"])
        Sclass = cla.Classifier()
        ZSC = ZeroQA(Sclass)
        self.tasks = []
        for AllQuestList in utilsLLM.Processor(question):
            for task in AllQuestList:
                self.tasks.append(task)
        for task in self.tasks:
            if "post" in task.lower():
                print("I'll post a collection for you")
                # TODO 1)Add ops-monitoring-cli
                # TODO 2)OutPut as a graph!! ()Optional....
                os.chdir(
                    r"C:\Users\SS17\PycharmProjects\NLTKGenerateConfig\Showcase\bins"
                )
                # os.system("ops-monitoring-ctl.exe create -f SumukhaAssumeRole.yaml")
            else:
                ZSC.Classifier(task)

    @staticmethod
    def Processor(questions: str):
        tasks = []
        if "and" in questions:
            tasks = questions.split("and")
            logger.info(f"Queueing Questions {tasks}")
        else:
            tasks.append(questions)
        questall = []
        for i in tasks:
            quest = i.replace("and", "").strip()
            logger.debug("+" * 25 + quest)
            questall.append(quest)
        yield questall

    def PreparePickle(self):
        GetKeyFromfiles = os.listdir("Samples\\")
        for keyFile in GetKeyFromfiles:
            self.YT.GetAllKeys(
                keyFile.replace(".yaml", ""), os.getcwd() + "\\Samples\\" + keyFile
            )
