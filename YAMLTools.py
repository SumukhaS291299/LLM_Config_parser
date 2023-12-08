import json
import os
import pickle

import yaml

import Logger

keys = []


class YamlTools:
    def __init__(self):
        self.logger = Logger.StartLogging("YAMLTools")
        self.GetAllJson()

    @staticmethod
    def CheckCogencyColl(CollYaml):
        # TODO Add all values back to pickle and collector config...
        CollName = input(
            "Please enter a collection name as a recommendation\nYou cal leave it blank if you want to reuse the old name"
        )
        CollYaml["metadata"]["name"] = CollName
        if CollName.strip() == "":
            try:
                print("Tring to get the previous  collector name...")
                if CollYaml["metadata"]["name"] == "":
                    print("No value was found please enter new value")
                    CollName = input("Please enter a collection name ")
                    CollYaml["metadata"]["name"] = CollName
            except:
                print("Something went wrong when parsing Collection Name")

        try:
            print("SubType Selected as :" + CollYaml["spec"]["subType"])
            print("Collection are enabled :" + CollYaml["spec"]["enabled"])
        except:
            pass

    @staticmethod
    def CheckCogencyTGT(TgtYaml):
        print("Checking subType")
        try:
            if TgtYaml["spec"]["subType"] == "":
                print("Please enter the subType Value")
            else:
                print(
                    "Using subType as default",
                    TgtYaml["spec"]["subType"],
                )
        except:
            print("Warning.....")
            print("Something went wrong when assigning subType")

        print("Checking endpoint")
        try:
            if TgtYaml["spec"]["endpoint"] == "":
                print("Please enter the endpoint Value")
            else:
                print(
                    "Using endpoint as default",
                    TgtYaml["spec"]["endpoint"],
                )
        except:
            print("Warning.....")
            print("Something went wrong when assigning endpoint")

        print("Checking region")
        try:
            if TgtYaml["spec"]["context"]["region"] == "":
                print("Please enter the region Value")
            else:
                print(
                    "Using region as",
                    TgtYaml["spec"]["context"]["region"],
                )
        except:
            print("Warning.....")
            print("Something went wrong when assigning region")

    @staticmethod
    def CheckCogencyCred(CredYAML: dict):
        # ["spec.context.access_key_id","spec.context.secret_access_key"]
        print("Checking AccessKeyID")
        try:
            if CredYAML["spec"]["context"]["access_key_id"] == "AAAA00000000":
                print("Please enter the Access_key_id Value")
            else:
                print(
                    "Using Access_key_id as",
                    CredYAML.get("spec")["context"]["access_key_id"],
                )
        except:
            print("Warning.....")
            print("Something went wrong when assigning access_key_id")
        try:
            if CredYAML["spec"]["context"]["secret_access_key"] == "QWER/?123RTYASDF":
                print("Please enter the Secret_access_key Value")
            else:
                sec_key = CredYAML.get("spec")["context"]["secret_access_key"]
                print(
                    "Using secret_access_key as",
                    (len(sec_key) - 5) * "*" + sec_key[-6:],
                )
        except:
            print("Warning.....")
            print("Something went wrong when assigning access_key_id")

    @staticmethod
    def CheckCollectionCogency():
        with open(
            os.getcwd() + "\\CurrentConfig\\SampleCollection.pickle", "rb"
        ) as currConfg:
            CollYaml = pickle.load(currConfg)
        with open(
            os.getcwd() + "\\CurrentConfig\\SampleCredential.pickle", "rb"
        ) as currConfg:
            CredYaml = pickle.load(currConfg)
        with open(
            os.getcwd() + "\\CurrentConfig\\SampleTarget.pickle", "rb"
        ) as currConfg:
            TgtYaml = pickle.load(currConfg)

        print("Checking for value....")
        print("Checking Cred....")
        YamlTools.CheckCogencyCred(CredYaml)
        print("Checking Target....")
        YamlTools.CheckCogencyTGT(TgtYaml)
        print("Checking Collection....")
        YamlTools.CheckCogencyColl(CollYaml)
        print(CollYaml)
        print(CredYaml)
        print(TgtYaml)

    def GetAllJson(self):
        currDir = os.getcwd()
        SampleFiles = lambda path: currDir + "\\Samples\\" + path
        listSamples = os.listdir("Samples\\")
        self.allSampleFiles = list(map(SampleFiles, listSamples))

    def GetYaml(self):
        for samples in self.allSampleFiles:
            with open(samples, "r") as f:
                YAML = yaml.safe_load(f.read())
                self.logger.debug(samples)
                self.logger.debug(YAML)
                pickleName = samples.split("\\")[-1].split(".")[0] + ".pickle"
                self.logger.debug(f"Setting {samples} as :" + pickleName)
                with open(
                    os.getcwd() + "\\CurrentConfig\\" + pickleName, "wb"
                ) as currConfg:
                    pickle.dump(YAML, currConfg)
                self.logger.info(f"Written {samples} to {pickleName} successfully")

    # Common Keys ["tenant","type","displayLabel","namespace","spec","resourceVersion","subType","name","apiVersion","context","metadata"]

    def GetAllKeys(self, name: str, filePath: str):
        global keys
        keys = []
        with open(filePath, "r") as f:
            dict = yaml.safe_load(f.read())
        YamlTools.AllKeys(dict)
        # TODO Handel frequency and metricConfig:
        # handle()
        self.logger.info(keys)
        CommonRemove = [
            "tenant",
            "type",
            "displayLabel",
            "namespace",
            "spec",
            "resourceVersion",
            "subType",
            "apiVersion",
            "context",
            "metadata",
        ]
        for remCommon in set(CommonRemove):
            # print(remCommon in keys, remCommon)
            keys.remove(remCommon)
        with open(
            os.getcwd() + "\\CurrentConfig\\" + name + "KeyList" + ".pickle", "wb"
        ) as f:
            pickle.dump(keys, f)

    @staticmethod
    def AllKeys(dictitems: dict):
        global keys
        for key in dictitems.keys():
            if isinstance(dictitems[key], dict):
                keys.append(key)
                YamlTools.AllKeys(dictitems[key])
            else:
                keys.append(key)

    @staticmethod
    def ShowDict(fullDict: dict):
        print(json.dumps(fullDict, indent=4))

    @staticmethod
    def SaveChanges(fullDict: dict, type: str):
        if type == "credential":
            with open(
                os.getcwd() + "\\CurrentConfig\\SampleCredential.pickle", "wb"
            ) as f:
                pickle.dump(fullDict, f)
        elif type == "collector":
            with open(
                os.getcwd() + "\\CurrentConfig\\SampleCollection.pickle", "wb"
            ) as f:
                pickle.dump(fullDict, f)
        elif type == "target":
            with open(os.getcwd() + "\\CurrentConfig\\SampleTarget.pickle", "wb") as f:
                pickle.dump(fullDict, f)

    @staticmethod
    def ChangeValueFromKey(dictitems: dict, keyToChange: str, value):
        # print("VALUEEE", type(value))
        for key in dictitems.keys():
            if key == keyToChange:
                print(
                    key,
                    dictitems[key],
                    isinstance(dictitems[key], int),
                    isinstance(dictitems[key], str),
                )
                if isinstance(dictitems[key], int):
                    try:
                        dictitems[key] = int(value)
                    except:
                        try:
                            dictitems[key] = bool(value)
                        except:
                            pass
                elif isinstance(dictitems[key], str):
                    dictitems[key] = str(value)
            elif isinstance(dictitems[key], dict):
                YamlTools.ChangeValueFromKey(dictitems[key], keyToChange, value)
        return dictitems

    def ChangeYaml(self, type: str, key: str, value):
        dict = {}
        if type == "credential":
            with open("CurrentConfig\\SampleCredential.pickle", "rb") as f:
                dict = pickle.load(f)
            self.logger.debug(dict)
            dict = YamlTools.ChangeValueFromKey(dict, key, value)
            YamlTools.SaveChanges(dict, "credential")
            self.logger.debug("Saved file as CurrentCredential.pickle")
        elif type == "collector":
            with open("CurrentConfig\\SampleCollection.pickle", "rb") as f:
                dict = pickle.load(f)
            self.logger.debug(dict)
            dict = YamlTools.ChangeValueFromKey(dict, key, value)
            YamlTools.SaveChanges(dict, "collector")
            self.logger.debug("Saved file as CurrentCollection.pickle")
        elif type == "target":
            with open("CurrentConfig\\SampleTarget.pickle", "rb") as f:
                dict = pickle.load(f)
            self.logger.debug(dict)
            dict = YamlTools.ChangeValueFromKey(dict, key, value)
            YamlTools.SaveChanges(dict, "target")
            self.logger.debug("Saved file as CurrentTarget.pickle")
        YamlTools.ShowDict(dict)


#         ['apiVersion', 'type', 'metadata', 'name', 'namespace', 'resourceVersion', 'tenant', 'displayLabel', 'spec', 'subType', 'enabled',
#         'collectionModes', 'context', 'filterConfig', 'matchRegex', 'metricConfig', 'startTimeOffsetInSeconds', 'requestTimeoutInSeconds',
#         'appendConfigTags', 'granularity', 'targets']
