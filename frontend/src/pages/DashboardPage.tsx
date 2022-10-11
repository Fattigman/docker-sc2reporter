import React, { useEffect, useState } from 'react'
import { getDashboard } from 'services/api'
import { Area } from '@ant-design/plots'

export const DashboardPage = ({ token }) => {
  const [data, setData] = useState<any>()
  useEffect(() => {
    getDashboard(token).then((response) => setData(response.graph))
  }, [])

  console.log(data)

  const config = {
    data,
    xField: 'date',
    yField: 'value',
    seriesField: 'pangolin',
  }

  return <>{data ? <Area {...config} /> : <h1>DashboardPage</h1>}</>
}
