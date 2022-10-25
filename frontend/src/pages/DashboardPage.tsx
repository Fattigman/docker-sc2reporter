import React, { useEffect, useState } from 'react'
import { getDashboard } from 'services/api'
import { Area } from '@ant-design/plots'
import { Card, Descriptions, PageHeader } from 'antd'

export const DashboardPage = ({ token }) => {
  const [data, setData] = useState<any>()
  const [generalStats, setGeneralStats] = useState<any>()
  useEffect(() => {
    getDashboard(token).then((response) => {
      setData(response.dashboard_data.sort(customSort))
      setGeneralStats(response.general_stats)
    })
  }, [])

  const customSort = (a, b) => {
    const dateA = new Date(a.date)
    const dateB = new Date(b.date)
    if (dateA > dateB) return 1
    else if (dateA < dateB) return -1
    return 0
  }

  const config = {
    data,
    xField: 'date',
    yField: 'pango_count',
    seriesField: 'pangolin',
  }

  return data ? (
    <Card>
      <PageHeader onBack={() => history.back()} title={'Dashboard'}>
        <>
          <Descriptions bordered size="small">
            <Descriptions.Item label="Passed qc samples">
              {generalStats.passed_qc_samples}
            </Descriptions.Item>
            <Descriptions.Item label="Unique mutations">
              {generalStats.unique_mutations}
            </Descriptions.Item>
            <Descriptions.Item label="Unique pangos">
              {generalStats.unique_pangos}
            </Descriptions.Item>
          </Descriptions>
          <br />
          <Card>
            <Area {...config} />
          </Card>
        </>
      </PageHeader>
    </Card>
  ) : (
    <h2>DashboardPage</h2>
  )
}
