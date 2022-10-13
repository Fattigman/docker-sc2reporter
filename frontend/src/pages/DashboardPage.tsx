import React, { useEffect, useState } from 'react'
import { getDashboard } from 'services/api'
import { DualAxes } from '@ant-design/plots'

export const DashboardPage = ({ token }) => {
  const [data, setData] = useState<any>()
  useEffect(() => {
    getDashboard(token).then((response) => setData(response.graph))
  }, [])

  console.log(data)

  const graph = [
    {
      date: '2021-03-01',
      value: 0,
      pangolin: 'B.1.177.21',
      count: 100,
    },
    {
      date: '2021-03-02',
      value: 2,
      pangolin: 'Undetermined',
      count: 90,
    },
    {
      date: '2021-03-03',
      value: 3,
      pangolin: 'Undetermined',
      count: 80,
    },
    {
      date: '2021-03-04',
      value: 3,
      pangolin: 'Undetermined',
      count: 60,
    },
    {
      date: '2021-03-05',
      value: 2,
      pangolin: 'Undetermined',
      count: 50,
    },
    {
      date: '2021-03-06',
      value: 3,
      pangolin: 'B.1.1.7',
      count: 10,
    },
    {
      date: '2021-03-07',
      value: 2,
      pangolin: 'B.1.1.7',
      count: 20,
    },
    {
      date: '2021-03-08',
      value: 2,
      pangolin: 'B.1.1.39',
      count: 30,
    },
    {
      date: '2021-03-09',
      value: 2,
      pangolin: 'B.1.177.80',
      count: 40,
    },
    {
      date: '2021-03-10',
      value: 3,
      pangolin: 'B.1.1.7',
      count: 100,
    },
    {
      date: '2021-03-10',
      value: 5,
      pangolin: 'B.1.1.7',
      count: 70,
    },
    {
      date: '2021-03-10',
      value: 2,
      pangolin: 'B.1.474',
      count: 100,
    },
    {
      date: '2021-03-09',
      value: 7,
      pangolin: 'B.1.160',
      count: 100,
    },
    {
      date: '2021-03-09',
      value: 4,
      pangolin: 'B.1.1.7',
      count: 100,
    },
    {
      date: '2021-03-07',
      value: 2,
      pangolin: 'B.1.177.86',
      count: 100,
    },
    {
      date: '2021-03-08',
      value: 2,
      pangolin: 'B.1',
      count: 100,
    },
    {
      date: '2021-03-08',
      value: 2,
      pangolin: 'B.1.160',
      count: 100,
    },
    {
      date: '2021-03-11',
      value: 4,
      pangolin: 'B.1.1.7',
      count: 100,
    },
    {
      date: '2021-03-10',
      value: 2,
      pangolin: 'B.1.160',
      count: 100,
    },
  ]

  /* const config = {
    data,
    xField: 'date',
    yField: 'value',
    seriesField: 'pangolin',
  } */

  const config = {
    data: [graph, graph],
    xField: 'date',
    yField: ['count', 'value'],
    geometryOptions: [
      {
        geometry: 'line',
        seriesField: 'pangolin',
        lineStyle: {
          lineWidth: 3,
          lineDash: [5, 5],
        },
        smooth: true,
      },
      {
        geometry: 'line',
        seriesField: 'name',
        point: {},
      },
    ],
  }

  return <>{data ? <DualAxes {...config} /> : <h1>DashboardPage</h1>}</>
}
