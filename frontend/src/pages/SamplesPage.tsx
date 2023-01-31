import React from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card, PageHeader } from 'antd'

export const SamplesPage = ({ token, samples }) => {
  return (
    <Card>
      <PageHeader backIcon={false} title="Samples">
        <SamplesTable token={token} samples={samples} />
      </PageHeader>
    </Card>
  )
}
