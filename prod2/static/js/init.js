var dataset = d3.json("/movies").then(function(data) {
    return data;
});
var movies = dataset.then(function(value) {
    return Promise.all(value.map(function(results) {
        var img = "/static/images/movie_" + results.movie_id + ".jpg";
        return {"id": results.movie_id, "name": results.title, "date": results.release_date, "img": img};
    }))
});
movies.then(function(data) {
    //console.log(data);
    TimeKnots.draw("#timeline1", data, { dateFormat: "%B %Y", color: "#696", width: 1000, showLabels: true, labelFormat: "%Y" });
});