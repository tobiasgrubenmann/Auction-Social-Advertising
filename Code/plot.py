#%%
import pandas
from argparse import ArgumentParser
import seaborn as sns
import matplotlib.pyplot as plt


DIGG_FLIXSTER_VALUE = "value=random(0.5,2).csv"
TOP_SPREAD = "influence_10_iterations_top.csv"
TOP_DIVERSE_SPREAD = "influence_10_iterations_top_diverse.csv"
RANDOM_SPREAD = "influence_10_iterations_random.csv"
RANDOM_DIVERSE_SPREAD = "influence_10_iterations_random_diverse.csv"
RANDOM_VALUE_10 = "value=random(0,1)_b=5000_n=10.csv"


# default values
path = "Data/Results/"
input_filename = "results_flixster.csv"
#input_filename = "results_digg.csv"
#input_filename = "results_synthetic.csv"
method_order = ["RND", "EXT", "W-RND", "W-EXT"]
setting_order = ["top-50", "top-50 damp.", "random", "random damp."]
#setting_order = ["synth. random", "synth. diverse", "synth. inverted"]


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
    elif weighted and mode == "random":
        return "W-RND"
    else:
        return "RND"


def convert_setting(value):
    advertiser = value[0]
    spread = value[1]
    
    if advertiser == DIGG_FLIXSTER_VALUE:
        if spread == TOP_SPREAD:
            return "top-50"
        elif spread == TOP_DIVERSE_SPREAD:
            return "top-50 damp."
        elif spread == RANDOM_SPREAD:
            return "random"
        elif spread == RANDOM_DIVERSE_SPREAD:
            return "random damp."
        else:
            return "unknow"
    else:
        if not advertiser.endswith("n=100.csv"):
            return "other"

        if "value=increasing" in advertiser:
            return "synth. inverted"
        
        if "squared_diverse" in spread:
            return "synth. diverse"
        else:
            return "synth. random"


# prepare data
df = pandas.read_csv(path + input_filename)
df["method"] = df[["weighted", "mode"]].apply(convert_method, axis=1)
df["setting"] = df[["advertisers", "spread"]].apply(convert_setting, axis=1)
revenue_df = df[["method", "setting", "revenue"]]
revenue_df["type"] = "revenue"
revenue_df.rename(columns={"revenue": "value"}, inplace = True)
sw_df = df[["method", "setting", "sw"]]
sw_df["type"] = "sw"
sw_df.rename(columns={"sw": "value"}, inplace = True)
df = pandas.concat([revenue_df, sw_df])

sns.set_context('paper', font_scale=1.3)
sns.set_style("whitegrid")
g = sns.FacetGrid(df, col="setting", col_order=setting_order, row="type", row_order=["revenue"])#, height=2, aspect=2)
g.map(sns.boxplot, "method", "value", order=method_order)

# change labels
axes = g.axes.flatten()
for i in range(len(setting_order)):
    # title of upper row
    axes[i].set_title(setting_order[i])
    # title of lower row should be empty
    # axes[i + len(setting_order)].set_title("")

axes[0].set_ylabel("Revenue ($)")
#axes[len(setting_order)].set_ylabel("Social Welfare ($)")

# remove x-label on lower row
for i in range(len(setting_order)):
    axes[i].set_xlabel("")

# rotate x-tick labels
for ax in axes:
    for label in ax.get_xticklabels():
        label.set_rotation(90)

# change to black and white
for ax in axes:
    for i,box in enumerate(ax.artists):
        box.set_edgecolor('black')
        box.set_facecolor('white')

        # iterate over whiskers and median lines
        for j in range(6*i,6*(i+1)):
            ax.lines[j].set_color('black')

plt.tight_layout()
plt.show()
