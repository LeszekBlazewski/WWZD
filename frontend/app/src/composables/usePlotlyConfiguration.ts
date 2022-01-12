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
          },
        }

      default:
        return {
          ...plotDataDefaults(),
          name: type.filter,
          marker: {
            color: '#0091ff',
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
