# 📊 CoinMarketCap ETL Pipeline

> A modular Python ETL pipeline that extracts live cryptocurrency market data from the CoinMarketCap Pro API, cleans and standardises it, and bulk-loads it into a cloud-hosted PostgreSQL database on Aiven.

---

## 🗂️ Project Structure

```
coinMarketCap_etl_pipeline/
│
├── extract.py          # Calls CoinMarketCap Pro API; returns raw DataFrame + CSV snapshot
├── transform.py        # Drops irrelevant columns, removes nulls and duplicates
├── load.py             # Bulk-inserts cleaned records into Aiven PostgreSQL
├── main.py             # Orchestrates extract → transform → load with progress logging
│
├── .env                # API key and DB credentials (never committed)
├── .gitignore          # Excludes .venv, .env, __pycache__, *.csv
├── pyproject.toml      # Project metadata and dependencies managed by uv
├── uv.lock             # Locked dependency graph for reproducible installs
└── README.md
```

---

## ⚙️ Pipeline Flow

## ⚙️ Pipeline Flow

| Step | Script           | Phase                 | What It Does                                                                                                                                                                                                                             |
| ---- | ---------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `extract.py`   | **Extract**     | Sends a GET request to `CoinMarketCap Pro API /v1/cryptocurrency/listings/latest`with a limit of 5000 coins converted to USD · Parses the JSON response into a pandas DataFrame · Saves a raw snapshot to `crypto_market_data.csv` |
| 2    | `transform.py` | **Transform**   | Drops 7 irrelevant columns:`quote`,`tags`,`tvl_ratio`,`platform`,`self_reported_circulating_supply`,`self_reported_market_cap`,`minted_market_cap`· Removes rows containing any null values · Removes duplicate rows     |
| 3    | `load.py`      | **Load**        | Connects to Aiven PostgreSQL · Bulk-inserts 12 fields per record into `crypto.crypto_market_data`using `executemany()`· Commits the transaction and closes the connection cleanly                                                  |
| 4    | `main.py`      | **Orchestrate** | Single entry point (`python main.py`) that calls all three steps in sequence · Logs record counts after extraction and transformation                                                                                                 |

---

## 🗄️ Target Table — `crypto.crypto_market_data`

The following 12 fields are extracted from the cleaned DataFrame and inserted into PostgreSQL:

| Column                 | Type      | Description                           |
| ---------------------- | --------- | ------------------------------------- |
| `id`                 | INTEGER   | CoinMarketCap unique coin ID          |
| `name`               | VARCHAR   | Full coin name (e.g. Bitcoin)         |
| `symbol`             | VARCHAR   | Ticker symbol (e.g. BTC)              |
| `slug`               | VARCHAR   | URL-friendly identifier               |
| `infinite_supply`    | BOOLEAN   | Whether the coin has no supply cap    |
| `circulating_supply` | NUMERIC   | Coins currently in circulation        |
| `total_supply`       | NUMERIC   | Total coins in existence              |
| `max_supply`         | NUMERIC   | Maximum coins that will ever exist    |
| `date_added`         | TIMESTAMP | Date coin was listed on CoinMarketCap |
| `num_market_pairs`   | INTEGER   | Number of active trading pairs        |
| `cmc_rank`           | INTEGER   | CoinMarketCap market cap rank         |
| `last_updated`       | TIMESTAMP | Timestamp of last data update         |

---

## 🧰 Tech Stack

| Tool                          | Role                                                     |
| ----------------------------- | -------------------------------------------------------- |
| **Python 3.x**          | Core language                                            |
| **requests**            | HTTP calls to the CoinMarketCap Pro API                  |
| **pandas**              | DataFrame operations — drop, dropna, drop_duplicates    |
| **psycopg2-binary**     | PostgreSQL adapter — connection and executemany inserts |
| **python-dotenv**       | Loads secrets from `.env`at runtime                    |
| **uv**                  | Virtual environment creation and dependency management   |
| **PostgreSQL on Aiven** | Cloud-hosted target data store                           |
| **Git + GitHub**        | Version control and remote repository                    |

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x installed
* `uv` installed — [install guide](https://astral.sh/uv)
* A [CoinMarketCap Pro API key](https://coinmarketcap.com/api/)
* An Aiven (or any) PostgreSQL instance with the `crypto.crypto_market_data` table created

---

### 1. Clone the repository

```bash
git clone https://github.com/mac0duor0fficial-1028/coinMarketCap_etl_pipeline.git
cd coinMarketCap_etl_pipeline
```

### 2. Create and activate the virtual environment

```bash
uv venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows (Git Bash)
```

### 3. Install all dependencies

```bash
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock` to install the exact same dependency versions on any machine.

### 4. Set up your `.env` file

Create a `.env` file in the project root and populate it:

```env
CMC_API_KEY=your_coinmarketcap_pro_api_key

DB_NAME=coin_market_cap_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_aiven_host.aivencloud.com
DB_PORT=14233
```

> ⚠️ `.env` is listed in `.gitignore` and is pushed to GitHub.

### 5. Run the pipeline

```bash
python main.py
```

Expected output:

```
Starting ETL pipeline...
Step 1: Extracting crypto market data...
Extraction complete. 5000 records fetched.
Step 2: Transforming data...
Transformation complete. XXXX records after cleaning.
Step 3: Loading data into the database...
Load complete. ETL pipeline finished successfully.
```

---

## 📦 Dependencies

Declared in `pyproject.toml` and managed entirely by `uv`:

```toml
[project]
dependencies = [
    "requests",
    "pandas",
    "psycopg2-binary",
    "python-dotenv"
]
```

To add a new package:

```bash
uv add package-name
```

---

## 🔒 Security

* All credentials (API key, DB host, password) live exclusively in `.env`
* `.env` is excluded from version control via `.gitignore`
* Scripts read credentials at runtime using `os.getenv()` via `python-dotenv`
* No secrets are hardcoded in any `.py` file

---

## 🛣️ Roadmap

* [ ] Schedule automated runs with Apache Airflow
* [ ] Add pre-load data quality checks
* [ ] Store `quote` field data (price, volume, market cap) in a separate related table
* [ ] Containerise with Docker for portable deployment
* [ ] Build an analytics dashboard on top of the PostgreSQL data

---

## 👤 Author

**mac0duor0fficial-1028** · [GitHub](https://github.com/mac0duor0fficial-1028)

---

## 📄 License

This project is open source and available under the [MIT License](https://claude.ai/chat/LICENSE).
