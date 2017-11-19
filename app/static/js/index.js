var index =
webpackJsonp_name_([0],[
/* 0 */,
/* 1 */,
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(3);


/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


$.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?', function (data) {
  var detailChart;

  $(document).ready(function () {

    /* Reddit lazy load hack */
    var oScript = document.createElement("script");
    document.write = function (text) {
      document.getElementById("reddit").innerHTML += text;
    };
    oScript.src = "https://www.reddit.com/r/bitcoin.embed?limit=9";
    document.body.appendChild(oScript);

    setTimeout(function () {
      document.title = "Bitcoin (BTC)  $5358.00 (-6.87%) | CoinMarketCap";
    }, 10000);

    // create the detail chart
    function createDetail(masterChart) {

      // prepare the detail chart
      var detailData = [],
          detailStart = data[0][0];

      $.each(masterChart.series[0].data, function () {
        if (this.x >= detailStart) {
          detailData.push(this.y);
        }
      });

      // create a detail chart referenced by a global variable
      detailChart = Highcharts.chart('detail-container', {
        chart: {
          marginBottom: 120,
          reflow: false,
          marginLeft: 50,
          marginRight: 20,
          style: {
            position: 'absolute'
          }
        },
        credits: {
          enabled: false
        },
        title: {
          text: 'Historical USD to EUR Exchange Rate'
        },
        subtitle: {
          text: 'Select an area by dragging across the lower chart'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: null
          },
          maxZoom: 0.1
        },
        tooltip: {
          formatter: function formatter() {
            var point = this.points[0];
            return '<b>' + point.series.name + '</b><br/>' + Highcharts.dateFormat('%A %B %e %Y', this.x) + ':<br/>' + '1 USD = ' + Highcharts.numberFormat(point.y, 2) + ' EUR';
          },
          shared: true
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          series: {
            marker: {
              enabled: false,
              states: {
                hover: {
                  enabled: true,
                  radius: 3
                }
              }
            }
          }
        },
        series: [{
          name: 'USD to EUR',
          pointStart: detailStart,
          pointInterval: 24 * 3600 * 1000,
          data: detailData
        }],

        exporting: {
          enabled: false
        }

      }); // return chart
    }

    // create the master chart
    function createMaster() {
      Highcharts.chart('master-container', {
        chart: {
          reflow: false,
          borderWidth: 0,
          backgroundColor: null,
          marginLeft: 50,
          marginRight: 20,
          zoomType: 'x',
          events: {

            // listen to the selection event on the master chart to update the
            // extremes of the detail chart
            selection: function selection(event) {
              var extremesObject = event.xAxis[0],
                  min = extremesObject.min,
                  max = extremesObject.max,
                  detailData = [],
                  xAxis = this.xAxis[0];

              // reverse engineer the last part of the data
              $.each(this.series[0].data, function () {
                if (this.x > min && this.x < max) {
                  detailData.push([this.x, this.y]);
                }
              });

              // move the plot bands to reflect the new detail span
              xAxis.removePlotBand('mask-before');
              xAxis.addPlotBand({
                id: 'mask-before',
                from: data[0][0],
                to: min,
                color: 'rgba(0, 0, 0, 0.2)'
              });

              xAxis.removePlotBand('mask-after');
              xAxis.addPlotBand({
                id: 'mask-after',
                from: max,
                to: data[data.length - 1][0],
                color: 'rgba(0, 0, 0, 0.2)'
              });

              detailChart.series[0].setData(detailData);

              return false;
            }
          }
        },
        title: {
          text: null
        },
        xAxis: {
          type: 'datetime',
          showLastTickLabel: true,
          maxZoom: 14 * 24 * 3600000, // fourteen days
          plotBands: [{
            id: 'mask-before',
            from: data[0][0],
            to: data[data.length - 1][0],
            color: 'rgba(0, 0, 0, 0.2)'
          }],
          title: {
            text: null
          }
        },
        yAxis: {
          gridLineWidth: 0,
          labels: {
            enabled: false
          },
          title: {
            text: null
          },
          min: 0.6,
          showFirstLabel: false
        },
        tooltip: {
          formatter: function formatter() {
            return false;
          }
        },
        legend: {
          enabled: false
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          series: {
            fillColor: {
              linearGradient: [0, 0, 0, 70],
              stops: [[0, Highcharts.getOptions().colors[0]], [1, 'rgba(255,255,255,0)']]
            },
            lineWidth: 1,
            marker: {
              enabled: false
            },
            shadow: false,
            states: {
              hover: {
                lineWidth: 1
              }
            },
            enableMouseTracking: false
          }
        },

        series: [{
          type: 'area',
          name: 'USD to EUR',
          pointInterval: 24 * 3600 * 1000,
          pointStart: data[0][0],
          data: data
        }],

        exporting: {
          enabled: false
        }

      }, function (masterChart) {
        createDetail(masterChart);
      }); // return chart instance
    }

    // make the container smaller and add a second container for the master chart
    var $container = $('#chart').css('position', 'relative');

    $('<div id="detail-container">').appendTo($container);

    $('<div id="master-container">').css({
      position: 'absolute',
      top: 300,
      height: 100,
      width: '100%'
    }).appendTo($container);

    // create master and in its callback, create the detail chart
    createMaster();
  });
});

