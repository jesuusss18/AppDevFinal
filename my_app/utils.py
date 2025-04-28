import plotly.express as px
import plotly.io as pio

def generate_graph(data):
    # Create bar chart
    fig = px.bar(data, x='months', y='expenses', title='Monthly Expenses')

    # Update chart layout
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            tickangle=45,
            tickfont=dict(size=14),
            showgrid=True,
            title='Months',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(0,0,0,1)',
        width=1000,
        height=600,
        margin=dict(l=60, r=60, t=60, b=120)
    )

    # Set bar color
    fig.update_traces(marker_color='#008c41')

    # Convert figure to JSON
    graph_json = pio.to_json(fig)

    return graph_json

