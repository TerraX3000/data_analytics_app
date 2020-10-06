async function createPlot(plotEndpoint, tag_id) {
    var savedDataAnalyzerSettings_JSON = sessionStorage.getItem("SavedDataAnalyzerSettings");
    if (savedDataAnalyzerSettings_JSON) {
        if (savedDataAnalyzerSettings_JSON != "") {
            // Convert the saved settings into a JSON
            var savedDataAnalyzerSettings = JSON.parse(savedDataAnalyzerSettings_JSON);
            if (savedDataAnalyzerSettings['datasetName']) {
                my_dataset_id = savedDataAnalyzerSettings['datasetName']['value'];
            } else {
                my_dataset_id = false
            }
            if (savedDataAnalyzerSettings['columnName']) {
                my_columnName = savedDataAnalyzerSettings['columnName']['value'];
            } else {
                my_columnName = false
            }
            console.log('dataset_id =' + my_dataset_id);
            if (my_dataset_id && my_columnName) {
                const response = await fetch(plotEndpoint + my_dataset_id + '&' + my_columnName);
                const item = await response.json();
                Bokeh.embed.embed_item(item, tag_id);
                // On form reset, clear the saved learning lab details and reload the form
                // console.log('Reset form pressed');
                sessionStorage.setItem("SavedDataAnalyzerSettings", "");
            }
        }
    }
};