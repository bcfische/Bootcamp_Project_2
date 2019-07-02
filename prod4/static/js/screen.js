d3.json("/characters/sort_by_time").then(function(data) {
    var x = [], y = [];
    for (var i=0; i<10; i++) {
        x.push(data[i][0]);
        y.push(data[i][1]/3600);
    }
    var d = [{ x:x, y:y, type:'bar' }];
    var l = { xaxis: {automargin: true}, yaxis: {title: 'Hours'}};
    Plotly.newPlot("bar", d, l);
});