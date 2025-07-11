import os

def generate_report(images_dir: str, output_md: str):
    try:
        pie_charts_dir = os.path.join(images_dir, "pie_charts")

        with open(output_md, "w") as f:
            if os.path.isdir(pie_charts_dir):
                pie_chart_files = [file for file in os.listdir(pie_charts_dir)if file.lower().endswith(".png")]

                if pie_chart_files:
                    f.write("<table>\n")
                    for i, filename in enumerate(pie_chart_files):
                        if i != 0 and i % 3 == 0:
                            f.write("</tr>\n<tr>\n")
                        
                        f.write(f'  <td><img src="{os.path.join(pie_charts_dir, filename).replace("\\", "/")}" width="300"/></td>\n')
                    
                    f.write("</tr>\n</table>\n\n<br><br><br><br>")

            other_files = [file for file in os.listdir(images_dir) if file.lower().endswith(".png")]

            for filename in other_files:
                f.write(f"![{filename}]({os.path.join(images_dir, filename).replace("\\", "/")})\n\n")

        print(f"Markdown report generated: {output_md}")
    except Exception as e:
        print(f"Failed to produce report: {e}")

