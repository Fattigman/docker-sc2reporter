import React, { useEffect, useState } from 'react'
import { getDashboard } from 'services/api'
import { Area } from '@ant-design/plots'
import { Card, Descriptions, Checkbox, Space, Result } from 'antd'
import { decodeHTMLEntities, urlEncode } from 'helpers'
import { LoadingPage } from './LoadingPage'

const CheckboxGroup = Checkbox.Group

export const DashboardPage = ({ token }) => {
  const [data, setData] = useState<any[]>()
  const [selectionCriterions, setSelectionCriterions] = useState<any[]>([])
  const [generalStats, setGeneralStats] = useState<any>()
  const [errorStatus, setErrorStatus] = useState<any>()
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const filtersList = decodeHTMLEntities(selectionCriterions)
  let filters = ''

  useEffect(() => {
    getDashboard(token, filters)
      .then((response) => {
        setData(response.dashboard_data)
        setGeneralStats(response.general_stats)
        setSelectionCriterions(response.selection_criterions)
        setIsLoading(false)
      })
      .catch((error) => {
        setIsLoading(false)
        setErrorStatus(error?.response?.status)
      })
  }, [])

  const onChange = (list) => {
    list.map((item) => {
      filters += 'selection_criterion=' + urlEncode(item) + '&'
    })

    getDashboard(token, filters)
      .then((response) => {
        setData(response.dashboard_data)
      })
      .catch((error) => {
        setIsLoading(false)
        setErrorStatus(error?.response?.status)
      })
  }

  const config = {
    data: data as Record<string, any>[],
    xField: 'date',
    yField: 'pango_count',
    seriesField: 'pangolin',
  }

  const options = filtersList.map((label, index) => ({
    label,
    value: selectionCriterions[index],
  }))

  return isLoading ? (
    <LoadingPage />
  ) : data ? (
    <Card>
      <Descriptions bordered size="small" title={'General stats'}>
        <Descriptions.Item label="Passed qc samples">
          {generalStats.passed_qc_samples}
        </Descriptions.Item>
        <Descriptions.Item label="Unique mutations">
          {generalStats.unique_mutations}
        </Descriptions.Item>
        <Descriptions.Item label="Unique pangos">{generalStats.unique_pangos}</Descriptions.Item>
      </Descriptions>
      <br />
      <Card title={'Most common pango types over time'}>
        <Space direction="vertical" size="large" style={{ display: 'flex' }}>
          <CheckboxGroup options={options} onChange={onChange} />
          <Area {...config} />
        </Space>
      </Card>
    </Card>
  ) : (
    <Result status="error" title={errorStatus} subTitle="Sorry, something went wrong." />
  )
}
