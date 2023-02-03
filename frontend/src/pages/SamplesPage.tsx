import React from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card } from 'antd'
import { PageHeader } from '@ant-design/pro-layout'

export const SamplesPage = ({ samples }) => {
  return (
    <Card>
      <PageHeader backIcon={false} title="Samples">
        <SamplesTable samples={samples} />
      </PageHeader>
    </Card>
  )
}
