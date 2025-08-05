import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="watsonx Governance Prompt Evaluator",
    page_icon="🔍",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'evaluation_results' not in st.session_state:
        st.session_state.evaluation_results = None
    if 'config_valid' not in st.session_state:
        st.session_state.config_valid = False
    if 'last_prompt' not in st.session_state:
        st.session_state.last_prompt = ''

def render_header():
    """Render the application header"""
    st.title("🔍 watsonx Governance Prompt Evaluator")
    st.markdown("Evaluate prompts and models using IBM watsonx Governance framework")
    st.divider()

def render_configuration_sidebar():
    """Render configuration inputs in sidebar"""
    st.sidebar.header("⚙️ Configuration")
    
    # watsonx configuration
    st.sidebar.subheader("watsonx Settings")
    api_key = st.sidebar.text_input("API Key", type="password", value=os.getenv("WATSONX_API_KEY", ""))
    project_id = st.sidebar.text_input("Project ID", value=os.getenv("WATSONX_PROJECT_ID", ""))
    instance_id = st.sidebar.text_input("Instance ID", value=os.getenv("WATSONX_INSTANCE_ID", ""))
    
    # Optional URL configuration
    st.sidebar.subheader("Optional Settings")
    base_url = st.sidebar.text_input("Base URL", value=os.getenv("WATSONX_BASE_URL", "https://us-south.ml.cloud.ibm.com"))
    
    # Real-time Guardrails Configuration
    st.sidebar.subheader("🛡️ Real-time Guardrails")
    enable_guardrails = st.sidebar.checkbox("Enable Real-time Guardrails", value=True)
    
    guardrails_config = {}
    if enable_guardrails:
        st.sidebar.markdown("**Content Safety Filters:**")
        guardrails_config['toxicity'] = st.sidebar.checkbox("Toxicity Detection", value=True)
        guardrails_config['hate_speech'] = st.sidebar.checkbox("Hate Speech Detection", value=True)
        guardrails_config['profanity'] = st.sidebar.checkbox("Profanity Filter", value=True)
        guardrails_config['pii'] = st.sidebar.checkbox("PII Detection", value=True)
        guardrails_config['prompt_injection'] = st.sidebar.checkbox("Prompt Injection Detection", value=True)
        
        st.sidebar.markdown("**Thresholds:**")
        guardrails_config['toxicity_threshold'] = st.sidebar.slider(
            "Toxicity Threshold", 0.0, 1.0, 0.7, 0.1, 
            help="Block content above this toxicity score"
        )
        guardrails_config['confidence_threshold'] = st.sidebar.slider(
            "Confidence Threshold", 0.0, 1.0, 0.8, 0.1,
            help="Minimum confidence for guardrail decisions"
        )
    
    # Validate configuration
    config_valid = bool(api_key and project_id and instance_id)
    st.session_state.config_valid = config_valid
    
    if not config_valid:
        st.sidebar.error("⚠️ Please provide all required configuration fields")
    else:
        st.sidebar.success("✅ Configuration valid")
    
    return {
        'api_key': api_key,
        'project_id': project_id,
        'instance_id': instance_id,
        'base_url': base_url,
        'enable_guardrails': enable_guardrails,
        'guardrails_config': guardrails_config
    }

def get_available_evaluators():
    """Get list of available watsonx governance evaluators"""
    return {
        "Quality Evaluation": {
            "description": "Evaluate model output quality and accuracy",
            "metrics": ["accuracy", "precision", "recall", "f1_score"]
        },
        "Fairness Evaluation": {
            "description": "Assess model fairness across different groups",
            "metrics": ["demographic_parity", "equalized_odds", "statistical_parity"]
        },
        "Drift Evaluation": {
            "description": "Detect data drift and model performance drift",
            "metrics": ["data_drift", "prediction_drift", "accuracy_drift"]
        },
        "Guardrails Evaluation": {
            "description": "Apply content safety and policy guardrails",
            "metrics": ["content_safety", "toxicity", "bias_detection"]
        },
        "Prompt Template Evaluation": {
            "description": "Evaluate prompt template effectiveness",
            "metrics": ["relevance", "coherence", "completeness"]
        },
        "RAG Metrics Evaluation": {
            "description": "Evaluate Retrieval-Augmented Generation performance",
            "metrics": ["retrieval_accuracy", "answer_relevance", "context_precision"]
        },
        "Model Risk Evaluation": {
            "description": "Assess risks associated with foundation models",
            "metrics": ["risk_score", "vulnerability_assessment", "compliance_check"]
        }
    }

