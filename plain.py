def strip_down(text):
    return  " ".join(text.replace("\n", " ").split())



with open("autosave_plain.hoi4") as f:
    data = f.read()

data = strip_down(data)

