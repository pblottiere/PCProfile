import QtCharts 2.0
import QtQuick 2.0

ChartView {
  id: chart
  antialiasing: true
  backgroundColor: pychart.background_color
  legend.visible: false

  ValueAxis {
      id: axisX
      min: pychart.xmin
      max: pychart.xmax
      labelsVisible: true
      tickCount: 1
      minorTickCount: 1
      labelsColor: pychart.labels_color
      color: pychart.axis_color
      gridLineColor: pychart.axis_color
      minorGridLineColor: pychart.axis_color
      shadesColor: pychart.axis_color
      shadesBorderColor: pychart.axis_color
  }

  ValueAxis {
      id: axisY
      min: pychart.zmin
      max: pychart.zmax
      tickCount: 1
      labelsColor: pychart.labels_color
      color: pychart.axis_color
      gridLineColor: pychart.axis_color
      minorGridLineColor: pychart.axis_color
      shadesColor: pychart.axis_color
      shadesBorderColor: pychart.axis_color
  }

  ScatterSeries {
    id: serie0
    color: pychart.ramp_color(0)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie1
    color: pychart.ramp_color(1)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie2
    color: pychart.ramp_color(2)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie3
    color: pychart.ramp_color(3)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie4
    color: pychart.ramp_color(4)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie5
    color: pychart.ramp_color(5)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie6
    color: pychart.ramp_color(6)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie7
    color: pychart.ramp_color(7)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie8
    color: pychart.ramp_color(8)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie9
    color: pychart.ramp_color(9)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie10
    color: pychart.ramp_color(10)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  ScatterSeries {
    id: serie11
    color: pychart.ramp_color(11)
    useOpenGL: pychart.opengl
    axisX: axisX
    axisY: axisY
    markerSize: pychart.marker_size
    borderWidth: 0
  }

  function addPoints() {
    serie0.clear()
    serie1.clear()
    serie2.clear()
    serie3.clear()
    serie4.clear()
    serie5.clear()
    serie6.clear()
    serie7.clear()
    serie8.clear()
    serie9.clear()
    serie10.clear()
    serie11.clear()

    axisX.min = pychart.xmin
    axisY.min = pychart.zmin

    var step = (pychart.zmax - pychart.zmin) / 12

    if (pychart.is_scaled) {
      var ratio_x = (pychart.xmax - pychart.xmin) / chart.plotArea.width
      var ratio_z = (pychart.zmax-pychart.zmin) / chart.plotArea.height

      if (ratio_x > ratio_z) {
        axisX.max = pychart.xmax
        axisY.max = pychart.zmin + ratio_x * chart.plotArea.height
      } else {
        axisX.max = pychart.xmin + ratio_z * chart.plotArea.width
        axisY.max = pychart.zmax
      }
    } else {
        axisX.max = pychart.xmax
        axisY.max = pychart.zmax
    }

    var points_x = pychart.points_x
    var points_y = pychart.points_y

    for (var index in points_x) {
      var z = points_y[index];

      if (z <= pychart.zmin + step) {
        serie0.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 2*step ) {
        serie1.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 3*step ) {
        serie2.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 4*step ) {
        serie3.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 5*step ) {
        serie4.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 6*step ) {
        serie5.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 7*step ) {
        serie6.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 8*step ) {
        serie7.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 9*step ) {
        serie8.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 10*step ) {
        serie9.append(points_x[index], z)
      } else if ( z <= pychart.zmin + 11*step ) {
        serie10.append(points_x[index], z)
      } else {
        serie11.append(points_x[index], z)
      }
    }
  }

  function updateColors() {
    serie0.color = pychart.ramp_color(0)
    serie1.color = pychart.ramp_color(1)
    serie2.color = pychart.ramp_color(2)
    serie3.color = pychart.ramp_color(3)
    serie4.color = pychart.ramp_color(4)
    serie5.color = pychart.ramp_color(5)
    serie6.color = pychart.ramp_color(6)
    serie7.color = pychart.ramp_color(7)
    serie8.color = pychart.ramp_color(8)
    serie9.color = pychart.ramp_color(9)
    serie10.color = pychart.ramp_color(10)
    serie11.color = pychart.ramp_color(11)
  }

  Connections {
    target: pychart
    onUpdated: {
      addPoints()
    }
  }

  Connections {
    target: pychart
    onColor: {
      updateColors()
    }
  }
}
