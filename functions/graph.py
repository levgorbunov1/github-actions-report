import pandasql as ps
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from data.graph_config import GraphConfig

def plot_barchart(query: str, config: GraphConfig) -> None:
    try:
        table = ps.sqldf(query, {'df': config.source})

        print("Graph table:")
        print(table)

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

        print("Graph table:")
        print(table)

        plt.figure(figsize=(16, 8))
        plt.pie(
            table[config.y],
            labels=[
                f"{version} (latest)" if latest == 1 else version
                for version, latest in zip(table['version'], table['latest'])
            ],
            startangle=140,
            colors=['red' if value == 0 else 'green' for value in table[config.color_separation_variable]] if config.color_separation_variable else None,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5} if table.shape[0] > 1 else None,
            autopct=lambda pct: f"{int(round(pct * sum(table[config.y].tolist()) / 100.0))} ({pct:.0f}%)"
        )

        if config.color_separation_variable:
            plt.legend(handles=[
                Patch(facecolor='green', label='Latest'),
                Patch(facecolor='red', label='Outdated')
            ])

        plt.axis('equal')
        plt.title(config.title)

        plt.savefig(config.output_path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Failed to create pie chart: {e}")