def render_prompt_input():
    """Render prompt and model input section"""
    st.header("📝 Prompt & Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prompt Input")
        prompt_text = st.text_area(
            "Enter your prompt:",
            height=150,
            placeholder="Enter the prompt you want to evaluate..."
        )
        
        # Optional: System prompt
        system_prompt = st.text_area(
            "System Prompt (optional):",
            height=100,
            placeholder="Enter system prompt if applicable..."
        )
    
    with col2:
        st.subheader("Model Configuration")
        model_type = st.selectbox(
            "Model Type:",
            ["IBM watsonx.ai", "External Model", "Custom Model"]
        )
        
        if model_type == "IBM watsonx.ai":
            model_name = st.selectbox(
                "Model Name:",
                ["meta-llama/llama-2-70b-chat", "ibm/granite-13b-chat-v2", "google/flan-t5-xxl", "meta-llama/llama-2-13b-chat"]
            )
        else:
            model_name = st.text_input("Model Name/ID:")
        
        # Model parameters
        st.subheader("Model Parameters")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.number_input("Max Tokens", 1, 4000, 100)
        
    return {
        'prompt_text': prompt_text,
        'system_prompt': system_prompt,
        'model_type': model_type,
        'model_name': model_name,
        'temperature': temperature,
        'max_tokens': max_tokens
    }

def render_evaluator_selection():
    """Render evaluator selection interface"""
    st.header("🎯 Evaluation Configuration")
    
    evaluators = get_available_evaluators()
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Select Evaluators")
        selected_evaluators = []
        
        for eval_name, eval_info in evaluators.items():
            if st.checkbox(eval_name, key=f"eval_{eval_name}"):
                selected_evaluators.append(eval_name)
    
    with col2:
        st.subheader("Evaluator Details")
        for eval_name in selected_evaluators:
            if eval_name in evaluators:
                with st.expander(f"{eval_name} Configuration"):
                    st.write(f"**Description:** {evaluators[eval_name]['description']}")
                    st.write(f"**Available Metrics:** {', '.join(evaluators[eval_name]['metrics'])}")
                    
                    # Allow metric selection
                    selected_metrics = st.multiselect(
                        f"Select metrics for {eval_name}:",
                        evaluators[eval_name]['metrics'],
                        default=evaluators[eval_name]['metrics'][:2],  # Default to first 2 metrics
                        key=f"metrics_{eval_name}"
                    )
    
    return selected_evaluators

