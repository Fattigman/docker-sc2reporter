import React, { useEffect, useState } from 'react'
import { getDashboard } from 'services/api'
import { Area } from '@ant-design/plots'
import { Card, Descriptions, Checkbox } from 'antd'
import { Loading } from 'components/Loading'

const CheckboxGroup = Checkbox.Group
const plainOptions = [
  'General monitoring',
  'Vaccine breakthrough',
  'Reinfection',
  'Travel history',
  'Others',
]
const defaultCheckedList = ['']

export const DashboardPage = ({ token }) => {
  const [data, setData] = useState<any>()
  const [generalStats, setGeneralStats] = useState<any>()
  const [checkedList, setCheckedList] = useState(defaultCheckedList)

  useEffect(() => {
    getDashboard(token).then((response) => {
      setData(response.dashboard_data)
      setGeneralStats(response.general_stats)
    })
  }, [])

  const onChange = (list) => {
    setCheckedList(list)
  }

  const config = {
    data,
    xField: 'date',
    yField: 'pango_count',
    seriesField: 'pangolin',
  }

  return !data ? (
    <Loading />
  ) : (
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
        <CheckboxGroup
          options={plainOptions}
          value={checkedList}
          onChange={onChange}
          disabled={true}
        />
      </Card>
      <Card>
        <Area {...config} />
      </Card>
    </Card>
  )
}
