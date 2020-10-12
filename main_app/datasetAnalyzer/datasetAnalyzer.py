import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, Dropdown, CustomJS, MultiChoice
from bokeh.layouts import column, row

# from pandas_profiling import ProfileReport

import io
import re
import json

from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry, createDropDownChoices
from main_app.main.referenceData import getDatasetSqlName


class dataframeHtmlTableComponents:
    def __init__(self, df):
        if df.index.to_list():
            self.index = df.index.to_list()
        else:
            self.index = list(range(0, len(df.columns.values)))
        self.column_names = df.columns.values
        self.row_data = list(df.values.tolist())


def analyzeDataset(dataset_id, datasetDetails):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetSqlName = log.datasetSqlName
    # print("datasetSqlName =", datasetSqlName)
    # sqlStatement = f"SELECT * FROM {datasetSqlName}"
    # print("sqlStatement =", sqlStatement)
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # print(df.shape)
    # print(df.columns)
    datasetDetails["columnChoices"] = createDropDownChoices(df.columns)
    datasetDetails["describeDataset"] = df.describe(include="all")

    datasetDetails["datasetInfo"] = getDatasetInfo(df)
    datasetDetails["datasetInfo_2"] = datasetDetails["datasetInfo"]

    datasetDetails["datasetPreview"] = dataframeHtmlTableComponents(
        pd.concat([df.head(10).round(3), df.tail(10).round(3)])
    )
    # print("saving report")
    # profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)
    # print(profile)
    # profile.to_file("/tmp/dataset_report.json")
    # profile.to_file("your_report.html")
    return datasetDetails


def getDatasetInfo(df):
    # Create a StringIO object to capture output of df.info since df.info returns output to stdout by default
    buf = io.StringIO()
    df.info(buf=buf)
    datasetInfo = buf.getvalue()
    # print("datasetInfo = ", datasetInfo)
    # Create a list of the dataset ino
    datasetInfo = datasetInfo.splitlines()
    # Define the column headings for display in html table
    datasetInfo[3] = ["#", "Column", "Non-Null Count", "Data Type"]
    # Convert each data row into a list of data elements beginning with row 5 through the
    #  third from last row
    count = 5
    for line in datasetInfo[5:-2]:
        # print("line = ", line)
        # data = line.split()
        # Use regex to split line info into list.  See tester at regexr.com/5d9cq
        # findall returns a list containing a tuple as noted here https://docs.python.org/2/library/re.html
        data = re.findall(
            r"([\S]+)[\s]+([\S]+[\s\S]*)[\s]+([\d]+)[\s]+[\S]+[\s]+([\S]*[\s]*)", line
        )
        # Verify that the row has data and convert the tuple into a list
        if len(data) > 0:
            data = list(data[0])
        # Replace the string with the list of elements
        datasetInfo[count] = data
        count = count + 1
    # print("datasetInfo = ", datasetInfo)
    return datasetInfo


def plotColumn(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # prepare some data
    x = df["index"]
    y = df[columnName]

    # create a new plot with a title and axis labels
    p = figure(
        title="Dataset Name: " + datasetName,
        x_axis_label="Index",
        y_axis_label=columnName,
        sizing_mode="fixed",
        plot_width=1100,
        plot_height=400,
    )

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label=columnName, line_width=2)

    # show the results
    return p


