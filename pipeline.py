import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

def get_processed_data():
    print("⚙️ Initiating High-Fidelity Synthetic Conversation Generation Pipeline...")
    
    # 1. Core Dimensions Configuration
    agents = ["Rahul Kumar", "Sneha Nair", "Amit Sharma", "Priya Patel", "Vikram Singh"]
    call_types = ["Technical Support", "Billing Complaint", "High-Value Sales"]
    
    # Predefined dialog templates to mimic real call center scripts
    dialogue_templates = {
        "Technical Support": [
            ("Agent: Welcome to Support. How can I help you resolve your router issue today?", "Customer: My internet keeps dropping. I am very frustrated with this service."),
            ("Agent: Let me check that for you right away. I am pulling up your diagnostic line data.", "Customer: Okay, please hurry up. I have a remote work shift starting soon."),
            ("Agent: I understand your concern completely. I have initiated a signal reset on your line.", "Customer: Great, the light on my router just turned solid green! Thank you for calling it out.")
        ],
        "Billing Complaint": [
            ("Agent: Thank you for calling account services. How can I help you navigate your bill today?", "Customer: You charged me double this month! This is an absolute joke."),
            ("Agent: Let me check that for you on our ledger systems.", "Customer: It should be $45, but you deducted $90 from my account without notice."),
            ("Agent: I see the error; a promo code dropped off. I understand your concern and applied a credit.", "Customer: Thank you. I appreciate you fixing this mistake so quickly.")
        ],
        "High-Value Sales": [
            ("Agent: Hello! How can I help you find the right enterprise software package today?", "Customer: I am looking to upgrade our team plan but want to negotiate pricing."),
            ("Agent: Let me check that for you. We have a tier discount if you sign an annual agreement.", "Customer: That sounds interesting. What features are included in that tier?"),
            ("Agent: You get unlimited storage and an automated QA dashboard module.", "Customer: That matches our operational needs perfectly. Let's go ahead and sign.")
        ]
    }
    
    processed_records = []
    analyzer = SentimentIntensityAnalyzer()
    
    # Generate 150 unique, highly analytic rows instantly
    for idx in range(150):
        c_type = random.choice(call_types)
        agent = random.choice(agents)
        
        # Pick the scenario template
        turns_pool = dialogue_templates[c_type]
        
        agent_turns = [turn[0] for turn in turns_pool]
        customer_turns = [turn[1] for turn in turns_pool]
        
        # Build the coherent full transcript text
        full_transcript = "\n".join([f"{a}\n{c}" for a, c in zip(agent_turns, customer_turns)])
        
        # --- NLP CALCULATION ENGINE ---
        # 1. Sentiment Arc Implementation
        customer_scores = [analyzer.polarity_scores(turn)['compound'] for turn in customer_turns]
        avg_customer_sentiment = np.mean(customer_scores) if customer_scores else 0.0
        
        # Sentiment Recovery Metric (Did the sentiment improve over the call?)
        sentiment_recovery = 1.0 if (len(customer_scores) > 1 and customer_scores[-1] > customer_scores[0]) else 0.0
        
        # 2. Conversational Balance (Talk-to-Listen Ratio)
        agent_words = len(" ".join(agent_turns).split())
        customer_words = len(" ".join(customer_turns).split())
        total_words = agent_words + customer_words
        talk_ratio = (agent_words / total_words) if total_words > 0 else 0.5
        talk_balance_score = 1.0 if talk_ratio <= 0.60 else (1.0 - (talk_ratio - 0.60))
        
        # 3. Compliance Framework Script Adherence
        REQUIRED_PHRASES = ["how can i help", "let me check", "understand your concern", "thank you for calling"]
        agent_text_lower = " ".join(agent_turns).lower()
        matched_phrases = sum(1 for phrase in REQUIRED_PHRASES if phrase in agent_text_lower)
        script_adherence = matched_phrases / len(REQUIRED_PHRASES)
        
        # 4. Enterprise Composite Weight Matrix
        quality_score = (
            (avg_customer_sentiment * 35) + 
            (script_adherence * 30) + 
            (talk_balance_score * 20) + 
            (sentiment_recovery * 15)
        )
        # Scale cleanly between 0-100%
        normalized_score = max(0.0, min(100.0, (quality_score + 35) if avg_customer_sentiment < 0 else quality_score))

        # Inject deliberate poor-performance outliers to make charts beautiful
        if agent == "Amit Sharma" and c_type == "Billing Complaint":
            normalized_score -= 25.0
            avg_customer_sentiment -= 0.4
            script_adherence = 0.25

        processed_records.append({
            "call_id": f"CNV-2026-{idx:04d}",
            "date": pd.Timestamp('2026-06-01') + pd.to_timedelta(random.randint(0, 22), unit='D'),
            "agent_name": agent,
            "call_type": c_type,
            "duration_seconds": random.randint(120, 600),
            "full_transcript": full_transcript,
            "quality_score": max(5.0, min(100.0, normalized_score)),
            "sentiment_score": avg_customer_sentiment,
            "talk_ratio": talk_ratio,
            "script_adherence": script_adherence,
            "individual_customer_scores": customer_scores
        })
        
    print(f"✅ Successfully initialized {len(processed_records)} clean analytics records!")
    return pd.DataFrame(processed_records)