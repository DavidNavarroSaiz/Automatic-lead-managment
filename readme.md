tutorial to configure the email to send messages https://www.youtube.com/watch?v=g_j6ILT-X0k


<a name="readme-top"></a>





<h3 align="center">Automatic lead managment</h3>




</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


#The Lead Generation and Management System is a comprehensive solution designed to streamline the process of generating and managing leads for businesses. Leveraging various technologies and integrations, this system automates lead generation, captures lead information, and facilitates communication with potential customers through emails and SMS. Additionally, the system incorporates the use of GPT (Generative Pre-trained Transformer) for creating automatic and personalized responses to emails and SMS, enhancing the engagement and interaction with leads.


Key Features:


* FastAPI Backend: Utilizes FastAPI, a modern web framework for building APIs with Python, to handle HTTP requests and responses efficiently.

* Twilio Integration: Integrates with Twilio API to send SMS messages, allowing real-time communication with leads.

* HubSpot Integration: Integrates with HubSpot CRM API to manage lead data, including creation, retrieval, updating, and deletion of contacts.

* Email Communication: Enables communication with leads via email using SMTP protocol. Supports sending personalized email responses based on lead inquiries.

* Lead Generation Scripts: Provides scripts to generate leads either randomly or with specific names, simulating interactions with potential customers.

* GPT for Automatic Responses: Incorporates GPT (Generative Pre-trained Transformer) to create automatic and personalized responses to emails and SMS. GPT analyzes lead inquiries and generates relevant and engaging responses, enhancing lead interaction.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* python
* FastaPI
* HubSpot
* openai

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Make sure you have the following prerequisites installed:

- Python (3.7 or higher)
- Git (for version control)


* It is recommended to create your own environment for this project:


### Installation
1. Clone the repository to your local machine:

    ```
    git clone https://github.com/DavidNavarroSaiz/Automatic-lead-managment
    ```

2. Navigate to the project directory:

    ``` 
    cd your-project
    ```

3. Install project dependencies using `pip`:

    ```
    pip install -r requirements.txt
    ```

4. setup the environment variables:
    Follow these steps to set up the necessary environment variables for your project:

    Create a new file named .env in the root directory of your project.

    Open the .env file and add the following line with the corresponding values


    ```
    OPENAI_API_KEY= ""
    EMAIL_PASSWORD = ""
    TWILIO_ACCOUNT_SID = ''
    TWILIO_AUTH_TOKEN = ''
    TWILIO_PHONE_NUMBER = ''
    HUBSPOT_API_KEY= ''
    ```
    Save the .env file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Generator Setup
for sending data to configure the send_data.json
there you will be putting the data of the emails that you want to send
in this case receiver email has to be configured properly in the google gmail api, you can follow this tutorial:
https://www.youtube.com/watch?v=g_j6ILT-X0k

{"sender_email": "",
 "receiver_email": "",
 "recipient_number": ""
}



### Lead Generator API 

in the file main_generator.py you will find methods to generate leads

1. Run the FastAPI service:

    ```
    python main.py
    ```
    or using the console:

    ```
    uvicorn main:app --reload --port 8001
    ```



<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Using the docker:

a docker-compose.yml is used to create the database called "my_dev_database" but it can be changed you can also run the following command:
```
 docker-compose up --build
```

it will create a docker image with the database and the fastapi app.


In both cases you can acces to the fastAPI documentation and usage in the  specified port(typically 8000)
```
http://127.0.0.1:8000/docs#

```

# FastAPI Endpoints Documentation

This documentation provides details about the endpoints available in the FastAPI project.

## Run Generator Endpoint

### Endpoint: `/run-generator`

**Description:**  
Executes the elevator state generator.

## Delete All Rows Endpoint

### Endpoint: `/delete-all-rows`
**Description:**  
Deletes all elevator state rows from the database.

HTTP Method: GET

## Get All Rows Endpoint
### Endpoint: `/get-all-rows`
**Description:**  
Retrieves all elevator state rows from the database.

## Save to CSV Endpoint

### Endpoint: `/save-to-csv`
**Description:**  
Saves all elevator state rows to a CSV file and allows users to download it.


## How to use it to train a ML model:

To enhance the training of a machine learning (ML) model, it is advisable to engage in thoughtful feature engineering. Extracting a diverse set of features, including Time-related Features, Distance Features between floors, Time Spent Features, Directional Features, Time Series Split, Lag Features, Rolling Window Statistics, and more, can significantly contribute to the model's predictive capabilities.

After performing feature engineering, a strategic choice for the target variable is to use demand_floor. By designating demand_floor as the target variable, the model aims to predict the most probable floor in demand, guiding the elevator to rest optimally at that position.

Moreover, to effectively capture the temporal dependencies inherent in the dataset, it is recommended to employ models designed for time series analysis. Autoregressive models like ARIMA or SARIMA provide a robust framework for understanding time series patterns. Alternatively, models like Recurrent Neural Networks (RNNs) or Long Short-Term Memory (LSTM) Networks, with their capacity to capture sequential dependencies, can offer valuable insights into the temporal dynamics of the elevator operations.