def evaluate_guardrails_realtime(prompt_text: str, config: Dict) -> Dict[str, Any]:
    """Evaluate guardrails in real-time before model inference"""
    if not config.get('enable_guardrails', False):
        return {'passed': True, 'message': 'Guardrails disabled'}
    
    guardrails_config = config.get('guardrails_config', {})
    
    # Simulate real-time guardrails evaluation
    # In actual implementation, this would use watsonx governance SDK
    import random
    import re
    
    results = {
        'passed': True,
        'violations': [],
        'scores': {},
        'message': 'All guardrails passed'
    }
    
    # Simple content checks (placeholder implementation)
    prompt_lower = prompt_text.lower()
    
    # Toxicity check
    if guardrails_config.get('toxicity', False):
        toxicity_score = random.uniform(0.0, 0.3)  # Simulate low toxicity for most prompts
        
        # Check for potentially toxic keywords
        toxic_keywords = ['hate', 'kill', 'violent', 'attack', 'destroy']
        if any(keyword in prompt_lower for keyword in toxic_keywords):
            toxicity_score = random.uniform(0.6, 0.9)
        
        results['scores']['toxicity'] = round(toxicity_score, 3)
        
        if toxicity_score > guardrails_config.get('toxicity_threshold', 0.7):
            results['passed'] = False
            results['violations'].append(f"High toxicity detected (score: {toxicity_score:.3f})")
    
    # Hate speech check
    if guardrails_config.get('hate_speech', False):
        hate_score = random.uniform(0.0, 0.2)
        hate_keywords = ['discrimination', 'prejudice', 'supremacy']
        if any(keyword in prompt_lower for keyword in hate_keywords):
            hate_score = random.uniform(0.7, 0.95)
        
        results['scores']['hate_speech'] = round(hate_score, 3)
        
        if hate_score > 0.5:
            results['passed'] = False
            results['violations'].append(f"Hate speech detected (score: {hate_score:.3f})")
    
    # Profanity check
    if guardrails_config.get('profanity', False):
        profanity_words = ['damn', 'hell', 'shit', 'fuck', 'bitch']
        profanity_count = sum(1 for word in profanity_words if word in prompt_lower)
        profanity_score = min(profanity_count * 0.3, 1.0)
        
        results['scores']['profanity'] = round(profanity_score, 3)
        
        if profanity_score > 0.3:
            results['passed'] = False
            results['violations'].append(f"Profanity detected (score: {profanity_score:.3f})")
    
    # PII check
    if guardrails_config.get('pii', False):
        # Simple regex patterns for common PII
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        
        pii_found = []
        if re.search(email_pattern, prompt_text):
            pii_found.append('email')
        if re.search(phone_pattern, prompt_text):
            pii_found.append('phone')
        if re.search(ssn_pattern, prompt_text):
            pii_found.append('ssn')
        
        pii_score = len(pii_found) * 0.5
        results['scores']['pii'] = round(min(pii_score, 1.0), 3)
        
        if pii_found:
            results['passed'] = False
            results['violations'].append(f"PII detected: {', '.join(pii_found)}")
    
    # Prompt injection check
    if guardrails_config.get('prompt_injection', False):
        injection_patterns = [
            r'ignore\s+(previous|above|all)\s+(instructions?|prompts?)',
            r'forget\s+(everything|all|previous)',
            r'act\s+as\s+(if\s+you\s+are\s+)?\w+',
            r'pretend\s+(to\s+be|you\s+are)',
            r'system\s*:\s*',
            r'admin\s*:\s*',
            r'root\s*:\s*',
            r'\[\s*system\s*\]',
            r'<\s*system\s*>',
            r'jailbreak',
            r'override\s+(safety|security)',
            r'disable\s+(filter|safety|guardrail)',
            r'\b(DAN|DevMode|Developer Mode)\b',
        ]
        
        injection_score = 0.0
        detected_patterns = []
        
        for pattern in injection_patterns:
            if re.search(pattern, prompt_text, re.IGNORECASE):
                injection_score += 0.3
                detected_patterns.append(pattern)
        
        # Additional heuristics
        if len(re.findall(r'[!@#$%^&*()]{3,}', prompt_text)) > 2:
            injection_score += 0.2
        
        if prompt_text.count('\n') > 10 and len(prompt_text) < 500:
            injection_score += 0.1
        
        injection_score = min(injection_score, 1.0)
        results['scores']['prompt_injection'] = round(injection_score, 3)
        
        if injection_score > 0.5:
            results['passed'] = False
            results['violations'].append(f"Prompt injection detected (score: {injection_score:.3f})")
    
    # Update message based on results
    if not results['passed']:
        results['message'] = f"Guardrails violations: {'; '.join(results['violations'])}"
    
    return results

