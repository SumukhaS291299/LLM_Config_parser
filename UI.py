import json
import pickle
import tkinter

import yaml


# from utils


def setContext():
    Context.delete(1.0, tkinter.END)
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
    # utils


mainwin = tkinter.Tk()
mainwin.title("Next-Gen AI")

mainwinWinBg = tkinter.PhotoImage(file="AIimg.gif")  # make sure to add "/" not "\"

mainwin.geometry("800x600")
mainwin.config(background="black")
mainwin.minsize(850, 600)
mainwin.maxsize(850, 600)

ProcessLabel = tkinter.Label(
    mainwin,
    image=mainwinWinBg,
    text="Hello, welcome to Next-Gen-AI",
    borderwidth=3,
    font=("Calibri", 16),
    fg="orange",
    compound="center",
)

Context = tkinter.Text(
    mainwin,
    borderwidth=3,
    font=("Calibri", 11),
    fg="orange",
    background="black",
)

textInput = tkinter.Entry(
    mainwin,
    font=("Calibri", 16),
    justify="left",
    width=56,
    bg="purple",
    fg="yellow",
    disabledbackground="#1E6FBA",
    disabledforeground="yellow",
    highlightbackground="black",
    highlightcolor="red",
    highlightthickness=2,
    bd=0,
    relief=tkinter.SUNKEN,
)

options = ["Collector", "Credential", "Target"]
CurrContext = tkinter.StringVar()
CurrContext.set("Collector")
ShowSpecficContextDropDown = tkinter.OptionMenu(mainwin, CurrContext, *options)
ShowSpecficContextDropDown.config(bg="purple", font=("Calibri", 11), fg="orange")

options = ["yaml", "json"]
StructuredType = tkinter.StringVar()
StructuredType.set("yaml")
StructuredTypeDropDown = tkinter.OptionMenu(mainwin, StructuredType, *options)
StructuredTypeDropDown.config(
    bg="purple", font=("Calibri", 11), fg="orange", relief=tkinter.RAISED
)


Done = tkinter.Button(mainwin, relief=tkinter.RAISED, bg="gray", command=AskQuestion)
img = tkinter.PhotoImage(file="GONew.png")  # make sure to add "/" not "\"
Done.config(image=img)

referesh = tkinter.Button(
    mainwin, relief=tkinter.RAISED, bg="black", command=setContext
)
Refimg = tkinter.PhotoImage(file="Referesh.png")  # make sure to add "/" not "\"
referesh.config(image=Refimg)

ProcessLabel.place(x=30, y=10, height=400, width=500)
textInput.place(x=30, y=535, height=45, width=650)
Done.place(x=730, y=520)
Context.place(x=550, y=10, height=500, width=290)
ShowSpecficContextDropDown.place(x=30, y=400, width=100)
StructuredTypeDropDown.place(x=150, y=400, width=100)
referesh.place(x=300, y=405)


if __name__ == "__main__":
    mainwin.mainloop()
