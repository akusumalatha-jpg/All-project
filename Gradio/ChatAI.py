import gradio as gr

def chat(message, history):
    if history is None:
        history = []

    history.append({"role": "user", "content": message})

    reply = f"You said: {message}"

    history.append({"role": "assistant", "content": reply})

    return "", history

with gr.Blocks(title="Local AI Studio") as demo:

    gr.Markdown("# 🤖 Local AI Studio")

    chatbot = gr.Chatbot(height=500)

    msg = gr.Textbox(
        placeholder="Type your message..."
    )

    send = gr.Button("Send")

    send.click(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

    msg.submit(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

demo.launch()