def simulate_evaluation(config: Dict, prompt_config: Dict, evaluators: List[str]) -> Dict[str, Any]:
    """Simulate evaluation using watsonx governance (placeholder implementation)"""
    
    # This is a placeholder implementation
    # In actual implementation, you would use the watsonx governance SDK
    
    results = {
        'prompt': prompt_config['prompt_text'],
        'model': prompt_config['model_name'],
        'evaluations': {}
    }
    
    # Simulate results for each selected evaluator
    import random
    import time
    
    for evaluator in evaluators:
        time.sleep(0.5)  # Simulate processing time
        
        if evaluator == "Quality Evaluation":
            results['evaluations'][evaluator] = {
                'accuracy': round(random.uniform(0.7, 0.95), 3),
                'precision': round(random.uniform(0.75, 0.92), 3),
                'recall': round(random.uniform(0.68, 0.89), 3),
                'f1_score': round(random.uniform(0.72, 0.90), 3),
                'status': 'completed'
            }
        elif evaluator == "Fairness Evaluation":
            results['evaluations'][evaluator] = {
                'demographic_parity': round(random.uniform(0.8, 0.95), 3),
                'equalized_odds': round(random.uniform(0.75, 0.92), 3),
                'statistical_parity': round(random.uniform(0.78, 0.94), 3),
                'status': 'completed'
            }
        elif evaluator == "Guardrails Evaluation":
            results['evaluations'][evaluator] = {
                'content_safety': round(random.uniform(0.85, 0.98), 3),
                'toxicity': round(random.uniform(0.02, 0.15), 3),
                'bias_detection': round(random.uniform(0.88, 0.97), 3),
                'status': 'completed'
            }
        else:
            # Generic results for other evaluators
            results['evaluations'][evaluator] = {
                'score': round(random.uniform(0.7, 0.95), 3),
                'confidence': round(random.uniform(0.8, 0.98), 3),
                'status': 'completed'
            }
    
    return results

def render_results(results: Dict[str, Any]):
    """Render evaluation results"""
    st.header("📊 Evaluation Results")
    
    if not results:
        st.info("No evaluation results to display. Run an evaluation first.")
        return
    
    # Summary section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Evaluated", results['model'])
    with col2:
        st.metric("Evaluations Run", len(results['evaluations']))
    with col3:
        completed = sum(1 for eval_result in results['evaluations'].values() if eval_result.get('status') == 'completed')
        st.metric("Completed", f"{completed}/{len(results['evaluations'])}")
    with col4:
        if 'guardrails' in results:
            guardrails_status = "✅ Passed" if results['guardrails']['passed'] else "❌ Failed"
            st.metric("Guardrails", guardrails_status)
        else:
            st.metric("Guardrails", "Disabled")
    
    st.divider()
    
    # Guardrails results section
    if 'guardrails' in results:
        with st.expander("🛡️ Guardrails Results", expanded=True):
            guardrails = results['guardrails']
            
            col1, col2 = st.columns(2)
            with col1:
                if guardrails['passed']:
                    st.success("✅ All guardrails passed")
                else:
                    st.error("❌ Guardrails violations detected")
                
                st.write(f"**Status:** {guardrails['message']}")
                
                if guardrails['violations']:
                    st.subheader("Violations:")
                    for violation in guardrails['violations']:
                        st.warning(f"⚠️ {violation}")
            
            with col2:
                if guardrails['scores']:
                    st.subheader("Guardrails Scores")
                    guardrails_df = pd.DataFrame([
                        {"Check": k.replace('_', ' ').title(), "Score": v} 
                        for k, v in guardrails['scores'].items()
                    ])
                    st.dataframe(guardrails_df, use_container_width=True)
        
        st.divider()
    
    # Detailed results
    for eval_name, eval_results in results['evaluations'].items():
        with st.expander(f"📈 {eval_name} Results", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Metrics")
                metrics_df = pd.DataFrame([
                    {"Metric": k, "Value": v} 
                    for k, v in eval_results.items() 
                    if k != 'status' and isinstance(v, (int, float))
                ])
                
                if not metrics_df.empty:
                    st.dataframe(metrics_df, use_container_width=True)
            
            with col2:
                st.subheader("Status")
                if eval_results.get('status') == 'completed':
                    st.success("✅ Evaluation completed successfully")
                else:
                    st.warning("⏳ Evaluation in progress")
    
    # Export options
    st.subheader("📥 Export Results")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download JSON Report"):
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="evaluation_results.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Download CSV Report"):
            # Convert results to CSV format
            csv_data = []
            for eval_name, eval_results in results['evaluations'].items():
                for metric, value in eval_results.items():
                    if metric != 'status':
                        csv_data.append({
                            'Evaluator': eval_name,
                            'Metric': metric,
                            'Value': value
                        })
            
            if csv_data:
                csv_df = pd.DataFrame(csv_data)
                csv_str = csv_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_str,
                    file_name="evaluation_results.csv",
                    mime="text/csv"
                )

