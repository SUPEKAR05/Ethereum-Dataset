import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "Final Combined 1.csv"  # Update path if needed
df = pd.read_csv(file_path)

# Compute the correlation matrix for numerical features
corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()

# Set up the matplotlib figure
plt.figure(figsize=(15, 10))

# Draw the heatmap with a color map
sns.heatmap(corr_matrix, cmap="coolwarm", annot=False, fmt=".2f", linewidths=0.5)

# Set title
plt.title("Correlation Heatmap of Ethereum Transaction Features")

# Show the plot
plt.show()
