# News-Sentiment-Analysis

## Project Overview
This project aims to perform sentiment analysis on news articles using various AWS services. The architecture leverages AWS Lambda, SQL Electron, Amazon Comprehend, and Amazon S3 to automate the process of sentiment analysis and data storage.

## Architecture
![proj_3](https://github.com/user-attachments/assets/d7516ac4-21c8-4475-ab4c-0631e3b2cad3)
### Components
1. **Data Source**: 
   - **News URL**:[ Source of news articles](https://timesofindia.indiatimes.com/).
   
2. **Data Processing**:
   - **AWS Lambda**: Used to automate various steps in the data pipeline.
     - **Create First Table**: Lambda function to create the first table and store news URLs.
     - **Get RSS URLs**: Lambda function to extract RSS URLs from the news URLs.
     - **Get Sentiment from RSS Files**: Lambda function to get sentiment scores from the RSS files.
   - **SQL Electron**: Database used to store the data at various stages.
     - **Table 1**: Stores news URLs.
     - **Table 2**: Stores RSS URLs and files.
     - **Table 3**: Stores sentiment analysis results.
   - **Amazon Comprehend**: AWS service used for performing sentiment analysis on the news data.
   
3. **Data Storage**:
   - **Amazon S3**: Used to store the sentiment analysis results for further use and visualization.

## Setup Instructions
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/News-Sentiment-Analysis.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd News-Sentiment-Analysis
    ```

3. **Install dependencies** (if any):
    ```bash
    pip install -r requirements.txt
    ```

4. **Deploy AWS Lambda functions**:
   - Ensure you have the necessary AWS IAM roles and permissions set up.
   - Deploy the Lambda functions using AWS CLI or AWS Management Console.

5. **Configure SQL Electron**:
   - Set up your database and tables as per the architecture.
   - Update the Lambda functions with the database connection details.

6. **Run the data pipeline**:
   - Execute the Lambda functions as per the sequence defined in the architecture.
   - Ensure that data flows correctly through each stage and is stored in the respective tables.

7. **Visualize the results**:
   - Use Amazon S3 to access the sentiment analysis results.
   - Use your preferred visualization tool to generate insights from the analyzed data.

## Usage
- Ensure that the news URLs are correctly processed and stored in SQL Electron.
- Use the provided Lambda functions to automate the extraction and sentiment analysis process.
- Store and visualize the results to understand the sentiment of news articles.

## Contributing
Feel free to open issues or submit pull requests for improvements or new features.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any queries, please contact [akashatre123@gmail.com](mailto:akashatre123@gmail.com).
