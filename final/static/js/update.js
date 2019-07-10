var chartExists = false;

var width = 1000,
    height = 1000,  // this will change dynamically
    barHeight = 50;

var x = d3.scaleLinear()
    .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", height);

function minsec(s) {
    var min = Math.floor(s/60);
    var sec = s % 60;
    return min.toString()+":"+sec.toString().padStart(2, '0'); 
}

function updateTitle(movie_title) {
    d3.select("p").text(movie_title);
}

function updateBarChart(movie_id) {
    console.log(movie_id);
    var dataset = d3.json("/characters/"+movie_id).then(function(data) {
        return data;
    });
    var characters = dataset.then(function(value) {
        return Promise.all(value.map(function(results) {
            var name = results.name;
            if (results.alias!==null) name += " / " + results.alias;
            return {"name": name, "value": results.screen_time};
        }))
    });
    characters.then(function(data) {
        console.log(data);
        if (chartExists) {
            d3.selectAll("g").remove();
        }
        x.domain([0, d3.max(data, function(d) { return d.value; })]);
        chart.attr("height", barHeight * data.length);
        var bar = chart.selectAll("g")
            .data(data)
            .enter().append("g")
            .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });
        bar.append("rect")
            .attr("width", function(d) { return x(d.value); })
            .attr("height", barHeight - 1);
        // time label
        bar.append("text")
            .attr("class", function(d) {
                if (x(d.value)<30) return "time-outer";
                return "time-inner";
            })
            .attr("x", function(d) {
                if (x(d.value)<30) return x(d.value)+25;
                return x(d.value)-3;
            })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return minsec(d.value); });
        // name label
        bar.append("text")
            .attr("class", function(d) {
                if (x(d.value)<30) return "name-outer";
                if ((x(d.value)-30)<(7*d.name.length)) return "name-outer";
                return "name-inner";
            })
            .attr("x", function(d) {
                if (x(d.value)<30) return x(d.value)+30; 
                if ((x(d.value)-30)<(7*d.name.length)) return x(d.value)+3;
                return 3;
            })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d.name; });
        chartExists = true;
    });
}