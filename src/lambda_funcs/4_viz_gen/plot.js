var plots = ['uptime_heatmap']

for (let plot of plots) {
    Plotly.d3.json('plots/' + plot + ".json", function (error, data) {
        if (error) return console.warn(error);
        Plotly.newPlot(plot, data.data, data.layout, { responsive: true });
    });
}