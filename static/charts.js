const dataURL = "https://d3js-in-action-third-edition.github.io/hosted-data/apis/front_end_frameworks.json";
// for local development you can always download and place them in static "assets/front_end_frameworks.json";

document.addEventListener('alpine:init', () => {
Alpine.store('framework', {
    selected: 'satisfaction',
    data: [],
    colorScale: () => "black",
    loaded: false
});

});

document.addEventListener("alpine:init", () => {
Alpine.data("scatterplot", (width, height) => ({
    circles: [],
    width: width,
    height: height,
    xlabel: "User Count",
    ylabel: "Retention %",
    xScale: d3.scaleLinear(),
    yScale: d3.scaleLinear(),
    xticks: [],
    yticks: [],
    render(value) {
        let data = value.experience;
        this.xScale
            .domain([0, d3.max(data, d => d.user_count)])
            .range([0, this.width]);
        this.yScale
            .domain([0, 100])
            .range([height, 0]);
        this.xticks = this.xScale.ticks(this.width/100);
        this.yticks = this.yScale.ticks(this.height/50);
        this.circles = data.map(d => {return {x: this.xScale(d.user_count), 
                                              y: this.yScale(d.retention_percentage),
                                              f: this.$store.framework.colorScale(d.id)} });
    },
}))
}) ;

document.addEventListener('DOMContentLoaded', () => {
    d3.json(dataURL).then(data => {
                    Alpine.store("framework").data = data
                    Alpine.store("framework").loaded = true;
                    Alpine.store("framework").colorScale = d3.scaleOrdinal()
                    .domain(data.ids.map(d => d))
                    .range(d3.schemeTableau10);
                    htmx.trigger('#rankings','renderPlot');
                    htmx.trigger('#barchart','renderPlot')
                    });
});