# slider2scale
A tkinter scale with two sliders.

slider2scale.py
It contains the Slider2Scale object.
It is a scale with two sliders, made in tkinter.
I used it for plotting data because I wanted to dynamically set both end of the independent variable's range.
It supports only integer values for range variables, but these values can be used as indices to select the range to plot form a list or dataframe.

dataplotter.py
It contains a demo program for Slider2Scale.
You can load the example dataset (temp_rh_data.txt). Select the independent variable for x (it should be DateTime) and the dependent variable for y (Temperature or Relative Humidity).
Then plot the selected quantity and use the slider to select the desired range.

temp_rh_data.txt
It contains the example dataset.
It's a csv file with three columns (DateTime, Temperature, Relative Humidity) and ";" as delimiter.
