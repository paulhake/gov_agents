# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This is currently an empty repository with no source code, configuration files, or documentation. The repository appears to be newly initialized and ready for initial development.

## Project Overview

This is a Streamlit application for evaluating prompts and models using IBM watsonx Governance evaluation framework and SDK. The application provides an interactive UI for users to input prompts, configure models, select evaluators, and view detailed evaluation results.

## Development Setup

### Option 1: Using Conda (Recommended)
```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate watsonx-gov-evaluator

# Configure environment variables
cp .env.example .env
# Edit .env with your watsonx credentials

# Run the application
streamlit run app.py
```

### Option 2: Using pip
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your watsonx credentials

# Run the application
streamlit run app.py
```

## Architecture

### Core Components
- `app.py` - Main Streamlit application with UI components and evaluation logic
- `requirements.txt` - Python dependencies including watsonx-gov SDK
- `environment.yml` - Conda environment configuration with Python 3.10
- `.env.example` - Template for environment configuration

### Key Features
- Configuration sidebar for watsonx API credentials
- Prompt and model input interface
- Evaluator selection with full range of watsonx governance evaluators
- Results display and export functionality
- Error handling and validation

### Available Evaluators
- Quality Evaluation (accuracy, precision, recall, f1_score)
- Fairness Evaluation (demographic parity, equalized odds)
- Drift Evaluation (data drift, prediction drift)
- Guardrails Evaluation (content safety, toxicity, bias)
- Prompt Template Evaluation
- RAG Metrics Evaluation
- Model Risk Evaluation

## Development Notes

Use these links for context and background information:
- watsonx governance SDK: https://github.com/IBM/ibm-watsonx-gov/tree/samples/notebooks
- watsonx governance documentation: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-evaluating-models 
- Sample notebooks: https://github.com/IBM/ibm-watsonx-gov/tree/samples/notebooks