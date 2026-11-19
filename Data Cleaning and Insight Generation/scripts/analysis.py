
# Task 4: Data Cleaning and Insight Generation from Survey Data
# Dataset: Kaggle Data Science Survey 2017-2021
# Question: Which programming languages are most popular, and how does usage
# change by experience, job role and survey year?

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class SurveyAnalysis:

    def __init__(self):
        """Load the survey and choose 400 respondents (80 from each year)."""
        self.df = pd.read_csv("../data/kaggle_survey_2017_2021.csv", low_memory=False)

        #  The first row contains question descriptions What is your age (# years)? year not a person's answers.
        self.df = self.df[self.df["-"] != "Year"].copy()
        # convert years into number
        self.df["Year"] = pd.to_numeric(self.df["-"], errors="coerce")
        # remove rows where the yeara is misseing
        self.df = self.df.dropna(subset=["Year"])
        self.df["Year"] = self.df["Year"].astype(int)

        # Equal numbers per year make it easier to compare survey years.
        #  100 random respondents from each year
        self.df = self.df.groupby("Year").sample(n=100, random_state=42)
        print("Total respondents:", len(self.df))
        print("Dataset loaded. Respondents selected:", len(self.df))

    def explore_data(self, df):
        """Look at the rows, data types, missing values and duplicates."""
        print("\n--- FIRST FIVE ROWS ---")
        print(df[["Year", "Q5", "Q6", "Q8"]].head())
        print("\nDataset size:", df.shape)

        print("\nData types:")
        print(df[["Year", "Q5", "Q6", "Q8"]].dtypes)
        print("\nMissing values in important columns:")
        print(df[["Q5", "Q6", "Q8"]].isnull().sum())
        print("\nMissing values across all columns:", df.isnull().sum().sum())
        print("\nDuplicate rows:", df.duplicated().sum())
        print("\nRespondents by year:")
        print(df["Year"].value_counts().sort_index())

    def clean(self, df):
        """Remove duplicates, tidy labels and encode categories."""
        print("\n--- CLEANING DATA ---")
        before = len(df)
        df.drop_duplicates(inplace=True)
        print("Duplicates removed:", before - len(df))

        # Remove extra white space spaces. Empty answers stay missing: not selecting a
        # language is different from selecting it.
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].str.strip()
            df[column] = df[column].replace("", pd.NA)

        # Make similar job titles consistent across survey years.
        df["Job_Role"] = df["Q5"].replace({
            "Software Developer/Software Engineer": "Software Engineer",
            "Programmer": "Software Engineer",
            "Scientist/Researcher": "Research Scientist",
            "Researcher": "Research Scientist",
            "Currently not employed": "Not employed"
        })
        df["Job_Role"] = df["Job_Role"].fillna("Unknownmissing")


        print("\nProgramming experience answers:")
        print(df["Q6"].unique())

        # Put different experience answers into simpler groups.
        experience = {
            "I have never written code": "No experience",
            "I have never written code before": "No experience",
            "< 1 years": "Beginner", "< 1 year": "Beginner",
            "Less than a year": "Beginner", "1-2 years": "Beginner",
            "1 to 2 years": "Beginner", "1-3 years": "Beginner",
            "3-5 years": "Intermediate", "3 to 5 years": "Intermediate",
            "5-10 years": "Intermediate", "6 to 10 years": "Intermediate",
            "10-20 years": "Experienced", "10 to 20 years": "Experienced",
            "20+ years": "Experienced", "20 or more years": "Experienced"
        }
        df["Experience"] = df["Q6"].map(experience).fillna("Unknown")

        # Label encoding: keep readable categories and create number codes.
        df["Experience_Code"] = df["Experience"].map({
            "No experience": 0, "Beginner": 1,
            "Intermediate": 2, "Experienced": 3, "Unknown": 4
        })
        df["Job_Code"] = df["Job_Role"].astype("category").cat.codes

        # Find the columns for the multi-choice programming-language question.
        self.language_columns = [
            col for col in df.columns
            if col.startswith("Q7_Part_") or col == "Q7_OTHER"
        ]
        print("\nExperience groups:")
        print(df["Experience"].value_counts())
        print("\nProgramming language columns found:", len(self.language_columns))
        print("Rows after cleaning:", len(df))
        df.to_csv("../data/task4_cleaned_500.csv", index=False)


    ########################################################################################

    def analyse_data(self, df):
        """Compare language usage overall, by experience, job and year."""
        print("\n--- PROGRAMMING LANGUAGE USAGE ANALYSIS ---")

        # Q7 allows several answers. A blank cell means the option wasn't chosen.
        # Only include people who selected at least one Q7 option from langaueg columns
        answered = df[df[self.language_columns].notna().any(axis=1)].copy()
        print("Particiapnts who answered Q7:", len(answered))
        print("Q7 particiapnts by year:")
        print(answered["Year"].value_counts().sort_index())

        # Turn the separate language columns into one list rather than mutliple.
        programming_languages = answered.melt(
            id_vars=["Year", "Experience", "Job_Role"],
            value_vars=self.language_columns, value_name="Language"
        )

        # removing missing, extra space and none other etc.
        programming_languages = programming_languages.dropna(subset=["Language"])
        programming_languages["Language"] = programming_languages["Language"].str.strip()
        programming_languages = programming_languages[
            ~programming_languages["Language"].isin(["None", "Other", ""])
        ]

        print("\nWhich programming languages are most common?")
        self.top_languages = programming_languages["Language"].value_counts().head(5)
        print(self.top_languages)
        print("\nPercentage of Q7 respondents using each top language:")
        print((self.top_languages / len(answered) * 100).round(1))

        # Percentages use the number of people in each group as denominator.
        # One person may choose multiple languages, so totals can exceed 100%.
        top_five_languages = self.top_languages.index.tolist()

        self.by_experience = self.group_percentages(
            answered, programming_languages, "Experience", top_five_languages
        )
        print("\nTop languages by programming experience (%):")
        print(self.by_experience.round(1))

        # Find the five most common job roles
        self.common_techjob = answered["Job_Role"].value_counts().head(5).index.tolist()

        # Compare programming languages by job role
        self.by_job = self.group_percentages(
            answered, programming_languages, "Job_Role", top_five_languages
        ).reindex(self.common_techjob)

        print("\nTop languages by job role (%):")
        print(self.by_job.round(1))

        # Compare programming languages by year
        self.by_year = self.group_percentages(
            answered, programming_languages, "Year", top_five_languages
        )

        print("\nTop languages by survey year (%):")
        print(self.by_year.round(1))

        # Q8 is a separate question about which language to learn first.
        print("\nMost recommended first language by year (Q8):")
        for year, group in df.dropna(subset=["Q8"]).groupby("Year"):
            print(year, "-", group["Q8"].value_counts().index[0])

        self.top_languages.to_csv("task4_top_languages.csv")
        self.by_year.to_csv("..data/task5_languages_by_year.csv")

    def group_percentages(self, answered, programming_languages, group_column, top_five_languages):
        """Find the percentage of people using each language in each group."""

        # Only keep the five most popular programming languages
        counts = programming_languages[
        programming_languages["Language"].isin(top_five_languages)
        ]

        # Count how many times each language was selected in each group
        # For example, how many beginners selected Python or SQL
        counts = counts.groupby([group_column, "Language"]).size().unstack(fill_value=0)

        # Count how many people answered Q7 in each group
        # For example, the total number of beginners who answered
        group_sizes = answered.groupby(group_column).size()

        # Divide the language counts by the number of people in each group
        # Multiply by 100 to get percentages
        # Keep the top five languages and replace missing results with 0
        return counts.div(group_sizes, axis=0).mul(100).reindex(
            columns=top_five_languages
        ).fillna(0)

    def visualise_data(self, df):
        """Show four charts about programming language preferences."""
        print("\n--- CREATING CHARTS ---")
        fig, ax = plt.subplots(2, 2, figsize=(14, 10))

        ax[0, 0].bar(self.top_languages.index, self.top_languages.values)
        ax[0, 0].set_title("Most Used Programming Languages")
        ax[0, 0].set_ylabel("Number of selections")

        self.by_experience.plot(kind="bar", ax=ax[0, 1])
        ax[0, 1].set_title("Languages by Experience")
        ax[0, 1].set_ylabel("Respondents (%)")
        ax[0, 1].tick_params(axis="x", rotation=25)

        self.by_job.plot(kind="bar", ax=ax[1, 0])
        ax[1, 0].set_title("Languages by Job Role")
        ax[1, 0].set_ylabel("Respondents (%)")
        ax[1, 0].tick_params(axis="x", rotation=30)

        self.by_year.plot(marker="o", ax=ax[1, 1])
        ax[1, 1].set_title("Languages by Survey Year")
        ax[1, 1].set_ylabel("Respondents (%)")
        ax[1, 1].set_xlabel("Year")
        ax[1, 1].set_xticks(self.by_year.index.tolist())

        plt.tight_layout()
        plt.savefig("../data/task5_survey_charts.png", dpi=150)
        plt.show()
        print("Saved chart: task4_survey_charts.png")
        print("Saved cleaned data: task4_cleaned_500.csv")


if __name__ == "__main__":
    analysis = SurveyAnalysis()
    analysis.explore_data(analysis.df)
    analysis.clean(analysis.df)
    analysis.analyse_data(analysis.df)
    analysis.visualise_data(analysis.df)
