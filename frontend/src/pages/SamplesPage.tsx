import React from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card, PageHeader } from 'antd'

export const SamplesPage = ({ samples }) => {
  return (
    <Card>
      <PageHeader backIcon={false} title="Samples" />
      <SamplesTable samples={samples} />
    </Card>
  )
}
