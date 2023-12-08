import json
import pickle

import customtkinter
import yaml

from TextAnimation import Animation
from YAMLTools import YamlTools
from utils import utilsLLM

util = utilsLLM()
yamlreset = YamlTools()
yamlreset.GetYaml()


def setContext():
    Context.delete(1.0, customtkinter.END)
    load = CurrContext.get()
    type = StructuredType.get()
    # ["Collector", "Credential", "Target"]
    if load.strip() == "Collector":
        with open(
            r"C:\Users\SS17\PycharmProjects\NLTKGenerateConfig\Showcase\CurrentConfig\SampleCollection.pickle",
            "rb",
        ) as conf:
            dict = pickle.load(conf)
    elif load.strip() == "Credential":
        with open(
            r"C:\Users\SS17\PycharmProjects\NLTKGenerateConfig\Showcase\CurrentConfig\SampleCredential.pickle",
            "rb",
        ) as conf:
            dict = pickle.load(conf)
    elif load.strip() == "Target":
        with open(
            r"C:\Users\SS17\PycharmProjects\NLTKGenerateConfig\Showcase\CurrentConfig\SampleTarget.pickle",
            "rb",
        ) as conf:
            dict = pickle.load(conf)
    if type.strip() == "json":
        Context.insert("end", json.dumps(dict, indent=4, sort_keys=True))
    elif type.strip() == "yaml":
        Context.insert("end", yaml.dump(dict, indent=4, sort_keys=True))


def AskQuestion():
    Question = str(textInput.get())
    ta.textAnimation("Question \ts" + Question)
    quests = Question.split("$")
    for Quest in quests:
        util.AskQuestionAndProcess(question=Quest)


# mainwinWinBg = customtkinter.CTkImage(
#     Image.open("AIimg.gif")
# )  # make sure to add "/" not "\"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

mainwin = customtkinter.CTk()
mainwin.title("Collectify")

mainwin.geometry("800x600")
mainwin.config(background="black")
mainwin.minsize(850, 600)
mainwin.maxsize(850, 600)

ProcessLabel = customtkinter.CTkLabel(
    mainwin,
    text="",
    font=("Calibri", 16),
    compound="center",
    height=400,
    width=500,
)

Context = customtkinter.CTkTextbox(mainwin, font=("Calibri", 11), height=500, width=290)

textInput = customtkinter.CTkEntry(
    mainwin,
    font=("Calibri", 16),
    justify="left",
    # width=56,
    height=45,
    width=650
    # bg="purple",
    # fg="yellow",
    # disabledbackground="#1E6FBA",
    # disabledforeground="yellow",
    # highlightbackground="black",
    # highlightcolor="red",
    # highlightthickness=2,
    # bd=0,
    # relief=customtkinter.SUNKEN,
)

options = ["Collector", "Credential", "Target"]
CurrContext = customtkinter.StringVar()
CurrContext.set("Collector")
ShowSpecficContextDropDown = customtkinter.CTkOptionMenu(
    mainwin, variable=CurrContext, values=options, width=100
)
ShowSpecficContextDropDown.configure(font=("Calibri", 11))

Structoptions = ["yaml", "json"]
StructuredType = customtkinter.StringVar()
StructuredType.set("yaml")
StructuredTypeDropDown = customtkinter.CTkOptionMenu(
    mainwin, variable=StructuredType, values=Structoptions, width=100
)
StructuredTypeDropDown.configure(font=("Calibri", 11))


Done = customtkinter.CTkButton(mainwin, text="Done", command=AskQuestion)
# img = customtkinter.CTkImage(Image.open("GONew.png"))  # make sure to add "/" not "\"
# Done.configure(image=img)

referesh = customtkinter.CTkButton(mainwin, text="Refresh", command=setContext)
# Refimg = customtkinter.CTkImage(
#     Image.open("Referesh.png")
# )  # make sure to add "/" not "\"
# referesh.configure(image=Refimg)

ProcessLabel.place(x=30, y=10)
textInput.place(
    x=30,
    y=535,
)
Done.place(x=700, y=540)
Context.place(x=550, y=10)
ShowSpecficContextDropDown.place(x=30, y=425)
StructuredTypeDropDown.place(x=150, y=425)
referesh.place(x=300, y=425)
ta = Animation(ProcessLabel, mainwin)


if __name__ == "__main__":
    Intro = """Hello, welcome to Collectify\nYou can do a lot of stuff here\nAsk me anything\nLike: In credential, set access_key_id as sumukhaS and set secret_access_key \nas AKIAIOSFODNN7EXAMPLE 
    and post a collection"""
    ta.textAnimation(Intro)
    mainwin.mainloop()
