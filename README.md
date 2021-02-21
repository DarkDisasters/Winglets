# Winglets
Implementation of [Winglets: Visualizing Association with Uncertainty in Multi-class Scatterplots.](https://vcc.tech/research/2019/Winglets)  
  
### [Project page](https://vcc.tech/research/2019/Winglets) | [paper](https://vcc.tech/file/upload_file//image/research/att201908230922/Winglets.pdf) | [video](https://vcc.tech/file/upload_file//image/research/att202102101341/Winglets_demo.mp4)

![overview](https://github.com/DarkDisasters/Winglets/tree/main/doc/overview.png)

We introduce Winglets, an enhancement to the classic scatterplot to better perceptually pronounce multiple classes by improving the perception of association and uncertainty of points to their related cluster. Designed as a pair of dual-sided strokes belonging to a data point, Winglets leverage the Gestalt principle of Closure to shape the perception of the form of the clusters, rather than use an explicit divisive encoding. Through a subtle design of two dominant attributes, length and orientation, Winglets enable viewers to perform a mental completion of the clusters. 

## Dependencies
- python3: We used Python3.6
- Python Third-Party Libraries: tkinter, pandas, scipy, numpy, shapely, scikit-image, seaborn

## Usage
- Run `pip install Winglets` to install Winglets. Note that you should install other python third-party libraries according to the tip.
- Use `import Winglets` to import Winglets libraires.
- You can run python `testAPI.py` to test related API. We prepare related test file(./testAPI.py) and data(./testFile.json) .

## API
#### Winglets
```
drawWinglets(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'], onlyWinglets=True)
```
###### Parameters
- data: the data form can be array or object
    - object: the key of the object is class of each group of data, e.g.,
        ```
        {
            "1" : [ 
                {
                    "x" : 458.545253723722,
                    "y" : 517.796113219558
                }, 
                ...
            ],
            "4" : [ 
                {
                    "x" : 487.798180288922,
                    "y" : 346.750755518256
                }, 
                {
                    "x" : 458.787734845522,
                    "y" : 316.371739750119
                }, 
                ...
            ]
        }
        ```
    - array：The array data does not identify which class it belongs to, so internally the program will set the data classes starting at 1, e.g.,
        ```
        [
            [ 
                [458.545253723722, 517.796113219558], 
                [487.798180288922, 346.750755518256]
                ...
            ],
            [ 
                [487.798180288922, 346.750755518256],
                [458.787734845522, 316.371739750119],
                ...
            ]
        ]
        ```
- colorArray：set the color for each group, e.g.,
    ```
    colorArray = ['red', 'blue', 'pink', 'orange']
    data = {
            "1" : [ 
                {
                    "x" : 458.545253723722,
                    "y" : 517.796113219558
                }, 
            ],
            "4" : [ 
                {
                    "x" : 487.798180288922,
                    "y" : 346.750755518256
                }, 
                
            ]
        }
    
    ```
    Note: An error will be reported if the length of the **colorArray** is less than the number of classes in the data
- onlyWinglets：the default is True. Buttons corresponding to proximity and commonFate will not appear in the program; if False, buttons corresponding to all operations will appear
#### CommonFate
```
drawCommonFate(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'])
```
###### Parameters
- data：description same as API Winglets.
- colorArray：description same as API Winglets.
#### Proximity
```
drawProximity(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'])
```
###### Parameters
- data：description same as API Winglets.
- colorArray：description same as API Winglets.

#### circle
```
drawCirlce(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'], onlyCicle=True)
```
###### Parameters
- data：description same as API Winglets.
- colorArray：description same as API Winglets.
- onlyCircle: the default is True，there are no buttons for other actions. If False, there are buttons for all actions.

## Citation
Please cite the paper in your publications if it helps your research:
```
@article{Winglets19,
title = {Winglets: Visualizing Association with Uncertainty in Multi-class Scatterplots},
author = {Min Lu, Shuaiqi Wang, Joel Lanir, Noa Fish, Yang Yue, Daniel Cohen-Or, Hui Huang},
journal = {IEEE Transactions on Visualization and Computer Graphics (Proceedings of InfoVis 2019)},
volume = {26},
number = {1}, 

pages = {770--779}, 

year = {2020},
} 
```