def categoricalPlot(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    df = pd.read_sql_table(datasetSqlName, db.engine)
    vc = df[columnName].value_counts()
    categories = vc.index.to_list()

    # Categorical values can also be used as coordinates
    values = vc.to_list()
    print("categories and values:", categories, values)

    source = ColumnDataSource(data=dict(categories=categories, values=values))
    print("source dir=", dir(source))
    print("source.data=", source.data)
    print("source.data=", source.data["categories"])

    # Set the x_range to the list of categories above
    p = figure(
        x_range=source.data["categories"],
        plot_height=250,
        plot_width=1100,
        title=datasetName + ": " + columnName + " Counts",
    )

    p.vbar(
        x="categories",
        top="values",
        width=0.9,
        source=source,
        legend_field="categories",
        line_color="white",
        fill_color=factor_cmap(
            "categories", palette=Spectral6, factors=source.data["categories"]
        ),
    )

    # Set some properties to make the plot look better
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    # p.y_range.end = 9
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    # Create menu and options with name of data columns with numerical data
    columns = df.columns.to_list()
    menu = []
    columnNameList = []
    category_counts = []
    for columnName in columns:
        if not (is_numeric_dtype(df[columnName])):
            # Menu is a list of tuples of name/value pairs for dropdown widget
            menu.append((columnName, columnName))
            # Option is a list of column names for multi-select widget
            columnNameList.append(columnName)
            # Get value counts
            vc = df[columnName].value_counts()
            category_counts.append([vc.index.to_list(), vc.to_list()])
    # print("category_counts =", category_counts)

    # Create dropdown widget
    dropdown = Dropdown(
        label="Select Column", button_type="primary", menu=menu, width_policy="min"
    )
    category_counts_source = ColumnDataSource(
        data=dict(x=columnNameList, y=category_counts)
    )
    # Define JS callback to change column to plot
    print("p.x_range=", p.x_range.properties_with_values())
    print(dir(p.x_range))
    callback_dropdown = CustomJS(
        args=dict(
            source=source, category_counts=category_counts_source, x_range=p.x_range
        ),
        code="""
        console.log('dropdown=' + this.item);
        // Initialize x and y arrays
        var data = source.data;
        var categories = data['categories'];
        // console.log(' x=' + x);
        var values = data['values'];
        // console.log('y=' + y);
        console.log('categories=' + categories + ' values=' + values);

        // Get dataframe
        var category_counts_data = category_counts.data;
        console.log('category_counts_data=' + category_counts_data);
        console.dir(category_counts_data);
        console.log('category_counts_data.x=' + category_counts_data.x);
        console.dir(category_counts_data.x);
        console.dir(category_counts_data.y);
        var index = category_counts_data.x.indexOf(this.item);
        console.log('index=' + index);
        console.log(category_counts_data.y[index]);
        // categories = category_counts_data.y[index][0];
        // values = category_counts_data.y[index][1];

        source.data['categories'] = category_counts_data.y[index][0];
        source.data['values'] = category_counts_data.y[index][1];
        x_range.factors = source.data['categories'];

        console.log('categories=' + categories + ' values=' + values);
        // Update plot with new x,y source data
        source.change.emit();
        """,
    )

    # Define javascript events to trigger callbacks
    dropdown.js_on_event(
        "menu_item_click",
        callback_dropdown,
    )
    # return row(dropdown, p)
    return p


def multilinePlot(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # prepare some data
    x = df["index"]
    # create a new plot with a title and axis labels
    p = figure(
        title="Dataset Name: " + datasetName,
        x_axis_label="Index",
        y_axis_label="y",
        sizing_mode="fixed",
        plot_width=1100,
        plot_height=400,
    )

    # Initialize source to x=[x] and y=[x]
    # Note:
    # Multi-line plots take an array as x's and y's
    # The x and y arrays must be the same length
    initialColumnName = columnName
    y = df[columnName]
    source = ColumnDataSource(data=dict(x=[x], y=[y]))
    df_source = ColumnDataSource(data=dict(df))
    p.multi_line("x", "y", source=source)

    # Create menu and options with name of data columns with numerical data
    columns = df.columns.to_list()
    menu = []
    options = []
    for columnName in columns:
        # if df[columnName].dtype == np.float64 or df[columnName].dtype == np.int64:
        if is_numeric_dtype(df[columnName]):
            # Menu is a list of tuples of name/value pairs for dropdown widget
            menu.append((columnName, columnName))
            # Option is a list of column names for multi-select widget
            options.append(columnName)

    # Create dropdown widget
    dropdown = Dropdown(
        label="Select Column", button_type="primary", menu=menu, width_policy="min"
    )
    # Create multi-select widget
    multi_choice = MultiChoice(
        value=[initialColumnName], options=options, title="Select Columns"
    )

    # Define JS callback to change column to plot
    callback_dropdown = CustomJS(
        args=dict(source=source, df_source=df_source),
        code="""
        // Initialize x and y arrays
        var data = source.data;
        var x = data['x'];
        // console.log(' x=' + x);
        var y = data['y'];
        // console.log('y=' + y);

        // Get dataframe
        var df_data = df_source.data;

        // Set y array to selected value
        y[0] = df_data[this.item];

        // Update plot with new x,y source data
        source.change.emit();
        """,
    )
    callback_multi_select = CustomJS(
        args=dict(source=source, df_source=df_source),
        code="""
        // Initialize x and y arrays
        var data = source.data;
        var x = data['x'];
        var y = data['y'];
        x.length = 0;
        y.length = 0;
        // console.log(' x=' + x);
        // console.log('x.length=' + x.length);
        // console.log('y=' + y);
        // console.log('y.length=' + y.length);

        // Get dataframe
        var df_data = df_source.data;

        // Get value of multi-select widget
        // console.log('multi_select: ' + this.value, this.value.toString());
        var array = this.value;
        

        // Iterate through multi-select values and update x,y arrays with selected values
        var array_iterator = array.values();
        let next_value = array_iterator.next();
        while (!next_value.done) {
        // console.log(next_value.value);
        x.push(df_data['index']);
        y.push(df_data[next_value.value]);
        next_value = array_iterator.next();
        }
        // console.log('y=' + y);
        // console.log('y.length=' + y.length);
        // console.log('x.length=' + x.length);

        // Update plot with new x,y source data
        source.change.emit();
        """,
    )

    # Define javascript events to trigger callbacks
    dropdown.js_on_event(
        "menu_item_click",
        callback_dropdown,
    )

    multi_choice.js_on_change(
        "value",
        callback_multi_select,
    )

    layout = column(multi_choice, p)
    return layout