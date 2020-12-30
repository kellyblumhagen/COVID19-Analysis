# Imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

##########################################
############ PANDAS DATAFRAME ############
##########################################

# Read CSV file and create a Pandas dataframe
df = pd.read_csv("Resources/COVID19_data.csv")

# Change column heading "Number of Mentions" to "Total_Deaths" so it's more understandable
df.rename(columns={"Number of Mentions": "Total_Deaths"}, inplace=True)

# Convert "Total" column to float for aggregating
df["Total_Deaths"] = df["Total_Deaths"].str.replace(",", "").astype(float)

# Groupby "Total" to find total for each condition
df = df.groupby("Condition").Total_Deaths.sum().reset_index()

# Rank totals in descending order
df = df.sort_values("Total_Deaths", ascending=False)

# Reset index and make it start with 1 (instad of default 0)
df = df.reset_index(drop=True)
df.index = df.index + 1

# Drop first two rows/conditions of dataframe ("COVID-19" and "All other conditions and causes") - not helpful for analyzing conditionss
# Reset index
df = df.drop([df.index[0], df.index[1]]).reset_index(drop=True)

# Make index start with 1 (because displaying rank)
df.index = df.index + 1

# Save dataframe
df.to_csv("Output/Top_10_DataFrame.csv", index=False)

##########################################
########## MATPLOTLIB PIE CHART ##########
##########################################

#  Isolate the top 5 conditions to use for pie chart
top5 = df.iloc[0:5]

# Save NAMES for each of the top 5 conditions
names_top5 = top5["Condition"]

# Save TOTALS for each of the top 5 conditions
totals_top5 = top5["Total_Deaths"]

# Convert "Total" column to integer for pie chart calculatons
df["Total_Deaths"] = df["Total_Deaths"].astype(int)

# Esthetics
colors = ["lightcoral", "gold", "lightskyblue", "red", "green"]
explode = (0.1, 0, 0)

#  Create pie chart
plt.pie(totals_top5, labels=names_top5, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=250, radius=1.2)

# Chart title
plt.title("Most Common Underlying Health Conditions for COVID-19 Deaths")

# Save chart
plt.savefig("Output/COVID_piechart.png")

# Show chart
plt.show()
