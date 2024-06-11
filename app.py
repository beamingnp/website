import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="ICD-O Code Browser", layout="wide")

# Load the Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('C:/Users/user/Downloads/chatbot/icd/pregnancy ICD10-1.xlsx')
        return df
    except FileNotFoundError:
        st.error("Error: Excel file not found.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Main application
def main():
    st.title("ICD-O Code Browser")

    # Load the data from the Excel file
    df = load_data()

    if df is not None:
        # Introduction section
        st.header("Introduction to ICD-O")
        st.write("The International Classification of Diseases for pregnancy (ICD-O) is a system used for coding and classifying pregnancy diagnoses.")

        # Download the PDF file
        st.write("### Download the alphabetic list")
        st.download_button(
            label="Download PDF",
            data=open('C:/Users/user/Downloads/book-3-icd-94-2blak-581-586.pdf', 'rb').read(),
            file_name="book-3-pregnancy.pdf",
            mime="application/pdf"
        )

        # Alphabetic list and search bar section
        st.header("Browse ICD-O Codes")

        # Create a selectbox for the user to choose a column
        selected_column = st.selectbox("Select a column to browse:", ["Code", "Persian", "Explanation"])

        # Create a search bar for the user to enter a keyword
        search_keyword = st.text_input(f"Enter a keyword to search in column '{selected_column}':")

        # Initialize the filtered DataFrame
        filtered_df = pd.DataFrame()

        # Filter the DataFrame based on the user's search
        if search_keyword:
            if selected_column == "Code":
                filtered_df = df[df["Code"].str.contains(search_keyword, case=False, na=False)]
                filtered_df = filtered_df.dropna(subset=["Code"])  # Remove rows with null values in the "Code" column
            else:
                filtered_df = df[df[selected_column].str.contains(search_keyword, case=False, na=False)]

        # Display the results
        if not filtered_df.empty:
            st.write("Results:")
            combined_explanations = {}
            for index, row in filtered_df.iterrows():
                code = row['Code']
                if code not in combined_explanations:
                    combined_explanations[code] = {
                        'Persian': [],
                        'Explanation': []
                    }
                if not pd.isna(row['Persian']):
                    combined_explanations[code]['Persian'].append(row['Persian'])
                combined_explanations[code]['Explanation'].append(row['Explanation'])
            for code, explanations in combined_explanations.items():
                st.write(f"### Code: {code}")
                if explanations['Persian']:
                    st.write("### Persian:")
                    for persian in explanations['Persian']:
                        st.write(f"{persian}")
                st.write("### Explanation:")
                for explanation in explanations['Explanation']:
                    st.write(f"{explanation}")
                st.write("---")
        else:
            st.write(f"No results found for '{search_keyword}' in column '{selected_column}'.")

main()