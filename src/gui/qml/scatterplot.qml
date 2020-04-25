import QtCharts 2.0
import QtQuick 2.0

ChartView {
  id: chart
  antialiasing: true
  backgroundColor: "#404040"
  legend.visible: false

  ValueAxis {
      id: axisX
      min: pychart.xmin
      max: pychart.xmax
      labelsVisible: true
      tickCount: 1
      minorTickCount: 1
      labelsColor: "red"
  }

  ValueAxis {
      id: axisY
      min: pychart.zmin
      max: pychart.zmax
      tickCount: 1
      labelsColor: "red"
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
    axisY.min = pychart.zmin

    var ratio_x = (pychart.xmax - pychart.xmin) / chart.plotArea.width
    var ratio_z = (pychart.zmax-pychart.zmin) / chart.plotArea.height

    if (ratio_x > ratio_z) {
      axisX.max = pychart.xmax
      axisY.max = pychart.zmin + ratio_x * chart.plotArea.height
    } else {
      axisX.max = pychart.xmin + ratio_z * chart.plotArea.width
      axisY.max = pychart.zmax
    }

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
