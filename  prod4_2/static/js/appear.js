d3.json("/characters/sort_by_number").then(function(data) {
    var x = [], y = [];
    for (var i=0; i<10; i++) {
        x.push(data[i][0]);
        y.push(data[i][1]);
    }
    var d = [{ x:x, y:y, type:'bar' }];
    var l = { xaxis: {automargin: true}, yaxis: {title: 'Number of Movies'}};
    Plotly.newPlot("bar", d, l);
});