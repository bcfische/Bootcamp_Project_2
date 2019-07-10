d3.json("/movies").then(function(data) {
    var x = [], y = [];
    for (var i=0; i<data.length; i++) {
        x.push(data[i].title);
        y.push(data[i].gross);
    }
    var d = [{ x:x, y:y, type:'bar' }];
    var l = { xaxis: {automargin: true}, yaxis: {title: 'Millions ($)'}};
    Plotly.newPlot("bar", d, l);
});