$('.datepicker').pickadate({
  selectMonths: true, // Creates a dropdown to control month
  selectYears: 15, // Creates a dropdown of 15 years to control year,
  today: 'Today',
  clear: 'Clear',
  close: 'Ok',
  closeOnSelect: false // Close upon selecting a date,
});

/***/ })
],[2]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vc3JjL2pzL2luZGV4LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIiQuZ2V0SlNPTignaHR0cHM6Ly93d3cuaGlnaGNoYXJ0cy5jb20vc2FtcGxlcy9kYXRhL2pzb25wLnBocD9maWxlbmFtZT11c2RldXIuanNvbiZjYWxsYmFjaz0/JywgZnVuY3Rpb24gKGRhdGEpIHtcbiAgdmFyIGRldGFpbENoYXJ0O1xuXG4gICQoZG9jdW1lbnQpLnJlYWR5KGZ1bmN0aW9uICgpIHtcblxuXG4gICAgLyogUmVkZGl0IGxhenkgbG9hZCBoYWNrICovXG4gICAgdmFyIG9TY3JpcHQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwic2NyaXB0XCIpO1xuICAgIGRvY3VtZW50LndyaXRlID0gZnVuY3Rpb24odGV4dCkge1xuICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJyZWRkaXRcIikuaW5uZXJIVE1MICs9IHRleHQ7XG4gICAgfTtcbiAgICBvU2NyaXB0LnNyYyA9IFwiaHR0cHM6Ly93d3cucmVkZGl0LmNvbS9yL2JpdGNvaW4uZW1iZWQ/bGltaXQ9OVwiO1xuICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQob1NjcmlwdCk7XG5cblxuICAgIHNldFRpbWVvdXQoZnVuY3Rpb24oKSB7XG4gICAgICBkb2N1bWVudC50aXRsZSA9IFwiQml0Y29pbiAoQlRDKSAgJDUzNTguMDAgKC02Ljg3JSkgfCBDb2luTWFya2V0Q2FwXCI7XG4gICAgfSwgMTAwMDApO1xuXG5cbiAgICAvLyBjcmVhdGUgdGhlIGRldGFpbCBjaGFydFxuICAgIGZ1bmN0aW9uIGNyZWF0ZURldGFpbChtYXN0ZXJDaGFydCkge1xuXG4gICAgICAvLyBwcmVwYXJlIHRoZSBkZXRhaWwgY2hhcnRcbiAgICAgIHZhciBkZXRhaWxEYXRhID0gW10sXG4gICAgICAgIGRldGFpbFN0YXJ0ID0gZGF0YVswXVswXTtcblxuICAgICAgJC5lYWNoKG1hc3RlckNoYXJ0LnNlcmllc1swXS5kYXRhLCBmdW5jdGlvbiAoKSB7XG4gICAgICAgIGlmICh0aGlzLnggPj0gZGV0YWlsU3RhcnQpIHtcbiAgICAgICAgICBkZXRhaWxEYXRhLnB1c2godGhpcy55KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIC8vIGNyZWF0ZSBhIGRldGFpbCBjaGFydCByZWZlcmVuY2VkIGJ5IGEgZ2xvYmFsIHZhcmlhYmxlXG4gICAgICBkZXRhaWxDaGFydCA9IEhpZ2hjaGFydHMuY2hhcnQoJ2RldGFpbC1jb250YWluZXInLCB7XG4gICAgICAgIGNoYXJ0OiB7XG4gICAgICAgICAgbWFyZ2luQm90dG9tOiAxMjAsXG4gICAgICAgICAgcmVmbG93OiBmYWxzZSxcbiAgICAgICAgICBtYXJnaW5MZWZ0OiA1MCxcbiAgICAgICAgICBtYXJnaW5SaWdodDogMjAsXG4gICAgICAgICAgc3R5bGU6IHtcbiAgICAgICAgICAgIHBvc2l0aW9uOiAnYWJzb2x1dGUnXG4gICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBjcmVkaXRzOiB7XG4gICAgICAgICAgZW5hYmxlZDogZmFsc2VcbiAgICAgICAgfSxcbiAgICAgICAgdGl0bGU6IHtcbiAgICAgICAgICB0ZXh0OiAnSGlzdG9yaWNhbCBVU0QgdG8gRVVSIEV4Y2hhbmdlIFJhdGUnXG4gICAgICAgIH0sXG4gICAgICAgIHN1YnRpdGxlOiB7XG4gICAgICAgICAgdGV4dDogJ1NlbGVjdCBhbiBhcmVhIGJ5IGRyYWdnaW5nIGFjcm9zcyB0aGUgbG93ZXIgY2hhcnQnXG4gICAgICAgIH0sXG4gICAgICAgIHhBeGlzOiB7XG4gICAgICAgICAgdHlwZTogJ2RhdGV0aW1lJ1xuICAgICAgICB9LFxuICAgICAgICB5QXhpczoge1xuICAgICAgICAgIHRpdGxlOiB7XG4gICAgICAgICAgICB0ZXh0OiBudWxsXG4gICAgICAgICAgfSxcbiAgICAgICAgICBtYXhab29tOiAwLjFcbiAgICAgICAgfSxcbiAgICAgICAgdG9vbHRpcDoge1xuICAgICAgICAgIGZvcm1hdHRlcjogZnVuY3Rpb24gKCkge1xuICAgICAgICAgICAgdmFyIHBvaW50ID0gdGhpcy5wb2ludHNbMF07XG4gICAgICAgICAgICByZXR1cm4gJzxiPicgKyBwb2ludC5zZXJpZXMubmFtZSArICc8L2I+PGJyLz4nICsgSGlnaGNoYXJ0cy5kYXRlRm9ybWF0KCclQSAlQiAlZSAlWScsIHRoaXMueCkgKyAnOjxici8+JyArXG4gICAgICAgICAgICAgICcxIFVTRCA9ICcgKyBIaWdoY2hhcnRzLm51bWJlckZvcm1hdChwb2ludC55LCAyKSArICcgRVVSJztcbiAgICAgICAgICB9LFxuICAgICAgICAgIHNoYXJlZDogdHJ1ZVxuICAgICAgICB9LFxuICAgICAgICBsZWdlbmQ6IHtcbiAgICAgICAgICBlbmFibGVkOiBmYWxzZVxuICAgICAgICB9LFxuICAgICAgICBwbG90T3B0aW9uczoge1xuICAgICAgICAgIHNlcmllczoge1xuICAgICAgICAgICAgbWFya2VyOiB7XG4gICAgICAgICAgICAgIGVuYWJsZWQ6IGZhbHNlLFxuICAgICAgICAgICAgICBzdGF0ZXM6IHtcbiAgICAgICAgICAgICAgICBob3Zlcjoge1xuICAgICAgICAgICAgICAgICAgZW5hYmxlZDogdHJ1ZSxcbiAgICAgICAgICAgICAgICAgIHJhZGl1czogM1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgc2VyaWVzOiBbe1xuICAgICAgICAgIG5hbWU6ICdVU0QgdG8gRVVSJyxcbiAgICAgICAgICBwb2ludFN0YXJ0OiBkZXRhaWxTdGFydCxcbiAgICAgICAgICBwb2ludEludGVydmFsOiAyNCAqIDM2MDAgKiAxMDAwLFxuICAgICAgICAgIGRhdGE6IGRldGFpbERhdGFcbiAgICAgICAgfV0sXG5cbiAgICAgICAgZXhwb3J0aW5nOiB7XG4gICAgICAgICAgZW5hYmxlZDogZmFsc2VcbiAgICAgICAgfVxuXG4gICAgICB9KTsgLy8gcmV0dXJuIGNoYXJ0XG4gICAgfVxuXG4gICAgLy8gY3JlYXRlIHRoZSBtYXN0ZXIgY2hhcnRcbiAgICBmdW5jdGlvbiBjcmVhdGVNYXN0ZXIoKSB7XG4gICAgICBIaWdoY2hhcnRzLmNoYXJ0KCdtYXN0ZXItY29udGFpbmVyJywge1xuICAgICAgICBjaGFydDoge1xuICAgICAgICAgIHJlZmxvdzogZmFsc2UsXG4gICAgICAgICAgYm9yZGVyV2lkdGg6IDAsXG4gICAgICAgICAgYmFja2dyb3VuZENvbG9yOiBudWxsLFxuICAgICAgICAgIG1hcmdpbkxlZnQ6IDUwLFxuICAgICAgICAgIG1hcmdpblJpZ2h0OiAyMCxcbiAgICAgICAgICB6b29tVHlwZTogJ3gnLFxuICAgICAgICAgIGV2ZW50czoge1xuXG4gICAgICAgICAgICAvLyBsaXN0ZW4gdG8gdGhlIHNlbGVjdGlvbiBldmVudCBvbiB0aGUgbWFzdGVyIGNoYXJ0IHRvIHVwZGF0ZSB0aGVcbiAgICAgICAgICAgIC8vIGV4dHJlbWVzIG9mIHRoZSBkZXRhaWwgY2hhcnRcbiAgICAgICAgICAgIHNlbGVjdGlvbjogZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgICAgICAgICAgIHZhciBleHRyZW1lc09iamVjdCA9IGV2ZW50LnhBeGlzWzBdLFxuICAgICAgICAgICAgICAgIG1pbiA9IGV4dHJlbWVzT2JqZWN0Lm1pbixcbiAgICAgICAgICAgICAgICBtYXggPSBleHRyZW1lc09iamVjdC5tYXgsXG4gICAgICAgICAgICAgICAgZGV0YWlsRGF0YSA9IFtdLFxuICAgICAgICAgICAgICAgIHhBeGlzID0gdGhpcy54QXhpc1swXTtcblxuICAgICAgICAgICAgICAvLyByZXZlcnNlIGVuZ2luZWVyIHRoZSBsYXN0IHBhcnQgb2YgdGhlIGRhdGFcbiAgICAgICAgICAgICAgJC5lYWNoKHRoaXMuc2VyaWVzWzBdLmRhdGEsIGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgICAgICBpZiAodGhpcy54ID4gbWluICYmIHRoaXMueCA8IG1heCkge1xuICAgICAgICAgICAgICAgICAgZGV0YWlsRGF0YS5wdXNoKFt0aGlzLngsIHRoaXMueV0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgICAgLy8gbW92ZSB0aGUgcGxvdCBiYW5kcyB0byByZWZsZWN0IHRoZSBuZXcgZGV0YWlsIHNwYW5cbiAgICAgICAgICAgICAgeEF4aXMucmVtb3ZlUGxvdEJhbmQoJ21hc2stYmVmb3JlJyk7XG4gICAgICAgICAgICAgIHhBeGlzLmFkZFBsb3RCYW5kKHtcbiAgICAgICAgICAgICAgICBpZDogJ21hc2stYmVmb3JlJyxcbiAgICAgICAgICAgICAgICBmcm9tOiBkYXRhWzBdWzBdLFxuICAgICAgICAgICAgICAgIHRvOiBtaW4sXG4gICAgICAgICAgICAgICAgY29sb3I6ICdyZ2JhKDAsIDAsIDAsIDAuMiknXG4gICAgICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgICAgIHhBeGlzLnJlbW92ZVBsb3RCYW5kKCdtYXNrLWFmdGVyJyk7XG4gICAgICAgICAgICAgIHhBeGlzLmFkZFBsb3RCYW5kKHtcbiAgICAgICAgICAgICAgICBpZDogJ21hc2stYWZ0ZXInLFxuICAgICAgICAgICAgICAgIGZyb206IG1heCxcbiAgICAgICAgICAgICAgICB0bzogZGF0YVtkYXRhLmxlbmd0aCAtIDFdWzBdLFxuICAgICAgICAgICAgICAgIGNvbG9yOiAncmdiYSgwLCAwLCAwLCAwLjIpJ1xuICAgICAgICAgICAgICB9KTtcblxuXG4gICAgICAgICAgICAgIGRldGFpbENoYXJ0LnNlcmllc1swXS5zZXREYXRhKGRldGFpbERhdGEpO1xuXG4gICAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHRpdGxlOiB7XG4gICAgICAgICAgdGV4dDogbnVsbFxuICAgICAgICB9LFxuICAgICAgICB4QXhpczoge1xuICAgICAgICAgIHR5cGU6ICdkYXRldGltZScsXG4gICAgICAgICAgc2hvd0xhc3RUaWNrTGFiZWw6IHRydWUsXG4gICAgICAgICAgbWF4Wm9vbTogMTQgKiAyNCAqIDM2MDAwMDAsIC8vIGZvdXJ0ZWVuIGRheXNcbiAgICAgICAgICBwbG90QmFuZHM6IFt7XG4gICAgICAgICAgICBpZDogJ21hc2stYmVmb3JlJyxcbiAgICAgICAgICAgIGZyb206IGRhdGFbMF1bMF0sXG4gICAgICAgICAgICB0bzogZGF0YVtkYXRhLmxlbmd0aCAtIDFdWzBdLFxuICAgICAgICAgICAgY29sb3I6ICdyZ2JhKDAsIDAsIDAsIDAuMiknXG4gICAgICAgICAgfV0sXG4gICAgICAgICAgdGl0bGU6IHtcbiAgICAgICAgICAgIHRleHQ6IG51bGxcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHlBeGlzOiB7XG4gICAgICAgICAgZ3JpZExpbmVXaWR0aDogMCxcbiAgICAgICAgICBsYWJlbHM6IHtcbiAgICAgICAgICAgIGVuYWJsZWQ6IGZhbHNlXG4gICAgICAgICAgfSxcbiAgICAgICAgICB0aXRsZToge1xuICAgICAgICAgICAgdGV4dDogbnVsbFxuICAgICAgICAgIH0sXG4gICAgICAgICAgbWluOiAwLjYsXG4gICAgICAgICAgc2hvd0ZpcnN0TGFiZWw6IGZhbHNlXG4gICAgICAgIH0sXG4gICAgICAgIHRvb2x0aXA6IHtcbiAgICAgICAgICBmb3JtYXR0ZXI6IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIGxlZ2VuZDoge1xuICAgICAgICAgIGVuYWJsZWQ6IGZhbHNlXG4gICAgICAgIH0sXG4gICAgICAgIGNyZWRpdHM6IHtcbiAgICAgICAgICBlbmFibGVkOiBmYWxzZVxuICAgICAgICB9LFxuICAgICAgICBwbG90T3B0aW9uczoge1xuICAgICAgICAgIHNlcmllczoge1xuICAgICAgICAgICAgZmlsbENvbG9yOiB7XG4gICAgICAgICAgICAgIGxpbmVhckdyYWRpZW50OiBbMCwgMCwgMCwgNzBdLFxuICAgICAgICAgICAgICBzdG9wczogW1xuICAgICAgICAgICAgICAgIFswLCBIaWdoY2hhcnRzLmdldE9wdGlvbnMoKS5jb2xvcnNbMF1dLFxuICAgICAgICAgICAgICAgIFsxLCAncmdiYSgyNTUsMjU1LDI1NSwwKSddXG4gICAgICAgICAgICAgIF1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBsaW5lV2lkdGg6IDEsXG4gICAgICAgICAgICBtYXJrZXI6IHtcbiAgICAgICAgICAgICAgZW5hYmxlZDogZmFsc2VcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBzaGFkb3c6IGZhbHNlLFxuICAgICAgICAgICAgc3RhdGVzOiB7XG4gICAgICAgICAgICAgIGhvdmVyOiB7XG4gICAgICAgICAgICAgICAgbGluZVdpZHRoOiAxXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBlbmFibGVNb3VzZVRyYWNraW5nOiBmYWxzZVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcblxuICAgICAgICBzZXJpZXM6IFt7XG4gICAgICAgICAgdHlwZTogJ2FyZWEnLFxuICAgICAgICAgIG5hbWU6ICdVU0QgdG8gRVVSJyxcbiAgICAgICAgICBwb2ludEludGVydmFsOiAyNCAqIDM2MDAgKiAxMDAwLFxuICAgICAgICAgIHBvaW50U3RhcnQ6IGRhdGFbMF1bMF0sXG4gICAgICAgICAgZGF0YTogZGF0YVxuICAgICAgICB9XSxcblxuICAgICAgICBleHBvcnRpbmc6IHtcbiAgICAgICAgICBlbmFibGVkOiBmYWxzZVxuICAgICAgICB9XG5cbiAgICAgIH0sIGZ1bmN0aW9uIChtYXN0ZXJDaGFydCkge1xuICAgICAgICBjcmVhdGVEZXRhaWwobWFzdGVyQ2hhcnQpO1xuICAgICAgfSk7IC8vIHJldHVybiBjaGFydCBpbnN0YW5jZVxuICAgIH1cblxuICAgIC8vIG1ha2UgdGhlIGNvbnRhaW5lciBzbWFsbGVyIGFuZCBhZGQgYSBzZWNvbmQgY29udGFpbmVyIGZvciB0aGUgbWFzdGVyIGNoYXJ0XG4gICAgdmFyICRjb250YWluZXIgPSAkKCcjY2hhcnQnKVxuICAgICAgLmNzcygncG9zaXRpb24nLCAncmVsYXRpdmUnKTtcblxuICAgICQoJzxkaXYgaWQ9XCJkZXRhaWwtY29udGFpbmVyXCI+JylcbiAgICAgIC5hcHBlbmRUbygkY29udGFpbmVyKTtcblxuICAgICQoJzxkaXYgaWQ9XCJtYXN0ZXItY29udGFpbmVyXCI+JylcbiAgICAgIC5jc3Moe1xuICAgICAgICBwb3NpdGlvbjogJ2Fic29sdXRlJyxcbiAgICAgICAgdG9wOiAzMDAsXG4gICAgICAgIGhlaWdodDogMTAwLFxuICAgICAgICB3aWR0aDogJzEwMCUnXG4gICAgICB9KVxuICAgICAgLmFwcGVuZFRvKCRjb250YWluZXIpO1xuXG4gICAgLy8gY3JlYXRlIG1hc3RlciBhbmQgaW4gaXRzIGNhbGxiYWNrLCBjcmVhdGUgdGhlIGRldGFpbCBjaGFydFxuICAgIGNyZWF0ZU1hc3RlcigpO1xuICB9KTtcbn0pO1xuXG4kKCcuZGF0ZXBpY2tlcicpLnBpY2thZGF0ZSh7XG4gIHNlbGVjdE1vbnRoczogdHJ1ZSwgLy8gQ3JlYXRlcyBhIGRyb3Bkb3duIHRvIGNvbnRyb2wgbW9udGhcbiAgc2VsZWN0WWVhcnM6IDE1LCAvLyBDcmVhdGVzIGEgZHJvcGRvd24gb2YgMTUgeWVhcnMgdG8gY29udHJvbCB5ZWFyLFxuICB0b2RheTogJ1RvZGF5JyxcbiAgY2xlYXI6ICdDbGVhcicsXG4gIGNsb3NlOiAnT2snLFxuICBjbG9zZU9uU2VsZWN0OiBmYWxzZSAvLyBDbG9zZSB1cG9uIHNlbGVjdGluZyBhIGRhdGUsXG59KTtcblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gc3JjL2pzL2luZGV4LmpzIl0sIm1hcHBpbmdzIjoiO0E7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUFBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFEQTtBQUxBO0FBU0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQUNBO0FBREE7QUFHQTtBQUpBO0FBTUE7QUFDQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBTkE7QUFRQTtBQUNBO0FBREE7QUFHQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBRkE7QUFEQTtBQUZBO0FBREE7QUFEQTtBQWFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFKQTtBQUNBO0FBTUE7QUFDQTtBQURBO0FBQ0E7QUE1REE7QUFnRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFDQTtBQUtBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFKQTtBQUNBO0FBTUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBSkE7QUFDQTtBQU9BO0FBQ0E7QUFDQTtBQUNBO0FBdkNBO0FBUEE7QUFpREE7QUFDQTtBQURBO0FBR0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBSkE7QUFNQTtBQUNBO0FBREE7QUFWQTtBQWNBO0FBQ0E7QUFDQTtBQUNBO0FBREE7QUFHQTtBQUNBO0FBREE7QUFHQTtBQUNBO0FBVEE7QUFXQTtBQUNBO0FBQ0E7QUFDQTtBQUhBO0FBS0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQURBO0FBR0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUZBO0FBT0E7QUFDQTtBQUNBO0FBREE7QUFHQTtBQUNBO0FBQ0E7QUFDQTtBQURBO0FBREE7QUFLQTtBQWxCQTtBQURBO0FBQ0E7QUFzQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBTEE7QUFDQTtBQU9BO0FBQ0E7QUFEQTtBQUNBO0FBekhBO0FBNkhBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBRUE7QUFDQTtBQUVBO0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFKQTtBQUNBO0FBT0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBTkE7OztBIiwic291cmNlUm9vdCI6IiJ9