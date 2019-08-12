#%%
import pandas
from argparse import ArgumentParser
import seaborn as sns
import matplotlib.pyplot as plt


# default values
path = "Data/Results/"
input_filename = "results_synthetic.csv"
sns.set_palette(sns.color_palette(["#808080", "#000000", "#808080", "#000000"]))
method_order = ["RND", "EXT", "W-RND", "W-EXT"]


# parse command line arguments
parser = ArgumentParser()
parser.add_argument("-p", "--path", default=path)
parser.add_argument("-i", "--input", default=input_filename)
args = parser.parse_args()

path = args.path
input_filename = args.input


def convert_method(value):
    weighted = bool(value[0])
    mode = str(value[1])
    if weighted and mode == "extended":
        return "W-EXT"
    elif not weighted and mode == "extended":
        return "EXT"
    elif weighted:
        return "W-RND"
    else:
        return "RND"


def convert_setting(value):
    advertiser = value[0]
    spread = value[1]

    if "value=increasing" in advertiser:
        return "inverted"
    
    if "squared_diverse" in spread:
        return "diverse"
    else:
        return "random"


def convert_number_of_advertisers(value):

    advertiser = value[0]

    if advertiser.endswith("n=10.csv"):
        return 10
    if advertiser.endswith("n=50.csv"):
        return 50
    if advertiser.endswith("n=100.csv"):
        return 100
    if advertiser.endswith("n=500.csv"):
        return 500
    if advertiser.endswith("n=1000.csv"):
        return 1000


# prepare data
df = pandas.read_csv(path + input_filename)
df.rename(columns={"runtime_mean": "runtime (seconds)"}, inplace = True)
df["method"] = df[["weighted", "mode"]].apply(convert_method, axis=1)
df["setting"] = df[["advertisers", "spread"]].apply(convert_setting, axis=1)
df["number of advertisers"] = df[["advertisers"]].apply(convert_number_of_advertisers, axis=1)
df = df[["method", "setting", "number of advertisers", "runtime (seconds)"]]
df.drop_duplicates(subset=["method", "setting", "number of advertisers"], keep='first', inplace=True)
df = df.loc[df["setting"] == "random"]

print(df)


sns.set_context('paper', font_scale=1.8)
sns.set_style("whitegrid")

#fig, ax = plt.subplots()
#ax.set(xscale="log", yscale="log")
ax = sns.lineplot(x="number of advertisers", y="runtime (seconds)", hue="method", style="method", data=df, dashes=False, markers=True, markersize=12)
#g.set(yscale="log")
#g.set(xscale="log")
ax.set_xscale("log")
ax.set_yscale("log")

plt.ylim([0.0001,10000])
plt.xlim([8,1500])

# remove legend title
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:], labels=labels[1:], markerscale=2)


plt.tight_layout()
plt.show()
