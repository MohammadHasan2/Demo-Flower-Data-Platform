An end-to-end data engineering and analytics platform
built for an online flower store.

## Overview

The platform ingests order data from Google Sheets,
processes and validates the data through a Python ETL
pipeline, stores it in PostgreSQL, and provides business
analytics through a Streamlit dashboard.

## Architecture

Google Sheets
      ↓
Python ETL
      ↓
Data Validation
      ↓
Transformation
      ↓
Supabase PostgreSQL
      ↓
SQL Analytics
      ↓
Streamlit Dashboard

## Features

- Google Sheets data ingestion
- Data validation
- Data transformation
- PostgreSQL data storage
- Revenue analytics
- Order analytics
- Product performance
- Customer management
- Customer phone search
- Interactive date filtering
- ETL execution tracking
- Error handling
- Docker support

## Tech Stack

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Supabase
- Streamlit
- Docker

## Project Structure

```text
app/        → Streamlit dashboard
etl/        → ETL pipeline
database/   → Database configuration
queries.py  → Analytics queries
