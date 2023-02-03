import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getNextclade } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'
import { Card } from 'antd'
import { PageHeader } from '@ant-design/pro-layout'

export const NextcladePage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()
  const title = `Nextclade ${id}`

  useEffect(() => {
    if (id)
      getNextclade(token, id).then((response) => {
        setSamples(response.samples)
      })
  }, [id])

  return (
    <Card>
      <PageHeader onBack={() => history.back()} title={title}>
        <SamplesTable samples={samples} />
      </PageHeader>
    </Card>
  )
}
