import torch
from diffusers import CogVideoXPipeline
from diffusers.hooks import apply_group_offloading
from diffusers.utils import export_to_video

onload_device = torch.device("cuda")
offload_device = torch.device("cpu")

pipeline = CogVideoXPipeline.from_pretrained("THUDM/CogVideoX-5b")

pipeline.to("cuda", dtype=torch.float16)
pipeline.enable_group_offload(
  onload_device=onload_device,
  offload_device=offload_device,
  offload_type="leaf_level",
  use_stream=True
)

prompt = (
  "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest. "
  "The panda's fluffy paws strum a miniature acoustic guitar, producing soft, melodic tunes. Nearby, a few other "
  "pandas gather, watching curiously and some clapping in rhythm. Sunlight filters through the tall bamboo, "
  "casting a gentle glow on the scene. The panda's face is expressive, showing concentration and joy as it plays. "
  "The background includes a small, flowing stream and vibrant green foliage, enhancing the peaceful and magical "
  "atmosphere of this unique musical performance."
)
video = pipeline(prompt=prompt, guidance_scale=6, num_inference_steps=50).frames[0]
print(f"Max memory reserved: {torch.cuda.max_memory_allocated() / 1024**3:.2f} GB")
export_to_video(video, "output.mp4", fps=8)