import pandasql as ps
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx
import math

from data.graph_config import GraphConfig, NetworkGraphConfig

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

def relative_shell_layout(graph, root, base_layer1_distance=3.0, base_layer2_distance=0.5, scaling_factor=0.03):
    pos = {}
    pos[root] = (0, 0)

    repos = list(graph.successors(root))
    num_repos = len(repos)
    dynamic_layer1_distance = base_layer1_distance + scaling_factor * num_repos

    for i, repo in enumerate(repos):
        angle = 2 * math.pi * i / num_repos
        x = dynamic_layer1_distance * math.cos(angle)
        y = dynamic_layer1_distance * math.sin(angle)
        pos[repo] = (x, y)

        actions = list(graph.successors(repo))
        num_actions = len(actions)
        dynamic_layer2_distance = base_layer2_distance + scaling_factor * num_actions

        for j, action in enumerate(actions):
            angle_offset = 2 * math.pi * j / max(num_actions, 1)
            ax = x + dynamic_layer2_distance * math.cos(angle_offset)
            ay = y + dynamic_layer2_distance * math.sin(angle_offset)
            pos[action] = (ax, ay)

    return pos

def plot_network(query: str, config: NetworkGraphConfig) -> None:
    table = ps.sqldf(query, {'df': config.source})

    print("Graph table:")
    print(table)

    graph = nx.DiGraph()

    root_node = config.root_node
    graph.add_node(root_node, type='root', color='orange', size=6000)

    for i, row in table.iterrows():
        layer_1 = row[config.layer_1]
        layer_2 = f"{layer_1}:{row[config.layer_2]}"
        color_separator = row[config.color_separation_variable]

        graph.add_node(layer_1, type=config.layer_1, color='skyblue', size=1000)
        graph.add_node(layer_2, type=config.layer_2, color='green' if color_separator else 'red')

        graph.add_edge(root_node, layer_1)
        graph.add_edge(layer_1, layer_2)

    plt.figure(figsize=(20, 10))
    pos = relative_shell_layout(graph, root_node)

    nx.draw(
        graph, 
        pos, 
        with_labels=True, 
        labels={
            node: (
                node.split(":")[1]
                if data.get("type") == config.layer_2 else node
            )
            for node, data in graph.nodes(data=True)
        },
        node_color=[node.get('color') for i, node in graph.nodes(data=True)], 
        node_size = [node.get('size', 300) for i, node in graph.nodes(data=True)],
        font_size=8, 
        edge_color='gray', 
        arrows=True
    )

    plt.title(config.title)
    plt.savefig(config.output_path, dpi=300, bbox_inches='tight')
    plt.close()