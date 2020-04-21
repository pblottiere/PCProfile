import QtCharts 2.0
import QtQuick 2.0

ChartView {
  antialiasing: true
  title: "PointCloud Profile"
  titleColor: "white"
  backgroundColor: "#404040"
  legend.labelColor: "white"

  ValueAxis {
      id: axisX
      min: pychart.xmin
      max: pychart.xmax
      tickCount: 1
  }

  ValueAxis {
      id: axisY
      min: pychart.zmin
      max: pychart.zmax
      tickCount: 1
  }

  ScatterSeries {
    id: scatter2
    useOpenGL: true
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  Component.onCompleted: {
    addPoints()
  }

  function addPoints() {
    scatter2.clear()
    axisX.min = pychart.xmin
    axisX.max = pychart.xmax

    axisY.min = pychart.zmin
    axisY.max = pychart.zmax

    var points_x = pychart.points_x
    var points_y = pychart.points_y
    for (var index in points_x) {
      scatter2.append(points_x[index], points_y[index])
    }
  }

  Connections {
    target: pychart
    onUpdated: {
      addPoints()
    }
  }
}
