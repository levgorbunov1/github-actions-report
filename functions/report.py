import os

def generate_report(images_dir: str, output_md: str):
    try:
        with open(output_md, "w") as f:
            for filename in sorted(os.listdir(images_dir)):
                if filename.lower().endswith(".png"):
                    image_path = os.path.join(images_dir, filename).replace("\\", "/")
                    f.write(f"![{filename}]({image_path})\n\n")

        print(f"Markdown report generated: {output_md}")
    except Exception as e:
        print(f"Failed to produce report: {e}")