import pandasql as ps
import seaborn as sns
import matplotlib.pyplot as plt

from data.graph_config import GraphConfig

def plot_barchart(query: str, config: GraphConfig) -> None:
    try:
        table = ps.sqldf(query, {'df': config.source})

        plt.figure(figsize=(16, 8))
        sns.set_theme(style="whitegrid")

        plot = sns.catplot(
            data=table,
            x=config.x,
            y=config.y,
            hue=config.color_separation_variable,
            col=config.subplots_variable,
            kind=config.graph_type,
            legend_out=True,
            height=6,
            aspect=1.5,
        )

        plot.set_xticklabels(rotation=45, ha='right')             
        plot.figure.suptitle(config.title)

        plt.savefig(config.output_path, dpi=300, bbox_inches='tight')
    except Exception as e:
        print(f"Failed to create graph: {e}")

def plot_piechart(query: str, config: GraphConfig) -> None:
    try:
        table = ps.sqldf(query, {'df': config.source})

        plt.figure(figsize=(16, 8))
        plt.pie(
            table[config.y],
            labels=table[config.x],
            autopct='%1.0f%%',
            startangle=140
        )
        plt.axis('equal')
        plt.title(config.title)

        plt.savefig(config.output_path, dpi=300, bbox_inches='tight')
    except Exception as e:
        print(f"Failed to create pie chart: {e}")
