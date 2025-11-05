import gradio as gr
import joblib

# Load models from the same directory (upload these .pkl files to your Space!)
difficulty_reg = joblib.load("difficulty_estimator.pkl")
difficulty_cls = joblib.load("difficulty_classifier.pkl")
metrics_reg = joblib.load("metrics_regressor.pkl")

def predict_difficulty(avg_loops, avg_conditionals, avg_fns, avg_nesting, problem_length, num_solutions, num_tests):
    features = [avg_loops, avg_conditionals, avg_fns, avg_nesting, problem_length, num_solutions, num_tests]
    diff_score = float(difficulty_reg.predict([features])[0])
    diff_class = str(difficulty_cls.predict([features])[0])
    metrics = metrics_reg.predict([features])[0].tolist()
    return {
        "difficulty_score": diff_score,
        "difficulty_class": diff_class,
        "predicted_code_metrics": metrics,
    }

iface = gr.Interface(
    fn=predict_difficulty,
    inputs=[
        gr.Number(label="Avg Loops"),
        gr.Number(label="Avg Conditionals"),
        gr.Number(label="Avg Function Definitions"),
        gr.Number(label="Avg Max Nesting Depth"),
        gr.Number(label="Problem Length"),
        gr.Number(label="Num Solutions"),
        gr.Number(label="Num Test Cases"),
    ],
    outputs="json",
    title="DSA Mentor AI - Prediction API",
    description="Enter code/problem features to get difficulty, class, and code metrics from AI"
)

iface.launch()
