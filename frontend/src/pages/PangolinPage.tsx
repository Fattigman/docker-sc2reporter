import React, { useEffect, useState } from 'react'
import { Card, PageHeader } from 'antd'
import { SamplesTable } from 'components/SamplesTable'
import { useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'

export const PangolinPage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()
  const title = `Pangolin ${id}`
  const covLineagesLink = `https://cov-lineages.org/lineage.html?lineage=${id}`

  useEffect(() => {
    if (id)
      getPangolin(token, id).then((response) => {
        setSamples(response)
      })
  }, [id])

  return (
    <Card>
      <PageHeader
        onBack={() => history.back()}
        title={title}
        subTitle={<a href={covLineagesLink}>Lineage information</a>}
      >
        <SamplesTable samples={samples} />
      </PageHeader>
    </Card>
  )
}
