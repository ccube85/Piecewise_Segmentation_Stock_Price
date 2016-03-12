# Piecewise-Segmentation

In this python code I developed the three main approaches for approximating a signal given as input as a set
of segments.
The three algorithms implemented are :
- Sliding windows
- Top down
- Bottom up

All these algorithms are implemented and compared

Both interpolation and regression are developed, as shows the pictures here below:

In order to run the script:
- if you want to run the piecewise segmentation interpolation, run main_interpolation.py
- if you want to run the piecewise segmentation regression, run main_regression.py

Input data comes from two sources:
_ Yahoo API: implemented in method 'draw_window_API'
- Local Database (not included in the package)  : implemented in method 'draw_window'
By default when class method 'draw_window_API'
