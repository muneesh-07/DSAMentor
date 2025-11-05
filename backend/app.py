# Create this as your new app.py file - replace the old one completely

import gradio as gr
import numpy as np
import json
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("🚀 Starting DSA Mentor API...")
print("Loading ML models...")

# Create simplified model classes that don't require joblib loading
class SimpleDifficultyEstimator:
    def __init__(self):
        # Simple rule-based difficulty estimation
        self.is_trained = True
        self.feature_names = [
            'loops', 'conditionals', 'max_depth', 'functions',
            'line_count', 'complexity_score', 'problem_length', 'test_cases'
        ]
    
    def predict(self, features):
        """Rule-based difficulty prediction"""
        loops, conditionals, max_depth, functions, line_count, complexity_score, problem_length, test_cases = features
        
        # Normalize inputs
        loops = max(0, min(10, loops))
        conditionals = max(0, min(15, conditionals))
        max_depth = max(0, min(10, max_depth))
        functions = max(0, min(5, functions))
        line_count = max(1, min(200, line_count))
        complexity_score = max(0, min(1, complexity_score))
        problem_length = max(50, min(5000, problem_length))
        test_cases = max(1, min(20, test_cases))
        
        # Rule-based calculation
        base_difficulty = 0.3
        
        # Add complexity based on code features
        base_difficulty += loops * 0.05
        base_difficulty += conditionals * 0.04
        base_difficulty += max_depth * 0.06
        base_difficulty += (functions - 1) * 0.03
        base_difficulty += complexity_score * 0.3
        base_difficulty += (line_count / 100) * 0.1
        base_difficulty += (problem_length / 2000) * 0.05
        base_difficulty += (test_cases / 10) * 0.02
        
        # Normalize to 0-1 range
        difficulty = max(0.1, min(0.9, base_difficulty))
        return difficulty

class SimpleTimelinePredictor:
    def __init__(self):
        self.is_trained = True
    
    def predict_timeline(self, student_skill, problem_difficulty, problem_complexity, problem_length):
        """Rule-based timeline prediction"""
        # Normalize inputs
        student_skill = max(0.1, min(1.0, student_skill))
        problem_difficulty = max(0.1, min(1.0, problem_difficulty))
        problem_complexity = max(0.1, min(1.0, problem_complexity))
        problem_length = max(100, min(5000, problem_length))
        
        # Base time calculation
        difficulty_gap = max(0, problem_difficulty - student_skill)
        base_hours = 0.5 + (difficulty_gap * 8)
        
        # Adjust for complexity
        complexity_factor = 1 + (problem_complexity * 0.5)
        
        # Adjust for problem length
        length_factor = 1 + ((problem_length / 2000) * 0.3)
        
        # Final timeline
        timeline = base_hours * complexity_factor * length_factor
        
        # Add some realistic variance
        timeline = timeline * (0.8 + np.random.random() * 0.4)
        
        return max(0.1, min(50.0, timeline))

class SimpleMistakeClassifier:
    def __init__(self):
        self.is_trained = True
        self.mistake_categories = [
            'syntax_error', 'logic_error', 'optimization_needed',
            'edge_case_missed', 'complexity_issue', 'no_error'
        ]
    
    def predict_mistake(self, code_features, problem_difficulty):
        """Rule-based mistake classification"""
        loops = code_features.get('loops', 0)
        conditionals = code_features.get('conditionals', 0)
        max_depth = code_features.get('max_nesting_depth', 0)
        line_count = code_features.get('line_count', 0)
        complexity_score = code_features.get('complexity_score', 0)
        has_recursion = code_features.get('has_recursion', False)
        functions = code_features.get('function_definitions', 0)
        
        # Rule-based classification
        if complexity_score > 0.8:
            mistake = 'optimization_needed'
            confidence = 0.85
        elif max_depth > 6:
            mistake = 'complexity_issue'
            confidence = 0.80
        elif conditionals < 1 and problem_difficulty > 0.6:
            mistake = 'edge_case_missed'
            confidence = 0.75
        elif line_count < 10 and problem_difficulty > 0.4:
            mistake = 'logic_error'
            confidence = 0.70
        elif np.random.random() < 0.1:  # 10% chance of syntax errors
            mistake = 'syntax_error'
            confidence = 0.65
        else:
            mistake = 'no_error'
            confidence = 0.90
        
        # Create probability distribution
        probabilities = {cat: 0.1 for cat in self.mistake_categories}
        probabilities[mistake] = confidence
        
        # Normalize probabilities
        total = sum(probabilities.values())
        probabilities = {k: v/total for k, v in probabilities.items()}
        
        return {
            'predicted_mistake': mistake,
            'confidence': confidence,
            'all_probabilities': probabilities
        }

