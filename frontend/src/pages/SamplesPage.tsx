import React, { useEffect, useState } from 'react'
import { SamplesTable } from 'components/SamplesTable'
import { Card } from 'antd'
import { getSamples } from 'services/api'

export const SamplesPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    getSamples(token).then((samples) => setSamples(samples))
    setIsLoading(false)
  }, [refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <SamplesTable
        token={token}
        samples={samples}
        refreshSamples={refreshSamples}
        isAdmin={isAdmin}
        title="Samples"
        subTitle={null}
        loading={isLoading}
      />
    </Card>
  )
}
