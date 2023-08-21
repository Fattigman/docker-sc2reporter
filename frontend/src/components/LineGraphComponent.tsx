import React from 'react'
import { Line } from '@ant-design/plots'

export const LineGraphComponent = ({ data }) => {
  const config = {
    data,
    xField: 'date',
    yField: 'count',
    label: {},
    point: {
      size: 2,
      shape: 'circle',
      style: {
        fill: 'white',
        stroke: '#5B8FF9',
        lineWidth: 2,
      },
    },
  }
  return <Line {...config} />
}
