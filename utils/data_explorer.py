import pandas as pd
from IPython.core.display import display, HTML

class DataExplorer:
    def __init__(self, path_data_or_df):
        # If the input is a string, assume it's a CSV file path
        if isinstance(path_data_or_df, str):
            try:
                # Attempt to load the CSV file
                self.path_data = pd.read_csv(path_data_or_df)
            except Exception as e:
                raise ValueError(f"Error loading the CSV file: {e}")
        # If the input is already a DataFrame, assign it directly
        elif isinstance(path_data_or_df, pd.DataFrame):
            self.path_data = path_data_or_df
        else:
            raise TypeError("The argument must be a CSV file path (str) or a pandas DataFrame")
          
    def get_head(self):
        # Return the first 5 rows
        return self.path_data.head()
    
    def group_columns_by_type(self):
        # Create a dictionary to store the columns grouped by data type
        grouped_types = {}
        
        # Iterate over each column and its data type
        for column, dtype in self.path_data.dtypes.items():
            # If the data type already exists in the dictionary, append the column to that list
            if dtype in grouped_types:
                grouped_types[dtype].append(column)
            else:
                # If it's a new data type, initialize a new list with the column
                grouped_types[dtype] = [column]
        
        return grouped_types
    
    def get_mini_eda_html(self):
        # Get the columns and shape of the DataFrame
        self.columns = self.path_data.columns
        self.shape = self.path_data.shape

        # Get the DataFrame description
        self.describe = self.path_data.describe().to_html(classes='table table-striped')

        # Get rows containing null values
        self.null_rows = self.path_data[self.path_data.isnull().any(axis=1)]
        self.n_null_rows = self.null_rows.shape[0]
        
        # Limit the null rows to a maximum of 5 rows for display purposes
        null_rows_display = self.null_rows.head(5)

        # Get columns grouped by data type
        grouped_types = self.group_columns_by_type()

        # Create HTML for the columns grouped by data type, also showing the number of columns
        grouped_types_html = "<h3>COLUMNS GROUPED BY DATA TYPE:</h3><ul>"
        for dtype, columns in grouped_types.items():
            grouped_types_html += f"<li><strong>{dtype}: ({len(columns)} columns) </strong> {', '.join(columns)} </li>"
        grouped_types_html += "</ul>"

        # NEW SECTION: Calculate null counts per column
        null_counts = self.path_data.isnull().sum()
        null_counts = null_counts[null_counts > 0]  # Only show columns with at least one null value

        # HTML for null counts and null rows
        if not null_counts.empty:
            null_counts_df = null_counts.to_frame(name='Number of Null Values').reset_index()
            null_counts_df.rename(columns={'index': 'Column'}, inplace=True)
            null_counts_html = f"""
            <hr>
            <h3>NUMBER OF NULL VALUES PER COLUMN:</h3>
            {null_counts_df.to_html(index=False, classes='table table-bordered', border=0)}
            <hr>
            <h3>ROWS WITH NULL VALUES (showing up to 5 rows):</h3>
            {null_rows_display.to_html(classes='table table-bordered', border=0)}
            """
        else:
            null_counts_html = """
            <hr>
            <h3>NUMBER OF NULL VALUES PER COLUMN:</h3>
            <p>There are no null values in any column.</p>
            """

        # Generate the HTML output
        html_output = f"""
        <h2>Mini EDA Report</h2>
        <p><strong>DATAFRAME SHAPE:</strong><br>
        Number of rows: {self.shape[0]}<br>
        Number of columns: {self.shape[1]}</p>

        <hr>
        <h3>FIRST 5 ROWS:</h3>
        {self.get_head().to_html(classes='table table-striped')}
        
        <hr>

        <h3>COLUMN NAMES:</h3>
        <p>{', '.join(self.columns)}</p>

        <hr>

        <h3>DESCRIPTIVE STATISTICS:</h3>
        {self.describe}

        <hr>

        {grouped_types_html}
        
        {null_counts_html}
        """
        
        # Display the HTML
        display(HTML(html_output))
        
        # Return the DataFrame for further manipulation
        return self.path_data
