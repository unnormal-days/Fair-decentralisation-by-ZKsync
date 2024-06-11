import csv
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from colorama import Fore, Style

# Function to print stylized logos
def print_logos():
    print(f"{Fore.GREEN}{Style.BRIGHT}FAIR DECENTRALISATION")
    print(f"{Fore.RED}{Style.BRIGHT}powered by ZKsync{Style.RESET_ALL}\n")  # Add a newline here

# Print stylized logos
print_logos()

# Step 1: Read data from file
file_path = 'addresses.csv'  # Replace with your file path

addresses = []
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        address, reward = row[0], int(row[1])
        addresses.append((address, reward))

# Step 2: Sort by reward amount
addresses.sort(key=lambda x: x[1])

# Step 3: Categorize by reward amount
categories = {
    "0-2000": [],
    "2000-5000": [],
    "5000-10000": [],
    "10000-20000": [],
    "20000-50000": [],
    "50000+": []
}

for address, reward in addresses:
    if reward < 2000:
        categories["0-2000"].append((address, reward))
    elif 2000 <= reward < 5000:
        categories["2000-5000"].append((address, reward))
    elif 5000 <= reward < 10000:
        categories["5000-10000"].append((address, reward))
    elif 10000 <= reward < 20000:
        categories["10000-20000"].append((address, reward))
    elif 20000 <= reward < 50000:
        categories["20000-50000"].append((address, reward))
    else:
        categories["50000+"].append((address, reward))

# Step 4: Calculate total tokens
total_tokens = sum(reward for address, reward in addresses)

# Step 5: Calculate distribution by category
distribution = defaultdict(lambda: {"count": 0, "tokens": 0})
for category, entries in categories.items():
    distribution[category]["count"] = len(entries)
    distribution[category]["tokens"] = sum(reward for address, reward in entries)

# Step 6: Create a DataFrame for better visualization
data = []
for category, stats in distribution.items():
    count_percentage = (stats["count"] / len(addresses)) * 100
    token_percentage = (stats["tokens"] / total_tokens) * 100
    data.append([category, stats["count"], count_percentage, stats["tokens"], token_percentage])

df = pd.DataFrame(data, columns=["Category", "Wallet Count", "Wallet %", "Tokens", "Tokens %"])

# Function to colorize values
def colorize(value, category):
    if category in ["20000-50000", "50000+"]:
        return f"{Fore.RED}{value:.2f}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{value:.2f}{Style.RESET_ALL}"

# Apply colorize function to the DataFrame
df["Wallet %"] = df.apply(lambda x: colorize(x["Wallet %"], x["Category"]), axis=1)
df["Tokens %"] = df.apply(lambda x: colorize(x["Tokens %"], x["Category"]), axis=1)

# Print table with tabulate
print(f"{Fore.CYAN}Distribution by Categories:{Style.RESET_ALL}")
print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

# Step 7: Plot the data
plt.figure(figsize=(14, 7))
sns.barplot(x="Category", y="Wallet Count", data=df, hue="Category", palette="Blues_d", dodge=False, legend=False)
plt.ylabel("Wallet Count")
plt.twinx()
sns.lineplot(x="Category", y="Tokens %", data=df, marker='o', color='r', label="Token %")
plt.ylabel("Token %")
plt.title('Wallet and Token Distribution by Category')
plt.show()
