import React from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card, PageHeader } from 'antd'

export const SamplesPage = ({ token }) => {
  return (
    <Card>
      <PageHeader backIcon={false} title="Samples">
        <SamplesTable token={token} />
      </PageHeader>
    </Card>
  )
}
