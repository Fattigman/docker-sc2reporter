import React, { useEffect, useState } from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card, PageHeader } from 'antd'
import { getSamples } from 'services/api'

export const SamplesPage = ({ token, isAdmin }) => {
  const [samples2, setSamples2] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)

  useEffect(() => {
    getSamples(token).then((samples) => setSamples2(samples))
  }, [refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <PageHeader backIcon={false} title="Samples">
        <SamplesTable
          token={token}
          samples={samples2}
          refreshSamples={refreshSamples}
          isAdmin={isAdmin}
        />
      </PageHeader>
    </Card>
  )
}
