from typing import Any
import torch
import gradio as gr
from diffusers.pipelines.pipeline_utils import DiffusionPipeline

print("Loading Diffusion Pipeline...")
try:
    pipe: Any = DiffusionPipeline.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=torch.float32,   # float16 isn't reliably supported on CPU
        low_cpu_mem_usage=True,
    )

    # Move to GPU if available, otherwise stay on CPU but optimize it
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
        pipe.unet.to(memory_format=torch.channels_last)
        print("Running on GPU")
    else:
        # CPU-specific speedups
        torch.set_num_threads(torch.get_num_threads())  # uses all available cores
        pipe.unet.to(memory_format=torch.channels_last)
        print("Running on CPU (no GPU detected)")

    # Reduces VRAM/RAM spikes during attention computation
    pipe.enable_attention_slicing()

    print("Pipeline loaded successfully!")
except Exception as e:
    print(f"Error loading pipeline: {e}")
    pipe = None


def generate_image(prompt: str):
    if pipe is None:
        return None

    print(f"Generating image for prompt: {prompt}")
    result = pipe(
        prompt=prompt,
        num_inference_steps=1,   # sd-turbo is designed for 1-4 steps
        guidance_scale=0.0,
        height=512,
        width=512,
    )
    return result.images[0]


with gr.Blocks(theme="soft", title="Local Image Generator") as demo:
    gr.Markdown("# Local Image Generation (CPU-Optimized)")

    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(
                label="Enter prompt",
                placeholder="A small sailboat on a calm lake...",
            )
            generate_btn = gr.Button("Generate", variant="primary")
        with gr.Column():
            image_output = gr.Image(label="Generated Output")

    generate_btn.click(
        fn=generate_image,
        inputs=prompt_input,
        outputs=image_output,
    )

if __name__ == "__main__":
    demo.launch()