# Imports
import gradio as gr
from pipeline import generate

def main():
    # Gradio interface
    with gr.Blocks() as demo:
        gr.Markdown("# DataForge AI 🛢️")
        user_input = gr.Textbox(label="Enter dataset description: ")
        generate_button = gr.Button("Generate dataset")
        status = gr.Textbox(label="Status", interactive=False)
        file_output = gr.File(label="Download CSV")
        generate_button.click(fn=generate, inputs=user_input, outputs=[status, file_output])

    demo.launch()

if __name__ == "__main__":
    main()
