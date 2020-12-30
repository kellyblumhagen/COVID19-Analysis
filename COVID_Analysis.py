# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##########################################
############ PANDAS DATAFRAME ############
##########################################

# Read CSV file and create a Pandas dataframe
df = pd.read_csv("Resources/COVID19_data.csv")

# Replace NaN/blank entries with 0
df["COVID-19 Deaths"].fillna(0, inplace=True)

# Groupby "COVID-19 Deaths" to find total for each condition
df = df.groupby("Condition")["COVID-19 Deaths"].sum().reset_index()

# Convert "COVID-19 Deaths" column to integers
df["COVID-19 Deaths"] = df["COVID-19 Deaths"].astype("int")

# Rank totals deaths in descending order
df = df.sort_values(["COVID-19 Deaths"], ascending=False)

# Drop rows for "COVID-19" and "All other conditions and causes (residual)" - not helpful for determining top underlying conditionss
df = df.loc[~((df["Condition"] == "COVID-19") | (df["Condition"]
                                                 == "All other conditions and causes (residual)")), :]

# Reset index
df = df.reset_index(drop=True)

# Make index start with 1 (so that output dataframe will display rankings next to each condition)
df.index = df.index + 1

# Isolate top 10 conditions and create new variable to store new dataframe
top_10 = df.iloc[0:10].copy()

# Format totals in "COVID-19 Deaths" column with commas
top_10["COVID-19 Deaths"] = top_10["COVID-19 Deaths"].apply(lambda x: "{:,}".format(x))

# Save top_10 dataframe to csv file
df.to_csv("Output/Top_10_DataFrame.csv")


##########################################
########## MATPLOTLIB PIE CHART ##########
##########################################

#  Isolate the top 5 conditions to use for pie chart
top5 = df.iloc[0:5].copy()

# Save CONDITIONS for each of the top 5 conditions as list
conditions_top5 = top5["Condition"]

# Save DEATHS for each of the top 5 conditions as list
deaths_top5 = top5["COVID-19 Deaths"]

# Esthetics
colors = ["lightcoral", "gold", "lightskyblue", "red", "green"]
explode = (0.1, 0, 0)

#  Create pie chart
plt.pie(deaths_top5, labels=conditions_top5, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=250, radius=1.2)

# Chart title
plt.title("Top 5 Underlying Health Conditions for COVID-19 Deaths")

# Save chart
plt.savefig("Output/COVID_piechart.png")
