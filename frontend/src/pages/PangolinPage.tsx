import React, { useEffect, useState } from 'react'
import { Card } from 'antd'
import { SamplesTable } from 'components/SamplesTable'
import { useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'
import { PageHeader } from '@ant-design/pro-layout'

export const PangolinPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const { id } = useParams()
  const title = `Pangolin ${id}`
  const covLineagesLink = `https://cov-lineages.org/lineage.html?lineage=${id}`

  useEffect(() => {
    if (id)
      getPangolin(token, id).then((response) => {
        setSamples(response.samples)
      })
  }, [id, refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <PageHeader
        onBack={() => history.back()}
        title={title}
        subTitle={<a href={covLineagesLink}>Lineage information</a>}
      >
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
