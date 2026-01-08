# FlexiMart Data Architecture Project

**Student Name:** [Shreya Agarwal]
**Student ID:** [2507640]
**Email:** [agarwalshreya277@gmail.com]
**Date:** January 08, 2026

## Project Overview

This project implements a complete data pipeline for FlexiMart, an e-commerce platform. It demonstrates ETL processes to clean and load raw customer, product, and sales data into a relational database. Additionally, it includes NoSQL analysis using MongoDB for flexible product catalogs and a dimensional data warehouse with star schema for advanced OLAP analytics.

## Repository Structure

Fleximart-data-architecture/
├── part1-database-etl/
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ └── data_quality_report.txt
├── part2-nosql/
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
├── part3-datawarehouse/
│ ├── star_schema_design.md
│ ├── warehouse_schema.sql
│ ├── warehouse_data.sql
│ └── analytics_queries.sql
└── README.md


## Technologies Used

- **Python:** 3.x with pandas, mysql-connector-python
- **Relational Database:** MySQL 8.0
- **NoSQL Database:** MongoDB 6.0
- **Data Warehouse:** MySQL 8.0 with star schema
- **Documentation:** Markdown

## Setup Instructions

### Database Setup

```bash
# Create operational database
mysql -u root -p -e "CREATE DATABASE fleximart;"

# Create data warehouse database
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse Schema
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql

# Run Part 3 - Data Warehouse Data
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

# Run Part 3 - Analytics Queries
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql



### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

ETL Best Practices: Data quality is critical removing duplicates and standardizing formats upfront prevents downstream errors. Using pandas for transformation is efficient for moderate datasets.

Dimensional Modeling: Star schemas denormalize data for analytical queries, using surrogate keys and separate dimension tables. This design enables fast OLAP queries through pre-aggregated facts.

## Challenges Faced

Challenge: Python Environment PATH Issues

Problem: pip command not recognized in VS Code terminal; Python packages (pandas, mysql-connector) not installing.

Solution: Used Anaconda Prompt instead of regular PowerShell. Anaconda automatically configures Python PATH. Successfully installed dependencies via pip install pandas mysql-connector-python in Anaconda Prompt.