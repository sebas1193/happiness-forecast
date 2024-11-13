# Happiness Forecast


## Project Description

**Happiness Forecast** is a machine learning project aimed at predicting the happiness score of countries worldwide based on selected features derived from an exploratory data analysis (EDA). The project leverages an AI model to forecast happiness scores in real-time, storing predictions in a PostgreSQL database with the help of Apache Kafka for real-time streaming.

The workflow includes data ingestion, feature selection, model training, real-time data streaming, and evaluation of model performance, offering a comprehensive pipeline from data analysis to deployment.

## Project Structure


```

.
├── README.md
├── docker-compose.yaml
├── kafka_consumer.py
├── kafka_producer.py
├── models
│   └── xgboost_model.joblib
├── notebooks
│   ├── 001_EDA.ipynb
|   └──002_model_eval.ipynb
│
├── pyproject.toml
├── requirements.txt
├── utils
│   ├── data_explorer.py
│   ├── db_postgres.py
│   ├── kafka.py
│   ├── ne_110m_admin_0_countries.zip
│   └── ww_gif_generator.py
└── visualizations
    └── happiness_score_smooth.gif

```
## Dependencies

This project requires the following tools and libraries:

- **Docker**

- **Python** (version 3.12)

- **Poetry** (version 1.8)

- **Python venv**

## Getting Started

### 1. Set Up Environment Variables

Create a file named `.env` in the project’s root directory (where `docker-compose.yaml` is located) with the following structure:

```plaintext

POSTGRES_USER=your_user

POSTGRES_PASSWORD=your_password

POSTGRES_DB=your_db

HOST=localhost

PGADMIN_DEFAULT_EMAIL=your_email

```

# Virtual Enviroment:

### With Poetry:

```

poetry install

```

Once all dependencies are installed, activate the environment:

```

poetry shell

```  

### With Virtual Environment (venv):

```

python3 -m venv venv

```

### Activate the virtual environment:

On Windows:

```

venv\Scripts\activate

```

On macOS/Linux:

```

source venv/bin/activate

```

Then:
```

pip install -r requirements.txt

```

# Start Docker Containers

Run the following command to build and start Docker containers:

```

docker-compose up --build -d

```

# Enable Kafka Streaming

After starting Docker, access the Kafka container:

```

docker exec -it kafka-w3 bash

```

Create the Kafka topic:

```

kafka-topics --bootstrap-server kafka-w3:9092 --create --topic kafka-happiness

```

# Run Kafka Consumer and Producer

In two separate terminal windows, start the Kafka consumer first, followed by the producer:

Start the consumer:

```

python kafka_consumer.py

```

Start the producer:

```

python kafka_producer.py

```

⚠️ Important: Always ensure your virtual environment (Poetry or venv) is activated. Otherwise, the scripts may not run correctly.

# Evaluate Model Performance

Once streaming is complete, run the 002_model_eval.ipynb notebook to assess the model's performance.