function updateBarChart(movie_id) {
    console.log(movie_id);
    var dataset = d3.json("/characters/"+`${movie_id}`).then(function(data) {
        return data;
    });
    var characters = dataset.then(function(value) {
        return Promise.all(value.map(function(results) {
            return {"name": results.name, "alias": results.alias, "time": results.screen_time};
        }))
    });
    characters.then(function(data) {
        console.log(data);
    });
}