def main():
    """Main application function"""
    initialize_session_state()
    render_header()
    
    # Configuration sidebar
    config = render_configuration_sidebar()
    
    # Main content
    if not st.session_state.config_valid:
        st.warning("⚠️ Please configure your watsonx settings in the sidebar to continue.")
        st.info("💡 You can set environment variables WATSONX_API_KEY, WATSONX_PROJECT_ID, and WATSONX_INSTANCE_ID to pre-fill the configuration.")
        return
    
    # Prompt and model input
    prompt_config = render_prompt_input()
    
    # Check if prompt has changed and clear results if so
    current_prompt = prompt_config['prompt_text']
    if current_prompt != st.session_state.last_prompt:
        st.session_state.evaluation_results = None
        st.session_state.last_prompt = current_prompt
    
    # Real-time guardrails check
    if config.get('enable_guardrails', False) and prompt_config['prompt_text'].strip():
        st.header("🛡️ Real-time Guardrails Check")
        
        guardrails_results = evaluate_guardrails_realtime(prompt_config['prompt_text'], config)
        
        col1, col2 = st.columns(2)
        with col1:
            if guardrails_results['passed']:
                st.success("✅ Guardrails Passed")
                st.write(guardrails_results['message'])
            else:
                st.error("❌ Guardrails Violations Detected")
                st.write(guardrails_results['message'])
                for violation in guardrails_results['violations']:
                    st.warning(f"⚠️ {violation}")
        
        with col2:
            if guardrails_results['scores']:
                st.subheader("Guardrails Scores")
                scores_df = pd.DataFrame([
                    {"Check": k.replace('_', ' ').title(), "Score": v} 
                    for k, v in guardrails_results['scores'].items()
                ])
                st.dataframe(scores_df, use_container_width=True)
        
        # If guardrails failed, don't proceed with model evaluation
        if not guardrails_results['passed']:
            st.error("🚫 Model evaluation blocked due to guardrails violations. Please modify your prompt and try again.")
            return
        
        st.divider()
    
    # Evaluator selection
    selected_evaluators = render_evaluator_selection()
    
    # Evaluation and reset buttons
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
    
    with col2:
        if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
            if not prompt_config['prompt_text'].strip():
                st.error("Please enter a prompt to evaluate.")
                return
            
            if not selected_evaluators:
                st.error("Please select at least one evaluator.")
                return
            
            # Final guardrails check before evaluation
            if config.get('enable_guardrails', False):
                final_guardrails = evaluate_guardrails_realtime(prompt_config['prompt_text'], config)
                if not final_guardrails['passed']:
                    st.error("❌ Final guardrails check failed. Cannot proceed with evaluation.")
                    return
            
            # Show progress
            with st.spinner("Running evaluation..."):
                try:
                    results = simulate_evaluation(config, prompt_config, selected_evaluators)
                    # Add guardrails results to evaluation results
                    if config.get('enable_guardrails', False):
                        results['guardrails'] = guardrails_results
                    st.session_state.evaluation_results = results
                    st.success("✅ Evaluation completed successfully!")
                except Exception as e:
                    st.error(f"❌ Evaluation failed: {str(e)}")
                    return
    
    with col3:
        if st.button("🔄 Reset Results", use_container_width=True):
            st.session_state.evaluation_results = None
            st.rerun()
    
    # Display results
    if st.session_state.evaluation_results:
        st.divider()
        render_results(st.session_state.evaluation_results)

if __name__ == "__main__":
    main()