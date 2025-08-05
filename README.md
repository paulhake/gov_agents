# watsonx Governance Prompt Evaluator

A Streamlit application for evaluating prompts and models using IBM watsonx Governance evaluation framework and SDK.

## Features

- **Interactive UI**: User-friendly Streamlit interface for prompt evaluation
- **Multiple Evaluators**: Support for all watsonx governance evaluators including:
  - Quality Evaluation
  - Fairness Evaluation
  - Drift Evaluation
  - Guardrails Evaluation
  - Prompt Template Evaluation
  - RAG Metrics Evaluation
  - Model Risk Evaluation
- **Flexible Configuration**: Easy setup with API keys, project IDs, and model parameters
- **Results Export**: Download evaluation results as JSON or CSV reports
- **Real-time Evaluation**: Run evaluations and see results immediately in the UI
- **Real-time Guardrails**: Pre-model inference content safety checks with configurable thresholds

## Setup

### Option 1: Using Conda (Recommended)

1. **Create Conda Environment**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate Environment**
   ```bash
   conda activate watsonx-gov-evaluator
   ```

3. **Configure Environment**
   Copy `.env.example` to `.env` and fill in your watsonx credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```
   WATSONX_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_INSTANCE_ID=your_instance_id_here
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

### Option 2: Using pip

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Copy `.env.example` to `.env` and fill in your watsonx credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```
   WATSONX_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_INSTANCE_ID=your_instance_id_here
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Configure Settings**: Enter your watsonx API credentials in the sidebar
2. **Configure Guardrails**: Enable real-time guardrails and set content safety thresholds
3. **Input Prompt**: Enter the prompt you want to evaluate
4. **Select Model**: Choose your model type and configuration
5. **Choose Evaluators**: Select which evaluation frameworks to run
6. **Run Evaluation**: Click the "Run Evaluation" button (prompts are automatically checked by guardrails first)
7. **View Results**: See detailed results including guardrails status and export reports

## Real-time Guardrails

The application includes comprehensive real-time guardrails that evaluate prompts before model inference:

### Key Features
- **Real-time Content Safety**: Immediate evaluation of prompts for harmful content
- **Configurable Filters**: Toggle individual safety checks (toxicity, hate speech, profanity, PII)
- **Adjustable Thresholds**: Set custom sensitivity levels for toxicity and confidence scores
- **Violation Blocking**: Automatically prevents model evaluation if guardrails fail
- **Detailed Reporting**: Clear feedback on detected violations with specific scores

### Content Safety Checks
- **Toxicity Detection**: Identifies potentially harmful or offensive content
- **Hate Speech Detection**: Flags discriminatory or prejudiced language  
- **Profanity Filter**: Detects inappropriate language
- **PII Detection**: Identifies personally identifiable information (emails, phone numbers, SSNs)

### Configuration Options
- **Toxicity Threshold** (0.0-1.0): Set the maximum allowed toxicity score
- **Confidence Threshold** (0.0-1.0): Minimum confidence level for guardrail decisions
- **Enable/Disable**: Toggle individual safety checks as needed

### How It Works
1. User enters a prompt in the interface
2. Real-time guardrails automatically evaluate the content
3. If violations are detected, the evaluation is blocked with detailed feedback
4. Only prompts that pass all enabled guardrails proceed to model evaluation
5. Guardrails results are included in the final evaluation report

## Supported Evaluators

- **Quality Evaluation**: Assess model output quality and accuracy
- **Fairness Evaluation**: Check for bias across different demographic groups
- **Drift Evaluation**: Detect data and model performance drift
- **Guardrails Evaluation**: Apply content safety and policy checks
- **Prompt Template Evaluation**: Evaluate prompt effectiveness
- **RAG Metrics Evaluation**: Assess retrieval-augmented generation performance
- **Model Risk Evaluation**: Evaluate foundation model risks

## Requirements

- Python 3.8+
- Valid watsonx.ai account and credentials
- Internet connection for API calls

## Note

This application currently includes a simulation mode for demonstration purposes. To connect to the actual watsonx governance SDK, update the `simulate_evaluation` function in `app.py` with proper SDK integration.