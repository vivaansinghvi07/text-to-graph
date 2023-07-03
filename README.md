# Text To Graph
Creates Desmos graphs from text!

## Usage
To use, install the requirements using `$ pip install -r requirements.txt`. Then, call with the following arguments: 


```
$ python3 main.py [-h] [--font_family FONT_FAMILY] [--polynomial] side_length text point_count
```
```
positional arguments:
  side_length           The side length of the square which text is rendered in
  text                  The text that will be rendered by the program
  point_count           The number of points that will be rendered

options:
  -h, --help            show this help message and exit
  --font_family FONT_FAMILY
                        The path to the font file that will be used to render your text
  --polynomial          Determines if polynomial behaviour is used
```

Note: The default font family is Courier, which will be used unless you provide your own font.

## Results 
The program generates a list of points in a file called `points.txt`. Copy the contents of the file and paste it into a blank desmos graph. Set the slider of the variable `t` to be between `1` and the length of your text. Then, let your animation play! A sample set of points is provided in `points.txt` currently.

## Limitations
Using polynomial interpolation to display the points on a smooth, curved path can be slow in point generation when lengths exceed 10. Using the linear approach (without the `--polynomial` argument) will result in more efficient generation, but less efficient desmos rendering. 