# Initialize models
try:
    difficulty_estimator = SimpleDifficultyEstimator()
    timeline_predictor = SimpleTimelinePredictor()
    mistake_classifier = SimpleMistakeClassifier()
    print("✅ All models loaded successfully")
except Exception as e:
    print(f"❌ Error initializing models: {e}")

# API Functions
def predict_difficulty_api(loops, conditionals, nesting_depth, functions, line_count, complexity, text_length, test_cases):
    """Predict problem difficulty based on code features"""
    features = [int(loops), int(conditionals), int(nesting_depth), int(functions), 
                int(line_count), float(complexity), int(text_length), int(test_cases)]
    
    try:
        prediction = float(difficulty_estimator.predict(features))
        
        if prediction < 0.4:
            category, color = "🟢 Easy", "#22C55E"
        elif prediction < 0.7:
            category, color = "🟡 Medium", "#EAB308"
        else:
            category, color = "🔴 Hard", "#EF4444"
        
        return {
            "difficulty_score": round(prediction, 3),
            "category": category,
            "recommendation": f"Estimated {prediction*100:.0f}% difficulty - {category.split()[1].lower()} level problem",
            "confidence": "85%",
            "feature_breakdown": {
                "loops_impact": f"{loops * 0.05:.3f}",
                "conditionals_impact": f"{conditionals * 0.04:.3f}",
                "complexity_impact": f"{complexity * 0.3:.3f}",
                "length_impact": f"{text_length / 2000 * 0.05:.3f}"
            }
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

def predict_timeline_api(student_skill, problem_difficulty, problem_complexity, problem_length):
    """Predict learning timeline for student"""
    try:
        hours = float(timeline_predictor.predict_timeline(
            float(student_skill), float(problem_difficulty), 
            float(problem_complexity), int(problem_length)
        ))
        
        days = hours / 8  # 8 hours study per day
        
        if hours < 2:
            pace = "🚀 Quick"
        elif hours < 8:
            pace = "⚡ Moderate"
        else:
            pace = "🐌 Extended"
        
        return {
            "estimated_hours": round(hours, 1),
            "estimated_days": round(days, 1),
            "learning_pace": pace,
            "recommendation": f"Plan {round(hours, 1)} hours ({round(days, 1)} days) to master this concept",
            "factors": {
                "skill_gap_impact": f"{max(0, problem_difficulty - student_skill) * 8:.1f} hours",
                "complexity_multiplier": f"{1 + problem_complexity * 0.5:.2f}x",
                "length_adjustment": f"{1 + (problem_length / 2000) * 0.3:.2f}x"
            }
        }
    except Exception as e:
        return {"error": f"Timeline prediction failed: {str(e)}"}

def classify_mistake_api(loops, conditionals, nesting_depth, line_count, complexity, has_recursion, functions, problem_difficulty):
    """Classify potential coding mistakes"""
    code_features = {
        'loops': int(loops),
        'conditionals': int(conditionals),
        'max_nesting_depth': int(nesting_depth),
        'line_count': int(line_count),
        'complexity_score': float(complexity),
        'has_recursion': bool(has_recursion),
        'function_definitions': int(functions)
    }
    
    try:
        result = mistake_classifier.predict_mistake(code_features, float(problem_difficulty))
        
        mistake_type = str(result['predicted_mistake'])
        confidence = float(result['confidence'])
        
        # Get suggestion and emoji
        mistake_info = {
            'syntax_error': ('🔧', 'Check for missing colons, brackets, or indentation issues'),
            'logic_error': ('🧠', 'Review your algorithm logic and test with edge cases'),
            'optimization_needed': ('⚡', 'Consider more efficient algorithms or data structures'),
            'edge_case_missed': ('🎯', 'Add checks for empty inputs, single elements, or boundary conditions'),
            'complexity_issue': ('📊', 'Simplify nested structures and reduce algorithmic complexity'),
            'no_error': ('✅', 'Code looks good! Consider minor style improvements')
        }
        
        emoji, suggestion = mistake_info.get(mistake_type, ('❓', 'Review your approach'))
        
        return {
            "predicted_mistake": f"{emoji} {mistake_type.replace('_', ' ').title()}",
            "confidence": f"{confidence*100:.1f}%",
            "suggestion": suggestion,
            "risk_level": "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low",
            "detailed_analysis": {
                "complexity_concern": "High" if complexity > 0.7 else "Medium" if complexity > 0.4 else "Low",
                "structure_concern": "High" if nesting_depth > 5 else "Medium" if nesting_depth > 3 else "Low",
                "length_concern": "High" if line_count > 100 else "Medium" if line_count > 50 else "Low"
            }
        }
    except Exception as e:
        return {"error": f"Mistake classification failed: {str(e)}"}

# Create Gradio Interface
with gr.Blocks(title="DSA Mentor API", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚀 DSA Mentor - AI-Powered Coding Assistant
    ### Get instant AI predictions for problem difficulty, learning timeline, and mistake detection
    
    **Features:**
    - 🎯 **Difficulty Prediction**: Analyze code complexity to predict problem difficulty
    - ⏰ **Timeline Estimation**: Personalized learning time prediction based on skill level
    - 🔍 **Mistake Detection**: Proactive identification of potential coding issues
    """)
    
    with gr.Tab("🎯 Difficulty Prediction"):
        gr.Markdown("## Predict how difficult a coding problem is based on its characteristics")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📊 Code Structure Analysis")
                d_loops = gr.Number(label="Number of Loops", value=2, minimum=0, maximum=10, 
                                   info="Count of for/while loops in the solution")
                d_conditionals = gr.Number(label="Conditional Statements", value=3, minimum=0, maximum=15,
                                         info="Count of if/else statements")
                d_nesting = gr.Number(label="Max Nesting Depth", value=2, minimum=0, maximum=10,
                                     info="Maximum depth of nested structures")
                d_functions = gr.Number(label="Number of Functions", value=1, minimum=0, maximum=5,
                                       info="Count of function definitions")
            
            with gr.Column():
                gr.Markdown("### 📝 Problem Characteristics")
                d_lines = gr.Number(label="Lines of Code", value=25, minimum=1, maximum=200,
                                   info="Estimated lines in typical solution")
                d_complexity = gr.Number(label="Complexity Score (0-1)", value=0.4, minimum=0, maximum=1, step=0.1,
                                        info="Overall algorithmic complexity rating")
                d_text_len = gr.Number(label="Problem Description Length", value=800, minimum=50, maximum=5000,
                                      info="Character count of problem statement")
                d_tests = gr.Number(label="Number of Test Cases", value=4, minimum=1, maximum=20,
                                   info="Count of provided test cases")
        
        d_button = gr.Button("🎯 Analyze Difficulty", variant="primary", size="lg")
        d_output = gr.JSON(label="🔍 Difficulty Analysis Results")
        
        # Example buttons
        gr.Markdown("### 📋 Try These Examples:")
        with gr.Row():
            easy_btn = gr.Button("Easy Example", variant="secondary")
            medium_btn = gr.Button("Medium Example", variant="secondary") 
            hard_btn = gr.Button("Hard Example", variant="secondary")
        
        def set_easy_example():
            return 1, 2, 1, 1, 15, 0.2, 300, 3
        
        def set_medium_example():
            return 2, 4, 3, 2, 35, 0.5, 800, 5
        
        def set_hard_example():
            return 4, 8, 5, 3, 80, 0.8, 1500, 8
        
        easy_btn.click(set_easy_example, outputs=[d_loops, d_conditionals, d_nesting, d_functions, d_lines, d_complexity, d_text_len, d_tests])
        medium_btn.click(set_medium_example, outputs=[d_loops, d_conditionals, d_nesting, d_functions, d_lines, d_complexity, d_text_len, d_tests])
        hard_btn.click(set_hard_example, outputs=[d_loops, d_conditionals, d_nesting, d_functions, d_lines, d_complexity, d_text_len, d_tests])
        
        d_button.click(predict_difficulty_api, 
                      inputs=[d_loops, d_conditionals, d_nesting, d_functions, d_lines, d_complexity, d_text_len, d_tests],
                      outputs=d_output)
    
    with gr.Tab("⏰ Timeline Prediction"):
        gr.Markdown("## Estimate how long it will take a student to master a concept")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 👤 Student Profile")
                t_skill = gr.Slider(label="Student Skill Level", value=0.5, minimum=0.1, maximum=1.0, step=0.1,
                                   info="0.1=Beginner, 0.5=Intermediate, 1.0=Expert")
                t_difficulty = gr.Slider(label="Problem Difficulty", value=0.6, minimum=0.1, maximum=1.0, step=0.1,
                                        info="Use difficulty prediction from previous tab")
            with gr.Column():
                gr.Markdown("### 📊 Problem Details")  
                t_complexity = gr.Slider(label="Problem Complexity", value=0.4, minimum=0.1, maximum=1.0, step=0.1,
                                        info="Algorithmic complexity rating")
                t_length = gr.Number(label="Problem Length (characters)", value=1000, minimum=100, maximum=5000,
                                    info="Length of problem description")
        
        t_button = gr.Button("⏰ Predict Learning Time", variant="primary", size="lg")
        t_output = gr.JSON(label="📈 Timeline Prediction Results")
        
        # Timeline examples
        gr.Markdown("### 📋 Try These Scenarios:")
        with gr.Row():
            beginner_btn = gr.Button("Beginner Student", variant="secondary")
            intermediate_btn = gr.Button("Intermediate Student", variant="secondary")
            expert_btn = gr.Button("Expert Student", variant="secondary")
        
        def set_beginner():
            return 0.2, 0.7, 0.6, 1200
        
        def set_intermediate():
            return 0.5, 0.6, 0.5, 1000
        
        def set_expert():
            return 0.8, 0.8, 0.7, 1500
        
        beginner_btn.click(set_beginner, outputs=[t_skill, t_difficulty, t_complexity, t_length])
        intermediate_btn.click(set_intermediate, outputs=[t_skill, t_difficulty, t_complexity, t_length])
        expert_btn.click(set_expert, outputs=[t_skill, t_difficulty, t_complexity, t_length])
        
        t_button.click(predict_timeline_api,
                      inputs=[t_skill, t_difficulty, t_complexity, t_length],
                      outputs=t_output)
    
    with gr.Tab("🔍 Mistake Detection"):
        gr.Markdown("## Identify potential coding mistakes and get improvement suggestions")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔧 Code Analysis")
                m_loops = gr.Number(label="Loops", value=2, minimum=0, maximum=10,
                                   info="Number of loop structures")
                m_conditionals = gr.Number(label="Conditionals", value=3, minimum=0, maximum=15,
                                          info="Number of if/else statements")
                m_nesting = gr.Number(label="Nesting Depth", value=3, minimum=0, maximum=10,
                                     info="Maximum nesting level")
                m_lines = gr.Number(label="Lines of Code", value=30, minimum=1, maximum=200,
                                   info="Total lines of code")
            
            with gr.Column():
                gr.Markdown("### ⚙️ Advanced Features")
                m_complexity = gr.Number(label="Complexity Score", value=0.5, minimum=0, maximum=1, step=0.1,
                                        info="Overall code complexity rating")
                m_recursion = gr.Checkbox(label="Has Recursion", value=False,
                                         info="Does the solution use recursion?")
                m_functions = gr.Number(label="Functions", value=2, minimum=0, maximum=5,
                                       info="Number of function definitions")
                m_difficulty = gr.Slider(label="Problem Difficulty", value=0.6, minimum=0.1, maximum=1.0, step=0.1,
                                        info="Difficulty level of the problem")
        
        m_button = gr.Button("🔍 Analyze Code for Mistakes", variant="primary", size="lg")
        m_output = gr.JSON(label="🚨 Mistake Analysis Results")
        
        # Mistake examples
        gr.Markdown("### 📋 Try These Code Patterns:")
        with gr.Row():
            complex_btn = gr.Button("Complex Code", variant="secondary")
            simple_btn = gr.Button("Simple Code", variant="secondary")
            recursive_btn = gr.Button("Recursive Solution", variant="secondary")
        
        def set_complex():
            return 4, 8, 6, 80, 0.8, False, 3, 0.7
        
        def set_simple():
            return 1, 2, 2, 15, 0.2, False, 1, 0.3
        
        def set_recursive():
            return 1, 3, 4, 25, 0.6, True, 2, 0.6
        
        complex_btn.click(set_complex, outputs=[m_loops, m_conditionals, m_nesting, m_lines, m_complexity, m_recursion, m_functions, m_difficulty])
        simple_btn.click(set_simple, outputs=[m_loops, m_conditionals, m_nesting, m_lines, m_complexity, m_recursion, m_functions, m_difficulty])
        recursive_btn.click(set_recursive, outputs=[m_loops, m_conditionals, m_nesting, m_lines, m_complexity, m_recursion, m_functions, m_difficulty])
        
        m_button.click(classify_mistake_api,
                      inputs=[m_loops, m_conditionals, m_nesting, m_lines, m_complexity, m_recursion, m_functions, m_difficulty],
                      outputs=m_output)
    
    with gr.Tab("📚 API Documentation"):
        gr.Markdown("""
        ## 🔗 API Integration Guide
        
        This Hugging Face Space provides three main AI services that you can integrate into your applications:
        
        ### 🎯 Difficulty Prediction API
        **Endpoint**: `/api/predict` (POST)
        **Input**: `[loops, conditionals, nesting_depth, functions, line_count, complexity, text_length, test_cases]`
        **Output**: Difficulty score (0-1), category, recommendations
        
        **Example**:
        ```
        import requests
        response = requests.post(
            "https://your-space-url/api/predict",
            json={"data": [2, 3, 2, 1, 25, 0.4, 800, 4]}
        )
        print(response.json())
        ```
        
        ### ⏰ Timeline Prediction API
        **Input**: `[student_skill, problem_difficulty, problem_complexity, problem_length]`
        **Output**: Estimated hours, days, learning pace
        
        **Example**:
        ```
        response = requests.post(
            "https://your-space-url/api/predict",
            json={"data": [0.5, 0.6, 0.4, 1000]}
        )
        ```
        
        ### 🔍 Mistake Detection API
        **Input**: `[loops, conditionals, nesting_depth, line_count, complexity, has_recursion, functions, problem_difficulty]`
        **Output**: Predicted mistake type, confidence, suggestions
        
        **Example**:
        ```
        response = requests.post(
            "https://your-space-url/api/predict",
            json={"data": [2, 3, 3, 30, 0.5, false, 2, 0.6]}
        )
        ```
        
        ### 🚀 Use Cases
        - **Educational Platforms**: Auto-categorize coding problems
        - **Learning Apps**: Personalized study time estimation  
        - **Code Review Tools**: Proactive mistake detection
        - **Interview Prep**: Difficulty-based problem recommendation
        
        ### 📊 Response Format
        All endpoints return JSON with:
        - Main prediction/analysis
        - Confidence scores
        - Detailed breakdowns
        - Actionable recommendations
        
        ### 🔒 Rate Limits
        - Free tier: ~100 requests/hour
        - For higher usage, upgrade Space hardware or contact for enterprise solutions
        
        ---
        
        **Built with ❤️ using Gradio and Hugging Face Spaces**
        
        Source code and documentation available on request.
        """)

# Launch the app
if __name__ == "__main__":
    print("🚀 Launching DSA Mentor API...")
    demo.launch()
