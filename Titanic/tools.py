def survived(dataframe):
    return dataframe[dataframe["Survived"] == 1]

def died(dataframe):
    return dataframe[dataframe["Survived"] == 0]

def calculate_surv_rate(dataframe):
    s = survived(dataframe)
    d = died(dataframe)
    return len(s), len(d), len(s)/len(dataframe), len(d)/len(dataframe)

def from_port(dataframe, port):
    return dataframe[dataframe["Embarked"] == port]