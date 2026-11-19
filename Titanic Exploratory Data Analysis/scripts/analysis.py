# Task 2: Exploratory Data Analysis on Titanic Dataset

# Description:
# Dataset (Recommended): Titanic: Machine Learning from Disaster (Kaggle)
# Explore the classic Titanic dataset using Python
# Perform data cleaning: handle missing values, convert types
# Generate summary statistics and group-based insights (e.g., survival by gender/class)
# Visualize key patterns and correlations
# Tools & Libraries:
# Python Pandas Seaborn or Matplotlib
# Covered Topics
# EDA

# | Data types & missing data
# |
# Data visualization
# /-
# Bonus:
# Visualize survival rates using bar plots and heatmaps


import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

class Titanic:

    def __init__(self):
        self.df = pd.read_csv("../data/train.csv" ) 
    
    def explore_data(self,df):
        print(" \n -- rows", df.head(10))
        print("\n -- data types: ", df.dtypes)
        print("\n -- missing values: ", df.isnull().sum())
        print("\n -- duplicated values: ", df.duplicated().sum())
        print("\n -- desbive values: ", df.describe())

    
    def clean(self,df):
        ## replace the Nan age with mean age
        df["Age"] = df["Age"].fillna(df['Age'].mean())

        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
        df.drop(columns=["Cabin"], inplace=True)
        print(df.isnull().sum())
        # Convert data types
        df["Pclass"] = df["Pclass"].astype("category")
        df["Sex"] = df["Sex"].astype("category")
        df["Embarked"] = df["Embarked"].astype("category")

        ## identified age has  177 missing values Cabin has 687 and Embarked has  2

        ## What percentage of male and female passengers survived?
        
    def analyse_data(self, df):
        print("\nWhat percentage of male and female passengers survived?")

        # Male passengers
        males = df[df["Sex"] == "male"]
        males_survived = males[males["Survived"] == 1]

        print("Total males:", len(males))
        print("Males who survived:", len(males_survived))

        male_percentage = (len(males_survived) / len(males)) * 100
        print("Male survival percentage:", male_percentage)

        # Female passengers
        females = df[df["Sex"] == "female"]
        females_survived = females[females["Survived"] == 1]

        print("Total females:", len(females))
        print("Females who survived:", len(females_survived))

        female_percentage = (len(females_survived) / len(females)) * 100
        print("Female survival percentage:", female_percentage)

 
        ####the survival percentage for first-class passengers using the same approach you used for males and females?
        survival_by_class = (
            df.groupby("Pclass", observed=True)["Survived"].mean() * 100
        )

        first_class_percentage = survival_by_class.loc[1]
        second_class_percentage = survival_by_class.loc[2]
        third_class_percentage = survival_by_class.loc[3]

        print(f"First class: {first_class_percentage:.2f}%")
        print(f"Second class: {second_class_percentage:.2f}%")
        print(f"Third class: {third_class_percentage:.2f}%")

        ## survival percentage for passenager from each embarkiton port

        survival_port=(
            df.groupby("Embarked", observed=True)["Survived"].mean() * 100
        )
        print(survival_port.round(2))


        print(df["Embarked"])


        print("\n Average age of passengers who survived")
        survivors = df[df["Survived"] ==1]
        average_age = survivors["Age"].mean()
        print(f"Average age of survivors: {average_age:.2f}")

        print("\nAverage age of male survivors")
        average_male_age = males_survived["Age"].mean()
        print(f"Average male survivor age: {average_male_age:.2f}")

        print("\nAverage age of female survivors")
        average_female_age = females_survived["Age"].mean()
        print(f"Average female survivor age: {average_female_age:.2f}")



        print("\nWhich age group had the highest survival rate?")
        children = df[df["Age"] < 18]
        adults = df[(df["Age"] >= 18) & (df["Age"] < 60)]
        seniors = df[df["Age"] >= 60]

        # Calculate survival percentages
        children_percen = children["Survived"].mean() * 100
        adults_percen = adults["Survived"].mean() * 100
        seniors_percen = seniors["Survived"].mean() * 100

        # Display results
        print(f"Children survival rate: {children_percen:.2f}%")
        print(f"Adults survival rate: {adults_percen:.2f}%")
        print(f"Seniors survival rate: {seniors_percen:.2f}%")

        survival_age = {
        "Children": children_percen,
        "Adults": adults_percen,
        "Seniors": seniors_percen
        }

        highest_age_group = max(survival_age,key=survival_age.get)

        print("Age group with highest survival rate:", highest_age_group)
        # Store results for the bar charts
        self.survival_by_class = survival_by_class
        self.male_percentage = male_percentage
        self.female_percentage = female_percentage
        self.survival_port = survival_port
        self.survival_age = survival_age

    
    def visualise_data(self,df):

        fig, ax = plt.subplots(2, 2,figsize=(12, 9))

        ax[0,0].bar(
            self.survival_by_class.index, self.survival_by_class.values  

        )
        ax[0,0].set_title("Survival Rate by Passenger Class")
        ax[0,0].set_xlabel("Passenger Class")
        ax[0,0].set_ylabel("Survival Rate (%)")


        ax[0,1].bar( ["Male", "Female"],
            [self.male_percentage, self.female_percentage]

        )
        ax[0,1].set_title("Survival Rate by Gender")
        ax[0,1].set_xlabel("Gender")
        ax[0,1].set_ylabel("Survival Rate (%)")

        ax[1,0].bar(
            self.survival_port.index,  self.survival_port.values
        )
        ax[1,0].set_title("Survival Rate by Embarkation Port")
        ax[1,0].set_xlabel("Embarkation Port")
        ax[1,0].set_ylabel("Survival Rate (%)")

        ax[1,1].bar(
            self.survival_age.keys(),
            self.survival_age.values()
        )
        ax[1, 1].set_title("Survival Rate by Age Group")
        ax[1, 1].set_xlabel("Age Group")
        ax[1, 1].set_ylabel("Survival Rate (%)")








        plt.tight_layout()
       


        #### Correlation:

        correlation = df[["Survived", "Age", "Fare", "Pclass"]].astype(float).corr()
        print(correlation)
        # Create the heatmap
        plt.figure(figsize=(8, 6))

        sns.heatmap(correlation, annot=True, cmap="coolwarm")
        plt.title("Titanic Correlation Heatmap")
        plt.show()
                    


        



if __name__ == "__main__":
    analysis = Titanic()
    analysis.explore_data(analysis.df)
    analysis.clean(analysis.df)
    analysis.analyse_data(analysis.df)
    analysis.visualise_data(analysis.df)