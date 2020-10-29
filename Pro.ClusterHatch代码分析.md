- 在全局也就是index.html的第203行初始化 g_spWidget = new ScatterPlotWidget('spcanvas')
- ScatterPlotWidge函数再spcanvas.js里面定义
- strokenenhancer.js  
第19行调用clusterKDE2请求后拿到返回值，response['clusters']中包含有kde的信息，response['mm']中是设定的计算核密度的范围
- geooperate.js里定义的应该是获取矢量，centroid等

#### 下面是画二维相关的
- strokeenhancer.js里面调用addStrokes将返回值作为参数
- addStrokes在spcanvas.js中2353行
- 2372行调用computeDisMatrix
- 2373行调用computeSilhouette
- computeDisMatrix从第一个类开始，与随后的每一个类进行了求距离，使用的是getDis，m_mapDisMatrixKNNDis[dot1.index] = mapDot2Dis20获得knn的距离数组，但是不是很懂怎么求的

#### 下面的是画三维相关的
- serversender.js 里关键的是定义了计算kde的接口，用successKDE来接返回值
- successKDE在src_3d/datacenter_3d.js里面
- datacenter_3d.js中会调用liftZ2中的transfeDots(351行)对数据进行转换为canvasDot，求取当前点对应的行列来获取当前点位置的density，其中会调用dot2SpaceDot
- dot2SpaceDot返回值是return [(pos[0]/originScale - 0.5) * this.m_scale, (0.5 - pos[1]/originScale) * this.m_scale, z], 感觉应该是想对点进行缩放使得位置在设定的横纵范围内
- 在transferDots中将normalizeDot[2]调用liftZ进行处理，也就是上面的z，按照定义的zMin和zMax把density转换到其范围，对每个点进行处理后将其push到liNormalizeDot中