Alpha Shapes
============

Credits
-------
The main python script is based on the Stack Overflow question [here](http://stackoverflow.com/questions/6833243/how-can-i-find-the-alpha-shape-concave-hull-of-a-2d-point-cloud)

This [post](http://bocoup.com/weblog/compiling-clarksons-hull-in-os-x/) helped in solving an installation issue.

This [post](http://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates) was used to calculate the area of the hull.

Requirements
-------------
- C compiler

Installation
-------------
1. Download source code from [here](http://www.netlib.org/voronoi/hull.zip)
2. Replace the stormacs.h file with [this one](http://bocoup.com/weblog/wp-content/uploads/2010/03/stormacs.h)
3. Run `make`


Example
-----
        
        >>> import hull
        >>> import matplotlib.pyplot as plt
        >>> import os
        >>> with open(os.path.join('examples', 'cshape-full')) as f:
        ...     points = hull.read_points(f)
        >>> fig, ax = plt.subplots()
        >>> hull.plot_hull(ax, points, hull.get_alpha_shape(points))
        >>> plt.show()


![Picture Output](outputs/cshape-full.png)
