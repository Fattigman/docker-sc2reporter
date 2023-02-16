import React, { useEffect, useState } from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card } from 'antd'
import { PageHeader } from '@ant-design/pro-layout'
import { getSamples } from 'services/api'

export const SamplesPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)

  useEffect(() => {
    getSamples(token).then((samples) => setSamples(samples))
  }, [refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <PageHeader backIcon={false} title="Samples">
        <SamplesTable
          token={token}
          samples={samples}
          refreshSamples={refreshSamples}
          isAdmin={isAdmin}
        />
      </PageHeader>
    </Card>
  )
}
