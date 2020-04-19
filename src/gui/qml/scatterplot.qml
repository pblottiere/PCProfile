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
      min: pyscatter.xmin
      max: pyscatter.xmax
      tickCount: 1
  }

  ValueAxis {
      id: axisY
      min: pyscatter.zmin
      max: pyscatter.zmax
      tickCount: 1
  }

  ScatterSeries {
    id: scatter2
    useOpenGL: true
    axisX: axisX
    axisY: axisY
    markerSize: 4.0
    borderWidth: 0
  }

  Component.onCompleted: {
    addPoints()
  }

  function addPoints() {
    scatter2.clear()
    axisX.min = pyscatter.xmin
    axisX.max = pyscatter.xmax

    axisY.min = pyscatter.zmin
    axisY.max = pyscatter.zmax

    var points_x = pyscatter.points_x
    var points_y = pyscatter.points_y
    for (var index in points_x) {
      scatter2.append(points_x[index], points_y[index])
    }
  }

  Connections {
    target: pyscatter
    onUpdated: {
      addPoints()
    }
  }
}
