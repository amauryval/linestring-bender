# linestring-bender


Because it's fun to bend a LineString :)

Based on this stackoverflow topic: https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy


![](https://media.giphy.com/media/2modwsnpzX93G/giphy.gif)

## Install the environment
```
conda env create -f environment.yml
```

## Here a short snippet 

```python
from shapely.wkt import loads

from core.line_bender import LineStringBender

input_line = loads("LINESTRING(0 0, 25 25)")
curve_process = LineStringBender(input_line, 0.5, 2, 'right')

curve = curve_process.curve_geom()
print(curve.wkt)
```

## And a bokeh app to bend some LineStrings

```
cd linestring-bender
bokeh serve main.py --show
```

![example](img/example.png)


