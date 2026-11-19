
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


class CustomerSegmentation:
    def __init__(self):
        self.df = pd.read_excel("../data/Online Retail.xlsx" )
        print(self.df.head())
    
    def explore(self):
        """Explore the dataset structure and data quality."""
        df = self.df

        print("\n--- DATASET OVERVIEW ---")
        print("\n-- First 10 rows:\n", df.head(10))
        print("\n-- Data types:\n", df.dtypes)
        print("\n - Column names: ", self.df.columns.tolist())
        print("\n-- Missing values:\n", df.isnull().sum())
        print("\n-- Missing values:\n", (df.isnull().mean() * 100).round(2))
        print("\n-- Duplicated rows:", df.duplicated().sum())
        print("\n-- Descriptive statistics:\n", df.describe())


        """ how much of MISSING customer ID HAS A VALID INVOICE"""
        missing_customers = df[df["CustomerID"].isnull()]
        valid_invoices = ~missing_customers["InvoiceNo"].astype(str).str.startswith("C")
        print("Valid invoice rows:", len(valid_invoices))

        ## check if values are posisve 
        print("Positive quantities:",
        (df["Quantity"] > 0).sum())

        print("Positive prices:",
            (df["UnitPrice"] > 0).sum())

        ## check unitprive negative
        print("\n Negative prices: ", (df["UnitPrice"]<0).sum())

        print(df[df["UnitPrice"] < 0])
        print("NO quantities:", (df["Quantity"] == 0).sum())
        print("Cost 0 :", (df["UnitPrice"] == 0).sum())
        print("Negative quantities:", (df["Quantity"] < 0).sum())
            
        #check invoicde date
        print("\nInvoiceDate type:", df["InvoiceDate"].dtype)

    
    def clean_data(self):
        """Clean the dataset before RFM analysis."""

        df = self.df.copy()

        ## remove missing customer ids

        df = df.dropna(subset=["CustomerID"])
        # Remove exact duplicate rows
        df = df.drop_duplicates()

        # Remove cancelled invoices
        df = df[
                ~df["InvoiceNo"].astype(str).str.startswith("C")
            ]

        # Keep positive quantities and prices
        df = df[
            (df["Quantity"] > 0) &
            (df["UnitPrice"] > 0)
        ]

        self.df = df

        print("Cleaned dataset shape:", self.df.shape)
        
    """ RFM Analysis)"""
    """ 
    - Recency (R): How recently a customer made a purchase (time since their last transaction). 
    - Frequency (F): How often a customer makes a purchase within a set period.
    -  Monetary Value (M): How much total money a customer spends on those purchases.
    
    """
    def Recency_frequency_Monetary(self):
        df = self.df.copy()
        reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
        print(reference_date)
        most_recent_purchase = df.groupby("CustomerID")["InvoiceDate"].max()
        recency = (reference_date - most_recent_purchase).dt.days
        # print(recency.head())
        frequency = df.groupby("CustomerID")["InvoiceNo"].nunique()
        # print(frequency.head())
        df["Total_price"] = df["Quantity"] * df["UnitPrice"]
        monetary = df.groupby("CustomerID")["Total_price"].sum()
        # print(monetary.head())
        self.r_f_m = pd.DataFrame({
            "Recency": recency,
            "Frequency": frequency,
            "Monetary": monetary
        })

        print(self.r_f_m.head())


    def assign_rfm_scores(self):
        rfm = self.r_f_m.copy()

        rfm["R_Score"] = pd.cut(
            rfm["Recency"],
            bins=[-1, 30, 60, 90, 180, float("inf")],
            labels=[5, 4, 3, 2, 1]
        )
        print(rfm.head())
        print("\n--- Assigning Frequency Scores ---")
        print("Customers who make more purchases receive higher scores.")

        rfm["fscore"]=pd.cut(
            rfm["Frequency"],
            bins=[0, 1, 3, 5, 10, float("inf")],
            labels=[1, 2, 3, 4, 5]
        )
        print("\n--- Customer Frequency Scores ---")
        print(rfm[["Frequency", "fscore"]].head())

        # Monetary scoring
        print("\n--- Assigning Monetary Scores ---")
        print("Customers who spend more money receive higher scores.")


        rfm["M_Score"] = pd.cut(
        rfm["Monetary"],
        bins=[0, 100, 500, 1000, 5000, float("inf")],
        labels=[1, 2, 3, 4, 5]
        )

        self.r_f_m = rfm
        print("\n--- Customer Monetary Scores ---")
        print(rfm[["Monetary", "M_Score"]].head())

    def segment_customers(self):
        rfm = self.r_f_m.copy()

        segments = []

        # Loop through each customer using their row number
        for i in range(len(rfm)):
            current_r = int(rfm.iloc[i]["R_Score"])
            current_f = int(rfm.iloc[i]["fscore"])
            current_m = int(rfm.iloc[i]["M_Score"])

            if current_r >= 4 and current_f >= 4:
                segments.append("Champions")

            elif current_f >= 3:
                segments.append("Loyal Customers")

            elif current_r <= 2:
                segments.append("At Risk")

            else:
                segments.append("Other Customers")

        rfm["Segment"] = segments

        print("\n--- Customer Segments ---")
        print(rfm[["R_Score", "fscore", "M_Score", "Segment"]].head())

        self.r_f_m = rfm
if __name__ == "__main__":
    customer = CustomerSegmentation()
    customer.explore()
    customer.clean_data()
    customer.Recency_frequency_Monetary()
    customer.assign_rfm_scores()
    customer.segment_customers()

