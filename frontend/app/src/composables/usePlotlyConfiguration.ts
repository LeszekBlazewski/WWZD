export function usePlotlyConfiguration() {
  const plotLayout: Partial<Plotly.Layout> = {
    paper_bgcolor: '#101014',
    plot_bgcolor: '#101014',
    autosize: true,
    dragmode: 'pan',
    font: {
      color: '#ffffff',
    },
    xaxis: {
      autorange: true,
      gridwidth: 2,
      zerolinewidth: 2,
      gridcolor: '#171717',
    },
    yaxis: {
      autorange: true,
      gridwidth: 2,
      zerolinewidth: 2,
      gridcolor: '#171717',
    },
  }

  const plotConfig: Partial<Plotly.Config> = {
    scrollZoom: true,
  }

  const plotDataDefaults = () => {
    return {
      type: 'scattergl',
      mode: 'markers',
      hoverinfo: 'x+y',
    }
  }

  const getPlotDataDefaults = (
    type: 'notToxic' | 'toxic' | 'user' | { filter: string }
  ) => {
    switch (type) {
      case 'notToxic':
        return {
          ...plotDataDefaults(),
          name: 'good comment',
          marker: {
            color: '#116300',
          },
        }

      case 'toxic':
        return {
          ...plotDataDefaults(),
          name: 'toxic',
          marker: {
            color: '#8c0000',
          },
        }

      case 'user':
        return {
          ...plotDataDefaults(),
          name: 'added by user',
          marker: {
            color: '#ffdd00',
            line: {
              color: '#000000',
              width: 1,
            },
          },
        }

      default:
        return {
          ...plotDataDefaults(),
          name: type.filter,
          marker: {
            color: '#ff0000',
            line: {
              color: '#0000ff',
              width: 2,
            },
          },
        }
    }
  }

  return {
    plotLayout,
    plotConfig,
    getPlotDataDefaults,
  }
}
