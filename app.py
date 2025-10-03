import gradio as gr
from datetime import datetime

def reply(msg):
    return f"Hello, {msg}! ✅\n(Deployed from GitHub at {datetime.utcnow().isoformat()}Z)"

with gr.Blocks() as demo:
    gr.Markdown("# Space Auth Demo\nType your name and hit Send.")
    inp = gr.Textbox(label="Your name")
    out = gr.Textbox(label="Response")
    gr.Button("Send").click(fn=reply, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch()
